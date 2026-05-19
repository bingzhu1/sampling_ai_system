# Privacy Rules

Non-negotiable. A violation here is a review FAIL and must block commit.

## Do not record personal session data

Never write to notes, CSV, review, or any committed file:

- personal cart contents, cart seller names, or itemized cart prices
- account identifiers, usernames, email, sign-in state specifics
- shipping/billing address
- delivery ZIP code or a full city-level personal location
- order numbers / order history
- session identifiers, cookies, tokens

If login/cart/session state is used only to verify profile persistence, describe
it generically (e.g. "persistent profile worked; logged-in/cart state observed,
personal details redacted"). Location is recorded as **"US (ZIP redacted)"**, never
the actual ZIP or city tied to the user.

## Do not commit local browser/automation artifacts

These must never enter git history:

- browser profile directories — `.chrome-sampling-profile/`
- cookies — `*.cookies`
- session files — `*.session`
- HAR captures — `*.har`
- Playwright MCP snapshots/logs — `.playwright-mcp/`
- temp diagnostics — `search-results-*.md`

`.gitignore` must keep all of the above ignored. `.playwright-mcp/` in particular
must remain ignored (it can contain logged-in page snapshots with cart/account
fragments). Verify with `git check-ignore` and never `git add .` blindly.

## Persistent profile is local only

The persistent profile path `/Users/bingzhu/.chrome-sampling-profile` is referenced
as a local path only. Its **contents** are never committed, copied into the repo,
or described with personal specifics. Do not use the user's daily Chrome profile or
the default Chrome user-data directory.

## Outputs contain research sample data only

The three output files hold product comparison data: product_name, price, spec,
links, match grouping, and analysis. Nothing that identifies the user or their
account/session. When in doubt, redact and note the redaction rather than record
the detail.
