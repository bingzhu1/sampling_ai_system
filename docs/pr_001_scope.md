# Status: Paused

PR-001 is paused.

Reason: we are first validating real browser-based product sampling and comparison before building a larger local data pipeline. The active workstream is the `browser-sampling-compare` skill at `.claude/skills/browser-sampling-compare/SKILL.md`.

Do not implement PR-001 unless explicitly approved.

The rest of this document describes the original PR-001 scope and is retained for reference only.

---

# PR-001 Scope

PR-001 is the **data foundation** of the Triata Capital AI-Assisted Sampling System. It is intentionally narrow.

## Goal

Take a sampling task card (JSON) and an existing sample table (CSV / Excel) and produce:

- a normalized Excel file with standardized columns
- a Markdown QC report with duplicates, missing fields, low match scores, and category gaps

All processing is local. No network calls. No automation.

## Allowed

PR-001 may implement:

- Task schema (`task_schema.py`)
- Sample schema (`sample_schema.py`)
- CSV / Excel loader
- Column name normalization
- Price normalization (`$4.32` → `4.32`, `1,299.99` → `1299.99`, invalid → `None`)
- Duplicate link checker
- Duplicate product checker (platform + normalized product_name)
- Missing required field checker
- Low match score checker (`match_score < 60`)
- Category sample gap checker (`count < target_sample_size_per_category`)
- QC report builder (Markdown)
- Excel output writer
- Unit tests for all of the above

PR-001 may use only these dependencies:

- `pandas`
- `openpyxl`
- `pydantic`
- `pytest`

## Not Allowed

PR-001 must **not** implement any of the following:

- Web scraping
- HTTP clients pointed at platform sites
- Browser automation (Playwright, Selenium)
- Mobile automation (Appium, vphone-cli)
- OCR
- Screenshot processing
- OpenAI API calls (or any LLM API)
- LLM-based field extraction
- Automatic product search
- Login-based collection
- Cookie or session handling
- Platform anti-bot evasion
- Database integration
- Web servers / dashboards

If a feature is not on the "Allowed" list, it does not belong in PR-001.

## Definition of Done

PR-001 is complete when all of the following are true:

1. `python main.py --task tasks/amazon_haul_temu.json --input data/input/current_samples.xlsx --output data/output` runs successfully on a realistic sample file.
2. `data/output/normalized_samples.xlsx` is produced and opens correctly.
3. `data/output/qc_report.md` is produced and is readable.
4. `pytest` passes with tests covering: task loading, schema validation, column normalization, price normalization, duplicate link detection, duplicate product detection, missing field checks, low match score checks, and category gap checks.
5. No scraping, browser automation, OCR, or LLM code has been added.
6. `README.md` explains how to run the MVP.

## After PR-001

Once PR-001 is stable, future PRs may add (in order):

- PR-002: AI Extractor
- PR-003: Matcher
- PR-004: QC Agent v2
- PR-005: Excel review workflow
- PR-006: Browser collector
- PR-007: Screenshot collector
- PR-008: Dashboard export

Do not jump ahead of PR-001.
