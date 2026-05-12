---
name: sampling-ai-system
description: Use this skill when working on Triata Capital's AI-assisted sampling system, including sampling task schemas, sample normalization, duplicate checks, product/content matching, QC reports, and Excel/CSV outputs.
---

# Triata Capital AI-Assisted Sampling System

## Status: Phase 2 (Paused)

> **This skill is currently Phase 2.** Do not use it for the immediate browser-based sampling MVP unless the user explicitly asks to resume PR-001.
>
> For current browser sampling work, use `.claude/skills/browser-sampling-compare/SKILL.md`.
>
> The rest of this document is retained as a Phase 2 reference for when we revisit the local data-foundation pipeline.

## When To Use This Skill

Use this skill whenever the task touches:

- The sampling AI system in `sampling_ai_system/`
- Sampling task cards (`tasks/*.json`)
- Sample CSV / Excel loading or cleaning
- Column or price normalization
- Duplicate detection
- Missing field or category-gap checks
- QC reports
- Excel / CSV / Markdown output
- AI extractor, matcher, or reviewer design
- Amazon Haul vs Temu sampling
- Cross-platform product or content sampling (Temu, Amazon, Xiaohongshu, Douyin, WeChat Mini Programs)

Do not use this skill for unrelated stock analysis, AVGO work, resume work, school assignments, or general coding tasks.

## Project Goal

Build an AI-assisted sampling system for Triata Capital's investment and market research.

The correct model is:

> **Human** defines the research question and sampling rules.
> **AI** assists with extraction, matching, QC, and reporting.
> **Human** reviews the final samples before they are used.

This is not a scraping bot. Auditability and comparability matter more than volume.

## Current PR-001 Scope

PR-001 is the **data foundation only**. It reads an existing CSV / Excel of samples and produces a normalized Excel and a Markdown QC report.

PR-001 may implement:

- task schema
- sample schema
- CSV / Excel loader
- column normalizer
- price normalizer
- duplicate link checker
- possible duplicate product checker
- missing required field checker
- low match-score checker
- category sample gap checker
- QC report builder
- Excel output writer
- unit tests

PR-001 must **not** implement:

- web scraping
- HTTP clients pointed at platform sites
- browser automation (Playwright, Selenium)
- mobile automation (Appium, vphone-cli)
- OCR
- OpenAI API or any LLM API
- LLM-based extraction
- automatic product search
- login-based collection
- databases or web servers

See `docs/pr_001_scope.md` for the canonical allow/deny list.

## Current Step: Structure and Workflow Only

The repo is currently in the **structure and workflow** phase.

What exists right now:

- project skeleton
- documentation in `docs/`
- task card in `tasks/amazon_haul_temu.json`
- placeholder `main.py`
- empty `sampling_core/` package
- empty `tests/` package
- this skill file

What does **not** exist yet:

- any business logic in `sampling_core/`
- any tests in `tests/`
- a working `python main.py ...` command

**Do not implement automation yet. Do not implement PR-001 yet.** The next step is human approval to begin PR-001.

## Required Folder Structure

```
sampling_ai_system/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── requirements.txt
├── main.py
├── tasks/
│   └── amazon_haul_temu.json
├── docs/
│   ├── workflow.md
│   ├── pr_001_scope.md
│   ├── data_schema.md
│   └── development_rules.md
├── sampling_core/
│   └── __init__.py
├── data/
│   ├── input/
│   │   └── .gitkeep
│   └── output/
│       └── .gitkeep
├── tests/
│   └── __init__.py
└── .claude/
    └── skills/
        └── sampling-ai-system/
            └── SKILL.md
```

## Development Sequence

Follow this order. Do not skip steps.

1. **Structure and workflow docs** (this step — current).
2. **PR-001 schemas** — `task_schema.py`, `sample_schema.py` using Pydantic.
3. **PR-001 loader** — `loader.py` for CSV / Excel input.
4. **PR-001 normalizer** — `normalizer.py` for column names and prices.
5. **PR-001 duplicate checker** — `duplicate_checker.py`.
6. **PR-001 QC agent** — `qc_agent.py` (missing fields, low match score, category gaps).
7. **PR-001 report builder** — `report_builder.py` (Markdown + Excel).
8. **PR-001 tests** — `tests/test_*.py` covering each module.
9. **PR-001 main.py wiring** — connect loader → normalizer → duplicate → QC → report.
10. **Run `pytest`** — all tests must pass.
11. **Update README** — document the working MVP.

Future PRs (do not start before PR-001 is stable):

- PR-002: AI Extractor
- PR-003: Matcher
- PR-004: QC Agent v2
- PR-005: Excel review workflow
- PR-006: Browser collector
- PR-007: Screenshot collector
- PR-008: Dashboard export

## Definition Of Done For This Structure Step

The structure-and-workflow step is complete when:

1. The folder tree above exists exactly as specified.
2. `AGENTS.md`, `CLAUDE.md`, `README.md`, `requirements.txt`, and `main.py` exist at the repo root.
3. `tasks/amazon_haul_temu.json` exists with the agreed task card content.
4. `docs/workflow.md`, `docs/pr_001_scope.md`, `docs/data_schema.md`, and `docs/development_rules.md` exist.
5. `sampling_core/__init__.py` and `tests/__init__.py` exist (empty packages).
6. `data/input/.gitkeep` and `data/output/.gitkeep` exist.
7. `.claude/skills/sampling-ai-system/SKILL.md` exists (this file).
8. **No business logic** has been added to `sampling_core/`.
9. `main.py` prints a placeholder message and does nothing else.
10. The user has approved moving on to PR-001 implementation.

## Coding Style For Future PRs

- Python only.
- PR-001 dependencies: `pandas`, `openpyxl`, `pydantic`, `pytest`.
- Small, explicit modules — no unnecessary abstractions.
- No database, no web server, no LLM call in PR-001.
- Flag uncertainty, never silently drop bad data.
- Tests required before commit; `pytest` must pass.
