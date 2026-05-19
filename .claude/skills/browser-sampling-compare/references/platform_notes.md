# Platform Notes

Reference for platform-specific access and link handling in the browser-sampling-compare skill.

## Amazon (regular search)

- Search URL: `https://www.amazon.com/s?k=<keyword+with+plus+signs>`.
- Page title pattern: `Amazon.com : <keyword>` (confirms regular Amazon scope, **not** Haul).
- Result cards: `div[data-component-type="s-search-result"][data-asin]`. Title in
  `h2 a span`/`h2 span`; price in `.a-price .a-offscreen`; the card's `data-asin`
  is the stable product key.
- Cards mix organic and sponsored placements; capture both, flag sponsored.

### Amazon sponsored URL normalization rule

- Sponsored cards' anchors are `/sspa/click?...` redirect URLs that embed tracking
  tokens. **Do not store these URLs.**
- Build the canonical product URL from the card's `data-asin`:
  `https://www.amazon.com/dp/<ASIN>`.
- Write that canonical URL into **both** `link` and `canonical_link`.
- Record sponsored status in `is_sponsored=true` and in `notes`
  ("Sponsored slot; /sspa/click redirect normalized to /dp/ASIN").
- Also avoid storing organic `ref=sr_...` tracking URLs — prefer the clean
  `/dp/<ASIN>` form for consistency and hygiene.

## Amazon Haul (scoped search)

- The plain `/haul/s` path silently falls through to regular Amazon search — do not rely on it.
- **Scoped search rule:** use `srs=121974693011` and `search-alias=bazaar` when available:
  `https://www.amazon.com/s?srs=121974693011&search-alias=bazaar&k=<keyword>`
  (Amazon may rewrite this to `...&i=bazaar&srs=121974693011`).
- **Verify scope by page title:** it must read `Amazon Haul : <keyword>`. If it reads
  `Amazon.com : <keyword>`, the Haul scope did not apply — do not label the rows as Haul.
- Haul tiles often do not expose a standalone product anchor like regular search does.
  Derive `link`/`canonical_link` from the tile's `data-asin` as `/dp/<ASIN>`
  (this is taken from the page's own attribute, not guessed).
- If a product (same ASIN) appears on both Amazon and Amazon Haul, keep one row only and
  use a different product for the other surface — see `match_score_rules.md`
  (cross-listed rule).

## Temu

### Persistent profile rule

- Use Playwright MCP with the fixed profile directory:
  `/Users/bingzhu/.chrome-sampling-profile`
- This profile preserves cookies, localStorage, login, region, and currency between
  sessions. Do not attach to the user's daily Chrome profile and do not use the default
  Chrome user-data directory.
- Validated: across keyword 1 and keyword 2 the profile retained logged-in state, so
  keyword 2 reached Temu search results with no CAPTCHA and no login wall.

### Manual login / CAPTCHA handling rule

- Before extracting, run a block check: inspect URL + visible body text for
  `bgn_verification`, `login.html`, "verification", "captcha", "slide to", etc.
- If a CAPTCHA or login wall is present:
  - **Do not bypass it.** Do not solve the CAPTCHA, do not log in programmatically.
  - Stop and ask the user to complete login/CAPTCHA manually in the
    Playwright-opened browser, then resume on the **same** persistent profile.
  - If the run cannot continue, write one trace row with `match_group=blocked`,
    empty `match_score`, `data_source=blocked`, and a populated `block_reason`
    (e.g. "CAPTCHA (slide-puzzle /bgn_verification.html) + forced login wall
    (/login.html)"). Never fabricate `product_name`/`price`/`spec` for a blocked row.
- Temu search URL: `https://www.temu.com/search_result.html?search_key=<url-encoded keyword>`.
  Product URLs end in `-g-<numeric_id>.html`; treat that as the canonical key
  (use the same URL for `link` and `canonical_link`).

## Cross-platform rules (all platforms)

- **No WebFetch as sample evidence.** WebFetch / static HTML may only diagnose a blocker
  (e.g. confirm a page exists). It must never populate `product_name`, `price`, `spec`,
  `link`, or any sample field.
- **No personal data in notes or outputs.** Do not record personal cart, account,
  address, delivery ZIP, order, or session details. If login/cart/session state is used
  to verify persistence, describe it generically and redact specifics (e.g. write
  "US (ZIP redacted)", not the ZIP; do not name sellers in your cart or itemize cart prices).
