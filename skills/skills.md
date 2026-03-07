# Human PR Writer

Write PR descriptions that sound like a person wrote them.

## Before Writing

Ask yourself:
1. **What's the human impact?** Why does this matter to users?
2. **What questions will reviewers have?** Pre-answer them.
3. **What's the best reading order?** Guide reviewers through the diff.

## Gather Context

Run the context script to extract git information:

```bash
uv run scripts/pr_context.py
```

This outputs JSON with:
- Current branch and base branch
- Changed files with additions/deletions
- Recent commits

For just the diff:
```bash
uv run scripts/pr_context.py --diff
```

## PR Structure

### Title

```
[Impact prefix] [Action] [Context]
```

Keep under 72 chars. Human-readable.

**Good:**
- "Fix login timeout on slow connections"
- "Add password reset flow"
- "Speed up dashboard load by 40%"

**Avoid:**
- "Implement comprehensive authentication enhancement"
- "This PR introduces..." (never start with "This PR")

### Opening (The Why)

Start with user impact, not technical implementation.

**Template:**
> Users were experiencing [pain]. This change [solution] so that [benefit].

**Example:**
> Users were getting logged out mid-session. This adds a refresh token rotation so sessions stay alive during active use.

**Avoid:**
> This PR implements a comprehensive authentication enhancement to improve user experience.

### The Plot

Explain key changes with trade-off explanations.

**Template:**
```
## What changed

- [Change 1] because [reason/trade-off]
- [Change 2] - decided against [alternative] because [why]

## What I didn't do

- [Out of scope thing] - filing as #XXX for later
```

**Example:**
```
## What changed

- Switched to refresh tokens instead of extending session cookies. Cookies were getting too large and causing issues with some proxies.
- Added rate limiting to the refresh endpoint. Considered using Redis for distributed rate limiting but stuck with in-memory for now - we only have one instance.

## What I didn't do

- Didn't migrate existing sessions. Users will need to log in again after deploy. Filed #456 to add a migration script later.
```

### For Reviewers

Help reviewers navigate your changes.

**Template:**
```
## For reviewers

**Reading order:** [file1] → [file2] → [file3]

**Screenshots:** [prompt for screenshots if UI changes]

**Questions you might have:**
- Why [X]? → [answer]
```

**Example:**
```
## For reviewers

**Reading order:** `auth.py` → `middleware.py` → `tests/test_auth.py`

The diff looks big but most of it is test fixtures. The actual logic is ~50 lines.

**Why not use the existing token util?** It doesn't handle the refresh case correctly - it was generating new tokens on every request instead of reusing them.
```

## Humanizing Checklist

Before finalizing, check against [references/humanizing-pr-patterns.md](references/humanizing-pr-patterns.md):

- [ ] Opens with user impact, not "This PR..."
- [ ] No AI vocabulary (crucial, pivotal, enhance, seamless, etc.)
- [ ] No inline-header bullet lists ("**Performance:** ...")
- [ ] No em dash overuse
- [ ] States what wasn't done (scope honesty)
- [ ] Pre-answers obvious reviewer questions
- [ ] Has some personality/voice, not just dry facts

## Creating the PR

Use `gh` CLI to create:

```bash
gh pr create --title "[title]" --body-file pr_description.md
```

Or edit inline:
```bash
gh pr create --web
```

## Quick Reference

| Robotic | Human |
|---------|-------|
| "This PR implements..." | "Users were hitting X, so I..." |
| "Additionally, Moreover" | Just start the next sentence |
| "seamless, robust, intuitive" | Be specific about what changed |
| "**Category:** Description" bullets | Plain prose or simple bullets |
| "This should improve..." | "Benchmarks show X% faster..." |
