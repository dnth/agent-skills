---
name: dogfood
description: "Exploratory QA of web apps: find bugs, evidence, reports."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  tags: [qa, testing, browser, web, dogfood]
  related_skills: [playwright, browser]
---

# Dogfood: Systematic Web Application QA Testing

## Overview

This skill guides you through systematic exploratory QA testing of web applications using Playwright MCP, browser-harness, or another browser automation toolset. You will navigate the application, interact with elements, capture evidence of issues, and produce a structured bug report.

## Prerequisites

- Browser automation must be available through Playwright MCP, browser-harness, or an equivalent toolset with navigation, page inspection, interaction, screenshot, console, scrolling, history, and keyboard capabilities.
- A target URL and testing scope from the user

## Inputs

The user provides:
1. **Target URL** — the entry point for testing
2. **Scope** — what areas/features to focus on (or "full site" for comprehensive testing)
3. **Output directory** (optional) — where to save screenshots and the report (default: `./dogfood-output`)

## Workflow

Follow this 5-phase systematic workflow:

### Phase 1: Plan

1. Create the output directory structure:
   ```
   {output_dir}/
   ├── screenshots/       # Evidence screenshots
   └── report.md          # Final report (generated in Phase 5)
   ```
2. Identify the testing scope based on user input.
3. Build a rough sitemap by planning which pages and features to test:
   - Landing/home page
   - Navigation links (header, footer, sidebar)
   - Key user flows (sign up, login, search, checkout, etc.)
   - Forms and interactive elements
   - Edge cases (empty states, error pages, 404s)

### Phase 2: Explore

For each page or feature in your plan:

1. **Navigate** to the page using the available browser tool.
   - Playwright MCP: navigate to the URL, then wait for the page to settle.
   - browser-harness: `new_tab("https://example.com/page")`, then `wait_for_load()`.

2. **Take a snapshot** to understand the page structure.
   - Prefer an accessibility snapshot or interactive element list when the tool provides one.
   - With browser-harness, use `page_info()` for a quick state check and `js(...)` for targeted DOM inspection.

3. **Check the console** for JavaScript errors.
   - Clear or record the current console output before exercising a new page or flow when the tool supports it.
   - With browser-harness, use CDP or page scripts to collect console and runtime errors if they are not exposed by a higher-level helper.
   Do this after every navigation and after every significant interaction. Silent JS errors are high-value findings.

4. **Take a screenshot** to visually assess the page and identify interactive elements.
   - Use Playwright screenshots, browser-harness `capture_screenshot()`, or the active browser tool's screenshot command.
   - If the tool provides element refs, annotations, selectors, labels, or coordinates, use them to map visible targets to follow-up interactions.

5. **Test interactive elements** systematically:
   - Click buttons and links by element ref, selector, accessible label, text, or coordinates.
   - Fill forms with representative valid and invalid values.
   - Test keyboard navigation with Tab, Enter, Escape, and relevant shortcuts.
   - Scroll through pages and scrollable containers.
   - Test form validation with invalid inputs
   - Test empty submissions

6. **After each interaction**, check for:
   - Console errors or failed runtime/network events.
   - Visual changes via a fresh screenshot.
   - Expected vs actual behavior

### Phase 3: Collect Evidence

For every issue found:

1. **Take a screenshot** showing the issue.
   Save the screenshot path from Playwright, browser-harness, or the active browser tool; you will reference it in the report.

2. **Record the details**:
   - URL where the issue occurs
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Console errors (if any)
   - Screenshot path

3. **Classify the issue** using the issue taxonomy (see `references/issue-taxonomy.md`):
   - Severity: Critical / High / Medium / Low
   - Category: Functional / Visual / Accessibility / Console / UX / Content

### Phase 4: Categorize

1. Review all collected issues.
2. De-duplicate — merge issues that are the same bug manifesting in different places.
3. Assign final severity and category to each issue.
4. Sort by severity (Critical first, then High, Medium, Low).
5. Count issues by severity and category for the executive summary.

### Phase 5: Report

Generate the final report using the template at `templates/dogfood-report-template.md`.

The report must include:
1. **Executive summary** with total issue count, breakdown by severity, and testing scope
2. **Per-issue sections** with:
   - Issue number and title
   - Severity and category badges
   - URL where observed
   - Description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshot references (use `MEDIA:<screenshot_path>` for inline images)
   - Console errors if relevant
3. **Summary table** of all issues
4. **Testing notes** — what was tested, what was not, any blockers

Save the report to `{output_dir}/report.md`.

## Browser Capability Reference

| Capability | Purpose | Playwright MCP / browser-harness examples |
|------|---------|---------|
| Navigate | Go to a URL | Playwright navigate; browser-harness `new_tab(url)` |
| Inspect page | Read DOM, accessibility tree, or interactive targets | Playwright snapshot; browser-harness `page_info()` or `js(...)` |
| Click | Activate a visible target | Element refs/selectors/text; browser-harness `click_at_xy(x, y)` |
| Type/fill | Enter text into fields | Playwright fill/type; browser-harness keyboard or JS helpers |
| Scroll | Inspect below-the-fold content | Playwright mouse/wheel; browser-harness scroll helpers or CDP |
| History | Return to prior page | Playwright back; browser-harness browser history helpers or JS/CDP |
| Keyboard | Test focus and shortcuts | Press Tab, Enter, Escape, and relevant shortcuts |
| Screenshot | Capture visual evidence | Playwright screenshot; browser-harness `capture_screenshot()` |
| Console | Capture runtime errors and warnings | Playwright console events; browser-harness CDP/runtime inspection |

## Tips

- **Always check console output after navigating and after significant interactions.** Silent JS errors are among the most valuable findings.
- **Use screenshots before and after interactions** when you need to reason about visible state, element positions, or unclear refs/selectors.
- **Test with both valid and invalid inputs** — form validation bugs are common.
- **Scroll through long pages** — content below the fold may have rendering issues.
- **Test navigation flows** — click through multi-step processes end-to-end.
- **Check responsive behavior** by noting any layout issues visible in screenshots.
- **Don't forget edge cases**: empty states, very long text, special characters, rapid clicking.
- When reporting screenshots to the user, include `MEDIA:<screenshot_path>` so they can see the evidence inline.
