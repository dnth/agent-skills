---
name: persona-ux-test
description: >
  Run an isolated persona-based UX test through the real desktop or browser UI.
  Creates a precise non-developer user persona, gives the tester only an approved
  product introduction, prevents source-code and design-document leakage, and
  produces an evidence-based English evaluation report. Use for persona testing,
  blind UX evaluation, real-user simulation, interaction feedback, usability
  testing, first-time-user testing, or user-perspective product evaluation.
---

# Persona UX Test

Use an isolated subagent to simulate a precise target user and blind-test the product through its real UI. The tester may read only the approved product introduction and must not access source code, design documents, or implementation details.

## Scope and safety boundaries

- Applies to desktop applications, web products, and local web UIs.
- Prefer computer-use and browser tools that operate the real UI.
- Do not use source code, databases, logs, API calls, developer tools, or internal design notes to explain the product.
- Do not deploy, upload, publish, install OTA updates, make payments, send external messages, perform bulk deletion, or take other irreversible actions.
- Use user-provided accounts, tokens, and API keys only for this test's UI configuration. Never write them into the skill, report, screenshot notes, or messages.

## Step 1: Fix the test contract

Determine before testing:

1. The product entry point or launch method.
2. The single product introduction file or page the tester may read.
3. The real-environment tools the tester may use.
4. Permitted and prohibited external actions.
5. Where to enter test credentials and how to protect them.
6. The core user task and expected deliverable.

Ask the user only when missing information would change the permission boundary, risk an irreversible action, or prevent access to the product. The host agent sets other details reasonably.

Completion criterion: the entry point, allowed introduction, tools, side-effect boundary, credential handling, core task, and expected deliverable are explicit.

## Step 2: Define a precise persona

The persona must be specific enough to change operating decisions. Include at least:

| Dimension | Requirement |
|---|---|
| Identity | Name, age, location, occupation, or organizational role |
| Technical ability | Familiar tools and technical concepts they do not understand |
| Business context | The real problem they are trying to solve |
| Adoption motive | Why they would try this product |
| Main concerns | Privacy, cost, overreach, failure, result quality, or similar risks |
| Usage environment | Device, language, and available time |
| Behavioral traits | Patience, willingness to explore, and natural response to errors |
| Success criteria | What the user must receive to consider the task complete |

Do not tailor the persona to the existing interface. Do not include internal product terms or navigation answers.

Completion criterion: each dimension is concrete and can affect what the tester notices, attempts, trusts, or abandons.

## Step 3: Create an isolated subagent

Use a subagent with no conversation history. Give it only:

- the precise persona;
- the single approved product introduction;
- the core user task;
- authorization to use computer-use and browser tools;
- credentials required for this test;
- safety boundaries and the report format.

Explicitly prohibit it from reading:

- `AGENTS.md`, source code, design documents, implementation plans, or Git history;
- tests, databases, internal logs, or network/API responses;
- the host agent's analysis, existing defect lists, or expected navigation path.

Do not tell the tester the “correct” workflow. Failure to find an entry point, understand a concept, or recover from an error is test evidence.

Completion criterion: the subagent starts with only the approved context, permissions, credentials, task, and reporting contract.

## Step 4: Run the real-UI blind test

The tester follows ordinary user intuition to:

1. Find and enter the product, then describe its understanding of the first screen.
2. Complete first-time setup and connect an account or model when required.
3. Create a realistic task tied to the persona's work.
4. Try to start the task and observe progress, collaboration, failures, approvals, and takeover controls.
5. Inspect participant status, work history, artifacts, and the final deliverable.
6. On error, attempt natural recovery no more than twice.
7. Leave the environment recoverable and retain test data.

Record key actions, UI feedback, waits, wrong turns, errors, and recovery outcomes. If a sensitive field displays a complete credential, do not retain screenshots containing it.

Completion criterion: every reachable task step has observable UI evidence, and every blocked step records the blocker and recovery attempts.

## Step 5: Grade the evidence

Label every report conclusion as exactly one of:

- `Observed`: the tester directly saw or caused it through the UI.
- `User inference`: the tester's interpretation of the interface, which may differ from the product's actual behavior.
- `Unverified`: the tester could not confirm it because of access, permissions, errors, or the test boundary.

Automation success, page existence, or model self-report does not prove user understanding. Never report a blocked task as complete.

Completion criterion: every conclusion has one evidence label and no completion claim exceeds the observed UI evidence.

## Step 6: Write the evaluation report

Write the report in English with:

1. Persona and test environment.
2. Test scope, entry point, and completion status.
3. Key experience timeline.
4. Experience strengths.
5. Issue list.
6. Terms the user did not understand.
7. Trust, privacy, and sense of safety.
8. Willingness to keep using and pay for the product.
9. Top five improvements.
10. Unverified areas.

Each issue must include:

| Field | Meaning |
|---|---|
| Severity | P0 unusable; P1 core task blocked; P2 significant friction; P3 detail-level issue |
| Scenario | What the user was doing when the problem occurred |
| Reproduction steps | Ordinary user actions in the UI only |
| Actual result | Observable UI response |
| User impact | Effect on task completion, understanding, or trust |
| Evidence type | `Observed`, `User inference`, or `Unverified` |

Do not propose engineering implementations, cite source code or design documents, or reveal credentials.

Completion criterion: all ten sections are present, each issue has every required field, and claims remain within the graded evidence.

## Step 7: Close out as the host agent

After receiving the report:

- Confirm that the test respected isolation, sensitive-information handling, and irreversible-action boundaries.
- Separate real UI evidence from tester inference.
- Preserve important user language verbatim; do not defend the product.
- Deliver the report and state the completed test scope.
- State unverified items and any recoverable test data left in the real environment.

Completion criterion: the user receives the report, tested scope, unverified scope, and retained-test-data note without credential leakage.
