# Keyword-2 Quality Review — "dog toy rope"

**Reviewed files:**
- `outputs/dog_toy_rope_compare.csv`
- `outputs/dog_toy_rope_compare_notes.md`

**Review date:** 2026-05-19
**Reviewer mode:** Static review only. No browser collection, no WebFetch, no Python changes, no PR-001 resumption.
**Verdict:** **PASS** (one manual-review flag on AMZ-03; no required fixes).

---

## 1. Row count and platform balance

| Platform | Expected | Found | Status |
|---|---|---|---|
| Amazon | 5 | 5 (AMZ-01..AMZ-05) | OK |
| Amazon Haul | 5 | 5 (HAUL-01..HAUL-05) | OK |
| Temu | 5 | 5 (TEMU-01..TEMU-05) | OK |
| Blocked | 0 | 0 | OK |

Total: 15 verified rows, 0 blocked. `block_reason` is empty for all 15 rows. No `*-BLOCKED-*` sample IDs present.

**Status: PASS.**

---

## 2. Schema

Header row:

```
sample_id,category,keyword,platform,product_name,price,spec,link,canonical_link,
match_group,match_score,notes,data_source,fetch_method,region,currency,
is_sponsored,price_per_unit,block_reason
```

19 columns, exact match to the required schema and to the `SKILL.md` Default Output Columns block (now also pinned to this 19-column order in `SKILL.md`).

**Status: PASS.**

---

## 3. Match group quality

**`g1_rope_multipack_set` (6 rows) — multi-piece rope sets, count ≥ 3:**

| sample_id | count in title |
|---|---|
| AMZ-01 | 4 Pack |
| AMZ-02 | 11 Pack |
| HAUL-01 | 4 Pack |
| TEMU-01 | "Four" (4 pcs) |
| TEMU-02 | 3 Pack |
| TEMU-03 | 7pcs |

All have an explicit ≥3 count in the title and are rope chew/tug sets. Consistent. Pack counts span 3–11, so per-unit (not headline price) is the fair cross-row metric — correctly noted in the notes file.

**`g2_rope_small_multipack` (3 rows) — clean 2-piece sets:**

| sample_id | count |
|---|---|
| AMZ-04 | 2 Pack |
| AMZ-05 | 2 Pack |
| HAUL-02 | 2 Pieces per Pack |

All exactly 2-piece, clean. No 3+ or single items leaked in. Consistent.

**`g3_single_rope_tug` (4 rows) — single rope tug/chew, count = 1:**

| sample_id | basis |
|---|---|
| AMZ-03 | No count on card; size-variant listing; **treated as** single — see flag below |
| HAUL-04 | Single (no count in title) |
| HAUL-05 | Single (no count in title) |
| TEMU-04 | Single (no count in title) |

**`g_pack_unclear` (2 rows) — correctly separated:**

| sample_id | reason |
|---|---|
| HAUL-03 | "5 Pack" = 2 ropes + 3 non-rope supplies → rope count not cleanly comparable |
| TEMU-05 | "10pcs/20pcs/30pcs" variant selector → count cannot be locked without choosing a variant |

Both unclear rows are properly quarantined out of g1/g2/g3 and scored low (50 / 45) with blank per-unit.

**Flag — AMZ-03 (manual review, not a required move):**
AMZ-03 (Mammoth Flossy Chews) has no pack count on the card and is a size-variant listing. It was placed in `g3_single_rope_tug` by convention (Mammoth Flossy is conventionally sold as a single rope) and the score was already discounted to 70 with the ambiguity explained in the row notes. This is a defensible judgment call, but the count is **not confirmed on the card** — so it is the one row where a reviewer could reasonably argue for `g_pack_unclear` instead. Recommend a human spot-check of the listing. No automatic move required; the low score + explicit caveat keep it from distorting the g3 comparison.

**Status: PASS** with AMZ-03 flagged for manual review.

---

## 4. Price and per-unit quality

All 15 verified rows have a numeric `price`.

`price_per_unit` checks:

