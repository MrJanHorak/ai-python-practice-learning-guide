# Mentor playbook: troubleshooting, coaching and assessment evidence

Goal: help the learner explain and resolve a failure while retaining ownership of their work. Agree on the mentoring scope, review responsibilities, escalation contacts and availability. A learner studying independently can use the same questions for self-review or peer support.

## A short support routine

1. Ask for expected behavior, actual behavior and the smallest reproducing input.
2. Identify the layer: environment, data, interface, model, context, tool, permission or stored state.
3. Inspect evidence: error type/status, relevant code frame/diff, tool trajectory, request ID and state before/after.
4. Offer one small hint. Let the learner run the next diagnostic step.
5. Confirm the fix against the original acceptance criterion and a regression case.
6. Record a sanitized note if the issue is recurring or needs escalation.

If a live service is unavailable, switch to clearly labeled fixtures for independent learning while the service issue is escalated. A fixture pass does not establish live integration.

## Common failures and staged hints

| Symptom | First hint | Next diagnostic step | Escalation/evidence |
|---|---|---|---|
| Package import fails | Which interpreter runs this command? | Compare executable, version and `python -m pip --version`; install into the selected venv | Sanitized import error, Python/package version, launch command |
| Running from another directory fails | Where is the repository root? | Run module commands from the root; inspect module path | Working directory and exact command |
| Missing configuration | Where does this script read its settings? | Compare required environment variable names with `.env.example`; remember `.env` is not auto-loaded | Variable names/presence only, never values of keys |
| 401/authentication failure | Which identity or credential is being presented? | Check credential source, tenant, endpoint and supported authentication method | Timestamp, service, status and request ID; owner handles credential changes |
| 403/access denial | Can this identity perform the data operation? | Check service-data permissions, scope, network restrictions and policy; do not assume Contributor is sufficient | Resource scope, calling identity, request ID to authorized platform owner |
| 404/model not found | Is this a public model name or a deployment name? | Confirm endpoint, deployment/model access and API support | Endpoint host/path without secrets and configured deployment name |
| 429/rate or capacity issue | What limit did the response identify? | Separate quota/capacity from request/token rate; use bounded backoff only when appropriate | Model, time, request ID, volume; quota owner if needed |
| Timeout | Did the server finish after the client stopped waiting? | Inspect operation/request state before retry; use the same idempotency key for the same write | Trace, request ID, saved state and elapsed time |
| Tool selected incorrectly | What did the model see about the tool? | Inspect descriptions, schema, prompt/context and eval case | Minimal synthetic prompt and tool trace |
| Tool arguments invalid | What is the declared contract? | Compare actual keys/types with the schema; use recoverable error feedback | Reproducing arguments without sensitive data |
| Duplicate reviews | Which request ID was reused? | Inspect idempotency key, payload and transaction boundary | Before/after rows and retry sequence |
| Wrong policy/citation | Was the right source retrieved? | Check active version, retrieval results and claim support independently | Question, retrieved source IDs and failed claim |
| Local model chats but never calls tools | Does this model/server support tools? | Verify model tag, API dialect and actual returned tool-call structure | Server/model versions and a minimal tool request |
| Local model is slow | Is the model loading or generating? | Compare cold/warm timings, memory, size/quantization and context length | Hardware, model tag and measured timings |
| Hosted app fails but local works | Which settings/identity changed? | Compare hosted identity, environment variables, endpoint, service permissions and durable storage | Hosted logs with credentials/data excluded |

HTTP status is a clue, not a definitive diagnosis: providers and proxies can report errors differently. Inspect the service's documented error and request ID rather than resetting credentials indiscriminately.

## Three reproducible coaching drills

### Drill A: denied write

Run a mock review request without `--allow-write`. Hint 1: inspect the trace. Hint 2: distinguish the model's proposed action from the application's permission decision. Completion: the learner can explain `approval_required`, then authorize one customer explicitly and verify one pending record.

### Drill B: retry and payload conflict

Create one review, repeat it with the same request ID and then change the payload with that ID. Hint 1: inspect queue length. Hint 2: compare keys and payloads. Completion: one identical operation is replayed safely and a different operation is rejected as a conflict.

### Drill C: confidence and missing evidence

Inspect D-011 and D-012 in the extraction fixtures. Hint 1: separate a low value from an absent value. Hint 2: inspect the validation reason and original source/labels. Completion: the learner can justify review without inventing a confidence value or claiming a threshold is universally safe.

For advanced practice, run the injection PDF through a real model with writes disabled. Distinguish resistance by the model from enforcement by the application. Do not deliberately expose actual secrets as a test.

## Assessment evidence map

Use the following evidence to review understanding. Agree project-specific acceptance criteria with the learner and project owner, or use a peer review for self-study.

| Learning path point | Evidence folder contents | Mentor observation |
|---|---|---|
| Starting point | Code/diff reading, scoped brief, dataset quality findings and tool-comfort baseline | Where does this learner need pacing/support? |
| Scope and data | Discovery checklist, prioritized backlog, readiness note, spec, initial cost estimate and baseline evals | Are requirements testable and edge cases realistic? |
| Working system | Context strategy, scoped tool integration and working data + agent + interface | Can the learner trace a request and justify autonomy? |
| Evaluation and risk | Eval report, failure taxonomy, adversarial cases and ownership/approval decisions | Do checks cover tools, trajectory, state and recovery? |
| Handoff | Deployment plan, cost model, peer-reviewed brief and explanation | Are scope, limitations and next owner clear? |
| Transfer project | A second use case with independently chosen architecture and evaluation | Can the learner apply the ideas without copying the first design? |

The supplied twelve eval cases are starter checks. Do not invent a universal pass percentage or treat a mock pass as evidence of learner mastery. Calibrate feedback with examples of strong, borderline and incomplete work. A self-studying learner can record a teach-back and review it against the same criteria.

## Independent practice and help-request drills

Use [the learning workshops](learning-workshops.md) to record the selected project, interpreter, dependencies, branch, recording variant and expected selected tests. Explain new terms before using acronyms. Ask the learner to predict an observation before running a command.

Rehearse: (1) an MCP server waiting normally versus failing to start, (2) a query denied by Azure versus a local filtered result, (3) an unsupported replay variant, (4) skipped assignment tests, and (5) a reply lost after a committed write. Use [lesson 07](../lessons/07-mcp-and-integration-tests.md) for local reproducible checks.

Keep responsibilities explicit: **Own** diagnosis and staged hints; **Share** scope/rubric ambiguity with a study partner or project owner; **Hand off** credentials, platform policy, production access and authorization exceptions. Escalate with **Signal / Evidence / Ask**, naming an owner and leaving secrets out. A missing business fact remains an open question with an owner.

## Support-note template

```text
Date/session:
Learner/team (use the approved identifier):
Expected vs actual:
Layer and minimal synthetic reproduction:
Evidence/request ID (sanitized):
Hints offered and what the learner concluded:
Resolution and regression check:
Escalation owner / next update:
```
