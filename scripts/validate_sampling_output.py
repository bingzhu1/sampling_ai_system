#!/usr/bin/env python3
"""Tiny, local, read-only validator for browser-sampling-compare outputs.

Design: .claude/skills/browser-sampling-compare/references/validator_design.md

This is a standalone safety checker for the browser-sampling skill. It is NOT the
PR-001 data-foundation system: it imports nothing from sampling_core/, adds no
dependencies, opens no browser, hits no network, and never edits any file.

Usage:
    python scripts/validate_sampling_output.py outputs/<keyword_slug>_compare.csv [--strict]

Exit codes: PASS = 0, PASS WITH FIXES = 0 (1 with --strict), FAIL = 2.
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

# --- severities -------------------------------------------------------------
PASS, FIX, FAIL = "PASS", "FIX", "FAIL"

ALLOWED_DATA_SOURCE = {"visible browser page", "blocked"}
ALLOWED_FETCH_METHOD = {"playwright mcp"}
WEBFETCH_MARKERS = ("webfetch", "curl", "requests", "http fetch", "static html")

# Specific personal-data leak patterns (kept narrow to avoid false positives on
# legitimate redaction text like "US (ZIP redacted)").
PERSONAL_PATTERNS = [
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[A-Za-z]{2,}\b"), "email address"),
    (re.compile(r"\border\s*#\s*\d", re.I), "order number"),
    (re.compile(r"\border\s+number\b", re.I), "order number"),
    (re.compile(r"\bitems?\s+in\s+your\s+cart\b", re.I), "cart contents"),
    (re.compile(r"\bin\s+your\s+cart\b", re.I), "cart contents"),
    (re.compile(r"\bships?\s+from\s+this\s+seller\b", re.I), "cart seller"),
    (re.compile(r"\bsigned?\s+in\s+as\b", re.I), "account identity"),
    (re.compile(r"\bsubtotal\s*\$\s*\d", re.I), "cart subtotal"),
]
ZIP_CONTEXT = re.compile(r"(deliver|delivering to|ship to|shipping address|zip\s*code)", re.I)
ZIP_NUMBER = re.compile(r"\b\d{5}(-\d{4})?\b")

STAGED_FORBIDDEN = (".playwright-mcp/", ".chrome-sampling-profile/",
                    ".cookies", ".session", ".har")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_schema():
    """Canonical 19-column schema. Prefer the machine-readable template;
    fall back to the fenced block in output_contract.md."""
    base = repo_root() / ".claude" / "skills" / "browser-sampling-compare"
    tmpl = base / "templates" / "output_columns.csv"
    if tmpl.is_file():
        header = tmpl.read_text(encoding="utf-8").splitlines()[0].strip()
        return [c.strip() for c in header.split(",")], str(tmpl)
    contract = base / "references" / "output_contract.md"
    if contract.is_file():
        text = contract.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.count(",") >= 18 and line.strip().startswith("sample_id"):
                return [c.strip() for c in line.strip().strip("`").split(",")], str(contract)
    raise FileNotFoundError("Could not locate canonical schema (template or contract).")


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]
    return rows


def scan_personal(text, where, findings):
    leaked = []
    for pat, label in PERSONAL_PATTERNS:
        if pat.search(text):
            leaked.append(label)
    for line in text.splitlines():
        if ZIP_CONTEXT.search(line) and ZIP_NUMBER.search(line):
            leaked.append("delivery ZIP/location")
    if leaked:
        findings.append((FAIL, f"privacy: {where} contains personal-data markers: "
                                f"{', '.join(sorted(set(leaked)))}"))
    else:
        findings.append((PASS, f"privacy: no personal-data markers in {where}"))


def git_staged_check(findings):
    try:
        out = subprocess.run(["git", "diff", "--cached", "--name-only"],
                              cwd=str(repo_root()), capture_output=True,
                              text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        findings.append((PASS, "git: staged-file check skipped (git unavailable)"))
        return
    if out.returncode != 0:
        findings.append((PASS, "git: staged-file check skipped (not a git work tree)"))
        return
    staged = [p for p in out.stdout.splitlines() if p.strip()]
    bad = [p for p in staged if any(tok in p for tok in STAGED_FORBIDDEN)]
    if bad:
        findings.append((FAIL, f"git: forbidden artifacts staged: {', '.join(bad)}"))
    else:
        findings.append((PASS, f"git: no cookies/session/profile/HAR/snapshot files staged "
                                f"({len(staged)} staged)"))


def validate(csv_path, strict=False, sample_cap=5):
    """Return (verdict, findings, exit_code). Read-only."""
    findings = []
    path = Path(csv_path)
    schema, schema_src = load_schema()

    if not path.is_file():
        findings.append((FAIL, f"input: file not found: {csv_path}"))
        return _finish(findings, strict)

    # Sibling files (read-only; used for the privacy scan).
    slug_csv = path.name
    base = slug_csv[:-len("_compare.csv")] if slug_csv.endswith("_compare.csv") else path.stem
    notes_p = path.with_name(f"{base}_compare_notes.md")
    review_p = path.with_name(f"{base}_review.md")

    rows = read_rows(path)
    if not rows:
        findings.append((FAIL, "input: CSV is empty"))
        return _finish(findings, strict)

    # 1 + 2: schema + field count
    header = [c.strip() for c in rows[0]]
    if header == schema:
        findings.append((PASS, f"schema: header matches canonical 19 columns "
                                f"(source: {Path(schema_src).name})"))
    else:
        findings.append((FAIL, f"schema: header does not match canonical schema "
                                f"({len(header)} cols vs {len(schema)}); "
                                f"source {Path(schema_src).name}"))
    data = rows[1:]
    badlen = [i + 2 for i, r in enumerate(data) if len(r) != len(schema)]
    if badlen:
        findings.append((FAIL, f"schema: rows with != {len(schema)} fields: line(s) {badlen}"))
    else:
        findings.append((PASS, f"schema: every row has {len(schema)} fields ({len(data)} rows)"))

    if badlen or header != schema:
        # Without a stable shape, downstream column lookups are unreliable.
        findings.append((FAIL, "schema: aborting field-level checks (unstable shape)"))
        return _finish(findings, strict)

    idx = {name: i for i, name in enumerate(schema)}

    def col(r, name):
        return r[idx[name]].strip()

    # classify rows
    verified, blocked = [], []
    for r in data:
        if col(r, "match_group").lower() == "blocked" or col(r, "data_source").lower() == "blocked":
            blocked.append(r)
        else:
            verified.append(r)

    # 3: platform balance
    plat = {}
    for r in verified:
        plat[col(r, "platform")] = plat.get(col(r, "platform"), 0) + 1
    if not verified:
        findings.append((FAIL, "platform balance: no verified rows"))
    else:
        over = {p: n for p, n in plat.items() if n > sample_cap}
        bal = ", ".join(f"{p} {n}" for p, n in sorted(plat.items()))
        if over:
            findings.append((FIX, f"platform balance: over cap {sample_cap}: {over} ({bal}; "
                                   f"blocked {len(blocked)})"))
        else:
            findings.append((PASS, f"platform balance: {bal}; blocked {len(blocked)}"))

    # 4: no WebFetch as evidence (column-based, not prose)
    wf = []
    for i, r in enumerate(data):
        ds, fm = col(r, "data_source").lower(), col(r, "fetch_method").lower()
        if any(m in ds for m in WEBFETCH_MARKERS) or any(m in fm for m in WEBFETCH_MARKERS):
            wf.append(i + 2)
        elif ds not in ALLOWED_DATA_SOURCE:
            wf.append(i + 2)
        elif r in verified and fm not in ALLOWED_FETCH_METHOD:
            wf.append(i + 2)
    if wf:
        findings.append((FAIL, f"webfetch/source: invalid data_source/fetch_method at line(s) {wf}"))
    else:
        findings.append((PASS, "webfetch/source: all rows browser-sourced (no WebFetch evidence)"))

    # 5: personal data scan (CSV text + siblings)
    scan_personal(path.read_text(encoding="utf-8"), "CSV", findings)
    if notes_p.is_file():
        scan_personal(notes_p.read_text(encoding="utf-8"), f"{notes_p.name}", findings)
    else:
        findings.append((FIX, f"notes: sibling not found ({notes_p.name}) — run may be incomplete"))
    if review_p.is_file():
        scan_personal(review_p.read_text(encoding="utf-8"), f"{review_p.name}", findings)
    else:
        findings.append((FIX, f"review: sibling not found ({review_p.name}) — run may be incomplete"))

    # 6: verified rows have price + link/canonical_link
    price_missing, one_link, no_link = [], [], []
    for i, r in enumerate(data):
        if r not in verified:
            continue
        ln = i + 2
        price = col(r, "price")
        if not price or price.lower() == "unknown":
            price_missing.append(ln)
        link, canon = col(r, "link"), col(r, "canonical_link")
        if not link and not canon:
            no_link.append(ln)
        elif not link or not canon:
            one_link.append(ln)
    if price_missing:
        findings.append((FAIL, f"price: verified rows missing price at line(s) {price_missing}"))
    else:
        findings.append((PASS, "price: all verified rows have a price"))
    if no_link:
        findings.append((FAIL, f"links: verified rows with no link at all at line(s) {no_link}"))
    elif one_link:
        findings.append((FIX, f"links: verified rows with only one of link/canonical_link "
                               f"at line(s) {one_link}"))
    else:
        findings.append((PASS, "links: all verified rows have link + canonical_link"))

    # 7: ambiguous rows must not carry a computed price_per_unit
    amb_bad = []
    for i, r in enumerate(data):
        mg, spec = col(r, "match_group").lower(), col(r, "spec").lower()
        ambiguous = "pack_unclear" in mg or "ambiguous" in spec
        if ambiguous and col(r, "price_per_unit"):
            if not re.search(r"display", col(r, "notes"), re.I):
                amb_bad.append(i + 2)
    if amb_bad:
        findings.append((FIX, f"price_per_unit: ambiguous row has a value without a "
                               f"'platform-displayed' note at line(s) {amb_bad}"))
    else:
        findings.append((PASS, "price_per_unit: ambiguous rows blank (or justified as displayed)"))

    # 8: blocked rows well-formed and isolated
    blk_bad = []
    for i, r in enumerate(data):
        if r not in blocked:
            continue
        ln = i + 2
        if col(r, "match_group").lower() != "blocked":
            blk_bad.append(f"{ln}:group")
        if col(r, "match_score"):
            blk_bad.append(f"{ln}:score")
        if col(r, "data_source").lower() != "blocked":
            blk_bad.append(f"{ln}:data_source")
        if not col(r, "block_reason"):
            blk_bad.append(f"{ln}:block_reason")
    leak = [i + 2 for i, r in enumerate(data)
            if r in verified and col(r, "match_group").lower() == "blocked"]
    if blk_bad:
        findings.append((FAIL, f"blocked: malformed blocked row(s): {blk_bad}"))
    elif leak:
        findings.append((FAIL, f"blocked: blocked match_group on non-blocked row(s) {leak}"))
    else:
        findings.append((PASS, f"blocked: {len(blocked)} blocked row(s) well-formed and isolated"))

    # 9: is_sponsored populated + consistent
    sp_missing, sp_inconsistent = [], []
    for i, r in enumerate(data):
        ln = i + 2
        val = col(r, "is_sponsored").lower()
        if r in blocked:
            if not val:
                sp_missing.append(ln)
            continue
        if val not in ("true", "false"):
            sp_missing.append(ln)
            continue
        text = (col(r, "notes") + " " + col(r, "product_name")).lower()
        if val == "false" and re.search(r"\bsponsored\b|\bad\b", text):
            sp_inconsistent.append(ln)
    if sp_missing:
        findings.append((FAIL, f"is_sponsored: missing/invalid at line(s) {sp_missing}"))
    elif sp_inconsistent:
        findings.append((FIX, f"is_sponsored: false but text says sponsored at line(s) "
                               f"{sp_inconsistent}"))
    else:
        findings.append((PASS, "is_sponsored: populated and consistent"))

    # 10: fetch_method + data_source populated
    fd_missing = [i + 2 for i, r in enumerate(data)
                  if not col(r, "fetch_method") or not col(r, "data_source")]
    if fd_missing:
        findings.append((FAIL, f"provenance: fetch_method/data_source empty at line(s) {fd_missing}"))
    else:
        findings.append((PASS, "provenance: fetch_method + data_source populated on every row"))

    # 11: git staged-file hygiene
    git_staged_check(findings)

    return _finish(findings, strict)


def _finish(findings, strict):
    has_fail = any(s == FAIL for s, _ in findings)
    has_fix = any(s == FIX for s, _ in findings)
    if has_fail:
        return "FAIL", findings, 2
    if has_fix:
        return "PASS WITH FIXES", findings, (1 if strict else 0)
    return "PASS", findings, 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate a browser-sampling output CSV (read-only).")
    ap.add_argument("csv_path", help="outputs/<keyword_slug>_compare.csv")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 (not 0) on PASS WITH FIXES")
    ap.add_argument("--sample-cap", type=int, default=5,
                    help="max verified rows per platform before a FIX (default 5)")
    args = ap.parse_args(argv)

    verdict, findings, code = validate(args.csv_path, strict=args.strict,
                                       sample_cap=args.sample_cap)
    print(f"VERDICT: {verdict}")
    tag = {PASS: "[PASS]", FIX: "[FIX] ", FAIL: "[FAIL]"}
    for sev, msg in findings:
        print(f"{tag[sev]} {msg}")
    return code


if __name__ == "__main__":
    sys.exit(main())
