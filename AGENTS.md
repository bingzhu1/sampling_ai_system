# AGENTS.md

## Current Priority (Updated)

> **The current priority is the lightweight `browser-sampling-compare` skill, not PR-001.**

- We are **not** currently prioritizing the full PR-001 data foundation.
- We **are** prioritizing a lightweight browser-based sampling skill that uses Claude Chrome / Playwright MCP to do small-batch product search, comparison, and CSV / Markdown table export.
- The active workflow is now:

  ```
  Browser Sampling Skill
    → small-batch product search
    → collect visible product candidates
    → compare comparable products
    → export CSV / Markdown table
  ```

- PR-001 is now **Phase 2**. Do not continue PR-001 unless the user explicitly approves resuming it.
- Sampling work should first read `.claude/skills/browser-sampling-compare/SKILL.md`. The older `.claude/skills/sampling-ai-system/SKILL.md` is a Phase 2 reference.

## Project Name

Triata Capital AI-Assisted Sampling System

## Project Purpose

This project builds an AI-assisted sampling workflow for investment research and market research.

The goal is not to build an uncontrolled scraping bot. The goal is to build a reliable, auditable sampling system that helps researchers collect, clean, compare, quality-check, and export structured samples from platforms such as Amazon, Amazon Haul, Temu, Xiaohongshu, Douyin, WeChat Mini Programs, and other consumer platforms.

The system should help Triata Capital answer questions like:

- Are products on Amazon Haul materially cheaper or more expensive than Temu?
- Are comparable products being matched correctly across platforms?
- Which categories have enough clean samples?
- Which samples are duplicates, low-quality, or need human review?
- What additional samples should be collected next?

## Core Principle

Human defines the research question and sampling rules.
AI assists with execution, extraction, matching, quality control, and reporting.

The system must always optimize for:

1. Comparable samples
2. Clean structured data
3. Auditability
4. Repeatability
5. Human review before final use

Do not optimize only for speed or maximum data volume.

## Current MVP Scope

> **Status: Paused (Phase 2).** PR-001 is no longer the active priority — see "Current Priority (Updated)" at the top of this file. The text below is retained for Phase 2 reference only.

The (paused) MVP is PR-001.

PR-001 was scoped to build the data foundation:

- Sampling task schema
- Sample table loader
- Column normalization
- Price normalization
- Duplicate detection
- Missing field detection
- Low match-score detection
- Category sample gap detection
- QC report generation
- Clean Excel output

Do not implement web scraping, browser automation, OpenAI calls, screenshot OCR, Appium, or vphone-cli in PR-001.

## Long-Term System Layers

The full system should eventually have these layers:

1. Task Planner
2. Candidate Search / Collector
3. AI Extractor
4. Product / Content Matcher
5. QC Agent
6. Human Reviewer
7. Excel / CSV / Dashboard Exporter

### 1. Task Planner

Turns a research question into a structured sampling task.

Example input:

Compare Temu and Amazon Haul pricing for low-price consumer products.

Expected structured output:

- Platforms: Temu, Amazon Haul, Amazon US
- Categories: Men's Clothing, Home, Toys, Beauty, Pet Supplies
- Fields: product name, price, quantity, platform, link, match score, review status
- Rules: avoid duplicates, match comparable quantity and product type

### 2. Candidate Search / Collector

Collects raw candidate data from manual links, CSVs, screenshots, browser automation, APIs, or platform search results.

This layer is not part of PR-001.

### 3. AI Extractor

Extracts structured fields from raw product text, webpage text, screenshots, or JSON.

This layer is not part of PR-001.

### 4. Matcher

Determines whether two or more samples are comparable.

Match logic should consider:

- Product type
- Quantity
- Pack size
- Size / weight / volume
- Gender / use case
- Brand vs generic difference
- Whether the comparison is fair

### 5. QC Agent

Checks data quality.

The QC Agent should flag:

- Duplicate links
- Duplicate products
- Missing required fields
- Missing price
- Missing usable link
- Unclear quantity
- Low match score
- Category sample shortage
- Samples requiring human review

### 6. Human Reviewer

Humans make the final keep / replace / edit decision.

AI can recommend, but final research-grade samples should remain auditable.

### 7. Exporter

Exports clean results to:

- Excel
- CSV
- Markdown QC report
- Later: Superset / dashboard / database

## Repository Structure

Expected MVP structure:

sampling_ai_system/
├── AGENTS.md
├── README.md
├── main.py
├── requirements.txt
├── tasks/
│   └── amazon_haul_temu.json
├── sampling_core/
│   ├── __init__.py
│   ├── task_schema.py
│   ├── sample_schema.py
│   ├── loader.py
│   ├── normalizer.py
│   ├── duplicate_checker.py
│   ├── qc_agent.py
│   └── report_builder.py
├── data/
│   ├── input/
│   └── output/
└── tests/
    ├── test_task_schema.py
    ├── test_normalizer.py
    ├── test_duplicate_checker.py
    └── test_qc_agent.py

