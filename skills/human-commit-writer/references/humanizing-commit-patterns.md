# Humanizing Commit Patterns

Patterns to avoid and their fixes. Based on the humanizer skill and Simon Tatham's commit message guide.

## Opening Lines to Avoid

| Robotic | Human |
|---------|-------|
| "This commit implements..." | "add user login" |
| "This change introduces..." | "switch to JWT auth" |
| "In order to improve..." | "speed up dashboard load" |
| "This commit addresses issue #123 by implementing..." | "fix #123: users couldn't upload files >5MB" |

## AI Vocabulary to Avoid

These words signal AI-generated commits:

- **crucial, pivotal, key, vital** → Just say what it does
- **enhance, improve, optimize** → Be specific about what changed
- **seamless, intuitive, robust, comprehensive** → Show, don't tell
- **Additionally, Moreover, Furthermore** → Just use a new line
- **implement, introduce** → Use simpler verbs (add, fix, use, switch)

**Before:**
> feat: implement comprehensive authentication enhancement with seamless OAuth2 integration for improved user experience

**After:**
> feat: add Google login

## Over-Explanation

Commits don't need to be essays.

**Before:**
> fix: resolve issue where users were experiencing timeout errors when attempting to upload files larger than 10MB to the server, which was caused by the request body parser not being configured to handle large payloads

**After:**
> fix: timeout on files >10MB

> bump body parser limit to 50MB

## Promotional Language

Don't market your own code:

| Avoid | Use instead |
|-------|-------------|
| "elegant solution" | Just describe the change |
| "comprehensive refactor" | "refactor X to do Y" |
| "modern approach" | Name the specific tech |
| "significantly improved" | "improved X by Y%" or just the change |
| "clean up" | "remove X" or "simplify Y" |

## Rule of Three Forcing

**Before:**
> refactor: improve code readability, maintainability, and performance

**After:**
> refactor: extract user validation into helper

## Vague Scope

**Before:**
> fix: various bug fixes and improvements

**After:**
> fix: prevent duplicate emails on signup

## False Technicality

**Before:**
> feat: implement asynchronous non-blocking API request handling with promise-based architecture

**After:**
> feat: add async API calls

## The "Implement" Trap

"Implement" is overused in AI commits:

| Too formal | Natural |
|------------|---------|
| "implement user authentication" | "add user login" |
| "implement caching mechanism" | "add Redis caching" |
| "implement error handling" | "handle API errors" |
| "implement new feature" | Just say what the feature is |

## Em Dash Overuse

**Before:**
> fix: resolve race condition—which was causing duplicate entries—by adding mutex lock—specifically in the user service

**After:**
> fix: race condition causing duplicate users

> Add mutex lock in user service

## Sycophantic Tone

Never use in commits:

- "Hopefully this fixes it"
- "Tried to improve X"
- "Attempt to resolve"
- "Might help with"

State what you did. If you're not sure it works, test it first.

## Context Done Right

Only add context when it's not obvious from the diff:

**Good (non-obvious why):**
```
fix: retry failed payments

Stripe has occasional 500s. Retrying 3x catches most without user
impact. Saw 12 failed payments last week that would've succeeded.
```

**Unnecessary (obvious from diff):**
```
fix: retry failed payments

This commit adds retry logic to the payment function. The retry logic
will retry failed payments up to 3 times.
```

## Scope Honesty

Be specific about scope, not grandiose:

**Bad:**
> refactor: major codebase cleanup and optimization

**Good:**
> refactor: remove unused utils

**Also good:**
> chore: delete dead code from v1 migration

## Before/After Clarity (from Simon Tatham)

Make it clear which state you're describing. Don't rely on tense alone.

**Ambiguous:**
> The code validates email addresses. This is bad because...

Does "validates" describe before or after? Hard to tell.

**Clear:**
> Previously, the code validated emails. Now it also validates phone numbers.

**Clear:**
> Before this change: emails were case-sensitive. After: normalized to lowercase.

**Clear:**
> Users couldn't log in with uppercase emails. This patch normalizes to lowercase before checking.

## Pyramid Writing (from Simon Tatham)

Put the most important information first. Don't bury the lead.

**Bad (background first):**
```
refactor: update user module

The user module has been around since 2019 and uses callbacks.
Modern async/await patterns are more readable. This commit updates
the module to use async/await. The getUser() function now returns
a Promise instead of taking a callback.

Now users can log in faster because getUser() doesn't block.
```

**Good (impact first):**
```
refactor: convert user module from callbacks to async/await

getUser() now returns a Promise. All call sites updated.

This fixes the login delay - callbacks were causing queue blocking
under high load. The module predates async/await (2019).
```

## Unique Subject Lines (from Simon Tatham)

Subject lines should distinguish commits from each other. Generic subjects force readers to click through.

**Too generic (can't tell commits apart):**
```
fix: bug fix
fix: another fix
fix: update code
refactor: cleanup
```

**Unique and informative:**
```
fix: duplicate charges on double-click
fix: null pointer when user deleted mid-request
fix: timeout on large file uploads
refactor: extract validation logic from User model
```

## Adding Voice

Good commits can have personality in the body:

**Soulless:**
> refactor: consolidate error handling

**Has context:**
> refactor: consolidate error handling

> Had 3 different error formats across the codebase. Now just one.
> Should make debugging less painful.

## Pre-Answering Questions

Anticipate what reviewers will ask:

**Good:**
> You might wonder why I didn't use the existing util here - it doesn't handle null cases correctly, which is what caused the last incident. Filed #456 to fix that separately.

**Also good:**
> The diff looks big but 90% is generated protobuf code. The actual logic changes are in `handler.go` (lines 45-80).

## What's NOT Included

Be explicit about scope limitations:

**Good:**
> Note: This doesn't migrate existing sessions. Users will need to log in again after deploy. Filed #456 to add a migration script later.

**Also good:**
> I considered adding Redis caching here but decided against it - the DB is fast enough for our current scale. Can revisit if we add replicas.

## NFC (No Functional Change)

For pure refactoring, say so upfront:

```
refactor: extract helper function (NFC)

No functional change - just moves validation logic into separate
function for reuse in upcoming #456.
```

Some communities use NFCI (No Functional Change Intended) to acknowledge possibility of accidental changes.
