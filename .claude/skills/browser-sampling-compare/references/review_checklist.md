# Review Checklist

Use this to produce `outputs/<keyword_slug>_review.md` after a run.
Each item is PASS / FAIL with a one-line reason.

## 1. Row count & platform balance
- Verified rows per platform ≤ requested N (default 5).
- Platforms present as requested (Amazon, Amazon Haul, Temu).
- Blocked/trace rows counted separately, not toward the verified sample.

## 2. 19-column schema
- Header matches the canonical schema in `output_contract.md` exactly (19 columns, that order). The literal header is not restated here — avoids drift.
- Every row has exactly 19 fields (CSV parses cleanly).

## 3. match_group quality
- Group members are genuinely comparable (type + quantity tier).
- Ambiguous-pack rows in `g_pack_unclear` (or equivalent), not in clean groups.
- No same-ASIN product double-counted across Amazon/Haul.

## 4. Price & price_per_unit quality
- Every verified row has a numeric `price` from the visible card.
- `price_per_unit` present only where count is explicit; blank for ambiguous packs.
- Spot-check 2–3 per-unit values (price ÷ count) for arithmetic correctness.

## 5. Source / canonical link quality
- `link` and `canonical_link` populated for every verified row.
- No tracking URLs (`/sspa/click`, `ref=sr_`) stored; Amazon/Haul use `/dp/<ASIN>`.
- Temu uses the canonical `-g-<id>.html` URL.

## 6. Sponsored flag quality
- `is_sponsored=true` rows also explained in `notes`.
- Sponsored placement did not change `match_score`.
- No sponsored row silently dropped.

## 7. Blocked row quality
- Blocked rows have `match_group=blocked`, empty `match_score`,
  `data_source=blocked`, populated `block_reason`.
- `product_name`/`price`/`spec` = `unknown` (not fabricated).
- Excluded from all comparison groups.

## 8. Privacy check
- No personal cart/account/address/order/session data in CSV or notes.
- Location shown as "US (ZIP redacted)" or similar; no full ZIP/city.
- No seller names from a personal cart, no itemized cart prices.

## 9. WebFetch evidence check
- No sample field sourced from WebFetch/static HTML.
- `data_source=visible browser page`, `fetch_method=Playwright MCP` for verified rows.

## 10. Final verdict rule
- **PASS** — all checks pass; data usable as-is.
- **PASS WITH FIXES** — data sound but doc/hygiene/readability fixes needed;
  list them as P0/P1; none require re-collecting data.
- **FAIL** — any of: schema broken, fabricated/guessed price/spec/link,
  personal data committed, WebFetch used as evidence, or blocked rows leaking
  into comparison groups.