## Required MVP Behavior

The command:

python main.py \
  --task tasks/amazon_haul_temu.json \
  --input data/input/current_samples.xlsx \
  --output data/output

Should produce:

data/output/
├── normalized_samples.xlsx
└── qc_report.md

## Task JSON Format

Task files should live in:

tasks/

Example:

{
  "project_name": "Amazon Haul vs Temu Sampling",
  "description": "Compare comparable low-price products across Temu, Amazon Haul, and Amazon US.",
  "platforms": ["Temu", "Amazon Haul", "Amazon US"],
  "categories": [
    "Men's Clothing",
    "Home",
    "Toys",
    "Beauty",
    "Pet Supplies"
  ],
  "target_sample_size_per_category": 20,
  "required_fields": [
    "sample_id",
    "category",
    "product_keyword",
    "product_type",
    "spec_basis",
    "platform",
    "product_name",
    "price",
    "currency",
    "link",
    "match_score",
    "ai_notes",
    "human_review"
  ],
  "sampling_rules": [
    "Avoid duplicate products.",
    "Match comparable product type and quantity.",
    "Prefer clear price, quantity, and specification.",
    "Do not compare products with materially different package sizes.",
    "Flag uncertain matches for human review."
  ],
  "exclusion_rules": [
    "Exclude products with missing price.",
    "Exclude products without a usable product link.",
    "Exclude products where quantity or product type is unclear.",
    "Exclude obvious duplicates."
  ]
}

## Standard Sample Fields

All sample records should normalize toward this schema:

{
  "sample_id": "IDMC-001",
  "category": "Men's Clothing",
  "product_keyword": "men boxer briefs 4 pack",
  "product_type": "Men's boxer briefs",
  "spec_basis": "Quantity = 4 pack; gender = men's; type = boxer briefs",
  "platform": "Temu",
  "product_name": "4-Pack Men's Boxer Briefs Underwear",
  "price": 4.32,
  "currency": "USD",
  "link": "https://...",
  "match_score": 82,
  "ai_notes": "Quantity and product type are clear.",
  "human_review": "Keep"
}

## Development Rules

### Allowed in PR-001

PR-001 may implement:

- Python modules
- Pydantic schemas
- Pandas CSV / Excel loading
- Column normalization
- Basic price normalization
- Duplicate detection
- QC summary
- Markdown report output
- Excel output
- Unit tests

### Not Allowed in PR-001

PR-001 must not implement:

- Web scraping
- Playwright
- Selenium
- Appium
- vphone-cli
- OCR
- OpenAI API
- LLM-based extraction
- Automatic product search
- Login-based collection
- Platform automation

## Coding Standards

Use simple Python.

Keep modules small and explicit.

Prefer readable functions over clever abstractions.

Use clear function names:

- load_task()
- load_samples()
- normalize_samples()
- find_duplicate_links()
- find_possible_duplicate_products()
- run_qc()
- build_qc_report()
- save_outputs()

Do not create a large class hierarchy unless necessary.

## Testing Standards

All major functions should have unit tests.

PR-001 tests should cover:

- Task JSON loading
- Required field validation
- Column normalization
- Price normalization
- Duplicate link detection
- Duplicate product detection
- Missing required fields
- Low match score detection
- Category sample gap detection

Use:

pytest

All tests must pass before commit.

## Output Standards

The QC report should be easy for a researcher to read.

It should include:

- Total rows
- Missing required fields
- Duplicate link count
- Possible duplicate product count
- Low match-score count
- Category sample gaps

The normalized Excel should preserve all useful columns from the input, while standardizing known fields.

## Research Quality Rules

Never treat AI output as final truth.

Never silently drop uncertain samples.

If something is unclear, flag it for human review.

For product comparison sampling, comparable specifications matter more than finding the cheapest possible item.

A sample is only useful if the comparison is explainable and repeatable.

## Security and Compliance Rules

Do not store credentials in the repo.

Do not commit cookies, tokens, API keys, session files, or personal account data.

Do not bypass platform protections.

Do not collect private or sensitive user information unless the research task explicitly requires it and legal/compliance approval exists.

For now, this project should focus on clean data processing and human-auditable sampling.

## Current Development Priority

Start with PR-001.

Build the data foundation first.

After PR-001 is stable, future PRs may add:

- PR-002: AI Extractor
- PR-003: Matcher
- PR-004: QC Agent v2
- PR-005: Excel Review Workflow
- PR-006: Browser Collector
- PR-007: Screenshot Collector
- PR-008: Dashboard Export

Do not jump to automation before the schema and QC layer are stable.
