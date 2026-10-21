# Lesson 08: eight sessions to build and teach the project

Allow roughly 90-120 minutes per session plus environment/access delays. Adjust to your starting point. The completion checks are practice evidence, not the programme's official assessment rubric. Use Python 3.10+ from the repository root.

## Session 1: data readiness and scope

1. Inspect `data/customers_messy.csv` without looking at answers.
2. Write a small brief: who uses the onboarding review assistant, what it helps them do, and which decisions remain human.
3. Profile the data with `python -m examples.ia_prep profile` and inspect `core.py`.
4. Compare your findings with `data/answers/profile_expected.json` and explain which issues the profiler cannot detect.
5. Write the data readiness note from lesson 10; assign owners and blocking/nonblocking status.

Expected: twelve rows with intentional defects, including the duplicate ID on two lines. The clean dataset should have no issues under this narrow checker. All freshness comparisons default to 2026-10-21 for reproducibility; use `--as-of YYYY-MM-DD` for another date.

## Session 2: Python, tests and precise changes

```powershell
python -m unittest discover -s tests -v
```

Read `scoring.py`, then use your chosen coding agent to add one well-scoped validation requirement. Use the same spec if comparing Claude Code, Codex and Gemini CLI. Review every changed line, including tests. Break the range check in a disposable branch/worktree, diagnose the resulting failure and restore it.

Completion check: explain the exception type, relevant frame, input and expected behavior without relying on the coding agent's summary. Do not leave intentional breakage in the main exercise files.

## Session 3: one agent, three tools

```powershell
python -m examples.ia_prep agent --provider mock --prompt "What is the risk tier for C-1002?"
python -m examples.ia_prep agent --provider mock --prompt "Look up C-9999"
python -m examples.ia_prep agent --provider mock --prompt "Create a review for C-1001"
```

Trace model proposal, application validation, tool result and final response. The last command should show `approval_required` and create no review. Configure one real provider through lesson 06 and repeat. Inspect its behavior rather than expecting the mock's exact wording.

Completion check: explain how provider-specific messages connect the original call and its result, and where permission checks actually execute.

## Session 4: state, retries and a human decision

```powershell
python -m examples.ia_prep agent --provider mock --prompt "Create a review for C-1001" --allow-write --write-customer C-1001 --request-id session4-001
python -m examples.ia_prep agent --provider mock --prompt "Create a review for C-1001" --allow-write --write-customer C-1001 --request-id session4-001
python -m examples.ia_prep reviews
```

There should be one new record for that request ID. Try a new customer's request while keeping the allowed customer C-1001: it must be blocked by `write_scope_denied`. To test an idempotency conflict, authorize C-1002 and reuse `session4-001` for C-1002; the store must reject the changed payload.

Use the actual review ID in `python -m examples.ia_prep review --id 1 --decision approved --reviewer demo-reviewer`. Restart the app, verify the decision persists and attempt a conflicting rejection. The CLI human decision is not one of the model's tools.

Completion check: explain application authorization versus idempotency versus workflow state. They solve different problems.

## Session 5: extraction and Azure

```powershell
python -m examples.ia_prep validate
python -m examples.ia_prep validate --threshold 0.9
```

Inspect all twelve saved extractions before reading their expected labels. With the default threshold, two fixtures validate and ten require review. D-009's malicious note does not alter deterministic field validation; it still needs a separate agent injection test if used in model context.

Complete the live extraction in lesson 07 using the clean, missing-number and injection PDFs. Map the raw result to the application contract and explain each field and confidence value. Add a rendered/scanned version of a synthetic invoice if you want to investigate OCR separately.

Completion check: distinguish raw service output, normalized extraction, deterministic validation, agent explanation and human decision.

## Session 6: interface, evals and failure diagnosis

```powershell
python -m pip install streamlit
python -m streamlit run examples/ia_prep/ui.py
```

Inspect a fixture, run the agent, authorize a scoped review and restart the interface. The saved queue should remain. The fixture display and agent are deliberately separate panels: choosing a fixture does not implicitly send its notes to a model. To explore document context, copy only the synthetic extracted fields/notes into a clearly delimited prompt and keep writes disabled.

Run `python -m examples.ia_prep eval --provider mock`, then a configured real provider. Categorize tool, argument, state, recovery, context, answer and environment failures. Record a false positive or false negative caused by an overly strict eval; improve that check with an independently justified requirement.

Completion check: help another person diagnose one failure using hints while they operate the keyboard.

## Session 7: retrieval and provider comparison

```powershell
python -m examples.ia_prep search "confidence threshold"
python -m examples.ia_prep agent --provider mock --prompt "What does the retention policy say?"
```

Use the questions in `data/answers/retrieval_questions.json` as evaluator-only labels. Compare: all active policy text in the initial prompt; a deterministic search before generation; and model-triggered `search_policy`. Keep the question set and active source versions fixed. The supplied CLI implements the last approach; implement the first two as small exercises.

Check whether the right source was retrieved, whether the answer is supported, whether the citation names the right version, and whether missing evidence is acknowledged. Exclude the obsolete 0.70 policy. The corpus does not define a document-retention duration.

Repeat the same lookup/review questions across Anthropic, OpenAI, Gemini and a suitable local model as access permits. Track exact model/version, latency, usage, state and failure types using lesson 10's comparison table. You can prepare the lab using mock even if all cloud providers are not available yet.

Completion check: explain a measured difference without confusing model ability, API compatibility, account configuration or hardware limitations.

## Session 8: deployment plan, handoff and mock lab

Prepare the deployment plan from lesson 07 and templates from lesson 10. Include a cost model for multiple calls per request, retries, document extraction, retrieval, hosting and logs. Label assumed rates and volumes. Make the human workflow before/after visible.

Rehearse a five-minute technical defense and a two-minute executive explanation. Select one intentionally broken configuration from lesson 09, give it to a partner and coach them through recovery. Map your evidence to the lead's actual Day 10 rubric and identify remaining gaps for the later blocks.

Completion check: demonstrate the working data + agent + interface, eval results, risk/ownership decisions, deployment plan and handoff brief. Later capstone practice adds integrated extraction, orchestration and knowledge support across all six lenses.
