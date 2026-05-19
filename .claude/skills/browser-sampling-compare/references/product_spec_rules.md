# Product Spec Extraction Rules

Reference for filling the `spec` column in the browser-sampling-compare skill.

## Global rules (all categories)

- `spec` records **only what is literally visible on the listing card / title**.
- **Never infer** material, pack count, size, or dimensions. If a field is not on the
  card, write "<field> not stated on card" — do not guess and do not pull it from the
  URL slug, the brand's reputation, or prior knowledge.
- Order spec sub-fields by the category priority below so rows are scannable.
- A value read from a variant selector (e.g. "10/20/30 pcs") is **ambiguous**, not a spec —
  record it as ambiguous and handle quantity per `match_score_rules.md`.
- If a card shows dimensions/material for some rows but not others, only populate the rows
  where it is actually shown; absence is "not stated on card", recorded by observation.

## Apparel

Priority order for `spec`:
1. **quantity / pack count** — only if explicitly in the title ("4 Pack", "Pack of 4", "(4 Count)").
2. **gender** — men's / women's / kids', if stated.
3. **product type** — e.g. boxer briefs, crew socks, t-shirt.
4. **size range** — only if visible on the card (e.g. "S–XXL"); otherwise omit.
5. **material** — only if the title/card states it (e.g. "cotton stretch", "bamboo rayon").
6. **style / pattern** — if relevant to comparison (e.g. "geometric print", "solid color").

Do **not** infer material or pack count. "4-pack mens boxer briefs, cotton stretch" is
acceptable only if both "4" and "cotton" appear on the card. A variant title like
"10/4pcs" is ambiguous pack count, not a spec.

## Pet supplies

Priority order for `spec`:
1. **quantity / count** — explicit number/word in the title ("4 Pack", "Four", "7pcs", "2 Pieces per Pack").
2. **product type** — and specifically classify as one of: **rope toy**, **plush toy**,
   **squeaky toy**, or **mixed kit**. Always state which.
3. **dog size** — if visible (small / medium / large / aggressive chewers).
4. **material** — if visible (e.g. "100% cotton", "natural cotton", "non-toxic" — record
   exactly what is stated; "non-toxic" is not a fiber, note that).
5. **dimensions** — if visible (length, knot count, "3 Feet 5 Knots"); otherwise omit.

Comparison fairness:
- **Do not place rope-only toys and plush/squeaky non-rope toys in the same comparable
  group** unless the listing is clearly a mixed kit — and even then mark it weak
  (`g_pack_unclear` or a low score) and explain in `notes`.
- A "5 Pack" that is "2 Ropes + 3 Supplies" is a mixed kit: the usable rope count is 2,
  quantity is ambiguous → `g_pack_unclear`, per-unit blank.
- "2pcs handles" on a single tug toy is **not** a quantity of 2 toys — it describes one
  toy. Do not record it as count = 2.

## Home goods

Priority order for `spec`:
1. **quantity** — pack/set count if stated.
2. **dimensions** — size/volume/capacity if visible (the primary comparability axis for home goods).
3. **material** — if stated (e.g. stainless steel, bamboo, silicone).
4. **use case** — kitchen / bath / storage / organization, if it changes comparability.
5. **mounting / assembly** — if visible (e.g. "wall-mounted", "no tools required", "tension rod").

Do not infer dimensions or material from product images or the URL; only from card text.

## Cross-keyword examples

- Apparel (keyword 1): `4-pack; 6" inseam; brushed polyester` — all three facts were
  literally on the Amazon card. Where only pack was visible: `4-pack; Deer Head print
  (per title)` with material omitted, not guessed.
- Pet supplies (keyword 2): `4-pack; tug-of-war/chew rope, nearly indestructible; large
  & medium dogs; 100% cotton` — full chain visible. Where material absent: `7 pcs;
  knotted rope chew/teething; dog size not stated on card; material not stated on card`.
- No dimensions appeared on any rope-toy card in keyword 2, so the dimensions sub-field
  was absent for every row by observation, not omission.
