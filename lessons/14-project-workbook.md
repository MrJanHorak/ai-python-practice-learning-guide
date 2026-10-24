# 14: Project workbook — eight sessions to build and teach

Allow roughly 90-120 minutes per session plus environment/access delays. Adapt these estimates to your starting point. Use the completion checks for self-review or a conversation with a mentor. Use Python 3.10+ from the repository root.

## Session 1: data readiness and scope

1. Inspect `data/customers_messy.csv` without looking at answers.
2. Write a small brief: who uses the onboarding review assistant, what it helps them do, and which decisions remain human.
3. Profile the data with `python -m examples.ai_systems profile` and inspect `core.py`.
4. Compare your findings with `data/answers/profile_expected.json` and explain which issues the profiler cannot detect.
5. Write the [data readiness note](../guides/project-templates.md); assign owners and blocking/nonblocking status.

Expected: twelve rows with intentional defects, including the duplicate ID on two lines. The clean dataset should have no issues under this narrow checker. All freshness comparisons default to 2026-10-21 for reproducibility; use `--as-of YYYY-MM-DD` for another date.

## Session 2: Python, tests and precise changes

If pytest is new to you, complete [pytest guide](03-pytest.md) first. Its runnable examples cover the test techniques used in this session.

```powershell
python -m unittest discover -s tests -v
```

Read `scoring.py`, then use your chosen coding agent to add one well-scoped validation requirement. Use the same spec if comparing Claude Code, Codex and Gemini CLI. Review every changed line, including tests. Break the range check in a disposable branch/worktree, diagnose the resulting failure and restore it.

Completion check: explain the exception type, relevant frame, input and expected behavior without relying on the coding agent's summary. Do not leave intentional breakage in the main exercise files.

## Session 3: one agent, three tools

```powershell
python -m examples.ai_systems agent --provider mock --prompt "What is the risk tier for C-1002?"
python -m examples.ai_systems agent --provider mock --prompt "Look up C-9999"
python -m examples.ai_systems agent --provider mock --prompt "Create a review for C-1001"
```

Trace model proposal, application validation, tool result and final response. The last command should show `approval_required` and create no review. Configure one real provider through Providers guide and repeat. Inspect its behavior rather than expecting the mock's exact wording.

Completion check: explain how provider-specific messages connect the original call and its result, and where permission checks actually execute.

## Session 4: state, retries and a human decision

```powershell
python -m examples.ai_systems agent --provider mock --prompt "Create a review for C-1001" --allow-write --write-customer C-1001 --request-id session4-001
python -m examples.ai_systems agent --provider mock --prompt "Create a review for C-1001" --allow-write --write-customer C-1001 --request-id session4-001
python -m examples.ai_systems reviews
```

There should be one new record for that request ID. Try a new customer's request while keeping the allowed customer C-1001: it must be blocked by `write_scope_denied`. To test an idempotency conflict, authorize C-1002 and reuse `session4-001` for C-1002; the store must reject the changed payload.

Use the actual review ID in `python -m examples.ai_systems review --id 1 --decision approved --reviewer demo-reviewer`. Restart the app, verify the decision persists and attempt a conflicting rejection. The CLI human decision is not one of the model's tools.

Completion check: explain application authorization versus idempotency versus workflow state. They solve different problems.

## Session 5: extraction and Azure

```powershell
python -m examples.ai_systems validate
python -m examples.ai_systems validate --threshold 0.9
```

Inspect all twelve saved extractions before reading their expected labels. With the default threshold, two fixtures validate and ten require review. D-009's malicious note does not alter deterministic field validation; it still needs a separate agent injection test if used in model context.

Complete the live extraction in Azure guide using the clean, missing-number and injection PDFs. Map the raw result to the application contract and explain each field and confidence value. Add a rendered/scanned version of a synthetic invoice if you want to investigate OCR separately.

Completion check: distinguish raw service output, normalized extraction, deterministic validation, agent explanation and human decision.

