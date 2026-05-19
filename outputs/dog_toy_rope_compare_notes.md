# Sampling Notes — "dog toy rope" Compare (Keyword 2)

**Task:** Compare "dog toy rope" across Amazon, Amazon Haul, Temu (up to 5 candidates each).
**Date:** 2026-05-19
**Browser tool:** Playwright MCP, persistent profile `/Users/bingzhu/.chrome-sampling-profile`
**Schema:** 19-column (matches `templates/output_columns.csv`).
**Region observed:** US (ZIP redacted)
**Result:** 15 verified candidates (Amazon ×5, Amazon Haul ×5, Temu ×5). No blocked rows this keyword.

---

## Step 0 — Browser Tool Pre-flight

- Tool: Playwright MCP (`browser_navigate` + `browser_evaluate`).
- Test URL: `https://example.com` → real browser opened, page title `Example Domain` readable.
- **PASS.** Proceeded with sampling.

---

## Per-platform results

### Amazon — ACCESSIBLE

- URL: `https://www.amazon.com/s?k=dog+toy+rope`, title `Amazon.com : dog toy rope`.
- 60 organic + sponsored result cards visible. Captured 5 (AMZ-01..05).
- AMZ-01 (Fida 4-pack) and AMZ-02 (Pacific Pups 11-pack) are sponsored slots; original anchors were `/sspa/click` redirect URLs carrying tracking tokens. Per repo hygiene rules, these tracking URLs were **not stored** — `link`/`canonical_link` use the clean canonical `/dp/<ASIN>` form derived from each card's `data-asin`. The sponsored status is recorded in `is_sponsored` and `notes`.
- AMZ-03 (Mammoth Flossy Chews) is a size-variant listing with no pack count on the card; treated as a single rope tug and scored lower (70).

### Amazon Haul — ACCESSIBLE (scoped search)

- URL: `https://www.amazon.com/s?srs=121974693011&search-alias=bazaar&k=dog+toy+rope` → resolved to `…&i=bazaar&srs=121974693011`, title `Amazon Haul : dog toy rope` (Haul scope confirmed, per the URL pattern documented after keyword 1).
- 24 structured result cards visible. Captured 5 distinct rope toys (HAUL-01..05).
- Haul tiles do not expose a standalone product anchor in the same way regular Amazon search does; `link`/`canonical_link` were derived from each tile's `data-asin` as `/dp/<ASIN>` (not guessed — taken from the page's own attribute).
- Excluded clearly non-rope items returned by the query (plush/squeaky stuffed toys: ASINs B09CD2DT3C, B0D5DQ468J) to keep the rope-toy comparison fair; this is recorded here rather than silently dropped.
- HAUL-03 ("5 Pack" = 2 ropes + 3 non-rope supplies) has an ambiguous rope count and is placed in `g_pack_unclear`.
- Note: AMZ-04 (TLAZZ 2-pack, ASIN B0D4HC1TC7) also appears on the Amazon Haul surface at the same $9.99. To avoid double-counting it is kept only as the Amazon row; the Haul sample uses 5 different products.

### Temu — ACCESSIBLE (persistent profile, no manual check needed)

- URL: `https://www.temu.com/search_result.html?search_key=dog%20toy%20rope`, title `Temu`.
- Pre-extraction block check: no CAPTCHA, no login wall (`blocked=false`, `loginWall=false`), 40 product anchors present. Persistent profile retained logged-in state from the prior keyword; **no manual check was required**, so the task did not need to pause.
- Captured 5 (TEMU-01..05). 4 of 5 carry an `AD` (sponsored) badge.
- TEMU-05 ("10pcs/20pcs/30pcs …") is a variant-selector title — pack count cannot be locked without choosing a variant; placed in `g_pack_unclear`, score 45, `price_per_unit` blank.
- One excluded gotcha worth recording: a "Pet Dog Bite Rope Tug Toy … 2pcs Soft And Sturdy Handles" card states "2pcs" but that refers to **2 handles on one toy**, not 2 units — it was not selected, to avoid a misleading quantity.

---

## Match groups

