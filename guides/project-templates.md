# Reusable project and teaching templates

Copy sections into your own evidence folder. Replace bracketed prompts with concrete, testable statements. These are practice templates; use your project's official standards and rubric where provided.

## 1. Executable specification for any coding agent

```text
Task: Add [one precise behavior] to [module/function].
User need and scope:
Inputs and types:
Outputs and types:
Required behavior:
Error/recovery behavior:
Permission boundary and state changes:
Edge cases and expected outcomes (at least three):
Existing behavior to preserve:
Acceptance checks and commands:
Files/areas expected to change:
Completion report: explain the diff, checks run and remaining limitations.
```

Use this exact practice request with Claude Code, OpenAI Codex or Gemini CLI:

> In `examples/ai_systems/core.py`, extend `profile_csv` to flag an email with leading or trailing whitespace using the label `email_whitespace`. Preserve the existing labels. Add one isolated synthetic test proving the whitespace case is detected and a valid address remains accepted. Run the offline suite and explain the diff. Do not change provider integrations or the existing fixtures to make tests pass.

This is an exercise to perform in a branch/worktree, not an unimplemented requirement of the current sample.

## 2. Scoped brief / PRD

```text
Problem, user and current workflow:
Business/customer outcome and success measure:
In scope / non-goals:
Inputs, data sources, lineage and refresh cadence:
Output contract and interface:
Pseudocode / decision sequence:
Edge case 1: input -> expected behavior
Edge case 2: input -> expected behavior
Edge case 3: input -> expected behavior
Model vs deterministic software vs human decisions:
Permissions, data handling and review gates:
Evaluation cases and acceptance criteria:
Cost/latency assumptions:
Dependencies, owners and open questions:
```

## 3. Data readiness note

| Dataset/field | Finding and example | Impact on scope | Blocking? | Owner | Resolution/validation |
|---|---|---|---|---|---|
| Customer ID | [duplicate/missing/ambiguous] | [wrong join or duplicate write] | [yes/no] | [named role] | [testable check] |
| Dates/freshness | [format, stale record, future value] | [decision affected] | [yes/no] | [role] | [check and refresh cadence] |
| Provenance/permission | [source or access gap] | [data cannot be used yet] | [yes/no] | [role] | [evidence needed] |

Add profiling date/reference date, sample size, known blind spots and who signs off the remaining gaps. Keep sensitive record values out of shared notes.

## 4. Architecture decision and ownership

```text
Decision and date:
Context and constraints:
Options considered:
Chosen approach and why:
Evidence (eval quality, latency, cost and operational fit):
Tradeoffs and failure/recovery behavior:
Deployment/data/identity boundaries:
Conditions that would cause us to revisit the decision:
Owner and next review:
```

| Step | Model proposes | Software enforces | Human owns |
|---|---|---|---|
| Customer lookup | Tool choice/arguments | Validation and read scope | Correct source/access approval |
| Extraction | Service/model predicts fields | Contract validation and review routing | Ambiguous/unsupported evidence |
| Review creation | Reason and requested action | Caller authorization, allowed customer, idempotency | Authorization and review decision |
| Policy answer | Draft with source references | Source/version access and checks | Unsupported/high-impact interpretation |

Use measured evidence before moving from a deterministic workflow to a single agent or more elaborate coordination.

## 5. Eval and model comparison record

```text
Run ID/date and code revision:
Provider, exact model/deployment/tag and API:
SDK/server/runtime version and settings:
Dataset/corpus version and reference date:
Development cases vs held-out evaluation, with related records grouped:
Case ID, input, independently authored expected outcome:
Expected tools/arguments, state and recovery:
Actual trajectory, state, final answer and citations:
Failure category and severity:
Manual review of automatic grading:
Change made and regression result:
Baseline comparison, error costs and uncertainty/variation:
```

| Provider/model | Cases passed / total | Tool/state failures | Grounding/citation issues | Warm latency | Usage and actual cost | Notes |
|---|---|---|---|---|---|---|
| [exact deployed model] | [result] | [counts/types] | [observations] | [measured distribution] | [provider units/rates] | [limits] |
| [local model/tag] | [result] | [counts/types] | [observations] | [cold and warm] | [hardware/time; no fabricated API bill] | [memory/quantization] |

Keep mock results in a separate wiring-verification record. Avoid feeding expected answers to the model. Record false positives and false negatives in automated grading.

## 6. Cost, deployment and runbook

```text
Workload: requests/day, documents/pages, concurrency and peak assumptions.
Model calls/request: normal path, tool loop and retry scenarios.
Per-call usage: input, output, cache and reasoning fields per provider rules.
Additional costs: extraction, retrieval, compute, storage and monitoring.
Pricing source/date and uncertainty:
Monthly low/base/high estimate and biggest drivers:
Application/service limits and budget alerts:
Deployment host, region and rationale:
Identity, permissions, configuration and remaining secret handling:
Durable state, restart/retry, backup and rollback approach:
Logs/metrics/request IDs, failure alerts and support owner:
Practice resource inventory and cleanup date/owner:
```

Runbook: environment prerequisites -> install -> configure -> smoke test -> start -> reproduce common failure -> recover -> verify state -> escalate. Never include literal secrets. A budget alert is not a hard spending cap.

## 7. Implementation handoff and project review

```text
Purpose, user and demonstrated outcome:
Working POC: data layer, agent, interface and how to run it:
Architecture and ownership decisions:
Data sources, quality gaps and refresh/permission owners:
Evaluation results, representative failures and untested conditions:
Risk review, review gates and model/software/human split:
Deployment path, cost/latency assumptions and monitoring:
Human workflow before/after; exception and review ownership:
Known limitations, prioritized next work and receiving owner:
Evidence links and reproducible demo script:
```

Practise answering: Why is an agent justified here? What fails first? How do you know? Which decisions must remain human? What changes at ten times the volume? What is ready for handoff and what still needs engineering work?

## 8. Evidence and handoff templates

Use these independently of a provider. Replace sample requirements with the criteria you chose for your project.

| Requirement ID | Criterion | Command/input | Expected | Observed | Evidence file/line/correlation ID | Mode/build | PASS/FAIL/UNVERIFIED | Limit/owner |
|---|---|---|---|---|---|---|---|---|
| R-1 | Every linked party screened | Named synthetic case | All party IDs checked | Fill from trace | Sanitized path and event | Replay and commit | Fill after running | Live variation untested |

Five useful minimum demonstration checks cover reading real data rather than embedding case facts in prompts, completing the scoped task, an honest pending-review interface without application approval controls, a runnable case with clean logs, and missing-data/unknown-ID behavior without a crash or unnecessary model call. Write explicit checks for the subset you implement. Passing those five is not equivalent to passing every hard-rule eval or proving production readiness.

For each capability, write **claim → evidence → limitation**. Include mode (authored/replay/live), exact command, dataset/suite fingerprints, code version, relevant file/line or correlation ID, test selection and unverified conditions. Do not claim an eval run when you only ran a floor checker.

```text
Monitoring: metric / window / minimum sample / threshold / owner / response.
Control: action / permission class / identity source / resource+payload scope / approval check / default deny test.
Attack: ID / input path / command / correlation ID / observed / expected / severity.
Open question: question / impact / owner / evidence needed / blocked work / next review.
Escalation: Signal / sanitized Evidence / Ask / receiving owner / next update.
```

A runbook entry needs a trigger, immediate safe action, diagnostic command, expected observation, recovery verification and owner. Distinguish pausing a failing service workflow from approving one particular review. Ask another person to reproduce the handoff on a clean branch using only the instructions; record where they needed help.
