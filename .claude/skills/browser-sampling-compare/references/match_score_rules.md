# Match Score Rules

Reference for assigning `match_group` and `match_score` in the browser-sampling-compare skill.
Goal: make scoring **repeatable across keywords and reviewers**, not ad-hoc.

`match_score` answers one question: *how cleanly comparable is this row to the
keyword's intended product, given what is visible on the listing card?* It is a
comparability/confidence score, not a quality or price score.

## General bands

| Band | Meaning |
|---|---|
| 90–100 | Almost the same product basis; quantity + type fully clear and equal to the comparison basis |
| 80–89 | Comparable; type clear, quantity clear, minor differences (brand, material, exact count within the same tier) |
| 70–79 | Usable; right product type but a known weakness (single vs multipack basis, size-variant listing, count inferred from a word not a number) |
| 50–69 | Weak but usable with a caveat; quantity or type partially unclear; must be explained in `notes` |
| < 50 | Not recommended; quantity ambiguous (variant selector), or product type does not really match the keyword |

Rule: never assign a score without a one-line justification in the `notes` column.

## Scoring by situation

### Exact quantity match
- Count is stated as an explicit number in the card title (e.g. "4 Pack", "2 Pieces per Pack", "7pcs") **and** equals the keyword's intended basis: start at **86–90**.
- Same explicit count but generic brand or unstated material: **84–88**.
- Count stated as a written word ("Four ... Rope Toys") rather than a digit: still acceptable (title-literal), but cap at **84** and note the wording.

### Ambiguous pack count
- Title is a multi-variant selector (e.g. "10pcs/20pcs/30pcs", "10/4pcs"): assign **`g_pack_unclear`** (or `g2_pack_unclear`-style group) and score **45**. Leave `price_per_unit` blank.
- Mixed bundle where the headline count is not all the relevant item (e.g. "5 Pack Including 2 Ropes & 3 Supplies"): `g_pack_unclear`, score **50**, `price_per_unit` blank, explain the real usable count in `notes`.
- Count not shown on the card at all and the listing is a size/variant page: keep the right type group but score **70** and treat as a single unit; explain in `notes`.

### Same product type, different quantity
- Put them in the **same `match_group`** when the product type matches (e.g. all cotton rope chew/tug sets), even if pack counts differ (3 vs 4 vs 11).
- Score each on its own clarity (usually 84–88 if its own count is clear).
- State explicitly in `notes` that `price_per_unit` — not headline price — is the fair cross-row comparison when counts differ.
- If quantities differ so much that a per-unit comparison is misleading (e.g. single item vs 11-pack), keep them in separate groups (`g3_single_*` vs `g1_*_multipack_set`).

### Brand vs generic
- Comparability does not depend on brand. A branded and a generic item of the same type+quantity can both score 84–90.
- Do **not** add or subtract points for brand prestige. Only note brand in `notes` if it materially changes the comparison basis (e.g. a premium-material variant).

### Sponsored / ad products
- Sponsored placement does **not** lower `match_score`. Score on product comparability only.
- Always set `is_sponsored=true` and state "Sponsored (…)" in `notes`.
- Never drop a sponsored row silently; it is retained like any other.
- Normalize sponsored redirect links before storing (see `platform_notes.md`).

### Same product cross-listed on Amazon and Amazon Haul
- If the identical product (same ASIN) appears on both the Amazon and Amazon Haul surfaces:
  - Keep it as **one row only**, on the surface it was first/most cleanly captured (default: Amazon).
  - Use a different product for the other surface's sample so the two platform samples stay distinct.
  - Record the cross-listing in `notes` ("also appears on Amazon Haul, same ASIN — not double-counted").
- Do not create two rows that would inflate a `match_group` with the same physical product.

## Worked examples

### Keyword 1 — "men boxer briefs 4 pack" (apparel)
- Explicit "4 Pack"/"Pack of 4" in title, clear material → `g1_4pack_mens_boxer_briefs`, **84–88** (e.g. Southpole 88, PUMA 86).
- Title states "(4 Count)" **and** "4-Pack", lowest price, organic → **88**.
- Card title gives no pack count, per-unit math implies ~7-pack → `g2_pack_unclear`, **45**.
- Temu "10/4pcs" variant selector → `g2_pack_unclear`, **45**, `price_per_unit` blank.

### Keyword 2 — "dog toy rope" (pet supplies)
- "Rocfish [4 Pack] … 100% Cotton" explicit count + material → `g1_rope_multipack_set`, **88**.
- "Four Durable Woven Dog Rope Toys" (count as a word) → `g1_rope_multipack_set`, **84** (capped for word-count wording).
- Single rope tug, size-variant listing, no count on card → `g3_single_rope_tug`, **70**.
- "Tough … 5 Pack Including 2 Ropes & 3 Supplies" → `g_pack_unclear`, **50**, per-unit blank.
- "10pcs/20pcs/30pcs … Rope Toy" variant selector → `g_pack_unclear`, **45**, per-unit blank.
- TLAZZ 2-pack present on both Amazon and Amazon Haul (same ASIN) → kept once on Amazon, Haul sample used a different product.

### Home goods — provisional
Not yet validated against a real keyword run. The bands and rules above are
category-agnostic and apply; add worked examples after the first home-goods keyword.
Do not overbuild ahead of data.