- **`g1_rope_multipack_set`** — 6 rows: AMZ-01 (4pk), AMZ-02 (11pk), HAUL-01 (4pk), TEMU-01 (4pcs), TEMU-02 (3pk), TEMU-03 (7pcs). Cotton/woven rope chew-tug sets with an explicit count in the title. Comparable as "multipack rope toy set," but pack counts vary 3–11, so `price_per_unit` is the fair cross-row comparison, not headline price. Scores 84–88.
- **`g2_rope_small_multipack`** — 3 rows: AMZ-04 (2pk), AMZ-05 (2pk), HAUL-02 (2pk). Clean 2-piece rope sets. Scores 86–88.
- **`g3_single_rope_tug`** — 4 rows: AMZ-03, HAUL-04, HAUL-05, TEMU-04. Single rope tug/chew (count = 1). Scores 70–80 (AMZ-03 lowest at 70 due to size-variant count ambiguity).
- **`g_pack_unclear`** — 2 rows: HAUL-03 ("5 Pack" but only 2 ropes + 3 supplies) and TEMU-05 (10/20/30 pcs variant selector). Scores 50 / 45. `price_per_unit` deliberately blank for both.

No blocked rows this keyword; `block_reason` is empty for all 15 rows.

---

## Price quality

- All 15 rows have a numeric `price` taken from the visible card.
- `price_per_unit` = `price / count` only where the count is explicitly stated in the card title; single items (count = 1) carry per-unit = displayed price. Blank for the 2 `g_pack_unclear` rows.
- Spot checks: AMZ-01 14.99/4 = 3.7475 → 3.75; AMZ-02 22.99/11 = 2.09; TEMU-03 6.96/7 = 0.9943 → 0.99; HAUL-02 5.99/2 = 2.995 → 3.00. All consistent.
- AMZ-05: Amazon's card displayed "$12.99/count" for a 2-pack (Amazon's "count" = the pack as sold). Per-unit recorded as 12.99/2 = 6.50 with the discrepancy explained in the row's `notes`, not silently adopted.

## Sponsored / ad quality

- Sponsored rows: AMZ-01, AMZ-02, TEMU-01, TEMU-02, TEMU-03, TEMU-04 (`is_sponsored=true`, also flagged in `notes`). All retained, none dropped.
- Amazon sponsored `/sspa/click` redirect URLs (which contain tracking tokens) were normalized to clean `/dp/<ASIN>`; no tracking-token URLs were written to the CSV (verified: no `ref=sr_` or `sspa/click` URL strings in link columns).

## Source quality

- `data_source` = `visible browser page` for all rows; `fetch_method` = `Playwright MCP` for all rows.
- **No WebFetch used** anywhere — not for evidence, not for diagnosis.
- All rows have populated `link` and `canonical_link`. For Amazon/Haul they are identical clean `/dp/<ASIN>` URLs; for Temu they are the canonical `-g-<id>.html` product URLs.

## Missing / uncertain fields

- `spec` follows the requested priority: quantity/count → rope toy type → dog size → material → dimensions. Only title-literal facts were used. Where the card title did not state material or dog size, the spec says "material not stated on card" / "dog size not stated on card" rather than guessing.
- No dimensions were visible on any listing card (Amazon, Haul, or Temu) for this keyword, so the dimensions sub-field is absent for all rows by observation, not omission.
- AMZ-03 quantity is the main soft spot: a size-variant listing with no count shown; treated as a single rope tug and scored 70.
- No personal cart/account/address/order/session data was recorded (per the SKILL.md privacy rule). Persistent-profile/login state was used only to reach Temu results and is described generically here.

---

## Workflow check

- 19-column schema held with no drift; the synced `templates/output_columns.csv` matched the produced header exactly.
- Amazon Haul scoped-search URL pattern from keyword 1 worked first try — worth promoting into `SKILL.md`/`references/platform_notes.md` (still an open P1 from the keyword-1 audit).
- Match-score banding is still applied by judgment; a written `references/match_score_rules.md` (open P1) would make the g1 84–88 spread reproducible across reviewers.
- No P0 regressions: `.playwright-mcp/` remains gitignored; outputs contain no personal data; tracking URLs excluded.
