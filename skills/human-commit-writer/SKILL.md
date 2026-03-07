---
name: human-commit-writer
description: 'Write git commit messages that sound human, not AI-generated. Analyzes diffs, stages files intelligently, and generates conventional commit messages with natural voice. Use when user asks to commit changes, create a git commit, or mentions "/commit".'
license: MIT
allowed-tools: Bash
---

# Human Commit Writer

Write commit messages that sound like a person wrote them, using Conventional Commits.

Based on principles from [Simon Tatham's guide](https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/commit-messages/).

## Core Principle

**Information over typography.** Focus on what to include, not minor style details. A commit message's job is to communicate, not to follow arbitrary rules.

## Who Reads Your Commits

Consider your audience:
- **Users** - "Should I update to this version?"
- **Bug investigators** - "Was this change intentional or a side effect?"
- **Code reviewers** - "Should I accept this patch?"
- **Other developers** - "How has the code changed?"
- **Future you** - "What was I thinking?"

## Before Writing

Ask yourself:
1. **What's the user-visible change?** What does the program do differently?
2. **Why did I make this change?** What problem does it solve?
3. **What's NOT in this commit?** Be honest about scope.
4. **Would I say this out loud?** If it sounds robotic, rewrite it.

## Conventional Commit Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Commit Types

| Type       | Purpose                        |
| ---------- | ------------------------------ |
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `docs`     | Documentation only             |
| `style`    | Formatting/style (no logic)    |
| `refactor` | Code refactor (no feature/fix) |
| `perf`     | Performance improvement        |
| `test`     | Add/update tests               |
| `build`    | Build system/dependencies      |
| `ci`       | CI/config changes              |
| `chore`    | Maintenance/misc               |
| `revert`   | Revert commit                  |

## Workflow

### 1. Analyze Diff

```bash
# If files are staged, use staged diff
git diff --staged

# If nothing staged, use working tree diff
git diff

# Also check status
git status --porcelain
```

### 2. Stage Files (if needed)

If nothing is staged or you want to group changes differently:

```bash
# Stage specific files
git add path/to/file1 path/to/file2

# Stage by pattern
git add *.test.*
git add src/components/*
```

**Never commit secrets** (.env, credentials.json, private keys).

### 3. Generate Commit Message

Analyze the diff to determine:

- **Type**: What kind of change is this?
- **Scope**: What area/module is affected?
- **Description**: One-line summary in plain language (<72 chars)
- **Body** (if needed): Why this change? What's interesting? What's NOT included?

### 4. Execute Commit

```bash
# Single line
git commit -m "<type>[scope]: <description>"

# Multi-line with body/footer
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<optional body>

<optional footer>
EOF
)"
```

## What to Include

### Describe User-Visible Behavior

What does the program do differently after this change?

```
fix: prevent duplicate charges on slow connections

Previously, clicking "Pay" twice quickly would submit two charges.
Now the button disables after first click until request completes.
```

### Explain WHY

The reason isn't always obvious from the code.

```
refactor: drop IE11 support

Usage dropped below 0.5% last month. Removes ~200 lines of polyfills.
```

### Mention Side Effects

If your change has known side effects, say so.

```
feat: add request logging

All API calls now log to /var/log/api.log. Disk usage will increase
~50MB/day at current traffic levels.
```

### Describe What's NOT Included

Be honest about scope. What did you intentionally leave out?

```
fix: timeout on large file uploads

Bumped body parser limit to 50MB. Didn't add progress indicator yet -
that's tracked in #456.
```

### Pre-Answer Obvious Questions

If reviewers will wonder "why not do X?", answer it.

```
perf: use connection pooling for DB

Considered pgBouncer but decided against it - our single-instance setup
doesn't need the extra complexity. Can revisit if we add replicas.
```

### Link External Context

Reference related issues, commits, or documentation.

```
fix: handle null response from user API

Closes #123
Refs: a1b2c3d (where the null handling was removed)
```

## Writing Style

### Pyramid Writing

Put the most important information at the top. Readers should be able to stop when they lose interest.

**Bad (bury the lead):**
```
refactor: update user module

The user module has been around since 2019 and uses callbacks.
Modern async/await patterns are more readable. This commit updates
the module to use async/await. The getUser() function now returns
a Promise instead of taking a callback.
```

**Good (lead with impact):**
```
refactor: convert user module from callbacks to async/await

getUser() now returns a Promise. All call sites updated.

The module predates async/await (2019). Callbacks made error handling
error-prone - we had 3 bugs last month from forgotten callbacks.
```

### Make Before/After Clear

Use explicit markers to distinguish old vs new behavior.

**Good patterns:**
- "Previously X, now Y"
- "Before this change: X. After: Y"
- "X used to happen. This patch makes Y happen instead."

```
fix: prevent session expiry during active use

Previously, sessions expired after 30 minutes regardless of activity.
Now, the timer resets on each API call, so active users stay logged in.
```

### Make Every Commit Unique

Subject lines should distinguish commits from each other. Generic subjects force readers to click through.

**Too generic:**
```
fix: bug fix
fix: fix issue
refactor: cleanup
```

**Unique and informative:**
```
fix: duplicate charges on double-click
fix: null pointer when user deleted mid-request
refactor: extract validation logic from User model
```

### Line Wrapping

Wrap body text to 72 characters. Standard git tools don't rewrap, so long lines require horizontal scrolling.

## Humanizing Commits

### Quick Reference

| Robotic | Human |
|---------|-------|
| "Implement comprehensive auth enhancement" | "add password reset flow" |
| "Refactor codebase for improved maintainability" | "extract user validation into helper" |
| "Update dependencies to latest versions" | "bump react to 18.3, fixes hydration bug" |
| "Add functionality for X" | "let users do X" |
| "This commit introduces..." | Just say what changed |

### Anti-Patterns

**Don't start with "This commit":**
```
# Bad
feat: This commit adds user authentication

# Good
feat: add user authentication
```

**Avoid AI vocabulary:**
- crucial, pivotal, key, vital → just say what it does
- enhance, improve, optimize → be specific
- seamless, robust, comprehensive → show, don't tell
- Additionally, Moreover → just start the next sentence

**Don't over-explain:**
```
# Bad
fix: resolve issue where users were experiencing timeouts when attempting to upload large files to the server

# Good
fix: timeout on large file uploads
```

**Be specific, not promotional:**
```
# Bad
refactor: implement elegant solution for state management

# Good
refactor: use zustand instead of context for state
```

### Breaking Changes

```
# Exclamation mark after type/scope
feat!: remove deprecated /api/v1 endpoint

# Or with footer
feat: require auth for all /api routes

BREAKING CHANGE: unauthenticated requests to /api/* now return 401
```

### No Functional Change (NFC)

For pure refactoring, say so upfront:

```
refactor: extract helper function (NFC)

No functional change - just moves validation logic into separate
function for reuse in upcoming #456.
```

## Humanizing Checklist

Before committing, verify:

- [ ] Lead with user-visible impact (or NFC if refactoring)
- [ ] Explain WHY, not just WHAT
- [ ] Subject line is unique - distinguishes this commit
- [ ] No "This commit" or "This change" in message
- [ ] No AI vocabulary (crucial, enhance, seamless, etc.)
- [ ] Before/after states are clear (if describing behavior change)
- [ ] Under 72 characters in subject line
- [ ] Body wrapped to 72 characters
- [ ] Honest about scope - what's NOT included
- [ ] Links to related issues/commits

## Git Safety Protocol

- NEVER update git config
- NEVER run destructive commands (--force, hard reset) without explicit request
- NEVER skip hooks (--no-verify) unless user asks
- NEVER force push to main/master
- If commit fails due to hooks, fix and create NEW commit (don't amend)

## Further Reading

- [Simon Tatham - Writing Commit Messages](https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/commit-messages/)
- [Conventional Commits](https://www.conventionalcommits.org/)
