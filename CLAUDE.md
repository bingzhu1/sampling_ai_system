# CLAUDE.md

Claude-specific instructions for the Triata Capital AI-Assisted Sampling System.

## Before Doing Anything

1. Read `AGENTS.md` first. It is the canonical project description.
2. **For any sampling-related work, read `.claude/skills/browser-sampling-compare/SKILL.md` first** — this is the active skill.
3. The previous data-foundation skill at `.claude/skills/sampling-ai-system/SKILL.md` is now a **Phase 2 reference only**.
4. The previous PR-001 design docs in `docs/` (`workflow.md`, `pr_001_scope.md`, `data_schema.md`, `development_rules.md`) are also Phase 2 references. Do not act on them as if they were the active plan.

## Current Priority

The current priority is the **browser-sampling-compare** skill: lightweight, browser-based, small-batch product sampling and comparison using Claude Chrome / Playwright MCP, with CSV / Markdown table output.

PR-001 (the local data foundation) is paused. **Do not continue PR-001 unless the user explicitly approves resuming it.** If a request looks like it would extend PR-001 code, stop and confirm.

## What Not To Do

Do not implement any of the following until explicitly approved:

- Web scraping
- Browser automation (Playwright, Selenium)
- Mobile automation (Appium, vphone-cli)
- OCR
- OpenAI API calls
- LLM-based extraction
- Login-based data collection

PR-001 is local file processing only.

## Working Style

- Keep changes small and scoped.
- Prefer editing existing files over creating new ones.
- After any code change, run `pytest`.
- Do not silently delete or hide bad samples — flag them.
- Never commit credentials, cookies, tokens, API keys, or session files.

## When in Doubt

If a request is ambiguous or seems to push beyond PR-001 scope, stop and ask.
Research quality and auditability matter more than speed or volume.
