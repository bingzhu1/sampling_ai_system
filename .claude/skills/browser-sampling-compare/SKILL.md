---
name: browser-sampling-compare
description: This skill should be used for lightweight browser-based market sampling and product comparison across platforms such as Amazon, Amazon Haul, Temu, Xiaohongshu, Douyin web pages, or other accessible public pages.
---

# Browser Sampling Compare Skill

## Goal

Use browser automation to collect small, auditable comparison samples across platforms.

This skill is for small-batch market research sampling, not large-scale scraping.

## When to Use

Use this skill when the user asks to:
- compare products across platforms
- collect sample products from search results
- build a small product comparison table
- find comparable items on Temu / Amazon / Amazon Haul
- extract prices, specs, links, and notes from browser-visible pages

## Modes

Pick the mode from the request, then follow the matching reference. One keyword per run unless told otherwise.

- **Collection mode** — collect a fresh sample for a keyword. Triggers: "compare X across…", "sample/collect X", "run keyword …". Follow `references/runbook.md`. Requires browser pre-flight.
- **Review mode** — audit an existing run, no new collection. Triggers: "review/audit the run", "checkpoint", "is this ready?". Follow `references/review_checklist.md`; no browser needed.
- **Documentation-only mode** — edit skill/reference/docs, no collection, no outputs. Triggers: "improve the skill", "create reference docs", "quality pass". Do not open a browser or touch `outputs/`.
- **Manual-assisted mode** — a platform hits login/CAPTCHA; the user completes it manually in the Playwright-opened browser, then collection resumes on the same persistent profile. Triggers: "I logged in, continue", "handle it manually". Never bypass the protection; see `references/platform_notes.md`.

## Workflow (collection mode)

0. **Browser Tool Pre-flight (REQUIRED, run before any data collection):**

   Before collecting product data, verify that a real browser automation tool is available and operational.

   Acceptable tools:
   - Claude Chrome
   - Playwright MCP
   - Any other real browser automation tool that can open pages, click, scroll, and read visible page content

   NOT acceptable as a substitute:
   - WebFetch
   - Static HTML fetch (curl, requests, etc.)
   - Search-engine snippets
   - Summarizer-only page reads

   Pre-flight procedure:
   - Confirm a browser automation tool from the acceptable list is registered in the current session.
   - Open a known, harmless page (e.g. `https://example.com`) with that tool.
   - Confirm a real browser opened, the page title is readable, and visible page text can be retrieved.

   If no acceptable browser automation tool is available, or pre-flight fails:
   - ABORT the sampling task.
   - Do NOT collect candidates.
   - Do NOT estimate, guess, or hallucinate prices, specs, or links.
   - Create an incident notes file under `outputs/incidents/` (e.g. `outputs/incidents/<YYYY-MM-DD>_browser_unavailable.md`) describing:
     - which tools were checked
     - what was missing
     - the task that was aborted
   - Report to the user: "Browser automation unavailable — sampling aborted."

   **WebFetch is not browser automation.** Data obtained from WebFetch or static HTML may only be used to diagnose a blocker (e.g. confirming a page exists or returns a status code). It may NOT be used as product sample evidence, and must never populate `product_name`, `price`, `spec`, or other sample fields.

## Persistent Browser Profile Rule

Use Playwright MCP with the fixed local profile `/Users/bingzhu/.chrome-sampling-profile` for login / CAPTCHA / cart / region persistence. Do not use the user's daily Chrome profile or the default Chrome user-data dir, and do not switch back to WebFetch. The profile path is local-only and its contents are never committed. Manual login/CAPTCHA handling and the Temu validation note are in `references/platform_notes.md`; the privacy boundary is in `references/privacy_rules.md`.

1. Confirm task inputs:
   - platforms
   - keyword
   - category
   - sample count per platform
   - output format

2. Open browser search pages:
   - Amazon
   - Amazon Haul if accessible
   - Temu
   - other user-specified platforms

3. Collect candidates:
   - product_name
   - price
   - visible spec / quantity
   - link
   - platform
   - notes

4. Compare candidates:
   - product type
   - quantity / pack size
   - size / weight / volume
   - brand vs generic
   - use case
   - whether comparison is fair

5. Assign match_group:
   - products in the same group should be meaningfully comparable

6. Assign match_score and fill spec — bands, quantity/sponsored/cross-listing rules, and spec extraction are in `references/match_score_rules.md` and `references/product_spec_rules.md`. Do not inline the bands here.

7. Output — write the three files per `references/output_contract.md` (CSV + notes + review). Always include source links and explain uncertainty.

## Output Schema

The single source of truth for the 19-column CSV schema, file naming, and blocked/ambiguous row formats is `references/output_contract.md` (literal header also in `templates/output_columns.csv`). Do not restate the column list elsewhere — avoids schema drift.

## Rules

- Do not bypass login, CAPTCHA, paywalls, or platform protections.
- Do not collect private personal data.
- Do not store credentials, cookies, tokens, or session files; no personal cart/account/address/ZIP/order/session data in outputs (full rules: `references/privacy_rules.md`).
- Do not claim exactness if price or spec is unclear.
- If a page is blocked or dynamic, report it clearly.
- Prefer small batches.
- Keep human review possible.
- Always preserve source links.
- Do not silently drop uncertain samples.
- Use notes to explain uncertainty.

## References

Read the runbook first; consult the rest as needed. They hold the detail — do not duplicate it here. Each file is self-contained and linked directly from this section (one level deep); cross-links between references are optional "see also" pointers, not required reading.

- `references/runbook.md` — end-to-end one-keyword run flow and stop conditions.
- `references/output_contract.md` — file naming, 19-column schema, blocked/ambiguous row formats.
- `references/match_score_rules.md` — match_group / match_score bands and worked examples.
- `references/product_spec_rules.md` — category-specific spec extraction (never infer).
- `references/platform_notes.md` — Amazon / Amazon Haul scoped search / Temu profile + CAPTCHA handling.
- `references/review_checklist.md` — per-run review items and PASS / PASS WITH FIXES / FAIL rule.
- `references/privacy_rules.md` — no personal/session data; no committed profiles/cookies/snapshots.

## Done Criteria

A sampling task is done when:
- candidates were collected from accessible pages
- comparable products were grouped
- match_score was assigned
- output table or CSV was created
- uncertain samples were clearly marked
- source links are included
