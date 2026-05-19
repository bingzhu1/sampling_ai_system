# Validator Design (design-only — not implemented)

A tiny, local, read-only safety checker for browser-sampling outputs. **Not built
yet.** This document specifies behavior so a future implementation is mechanical.
Do not create `scripts/` or write Python from this doc until explicitly approved.

## Purpose

Catch obvious contract, hygiene, and privacy regressions in a finished run before
it is reviewed or committed. It is a guardrail, not a grader — it does not judge
match quality or pricing analysis.

## Proposed command

```
python scripts/validate_sampling_output.py outputs/<keyword_slug>_compare.csv
```

- One positional arg: the `*_compare.csv` path.
- Optional `--strict` (treat PASS WITH FIXES as non-zero exit) for future CI use.
- Read-only: never edits the CSV, notes, review, git, or any file.
- Derives sibling paths (`*_compare_notes.md`, `*_review.md`) from the slug for
  the cross-file checks, but only reads them.

## Expected output

Single verdict line + itemized findings, e.g.:

```
VERDICT: PASS WITH FIXES  (outputs/dog_toy_rope_compare.csv)
[PASS] schema: 19 columns match output_contract.md
[PASS] platform balance: Amazon 5, Amazon Haul 5, Temu 5, blocked 0
[PASS] verified rows: price + link + canonical_link present (15/15)
[FIX ] is_sponsored: row TEMU-04 noted "Sponsored" in notes but is_sponsored=false
[PASS] privacy: no ZIP/cart/account/order/session patterns found
[PASS] git: no cookies/session/profile/HAR/snapshot paths staged
```

Exit codes: PASS → 0; PASS WITH FIXES → 0 (or 1 with `--strict`); FAIL → 2.

## Validation rules

| # | Check | Verdict on failure |
|---|---|---|
| 1 | Header equals the canonical 19-column schema in `output_contract.md`, same order | FAIL |
| 2 | Every row has exactly 19 fields; CSV parses cleanly | FAIL |
| 3 | Per-platform verified-row count ≤ requested N (default 5); platforms present as expected | FIX |
| 4 | No sample field sourced from WebFetch: `fetch_method` = `Playwright MCP`, `data_source` ∈ {`visible browser page`, `blocked`}; no `data_source` mentioning fetch/curl/http | FAIL |
| 5 | No personal-data leakage in CSV or notes: regex scan for ZIP (`\b\d{5}(-\d{4})?\b` near "deliver/ship"), email, "order #", cart seller/itemized-cart phrasing, session/cookie tokens | FAIL |
| 6 | Verified rows (non-blocked) have non-empty `price` and at least one of `link`/`canonical_link`; prefer both | FAIL if price missing; FIX if only one link |
| 7 | `price_per_unit` blank for `g_pack_unclear`/ambiguous rows **unless** notes say the per-unit was displayed by the platform | FIX |
| 8 | Blocked rows (`match_group=blocked`) have empty `match_score`, `data_source=blocked`, populated `block_reason`, and never appear in a non-blocked match_group | FAIL |
| 9 | `is_sponsored` ∈ {`true`,`false`} for verified rows (`unknown` only for blocked); if notes/row text say "Sponsored"/"AD", `is_sponsored` must be `true` | FIX |
| 10 | `fetch_method` and `data_source` populated on every row | FAIL |
| 11 | `git diff --cached --name-only` (read-only) contains no `*.cookies`, `*.session`, `*.har`, `.chrome-sampling-profile/`, or `.playwright-mcp/` paths | FAIL |

"FIX" findings → at most PASS WITH FIXES. Any "FAIL" finding → FAIL.

## Verdict rule

- **PASS** — all checks pass.
- **PASS WITH FIXES** — only FIX-level findings (counts, single-link, sponsored
  flag, per-unit nuance); data is sound, fixes are mechanical.
- **FAIL** — any FAIL-level finding (broken schema, WebFetch evidence, personal
  data, missing price, blocked row leakage, staged secret/snapshot files).

This mirrors `review_checklist.md` so the human review and the validator agree.

## Non-goals

- Not a match-quality or price-analysis grader (humans + `match_score_rules.md` do that).
- Does not open a browser, hit the network, or re-collect anything.
- Does not modify, reformat, or "auto-fix" any file.
- Does not parse platform pages or validate that a product still exists.
- No external dependencies beyond the Python stdlib (`csv`, `re`, `subprocess`
  for the read-only `git` check); no pandas/pydantic.

## Relationship to PR-001

This is a **tiny standalone safety checker for the browser-sampling skill**, not
the resumed PR-001 data-foundation system. It does not implement the PR-001
schema/normalizer/duplicate/QC/report pipeline, shares no modules with it, and
does not depend on `sampling_core/`. PR-001 remains paused; building this
validator later does not constitute resuming PR-001. Implementation requires its
own explicit approval before `scripts/` is created.
