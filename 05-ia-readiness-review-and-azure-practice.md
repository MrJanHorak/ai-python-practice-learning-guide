# IA readiness review and Azure practice

Reviewed 21 October 2026 against the programme scope PDF and preparation guides 01-04. These are preparation recommendations, not additional programme requirements.

Implementation update: guides 01-04 have now been revised. [README](README.md) indexes the added provider, Azure, project, IA-support and template lessons. The original findings below are retained as the review record; current runnable examples are in `examples/ia_prep/` and synthetic datasets in `data/`.

## Overall assessment

The existing guides cover the first ten days' concepts well, especially specifications, reviewing agent changes, context, tools, evals, cost and risk. The largest opportunity is to connect these topics in one working application and practise helping someone else diagnose its failures.

The deck describes code literacy and agent-led engineering, including reading Python, rather than becoming a Python expert from scratch. It explicitly identifies Azure AI Document Intelligence in the later extraction lab. It does not fix a coding-agent vendor, model provider, Python-only stack, agent framework, database, UI framework or Azure hosting service. Obtain the actual lab stack before investing deeply in a framework.

## Gaps against the programme

| Priority | Deck evidence | Preparation to add | Evidence of readiness |
|---|---|---|---|
| First | Day 1, PDF p.4: profile data and name gaps and owners | Profile synthetic CSV/JSON: missing fields, duplicates, inconsistent types, dates, freshness and provenance. Produce a data readiness note. | Explain which defects block the use case, who resolves them and what can proceed. |
| First | Day 6, p.6: working data layer, agent and interface | Build a small interface connected to the same data and agent used in the tool exercises. Include loading, error and review states. | Demonstrate a complete request and trace a failure across the UI, agent, tool and stored state. |
| First | Days 5, 7 and 9, pp.6-8: permissions, recovery, production stack | Add HTTP/JSON, timeouts, bounded retries, identity, service permissions, deployment configuration and useful logs. | Diagnose an access failure, malformed response, rate limit, timeout and duplicate write. |
| First | Assessment, p.11: daily deliverables form the Day 10 assessment | Maintain an evidence folder mapped to each day. Obtain the official scoring guidance and examples. | Find the POC demo, eval report, risk review, deployment plan and handoff brief quickly. |
| Next | Protected Learning overview, p.9: workflow orchestration | Persist workflow state, pause for human review, resume after restart and avoid duplicate side effects. | Replaying or restarting a request does not create duplicate review records. |
| Next | Protected Learning overview, p.9: knowledge and decision support | Evaluate retrieval separately from generated answers; check citations, missing evidence, stale material and refresh. | Show a case where retrieval fails and one where the answer fails despite retrieving the right material. |
| Later | Capstone, pp.9 and 11 | Integrate extraction, workflow and knowledge support; prepare technical and executive explanations of the same solution. | Defend decisions across all six lenses and show human oversight. |

Day 9 asks for a deployment decision and plan; it does not require a fully production-ready Phase 1 deployment. Azure deployment practice is especially relevant to the Document Intelligence block.

## Specific changes to the existing material

### 01: Vocabulary glossary

- Add tenant, subscription, resource group, region, endpoint, deployment name, quota, Microsoft Entra ID, principal, RBAC, data-plane permission and managed identity.
- Add HTTP status, timeout, bounded retry, backoff, correlation ID, long-running operation and persistent workflow state.
- Clarify that retrieval is the process of fetching relevant information; RAG uses retrieved information for generation. Just-in-time search is a timing/control strategy that can also use retrieval. They are not mutually exclusive categories.
- Use provider-specific token and pricing terminology. Reasoning-token billing and caching behavior vary by provider and model.
- Treat MTA and CTD as programme labels until the lead confirms their formal expansions and responsibilities.

### 02: Python cheat sheet

