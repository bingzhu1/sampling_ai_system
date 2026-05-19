---
name: browser-sampling-compare
description: This skill should be used for lightweight browser-based market sampling and product comparison across platforms such as Amazon, Amazon Haul, Temu, Xiaohongshu, Douyin web pages, or other accessible public pages.
---

# Browser Sampling Compare Skill

## Goal

Use browser automation to collect small, auditable comparison samples across platforms.

This skill is for small-batch market research sampling, not large-scale scraping.

## When to Use

Use this skill when the user asks to:
- compare products across platforms
- collect sample products from search results
- build a small product comparison table
- find comparable items on Temu / Amazon / Amazon Haul
- extract prices, specs, links, and notes from browser-visible pages

## Workflow

0. **Browser Tool Pre-flight (REQUIRED, run before any data collection):**

   Before collecting product data, verify that a real browser automation tool is available and operational.

   Acceptable tools:
   - Claude Chrome
   - Playwright MCP
   - Any other real browser automation tool that can open pages, click, scroll, and read visible page content

   NOT acceptable as a substitute:
   - WebFetch
   - Static HTML fetch (curl, requests, etc.)
   - Search-engine snippets
   - Summarizer-only page reads

   Pre-flight procedure:
   - Confirm a browser automation tool from the acceptable list is registered in the current session.
   - Open a known, harmless page (e.g. `https://example.com`) with that tool.
   - Confirm a real browser opened, the page title is readable, and visible page text can be retrieved.

   If no acceptable browser automation tool is available, or pre-flight fails:
   - ABORT the sampling task.
   - Do NOT collect candidates.
   - Do NOT estimate, guess, or hallucinate prices, specs, or links.
   - Create an incident notes file under `outputs/incidents/` (e.g. `outputs/incidents/<YYYY-MM-DD>_browser_unavailable.md`) describing:
     - which tools were checked
     - what was missing
     - the task that was aborted
   - Report to the user: "Browser automation unavailable — sampling aborted."

   **WebFetch is not browser automation.** Data obtained from WebFetch or static HTML may only be used to diagnose a blocker (e.g. confirming a page exists or returns a status code). It may NOT be used as product sample evidence, and must never populate `product_name`, `price`, `spec`, or other sample fields.

## Persistent Browser Profile Rule

For platforms that require login, CAPTCHA handling, cart/session state, or region/currency persistence, use Playwright MCP with a fixed user data directory.

Current project profile:

/Users/bingzhu/.chrome-sampling-profile

Expected behavior:
- The Playwright-opened browser should preserve cookies, localStorage, cart state, login state, region, and currency between sessions.
- The user may manually complete login or CAPTCHA in the Playwright-opened browser.
- After manual login/CAPTCHA, continue using the same Playwright MCP profile.
- Do not switch back to WebFetch.
- Do not use a different Chrome profile unless explicitly approved.

Important:
Do not try to attach to the user's normal daily Chrome profile.
Do not use the default Chrome User Data directory.
Use a separate automation profile.

Note: This was validated when Temu search results loaded without CAPTCHA/login wall and the cart state persisted across MCP sessions.

1. Confirm task inputs:
   - platforms
   - keyword
   - category
   - sample count per platform
   - output format

2. Open browser search pages:
   - Amazon
   - Amazon Haul if accessible
   - Temu
   - other user-specified platforms

3. Collect candidates:
   - product_name
   - price
   - visible spec / quantity
   - link
   - platform
   - notes

4. Compare candidates:
   - product type
   - quantity / pack size
   - size / weight / volume
   - brand vs generic
   - use case
   - whether comparison is fair

5. Assign match_group:
   - products in the same group should be meaningfully comparable

6. Assign match_score:
   - 90-100 = almost same / highly comparable
   - 70-89 = comparable
   - 50-69 = weak but usable with caveat
   - <50 = not recommended

7. Output:
   - CSV preferred
   - Markdown table acceptable
   - include source links
   - include notes and uncertainty

## Default Output Columns

Use exactly this 19-column schema (this order):

sample_id,category,keyword,platform,product_name,price,spec,link,canonical_link,match_group,match_score,notes,data_source,fetch_method,region,currency,is_sponsored,price_per_unit,block_reason

## Rules

- Do not bypass login, CAPTCHA, paywalls, or platform protections.
- Do not collect private personal data.
- Do not store credentials, cookies, tokens, or session files.
- Do not record personal cart, account, address, delivery ZIP, order, or session details in notes or outputs. Only record research sample data. If login/cart/session state is used to verify persistence, describe it generically and redact personal details.
- Do not claim exactness if price or spec is unclear.
- If a page is blocked or dynamic, report it clearly.
- Prefer small batches.
- Keep human review possible.
- Always preserve source links.
- Do not silently drop uncertain samples.
- Use notes to explain uncertainty.

## Done Criteria

A sampling task is done when:
- candidates were collected from accessible pages
- comparable products were grouped
- match_score was assigned
- output table or CSV was created
- uncertain samples were clearly marked
- source links are included
