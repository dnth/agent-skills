# Humanizing PR Patterns

Patterns to avoid and their fixes, adapted for PR writing. Based on the humanizer skill.

## Opening Lines to Avoid

| Robotic | Human |
|---------|-------|
| "This PR implements..." | "Users were hitting X error, so I..." |
| "This change introduces..." | "The login flow was confusing users..." |
| "In order to improve..." | "To fix the timeout issue..." |
| "This PR addresses issue #123 by implementing..." | "Fixes #123 - users couldn't upload files larger than 5MB" |

## AI Vocabulary to Avoid

These words signal AI-generated text:

- **crucial, pivotal, key, vital** → Just say what it does
- **enhance, improve, optimize** → Be specific about what changed
- **seamless, intuitive, robust** → Show, don't tell
- **Additionally, Moreover, Furthermore** → Just start the next sentence
- **showcase, demonstrate, exemplify** → Use "adds", "shows", "includes"

**Before:**
> This PR introduces a crucial enhancement to the authentication flow, seamlessly integrating OAuth2 to provide a more robust and intuitive user experience.

**After:**
> Users can now log in with Google. This replaces the old email-only flow.

## Bullet List Anti-Patterns

### Inline-header lists (very AI-coded)

**Before:**
> - **Performance:** Improved query speed by 40%
> - **Security:** Added rate limiting to prevent abuse
> - **UX:** Simplified the form layout

**After:**
> Query speed improved 40% after adding an index. Rate limiting now blocks >100 req/min per IP. The form got simpler.

### Rule of three forcing

**Before:**
> This update makes the app faster, more reliable, and easier to maintain.

**After:**
> This update cuts load time by half. (The refactoring also made the code easier to debug.)

## Promotional Language

Don't market your own code:

| Avoid | Use instead |
|-------|-------------|
| "elegant solution" | "simple fix" or just describe it |
| "comprehensive rewrite" | "rewrote X to do Y" |
| "state-of-the-art" | name the specific tech |
| "significantly improved" | "improved X by Y%" |

## Em Dash Overuse

**Before:**
> The old implementation—which relied on synchronous calls—was causing timeouts—especially under load. This fix—using async—solves that.

**After:**
> The old implementation used synchronous calls and timed out under load. Switching to async fixed it.

## Vague Attributions

**Before:**
> This should improve performance in most cases.

**After:**
> Benchmarks show 40% faster load times on the test dataset.

## False Ranges

**Before:**
> This refactor touches everything from database queries to frontend components.

**After:**
> This refactor touches the User model and the profile page component.

## Sycophantic Tone

Never use in PRs:
- "Hopefully this helps"
- "Please let me know if you have questions"
- "Happy to make changes"
- "I believe this approach"

Just state what you did. Reviewers will ask questions if they have them.

## What Wasn't Done (Scope Honesty)

AI-generated PRs often omit what's missing. Be explicit:

**Good:**
> Note: This doesn't migrate existing users yet. They'll still see the old flow until phase 2.

**Also good:**
> I considered adding Redis caching here but decided against it - the DB is fast enough for our current scale.

## Adding Voice

Good PRs sound like a person wrote them:

**Soulless:**
> The authentication module was refactored. Error handling was improved. Tests were added.

**Has personality:**
> The auth module was getting hard to follow - three different error formats, no clear entry point. I consolidated it into one handler with consistent error types. Took a while but should save debugging time later.

## Pre-answering Questions

Anticipate what reviewers will ask:

**Good:**
> You might wonder why I didn't use the existing util here - it doesn't handle null cases correctly, which is what caused the last incident. Filed #456 to fix that separately.

**Also good:**
> The diff looks big but 90% is generated protobuf code. The actual logic changes are in `handler.go` (lines 45-80).
