# Runbook — One-Keyword Sampling Run

Step-by-step flow for a single keyword. Follow in order; do not skip steps.

## 0. Pre-flight browser check (REQUIRED)
- Confirm a real browser automation tool (Playwright MCP) is registered.
- Open `https://example.com`; confirm a real browser opened and the title
  `Example Domain` and visible text are readable.
- WebFetch / static HTML is **not** acceptable. If pre-flight fails, abort and
  write an incident file under `outputs/incidents/` (see SKILL.md step 0).

## 1. Git clean check
- Run `git status`.
- Acceptable to proceed when: no tracked-file modifications, nothing staged,
  prior P0/skill fixes already committed.
- Untracked files unrelated to this task (e.g. PR-001 skeleton) are fine — note them.
- Do not start collection on a dirty sampling-workflow tree.

## 2. Persistent profile check
- Use Playwright MCP with `/Users/bingzhu/.chrome-sampling-profile` only.
- Do not use the daily Chrome profile or the default Chrome user-data dir.
- The profile should retain cookies/login/region across sessions.

## 3. Confirm task inputs
- platforms, keyword, category, sample count per platform, output format.
- Derive `<keyword_slug>` (lowercase, words joined by `_`) for file naming.

## 4. Collection order
1. **Amazon** — `https://www.amazon.com/s?k=<keyword+with+plus>`; verify title
   `Amazon.com : <keyword>`. Collect up to N.
2. **Amazon Haul** — scoped: `https://www.amazon.com/s?srs=121974693011&search-alias=bazaar&k=<keyword>`;
   verify title `Amazon Haul : <keyword>`. Collect up to N distinct products.
3. **Temu** — `https://www.temu.com/search_result.html?search_key=<url-encoded keyword>`.
   Run the block check first. If CAPTCHA/login wall: do not bypass; stop and ask
   the user to handle it manually on the same profile, or write a blocked trace row.
- See `platform_notes.md` for selectors, URL normalization, and scope verification.

## 5. Scoring
- Assign `match_group` and `match_score` per `match_score_rules.md`.
- Fill `spec` per `product_spec_rules.md` (title-literal only; never infer).
- Compute `price_per_unit` only when count is explicit; blank for ambiguous packs.

## 6. Output file naming
- `outputs/<keyword_slug>_compare.csv`
- `outputs/<keyword_slug>_compare_notes.md`
- `outputs/<keyword_slug>_review.md`
- Exact 19-column schema; see `output_contract.md`.

## 7. Notes writing
- Pre-flight result, per-platform access status, match groups, price quality,
  sponsored handling, source quality, missing/uncertain fields, workflow check.
- Privacy: "US (ZIP redacted)", no personal cart/account/order data
  (see `privacy_rules.md`).

## 8. Review step
- Produce `outputs/<keyword_slug>_review.md` using `review_checklist.md`.
- Verdict: PASS / PASS WITH FIXES / FAIL.

## 9. Commit step
- Commit only when the user asks.
- Stage explicit paths (the 3 output files + any skill/reference changes).
  Do **not** `git add .` (would pull in unrelated untracked files / risk
  staging ignored artifacts).
- Never commit `.playwright-mcp/`, profiles, cookies, sessions, HAR files.

## Stop conditions
- Browser pre-flight fails → abort + incident file.
- CAPTCHA / login wall and user not available → blocked trace row, continue
  other platforms, do not bypass.
- Request pushes beyond skill scope (scraping, automation beyond this skill,
  PR-001) → stop and ask.
- One keyword per run unless told otherwise; stop after the review + notes.
