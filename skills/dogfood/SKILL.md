---
name: dogfood
description: "Exploratory QA of web apps: find bugs, evidence, reports. Use when testing a website or web app with browser interactions, screenshots, console/network checks, or structured QA reporting."
version: 1.1.0
platforms: [linux, macos, windows]
metadata:
  tags: [qa, testing, browser, web, dogfood]
  related_skills: [playwright, browser]
---

# Dogfood: Systematic Web Application QA Testing

## Operating Rule

Use Playwright MCP first whenever it is available. Load the `playwright` skill, then call `skill_mcp` with `mcp_name="playwright"` for browser work. Do not start with ad-hoc `npx playwright`, raw Chrome DevTools Protocol scripts, headless Chrome shell commands, Selenium, or generated browser scripts unless Playwright MCP is unavailable or missing a needed capability.

Fallback order:
1. Playwright MCP through `skill_mcp`.
2. browser-harness or another configured browser automation skill.
3. Direct HTTP checks with `curl` plus static screenshots only when no browser automation exists.
4. Ad-hoc local browser scripts only as a last resort, and note the limitation in the report.

## Overview

This skill guides systematic exploratory QA testing of web applications. Navigate the app, inspect page structure, interact with controls, capture screenshots, collect console/network evidence, classify issues, and produce a structured report.

## Inputs

The user provides:
1. Target URL: the entry point to test.
2. Scope: focused area or full-site pass.
3. Output directory: optional, default `./dogfood-output`.

## Phase 1: Plan

1. Create the output structure:
   ```
   {output_dir}/
   ├── screenshots/
   └── report.md
   ```
2. Identify the testing scope and key flows.
3. List pages/features to exercise: navigation, forms, auth, search, uploads, edge/error states, and responsive layouts.
4. If Playwright MCP is available, load the `playwright` skill before browser interaction.

## Phase 2: Explore With Playwright MCP

Use this MCP sequence for each important page or flow:

1. Set viewport with `browser_resize` for desktop.
2. Navigate with `browser_navigate` and wait for the page to settle using `browser_wait_for` when needed.
3. Capture structure with `browser_snapshot` and save it to `{output_dir}`. Prefer snapshot refs for actions.
4. Capture visual evidence with `browser_take_screenshot`, saving under `{output_dir}/screenshots`.
5. Capture console output with `browser_console_messages` after navigation and after each meaningful interaction.
6. Capture network activity with `browser_network_requests`; include static requests on initial page load and omit static requests for API-flow checks unless needed.
7. Interact through MCP actions: `browser_click`, `browser_fill_form`, `browser_type`, `browser_press_key`, `browser_select_option`, `browser_file_upload`, and `browser_evaluate`.
8. Use `browser_run_code_unsafe` only when normal MCP actions cannot express a needed multi-step interaction. Keep snippets small and evidence-focused.

Important: MCP snapshots expose element refs like `e400`. Prefer those exact refs for `browser_click` and `browser_fill_form`. If a text selector fails, take or read a fresh snapshot before trying another selector.

## Phase 3: Interaction Checklist

For each feature tested:

- Click links/buttons and confirm expected navigation or state change.
- Fill forms with valid, invalid, empty, long, and special-character inputs where relevant.
- Test keyboard navigation with Tab, Enter, Escape, and important shortcuts.
- Scroll long pages and scrollable containers.
- Test responsive behavior by resizing at least once to a mobile viewport.
- After every significant action, check console, network, screenshot, and expected vs actual behavior.

For API docs such as Swagger UI or ReDoc:

- Verify `/docs` or equivalent page renders, not just returns HTML.
- Verify the schema endpoint loads, usually `/openapi.json`.
- Expand representative operations.
- Use "Try it out" on at least one safe GET and one safe non-destructive write/search operation when credentials are available.
- Confirm required auth parameters are visible and executable.
- Do not execute destructive operations unless the user explicitly asks.

## Phase 4: Collect And Classify Evidence

For every issue:

1. Save a screenshot showing the issue.
2. Record URL, steps to reproduce, expected behavior, actual behavior, console errors, failed network requests, and screenshot path.
3. Classify using `references/issue-taxonomy.md`:
   - Severity: Critical, High, Medium, Low.
   - Category: Functional, Visual, Accessibility, Console, UX, Content.
4. De-duplicate repeated manifestations of the same root issue.

## Phase 5: Report

Generate `{output_dir}/report.md` using `templates/dogfood-report-template.md`.

The report must include:
1. Executive summary with issue counts by severity.
2. Per-issue sections sorted by severity.
3. Screenshot references using `MEDIA:<screenshot_path>`.
4. Console and network evidence when relevant.
5. Summary table.
6. Testing coverage: pages tested, features tested, not tested, blockers.
7. If no issues are found, say so explicitly and still include evidence screenshots/snapshots.

## Playwright MCP Evidence Pattern

Use this pattern to avoid losing evidence:

- Initial page: `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages`, `browser_network_requests` with `static=true`.
- After opening a flow: fresh `browser_snapshot`, screenshot, console, and non-static network log.
- After submission/execution: wait for visible success/error text, then snapshot, screenshot, console, and network log.
- Mobile pass: `browser_resize`, navigate or reload, screenshot, console, and `browser_evaluate` for horizontal overflow.

Example overflow check:
```js
() => ({
  bodyWidth: document.body.scrollWidth,
  viewportWidth: window.innerWidth,
  hasHorizontalOverflow: document.body.scrollWidth > window.innerWidth + 2
})
```

## Tips

- Always check console output after navigation and significant interactions.
- Read snapshots before clicking when selectors are ambiguous.
- Save artifacts to deterministic paths under the output directory.
- If a browser tool attempt fails, record why and switch to the next supported tool instead of repeatedly retrying the same failed path.
- Avoid creating temporary test files in the project unless needed; remove them before finishing.
- Do not install packages or rely on `npx` if Playwright MCP is already available.
- When reporting screenshots to the user, include `MEDIA:<screenshot_path>` so evidence can render inline.