1. Fix the mismatch between `test_bad_input_raises` and `score`: the shown `score` function does not raise for a negative score. Either validate the agreed range, or explicitly label this as an intentionally failing exercise with a repair task.
2. Put a maximum number of steps directly into the agent-loop example. Include a clear exhausted-budget result, request timeout, tool-name dispatch and validation of tool arguments. Keep write authorization in application code.
3. Label the tiny eval harness as incomplete: `run_agent` raises `NotImplementedError`. Supply a completed local exercise before relying on it during a lab.
4. Add pytest fixtures, monkeypatching/mocks and separation of offline tests from live API tests. Repeatable grading should not depend entirely on an external model call.
5. Add HTTP request/response inspection, status codes and retry behavior; distinguish asynchronous Python from a service's long-running operation/poller.
6. Add tested PowerShell instructions alongside Bash. For example: `py -m venv .venv`, `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, and `.\.venv\Scripts\python.exe -m pytest`. Check the lab's actual Python launcher and version first. Using the venv executable directly avoids requiring activation changes.
7. Configure the model name and endpoint rather than embedding one model throughout. A direct Anthropic example teaches useful mechanics, but it is not evidence that the programme uses that provider.
8. Expand cost estimates to include repeated model calls, retries, retrieval, document processing, hosting and monitoring where applicable. Use the selected provider's actual usage fields and rates.

Focus Python study on reading functions and modules, dictionaries/lists, type hints, exceptions, context managers, dataclasses/Pydantic, pytest, HTTP/JSON and the SDK calls in the real labs. Practise explaining what code does before asking an agent to change it.

### 03: Reading list

- Replace broad homepages and "search for" instructions with a specific page, a purpose and a small exercise. Keep the pre-Day-1 list manageable.
- Update Azure terminology: current Microsoft documentation uses **Microsoft Foundry**. Match the environment actually provisioned for learners.
- Use the current [AI-901 fundamentals material](https://learn.microsoft.com/en-us/credentials/certifications/exams/ai-901/) and selected [AI-103 developer topics](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/AI-103) as study maps rather than centering the older AI-900/AI-102 references. Taking an exam is optional for this preparation.
- Add the official [Document Intelligence exercises](https://microsoftlearning.github.io/mslearn-ai-document-intelligence/) and, if the programme uses Foundry, the [Azure agent exercises](https://microsoftlearning.github.io/mslearn-ai-agents/). Prioritize a basic agent, custom function and MCP exercise before multi-agent work.
- Prioritize the programme's own risk standards and examples of acceptable work. Public responsible-AI reading provides context but cannot establish the internal assessment bar.

### 04: Prep plan and exercises

- Keep the eight-hour weekend as orientation. It does not demonstrate readiness to troubleshoot the whole programme.
- Add the Day 1 data profiling task and Day 6 interface integration task.
- Extend Exercise F from a Studio experiment into a Python pipeline that reads a document, extracts results, validates the output schema and creates a human-review item when needed.
- Select the extraction model to match the document and inspect its actual output. Available fields and confidence values vary; missing confidence needs explicit handling.
- Compare extraction with labeled examples. Treat 0.8 and 0.9 as thresholds to investigate, not established production rules. Include missing required fields, date validity and inconsistent values in review decisions.
- Extend Exercise H with the human workflow before and after the POC: reviewer, evidence, approval/rejection, exceptions and final owner.
- Add a small workflow-state drill and a retrieval/citation drill for Protected Learning Blocks 2 and 3.

## One project to connect the preparation

Build a **synthetic onboarding document review assistant**. All service and framework choices below are practice options pending confirmation of the lab stack.

1. Load a small synthetic customer dataset and document its quality issues.
2. Accept a public sample or synthetic document through a basic interface. Streamlit is one possible Python UI; use the programme's framework when known.
3. Call Azure Document Intelligence from Python and validate the extracted result against a schema. Start with a model appropriate for the public sample, such as a prebuilt invoice model for an invoice.
4. Link the extraction to a synthetic customer record. Make absent or conflicting evidence visible.
5. Let an agent call a read-only customer lookup and draft a review explanation using the available evidence.
6. Create a review item through a narrowly scoped, idempotent write. Require any necessary approval in the application, not only in a prompt.
7. Persist the review state so restarting the app does not lose it. Local JSON or SQLite is sufficient for initial practice.
8. Add a small policy collection. Return source references and abstain when the evidence does not support an answer.
9. Run a starter eval set covering tool choice, arguments, resulting state, recovery and grounded answers. Ten cases are a starting exercise, not proof of general reliability.
10. Deploy once to the programme's approved Azure host if available. Otherwise, choose a simple host for personal practice and record the choice as provisional.

Suggested evidence: scoped brief, data readiness note, architecture sketch, runnable app, eval report, failure log, ownership table, cost estimate, deployment runbook and a one-page CTD handoff.

## Azure practice sequence

| Step | Practice | Completion check |
|---|---|---|
| 1. Establish access | Identify tenant, subscription, approved region, resource group, permitted services, quotas and who can assign roles. Use the programme sandbox if available. | Explain where resources live and which identity is making each call. |
| 2. Call one service | Run an official Document Intelligence exercise, then repeat a small extraction from Python. Record package/API versions and the endpoint used. | Inspect the raw result and explain how it maps into the app's schema. |
| 3. Understand identity | Learn local developer authentication, service data permissions and Azure managed identity. A portal role alone does not establish that an application can call the service. | Trace authentication separately from authorization. |
| 4. Deploy the same app | Configure environment settings, identity and an appropriate host. Use Key Vault for secrets that are still required. | Compare local and hosted behavior and explain any identity/configuration difference. |
| 5. Observe and recover | Capture request IDs, durations, status, tool steps, usage and failures with sensitive fields excluded. Practise restart and recovery. | Diagnose one hosted failure from logs. |
| 6. Control spend | Use a dedicated practice scope, small inputs, bounded loops and explicit cleanup. Add a budget alert where permitted. | Identify all resources created and their cost drivers. |

Microsoft recommends token authentication through Entra ID and managed identities for Azure-hosted applications where supported: [Python authentication overview](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview). Document Intelligence has endpoint/resource prerequisites for Entra authentication; follow the selected resource's current guidance: [Python client library](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python).

Budget alerts do **not** stop resources or consumption: [Microsoft budget guidance](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets). Use explicit resource cleanup and service/application limits as appropriate.

Do not treat Key Vault, Container Apps, Foundry, Azure AI Search, Functions or a specific database as programme requirements merely because they are useful Azure options.

## Rehearse the IA role

For each failure below, prepare the symptom, first diagnostic check, a small hint, a larger hint, recovery steps and when to escalate:

- Wrong Python interpreter or missing dependency.
- Missing configuration or wrong endpoint/model deployment.
- Authentication failure, denied service access or network restriction.
- Rate limit or insufficient quota.
- Timeout followed by a duplicate write on retry.
- Unexpected extraction schema, missing field or missing confidence.
- Wrong tool selected, incorrect arguments or an agent that does not stop.
- Relevant policy not retrieved, stale policy or unsupported citation.
- Application restart loses a pending human review.

Use sanitized logs and synthetic data. Have a local fixture-based path for practising while access or service problems are escalated; distinguish fixture results clearly from a successful live integration.

Practise a ten-minute teach-back: another person operates the keyboard while you help them investigate one failure. Assess whether they understand the diagnosis and can reproduce the fix themselves.

Suggested preparation rhythm, adaptable to the time available: two sessions on Python/data/tests; two on the integrated POC; two on Azure/deployment/diagnosis; one on workflow/retrieval; one on a mock lab and handoff. Allow roughly 90-120 minutes per session plus setup/access delays. These are planning estimates, not a readiness guarantee.

## Obtain from the programme lead

1. The exact IA responsibilities, learner support ratio, grading role, escalation route and availability expectations.
2. Actual lab repositories, dependency versions, coding-agent tool, model provider/deployment, UI and hosting choices.
3. Azure sandbox access, allowed regions/services, quota, role-assignment owner, data rules and budget/cleanup arrangements.
4. Day 1 data, Day 4 broken-agent exercise, tool integrations and reference solutions.
5. Internal risk checklist, diagnostic scoring guidance, example daily deliverables and the Day 10/capstone rubrics.
6. Whether your assignment covers all sixteen Protected Learning sessions, and which alliance-partner tools the later sessions introduce.

## Source map

- Programme scope: `GA - MTA Builder Programme - Revised Scope Deck.pdf`, particularly pp.4-11.
- Existing preparation: `01-vocabulary-glossary.md`, `02-python-cheatsheet-for-ia.md`, `03-reading-list-and-tutorials.md`, `04-prep-plan-and-exercises.md`.
- Confidence handling: [Microsoft guidance](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/accuracy-confidence?view=doc-intel-4.0.0).
- External documentation checked on 21 October 2026. The programme's approved environment and official assessment guidance should determine final preparation priorities.
