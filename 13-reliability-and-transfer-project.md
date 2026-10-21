# Lesson 13: make the system reliable and apply it elsewhere

Learning outcome: explain what happens after failure, then design a second use case without assuming the same architecture is always appropriate.

## 1. From demonstration to operation

A successful request is one observation. Before other people rely on an application, establish who can use it, what actions are permitted, which data is accessed, how failures are detected and who responds. The local sample intentionally has no production user authentication and uses a local SQLite database. Its permission flags and persistence demonstrate concepts; a hosted adaptation must choose appropriate identity, authorization and durable storage.

Use a simple record of the application version, prompt/tool definitions, corpus/data version, model/deployment and settings. If the model or source documents change, rerun relevant evals. Pin dependencies for a deployed environment and record the actual package versions; the optional requirements file is a learning convenience rather than a verified lockfile.

## 2. Recovery behavior to define explicitly

| Failure | Safe behavior to investigate | Evidence |
|---|---|---|
| Model/service unavailable | Show a clear status; use a declared fallback or human route | Error category, request ID, bounded attempts |
| Timeout after a write | Check saved state before retrying the same idempotent operation | Request ID, payload, existing record |
| Malformed tool arguments | Reject before execution and return a recoverable error | Arguments, schema check, unchanged state |
| Missing/contradictory evidence | Abstain or send to human review | Source versions and unresolved question |
| App restart | Restore durable pending work and avoid duplicate effects | Queue/state before and after restart |
| Bad release | Stop the affected action or roll back to a known version | Version history, failing cases, recovery owner |

Avoid an automatic approval fallback when a model, extraction step or service fails. Define retry budgets and appropriate backoff; do not retry every error. A circuit breaker can temporarily stop calls to a repeatedly failing dependency. Recovery must consider both model output and state already changed by software.

## 3. Observe what users experience

Track request success/review/error rates, latency distribution, timeouts, model/tool-call counts, token/service usage, invalid tool arguments and duplicate/conflict events. Observe quality on representative labeled samples and user feedback; a running endpoint can still deliver poor answers. Investigate source freshness and changing input distributions when performance shifts.

Use request/correlation IDs to connect events. Avoid logging secrets, unnecessary sensitive documents or hidden model reasoning. Prefer the minimum trace needed to explain permitted tool decisions, evidence, status and saved state, with appropriate access and retention for the real deployment.

## 4. Access and untrusted content

Treat retrieved documents, uploaded content and tool outputs as untrusted data. Prompt instructions help communicate intended behavior, but software must enforce access and action boundaries. Authenticate users; restrict accessible records; validate arguments; scope writes; and put required approvals before the consequential action.

Add tests for a disallowed record, a forged approval argument, an injected instruction, stale/conflicting policies and an unexpected response shape. Check that denied operations leave state unchanged. A model refusal and an application denial are different defenses and should be evaluated separately.

For broader governance study, [NIST's AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) provides a voluntary lifecycle framework. Translate relevant principles into concrete controls and ownership for the actual project rather than treating a checklist as proof of safety.

## 5. Transfer project: a support-ticket assistant

Choose a new domain to test whether the patterns have transferred. A small support-ticket assistant is one option; inventory notes, document triage or internal knowledge support are alternatives.

Start with eight to twelve fictional tickets you author yourself. Give each an ID, text, category, urgency, customer tier and expected handling. Include a missing description, duplicate request, unsupported request, misleading urgency language and an injected instruction. Keep expected labels in an evaluator-only file.

### Design before building

1. State the user need and a measurable outcome.
2. Build a deterministic baseline such as keyword routing and required-field checks.
3. Decide where a model adds value: category suggestion, relevant guidance or a draft response.
4. Define read-only tools and any proposed write, such as creating a pending follow-up. Sending a customer message is a separate consequential action and is not required for this exercise.
5. Specify data access, approval, state, idempotency and a human escalation route.
6. Author task and adversarial cases; choose a held-out subset before tuning.

### Acceptance evidence

- Compare the baseline and model-assisted design using the same relevant tasks.
- Show one correct answer, one abstention and one blocked action.
- Retry a pending follow-up request without duplicating it.
- Restart and restore state; explain the remaining operating limitations.
- Explain a failure and a tradeoff to a peer/mentor.

The existing `learning_demos metrics` command illustrates score/label arithmetic only. It does not train or classify your tickets; implement the baseline and chosen model step separately.

## 6. Self-review rubric

| Dimension | Evidence of understanding |
|---|---|
| Scope | Clear user, desired outcome and non-goals |
| Architecture | A justified role for rules, model, tools and people |
| Data | Known provenance, quality, access and refresh needs |
| Evaluation | Baseline, representative cases, held-out work and error analysis |
| Reliability | Explicit permission, retry, persistence and recovery behavior |
| Communication | Reproducible instructions, limitations and next owner |

For each dimension, mark: **can explain**, **can demonstrate**, or **needs another experiment**. Repeat the weakest part. A second working project with a different design choice is stronger evidence than memorizing the first project's code.