## Session 6: interface, evals and failure diagnosis

```powershell
python -m pip install streamlit
python -m streamlit run examples/ai_systems/ui.py
```

Inspect a fixture, run the agent, authorize a scoped review and restart the interface. The saved queue should remain. The fixture display and agent are deliberately separate panels: choosing a fixture does not implicitly send its notes to a model. To explore document context, copy only the synthetic extracted fields/notes into a clearly delimited prompt and keep writes disabled.

Run `python -m examples.ai_systems eval --provider mock`, then a configured real provider. Categorize tool, argument, state, recovery, context, answer and environment failures. Record a false positive or false negative caused by an overly strict eval; improve that check with an independently justified requirement.

Completion check: help another person diagnose one failure using hints while they operate the keyboard.

## Session 7: retrieval and provider comparison

```powershell
python -m examples.ai_systems search "confidence threshold"
python -m examples.ai_systems agent --provider mock --prompt "What does the retention policy say?"
```

Use the questions in `data/answers/retrieval_questions.json` as evaluator-only labels. Compare: all active policy text in the initial prompt; a deterministic search before generation; and model-triggered `search_policy`. Keep the question set and active source versions fixed. The supplied CLI implements the last approach; implement the first two as small exercises.

Check whether the right source was retrieved, whether the answer is supported, whether the citation names the right version, and whether missing evidence is acknowledged. Exclude the obsolete 0.70 policy. The corpus does not define a document-retention duration.

Repeat the same lookup/review questions across Anthropic, OpenAI, Gemini and a suitable local model as access permits. Track exact model/version, latency, usage, state and failure types using [the comparison template](../guides/project-templates.md). You can prepare the lab using mock even if all cloud providers are not available yet.

Completion check: explain a measured difference without confusing model ability, API compatibility, account configuration or hardware limitations.

## Session 8: deployment plan, handoff and mock lab

Prepare the deployment plan from [the Azure lesson](10-azure.md) and [project templates](../guides/project-templates.md). Include a cost model for multiple calls per request, retries, document extraction, retrieval, hosting and logs. Label assumed rates and volumes. Make the human workflow before/after visible.

Rehearse a five-minute technical explanation and a two-minute nontechnical explanation. Select one intentionally broken configuration from [the Mentor playbook](../guides/mentor-playbook.md), give it to a partner and coach them through recovery. Compare your evidence with the agreed project criteria and identify remaining gaps.

Completion check: demonstrate the working data + agent + interface, eval results, risk/ownership decisions, deployment plan and handoff brief. Extend the project by integrating extraction, orchestration and knowledge support, then apply the patterns to another domain.

## Integration workshops: connect the lessons

The eight sessions above use the original invoice/provider project. For the linked-record integration patterns, complete these additional sessions without mixing datasets:

1. **Scope/data/configuration:** lessons 04–05. Profile `data/linked_review/`, read the YAML example and write scope plus open questions with owners. Completion: explain one join and one coverage gap.
2. **Context/search:** lesson 06. Retrieve the current scoped policy, minimise document fields and test must-keep state. Completion: wrong-jurisdiction and stale-policy tests fail when filters are deliberately broken. Azure is optional.
3. **MCP and failures:** lesson 07. Run the server/client tests, inspect a schema error, a denied write and a timeout after commit. Completion: show actual tool calls and unchanged/one-row state as appropriate.
4. **Evaluation/oversight:** lessons 08 and 11. Write independent expected behavior, compare matching suite versions and record attack attempts. Completion: separate hard-rule evidence, ordinary quality scores and unverified conditions.
5. **Operations/documents/handoff:** lessons 12–13 and the templates. Explain per-case cost, a monitoring action, repeated document groups and privacy at each boundary. Completion: another learner can reproduce your evidence and name its limitations.

Use [the learning workshops](../guides/learning-workshops.md) to choose a project, define a small change and record baseline results. The practice runner has no interface; the original Streamlit interface is part of the separate invoice/provider example.
