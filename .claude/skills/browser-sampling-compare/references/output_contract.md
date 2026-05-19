# Output Contract

The required shape of every sampling run's output. Deviations are review FAILs.

## File naming convention

For a keyword, derive `<keyword_slug>` = lowercase, non-alphanumerics → single `_`.
Produce exactly three files:

- `outputs/<keyword_slug>_compare.csv` — the sample rows.
- `outputs/<keyword_slug>_compare_notes.md` — run notes.
- `outputs/<keyword_slug>_review.md` — review verdict.

Examples: `men boxer briefs 4 pack` → `men_boxer_briefs_4pack_compare.csv`;
`dog toy rope` → `dog_toy_rope_compare.csv`.

## Required 19-column CSV schema

Header, exactly this order:

```
sample_id,category,keyword,platform,product_name,price,spec,link,canonical_link,match_group,match_score,notes,data_source,fetch_method,region,currency,is_sponsored,price_per_unit,block_reason
```

- One header row + one row per sample. Must parse cleanly (quote fields with commas/quotes).
- `region`/`currency` from observed page (e.g. `US`/`USD`); never a guessed locale.
- `data_source` = `visible browser page` (verified) or `blocked`.
- `fetch_method` = `Playwright MCP`.
- `is_sponsored` = `true`/`false` (`unknown` only for blocked rows).

## Blocked row format

When a platform is blocked and cannot be collected:

- `sample_id` = `<PLATFORM>-BLOCKED-01` (etc.).
- `product_name` / `price` / `spec` = `unknown` (never fabricated).
- `link` = the attempted URL (so the block is auditable).
- `canonical_link` empty.
- `match_group` = `blocked`; `match_score` empty.
- `data_source` = `blocked`; `region`/`currency`/`is_sponsored` = `unknown`.
- `block_reason` populated (e.g. "CAPTCHA (slide-puzzle /bgn_verification.html) +
  forced login wall (/login.html)").
- Excluded from every comparison group.

## Ambiguous row format

When quantity cannot be locked (variant selector like "10/20/30 pcs", or a mixed
bundle like "5 Pack = 2 ropes + 3 supplies"):

- `match_group` = `g_pack_unclear` (or keyword-specific `g2_pack_unclear`).
- `match_score` ≤ 50 (variant selector 45; mixed bundle 50).
- `price_per_unit` left **blank** (not computable).
- `notes` must explain why it is ambiguous.
- Never silently drop it; never guess the count.

## Notes file requirements (`*_compare_notes.md`)

Must include: pre-flight result; per-platform access status; match groups with
membership; price & price_per_unit quality (with spot checks); sponsored handling;
source quality (no tracking URLs); missing/uncertain fields (stated, not hidden);
privacy line ("US (ZIP redacted)", no personal data); workflow check / open items.

## Review file requirements (`*_review.md`)

Must run every item in `review_checklist.md` with PASS/FAIL + one-line reason,
and end with a single verdict: PASS / PASS WITH FIXES / FAIL.

## No personal data in outputs

No personal cart, account, address, delivery ZIP, full location, order, or session
details in any of the three files. Research sample data only. See `privacy_rules.md`.
