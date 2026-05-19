# Sampling Notes — "men boxer briefs 4 pack" Compare

**Task:** Compare "men boxer briefs 4 pack" across Amazon, Amazon Haul, Temu (up to 5 candidates each).
**Date:** 2026-05-12
**Browser tool:** Playwright MCP (verified at Step 0 against https://example.com)
**Region observed:** US (ZIP redacted)
**Result:** 15 verified candidates (Amazon ×5, Amazon Haul ×5, Temu ×5) + 1 historical TEMU-BLOCKED row preserved.

**CSV schema migration (2026-05-12 follow-up):** The 4 columns proposed at the bottom of this notes file have now been added — `canonical_link`, `is_sponsored`, `price_per_unit`, `block_reason`. Existing Amazon and Amazon Haul rows were not content-modified; the 4 new columns were back-filled from facts already stated in their `notes` field (or computed from price/pack where the pack count is confirmed in the title). `TEMU-BLOCKED-01` is retained as a historical record of the prior block.

---

## Step 0 — Browser Tool Pre-flight

- Tool: `mcp__playwright__browser_navigate` + `mcp__playwright__browser_snapshot` + `mcp__playwright__browser_evaluate`
- Test URL: `https://example.com`
- Result: real browser opened, page title `Example Domain` readable, visible text readable (`This domain is for use in documentation examples...`).
- **PASS.** Proceeded with sampling.

---

## Per-platform results

### Amazon — ACCESSIBLE

- URL: `https://www.amazon.com/s?k=men+boxer+briefs+4+pack`
- Page loaded normally, 48 organic + sponsored results visible.
- Captured 5 candidates (AMZ-01..AMZ-05).
- 4 of 5 explicitly contain a "4 Pack" / "Pack of 4" string in the visible card title.
- AMZ-05 (Fruit of the Loom) was returned by the "4 pack" query but the card title does not state pack count — recorded in match_group `g2_pack_unclear` with `match_score=45` per skill rule 9.
- One row (AMZ-04 Gladbecke) is a Sponsored slot; flagged in notes column. The original anchor was a `/sspa/click` redirect; I normalized to the canonical `/dp/<ASIN>` URL.

### Amazon Haul — ACCESSIBLE (after URL discovery)

- First attempt: `https://www.amazon.com/haul/s?k=...` quietly fell through to the regular Amazon search (no Haul-specific markup; page title was `Amazon.com : ...` not `Amazon Haul : ...`).
- Inspected the Amazon Haul landing page's search dropdown to find the Haul-scoped search params: `srs=121974693011&search-alias=bazaar`.
- Working URL: `https://www.amazon.com/s?srs=121974693011&search-alias=bazaar&k=men+boxer+briefs+4+pack`
- Page title confirmed Haul scope: `Amazon Haul : men boxer briefs 4 pack`.
- 24 results visible; captured 5 candidates (HAUL-01..HAUL-05).
- All 5 explicitly contain a "4 Pack" / "4-Pack" / "Pack of 4" string in the visible card title.
- Skipped Tommy John "3-Pack" entries per skill rule 9.
- Skipped one Ethika listing where pack count was not visible on the card.

### Temu — BLOCKED (historical, 2026-05-12 first attempt)

- URL: `https://www.temu.com/search_result.html?search_key=men+boxer+briefs+4+pack`
- Server redirected the browser to a slide-puzzle CAPTCHA page (`/bgn_verification.html?verifyCode=...`). Page title became `Security verification`. No product DOM available.
- As a second probe I tried the homepage `https://www.temu.com/` — this redirected to a forced sign-in wall (`/login.html?...`). Page title `Temu | Login`. No product DOM available there either.
- Per skill rules, did NOT bypass CAPTCHA, did NOT log in, did NOT use WebFetch as a substitute.
- 0 Temu candidates collected on the first pass. One CSV row (`TEMU-BLOCKED-01`) is included so the block is recorded, not silently dropped.

### Temu — ACCESSIBLE (2026-05-12 second attempt, after manual login)

- Resumed with a persistent Playwright MCP profile at `/Users/bingzhu/.chrome-sampling-profile`. The user manually completed Temu login in the Playwright-opened browser. Persistent profile worked; logged-in/cart state was observed, but personal cart/account details were redacted.
- Re-opened `https://www.temu.com/` — homepage loaded normally (title `Temu | Explore the Latest Clothing, Beauty, Home, Jewelry & More`); no CAPTCHA, no forced sign-in wall this time.
- Navigated to `https://www.temu.com/search_result.html?search_key=men%20boxer%20briefs%204%20pack` — page title `Temu`, search grid rendered (40 unique product anchors detected on the page).
- Captured 5 candidates (TEMU-01..TEMU-05). 4 of 5 have a 4-pack count explicitly visible in the card title (`4-Pack`, `4pcs`, or `(4 Count)`). 1 row (TEMU-03) has an ambiguous `10/4pcs` variant selector in the title and was placed in `g2_pack_unclear` with `match_score=45`, mirroring how AMZ-05 was handled.
- 3 of the 5 Temu cards carried an `AD` badge (sponsored) — recorded in both `is_sponsored=true` and the row's `notes`. None of the rows required opening the product detail page; spec evidence was sufficient from listing-card title text, so the 2-detail-page smoke-test budget was not used.
- Per-unit price: not displayed on Temu listing cards. Computed as `price / pack_count` for the 4 rows with confirmed 4-pack counts (1.68, 1.96, 1.91, 1.20). Left blank for TEMU-03 since the pack is ambiguous.

---

## Match groups

- **`g1_4pack_mens_boxer_briefs`** — 13 rows: AMZ-01..04, HAUL-01..05, TEMU-01, TEMU-02, TEMU-04, TEMU-05. All explicitly marked as 4-pack on the card. Comparable across brands and platforms; material varies (cotton, polyester, viscose, nylon, bamboo rayon, polyester+elastane). Scores 82–88.
- **`g2_pack_unclear`** — 2 rows: AMZ-05, TEMU-03. Score 45 each (weak / not recommended). AMZ-05's card title does not state pack count; per-unit math (~$5.14 × pack) suggests it's a larger pack, not a 4-pack. TEMU-03's title has a `10/4pcs` variant selector — pack count cannot be locked down without choosing a variant.
- **`blocked`** — 1 row: TEMU-BLOCKED-01. Retained as a historical record of the prior CAPTCHA + login-wall block; no score.

## Uncertain matches

- **AMZ-05 Fruit of the Loom Coolzone** — pack size NOT visible on search card. Could be a 7-pack listed under a "4 pack" query. Marked weak.
- **AMZ-04 Gladbecke (sponsored)** — sponsored slot; price/spec read directly from the visible card, but the link was a sponsored redirect URL, which I normalized to `/dp/B0G43RMWMV`. The list price `$49.99` is also a card-shown value, not independently verified.
- **Cross-platform overlap** — Southpole "Pack of 4 with 6" Inseam" appears on both Amazon (ASIN `B0FY76177Q`, AMZ-01) and Amazon Haul (ASIN `B0FY74X8T4`, not in our 5-row Haul sample) at the same $12.99. Looks like a cross-listed SKU but ASIN differs; not folded into the comparison rows to avoid double-counting.

---

## Missing fields

- The only `unknown` row remains `TEMU-BLOCKED-01` (historical block, not omission).
- All five new Temu rows (TEMU-01..05) have non-empty price, spec, and link.
- "Spec" is limited to what the search card surfaces (pack count + any material/feature literally in the title). Detailed specs (fabric % composition, size range) would require navigating into each product page; this was not done because the task asked for visible search-card sampling and the listing-card evidence was sufficient. The 2-detail-page smoke-test budget allowed by the task was therefore not used.
- TEMU-03 (`10/4pcs` variant) has `price_per_unit` intentionally blank — per-unit cannot be computed without selecting a variant on the detail page.
- For Amazon, the visible-card price corresponds to a default size variant selected by Amazon; actual price varies by chosen size. Recorded as displayed.
- For Temu, `currency=USD` and `region=US` were inferred from the page rendering USD prices and the persistent profile's region setting; no explicit "Delivering to <ZIP>" indicator was visible the way Amazon shows one.

---

## Whether the skill needs another improvement

Yes — minor:

1. **Document the Amazon Haul URL pattern in SKILL.md.** Discovered today: Haul-scoped search requires `srs=121974693011&search-alias=bazaar` query params (or `i=bazaar` after redirect). The plain `/haul/s` path silently falls through to regular Amazon search, which is a quiet failure mode worth calling out so a future run does not mis-label regular Amazon results as Haul.
2. **Add a CAPTCHA / login-wall handling example** to the rules section. Today's Temu block was the canonical example: slide-puzzle then forced sign-in. The skill says "do not bypass platform protections" — good — but a one-line example of the right response (record an incident row, write 0 candidates for that platform, continue with other platforms) would make the expected behavior unambiguous.
3. ~~**Consider distinguishing "sponsored" vs "organic" placement** in the output.~~ **DONE 2026-05-12 follow-up.** Added `is_sponsored` boolean column. Back-filled for AMZ-04 (true) and Temu rows (3 of 5 carried an `AD` badge).
4. ~~**Per-unit price field.**~~ **DONE 2026-05-12 follow-up.** Added `price_per_unit` column. Back-filled where pack count is confirmed on the card; left blank for the 2 pack-unclear rows.

Additional improvements added in the 2026-05-12 follow-up:

5. **`canonical_link` column added.** For Amazon, the `/dp/<ASIN>` URL is already canonical and was copied from `link`. For Temu, the listing URL ending in `-g-<numeric_id>.html` is the canonical product key; copied from `link` (no shorter canonical form has been verified yet).
6. **`block_reason` column added.** Filled for `TEMU-BLOCKED-01` ("CAPTCHA (slide-puzzle /bgn_verification.html) + forced login wall (/login.html)"). Empty for all unblocked rows.

Open items for the next iteration:

7. **Persistent-profile Temu rule** is now validated. The skill correctly steered to use `/Users/bingzhu/.chrome-sampling-profile`; manual login + persistent cookies retained state across MCP sessions and unblocked the search results page. Suggest adding a one-line "validated" annotation in SKILL.md beside the persistent-profile rule.
8. **Temu canonical-URL minimization.** Worth a one-time check whether `https://www.temu.com/-g-<id>.html` resolves to the same product (i.e. whether the marketing slug is purely cosmetic) so `canonical_link` can be a shorter, stable form.
