"""Local tests for scripts/validate_sampling_output.py.

Uses tiny temp CSV fixtures only — never reads the real outputs/. Imports the
validator by file path (it lives in scripts/, not an installed package).
"""

import csv
import importlib.util
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_sampling_output.py"
_spec = importlib.util.spec_from_file_location("vso", _SCRIPT)
vso = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vso)

SCHEMA, _ = vso.load_schema()

_DEFAULTS = {
    "sample_id": "AMZ-01", "category": "cat", "keyword": "kw", "platform": "Amazon",
    "product_name": "Thing 4 Pack", "price": "9.99", "spec": "4-pack",
    "link": "https://x.test/dp/A1", "canonical_link": "https://x.test/dp/A1",
    "match_group": "g1", "match_score": "80", "notes": "organic listing",
    "data_source": "visible browser page", "fetch_method": "Playwright MCP",
    "region": "US", "currency": "USD", "is_sponsored": "false",
    "price_per_unit": "2.50", "block_reason": "",
}


def row(**over):
    d = dict(_DEFAULTS, **over)
    return [d[c] for c in SCHEMA]


def write_run(tmp_path, rows, header=None, notes="clean notes\nUS (ZIP redacted)\n",
              review="clean review\n"):
    csv_p = tmp_path / "widget_compare.csv"
    with csv_p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header if header is not None else SCHEMA)
        for r in rows:
            w.writerow(r)
    if notes is not None:
        (tmp_path / "widget_compare_notes.md").write_text(notes, encoding="utf-8")
    if review is not None:
        (tmp_path / "widget_review.md").write_text(review, encoding="utf-8")
    return csv_p


def test_clean_run_passes(tmp_path):
    csv_p = write_run(tmp_path, [
        row(sample_id="AMZ-01", platform="Amazon"),
        row(sample_id="HAUL-01", platform="Amazon Haul"),
        row(sample_id="TEMU-01", platform="Temu", is_sponsored="true",
            notes="Sponsored (AD) slot"),
    ])
    verdict, _, code = vso.validate(str(csv_p))
    assert verdict == "PASS", verdict
    assert code == 0


def test_bad_schema_fails(tmp_path):
    csv_p = write_run(tmp_path, [row()], header=["wrong", "header"])
    verdict, _, code = vso.validate(str(csv_p))
    assert verdict == "FAIL"
    assert code == 2


def test_personal_data_leak_fails(tmp_path):
    csv_p = write_run(tmp_path, [row()],
                      notes="we saw 5 items in your cart and Ships from this seller ACME\n")
    verdict, findings, code = vso.validate(str(csv_p))
    assert verdict == "FAIL"
    assert any("personal-data" in m for s, m in findings if s == vso.FAIL)


def test_zip_in_review_fails(tmp_path):
    csv_p = write_run(tmp_path, [row()], review="Delivering to St Louis 63108\n")
    verdict, _, code = vso.validate(str(csv_p))
    assert verdict == "FAIL"


def test_blocked_row_ok_is_not_fail(tmp_path):
    csv_p = write_run(tmp_path, [
        row(sample_id="AMZ-01"),
        row(sample_id="TEMU-BLOCKED-01", platform="Temu", product_name="unknown",
            price="unknown", spec="unknown", link="https://temu.test/search",
            canonical_link="", match_group="blocked", match_score="",
            notes="blocked", data_source="blocked", region="unknown",
            currency="unknown", is_sponsored="unknown", price_per_unit="",
            block_reason="CAPTCHA + login wall"),
    ])
    verdict, findings, code = vso.validate(str(csv_p))
    assert verdict == "PASS", [m for s, m in findings if s != vso.PASS]
    assert code == 0


def test_blocked_leak_into_group_fails(tmp_path):
    # non-blocked row carrying match_group=blocked
    csv_p = write_run(tmp_path, [row(match_group="blocked", data_source="visible browser page")])
    verdict, _, code = vso.validate(str(csv_p))
    assert verdict == "FAIL"


def test_ambiguous_per_unit_is_fix_and_strict(tmp_path):
    csv_p = write_run(tmp_path, [
        row(sample_id="TEMU-01", match_group="g_pack_unclear",
            spec="ambiguous pack (10/20/30 variant)", price_per_unit="1.50",
            notes="variant selector, computed anyway"),
    ])
    verdict, _, code = vso.validate(str(csv_p))
    assert verdict == "PASS WITH FIXES"
    assert code == 0
    _, _, code_strict = vso.validate(str(csv_p), strict=True)
    assert code_strict == 1


def test_ambiguous_per_unit_blank_passes(tmp_path):
    csv_p = write_run(tmp_path, [
        row(sample_id="TEMU-01", match_group="g_pack_unclear",
            spec="ambiguous pack", price_per_unit=""),
    ])
    verdict, _, _ = vso.validate(str(csv_p))
    assert verdict == "PASS"


def test_missing_price_fails(tmp_path):
    csv_p = write_run(tmp_path, [row(price="")])
    verdict, _, code = vso.validate(str(csv_p))
    assert verdict == "FAIL"
    assert code == 2


def test_missing_sibling_is_fix(tmp_path):
    csv_p = write_run(tmp_path, [row()], review=None)  # no review file
    verdict, findings, _ = vso.validate(str(csv_p))
    assert verdict == "PASS WITH FIXES"
    assert any("review" in m and s == vso.FIX for s, m in findings)
