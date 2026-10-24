# Learning path and readiness

This is a standalone guide to applied AI systems, with a practical focus on language models, retrieval, tools, evaluation and human review. It supports self-study, pairing or mentor-led sessions. The schedule is flexible; readiness comes from explaining and demonstrating behavior, not completing a fixed number of days.

## Scope and prerequisites

Start with basic programming: variables, functions, lists/dictionaries and running a command in a terminal. Prior Python experience helps but is not essential if you work through [the cheat sheet](../lessons/02-python.md) and [pytest tutorial](../lessons/03-pytest.md). Use Python 3.10+.

The core project runs offline with the standard library. Pytest, the UI, SDK snippets and Azure exercises have separately documented dependencies. Cloud and local-model inference are optional extensions requiring appropriate access or hardware.

The strongest outcome is understanding how to build, test and operate an AI-assisted application. Classical machine learning, probability, neural network training and model optimization are introduced conceptually; advanced study of those topics needs a longer track.

## Choose a route

| Route | Suggested sequence | Evidence you should produce |
|---|---|---|
| New to AI systems | Start-here guide -> foundations -> Python -> pytest -> project workbook | Explain a request end to end, run tests, diagnose one failure |
| Experienced programmer | Foundations review -> model-provider lab -> project -> evaluation -> reliability | Compare a deterministic baseline with an agent and justify the choice |
| Cloud practice | Offline project -> Azure lab -> deployment/recovery exercises | Explain identity, endpoint, permissions, state and resource cost |
| Mentor | Any learner route -> mentor playbook -> pairing/teach-back | Help someone diagnose a failure and explain the fix themselves |

See [Start here](start-here.md) for a more detailed sequence and checkpoints. Lesson numbers follow the recommended order; use reference guides when needed. For a practical sequence, follow [the learning workshops](learning-workshops.md): lessons 01–08 cover the local engineering patterns; providers and Azure are optional extensions when those services are actually used. No live model account is required for the local replay or MCP exercises.

## Readiness checkpoints

Use [the foundations checklist](foundations-checklist.md) if the technical background is new, and [the data coverage guide](data-coverage-and-next-steps.md) to separate a completed practice exercise from evidence of broader robustness.

| Stage | Demonstration | Understanding check |
|---|---|---|
| Foundations | Sketch the model, application and surrounding system | Explain what is learned during training and what changes during a normal request |
| Data | Profile clean/messy records and write a readiness note | Identify missing, duplicate, stale and untrusted data and the responsible owner |
| Software | Run and extend a small test suite | Explain an assertion, fixture, exception and isolated test double |
| Tools | Read a record and propose a scoped review | Locate validation, authorization and actual state change in code |
| Context/retrieval | Answer a policy question with the right source/version | Separate retrieval failure from unsupported generation |
| Evaluation | Compare outcomes, trajectories and saved state | Explain false positives/negatives, dataset leakage and a held-out test set |
| Integration | Run the interface and restart it | Demonstrate which state survives and which settings are environment-specific |
| Reliability | Inject a failure and recover safely | Explain bounded retries, duplicate prevention, human review and rollback |
| Transfer | Design a second small use case | Decide where rules, a model and a human belong without copying the original workflow |

## A manageable first pass

An orientation weekend can cover the offline setup, a small Python change, data profiling, one agent trace and starter evals. Add several focused sessions for deeper understanding, live model access, cloud setup, reliability and mentoring practice. Allow extra time for permissions and environment issues.

Useful evidence includes a scoped brief, data readiness note, architecture sketch, test/eval report, failure log, ownership table, cost estimate and handoff/runbook. [Templates guide](project-templates.md) supplies templates.

The sample project is a fictional onboarding document-review assistant. Its invoice validation and assigned risk labels are teaching mechanics, not regulatory standards. Transfer the patterns to another domain using [Reliability guide](../lessons/12-reliability-and-transfer.md).

## Mentoring and project agreements

Before working with others, agree who provides technical support, who reviews work, what data may be used, which services/models are available, who owns costs and how unresolved issues are escalated. For self-study, write the same decisions down and use teach-back recordings or a peer review to expose gaps.

A mentor helps the learner reason, diagnose and evaluate. A project owner accepts scope and operational responsibilities. An implementation team receives the handoff when further engineering is needed. One person may hold several roles in a small exercise, but the responsibilities should remain explicit.

## What to deepen after the first project

- Model foundations: tokenization, attention, embeddings, training/inference and uncertainty.
- Retrieval: chunking, metadata/access filters, semantic versus lexical search, reranking and source refresh.
- Evaluation: representative cases, holdouts, error costs, repeated runs and human calibration of graders.
- Reliable software: structured contracts, tests, durable state, authenticated access, observability and recovery.
- Broader ML: supervised/unsupervised learning, preprocessing, baselines, train/validation/test splits and deployment drift.

Deeper topics are linked from the reading list; a functioning demo is a starting point for those investigations.