| sample_id | price | count | per-unit | check |
|---|---|---|---|---|
| AMZ-01 | 14.99 | 4 | 3.75 | 14.99/4 = 3.7475 → 3.75 OK |
| AMZ-02 | 22.99 | 11 | 2.09 | 22.99/11 = 2.0900 OK |
| AMZ-03 | 5.98 | 1 (treated) | 5.98 | single = displayed price; inherits AMZ-03 flag |
| AMZ-04 | 9.99 | 2 | 5.00 | 9.99/2 = 4.995 → 5.00 OK |
| AMZ-05 | 12.99 | 2 | 6.50 | 12.99/2 = 6.495 → 6.50 OK; "$12.99/count" discrepancy explained in notes |
| HAUL-01 | 13.98 | 4 | 3.50 | 13.98/4 = 3.495 → 3.50 OK |
| HAUL-02 | 5.99 | 2 | 3.00 | 5.99/2 = 2.995 → 3.00 OK |
| HAUL-03 | 9.99 | mixed | *(blank)* | Correctly blank (mixed bundle) |
| HAUL-04 | 13.99 | 1 | 13.99 | single = displayed price OK |
| HAUL-05 | 4.40 | 1 | 4.40 | single = displayed price OK |
| TEMU-01 | 6.21 | 4 | 1.55 | 6.21/4 = 1.5525 → 1.55 OK |
| TEMU-02 | 5.11 | 3 | 1.70 | 5.11/3 = 1.7033 → 1.70 OK |
| TEMU-03 | 6.96 | 7 | 0.99 | 6.96/7 = 0.9943 → 0.99 OK |
| TEMU-04 | 7.88 | 1 | 7.88 | single = displayed price OK |
| TEMU-05 | 3.92 | variant | *(blank)* | Correctly blank (variant-ambiguous) |

- All confirmed-count rows have a correctly computed per-unit.
- Both ambiguous rows (HAUL-03, TEMU-05) have blank `price_per_unit`.
- Single-item rows carry per-unit = displayed price (consistent rule). AMZ-03's per-unit inherits the count-ambiguity flag from §3 but the convention itself is applied consistently.

**Status: PASS.**

---

## 5. Source and link quality

- Every row has both `link` and `canonical_link` populated. Amazon/Haul use clean `/dp/<ASIN>`; Temu uses canonical `-g-<id>.html`.
- Sponsored tracking URLs normalized: AMZ-01 and AMZ-02 were `/sspa/click` redirects with tracking tokens; both stored as clean `/dp/<ASIN>`. Verified by grep — the only `sspa/click` / `ref=sr_` strings in the CSV are inside the descriptive `notes` prose, **not** in any `link`/`canonical_link` field. No tracking-token URLs were written.
- `data_source` = `visible browser page` for all 15 rows; `fetch_method` = `Playwright MCP` for all 15 rows.
- **WebFetch not used** — notes explicitly state "No WebFetch used anywhere — not for evidence, not for diagnosis." Consistent with the CSV evidence fields.

**Status: PASS.**

---

## 6. Privacy / repo hygiene

- No personal cart / account / address / order data in the notes or CSV. Notes explicitly confirm: "No personal cart/account/address/order/session data was recorded."
- ZIP redacted: notes header records "Region observed: US (ZIP redacted)" — no delivery ZIP appears anywhere.
- No session/profile files referenced as committed outputs. `.gitignore` excludes `.chrome-sampling-profile/`, `.playwright-mcp/`, `*.cookies`, `*.session`, `*.har`. `git ls-files` shows none of these are tracked. The notes mention the profile *directory path* (`/Users/bingzhu/.chrome-sampling-profile`) only as a generic tool reference — consistent with `SKILL.md`, and not committed profile content.

**Status: PASS.**

---

## 7. Research usability

- **Usable?** Yes. 13 cleanly grouped comparable rows (g1 ×6, g2 ×3, g3 ×4) plus 2 properly quarantined `g_pack_unclear` rows, balanced 5/5/5 across Amazon, Amazon Haul, and Temu, with 0 blocked rows. Per-unit pricing makes the variable-pack-count g1 set fairly comparable.
- **Rows needing manual review:** AMZ-03 only — count unconfirmed (size-variant listing), placed in `g3` by convention with score discounted to 70 and caveat documented. Spot-check recommended; not blocking. HAUL-03 and TEMU-05 need no further review (correctly quarantined).
- **Ready for keyword 3?** Yes. 19-column schema held with no drift, no P0 regressions, tracking URLs excluded, privacy clean, persistent-profile workflow functioned without a manual-login pause.

**Overall verdict: PASS.**

---

## Carry-forward (open P1s from keyword-1 audit, still open — not blocking)

1. Promote the Amazon Haul scoped-search URL pattern (`srs=121974693011&i=bazaar`) into `SKILL.md` / `references/platform_notes.md` (worked first try this keyword).
2. Add a written `references/match_score_rules.md` so the g1 84–88 banding is reproducible across reviewers.

These are documentation improvements only; they do not affect the validity of the keyword-2 sample.
