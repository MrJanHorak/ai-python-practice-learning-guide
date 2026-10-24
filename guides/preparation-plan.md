# Prep Plan and Exercises

A hands-on plan that mirrors your project's arc. Start at [README](../README.md), use the supplied synthetic data, and complete [the project workbook](../lessons/14-project-workbook.md). Choose your pace and success criteria; local exercises do not require an organisation account.

---

## A beginner preparation sequence

1. **Understand one request:** foundations, Python and pytest (lessons 01–03). Explain a function and a failed assertion before delegating a change.
2. **Read the inputs:** configuration/replay and scope/data (04–05). Profile the linked tables and write the four-line scope.
3. **Choose the right evidence:** context/search (06). Find the right policy version locally before trying Azure Search.
4. **Connect real tools:** MCP/integration tests (07). List tools, inspect an error and prove one write survives a retry without duplication.
5. **Measure and explain:** evaluation (08), then the reliability cost exercise (12). Distinguish authored/replay/live results and preserve unverified gaps.
6. **Add live services when ready:** provider comparison (09), Azure (10), oversight (11) and document pipelines (13). Finish the workbook (14) and rehearse mentoring with the learning workshops.

Allow several sessions; installation and new concepts can take longer than running the commands. Use [the learning workshops](learning-workshops.md) to plan a practical sequence and [the glossary](glossary.md) whenever a word is unfamiliar. Complete the local path before spending time on unavailable services. Use one live model provider first, then compare through [the provider lesson](../lessons/09-model-providers.md).

## Exercise 0: Data readiness

1. Inspect `data/customers_messy.csv` before opening the answer key.
2. Record duplicates, missing fields, invalid formats, stale rows and unclear provenance.
3. Run `python -m examples.ai_systems profile` and compare with your own findings.
4. Write a data readiness note using [Templates guide](project-templates.md), naming the owner and whether each gap blocks the build.
5. Compare with `data/customers_clean.csv`. The profiler is a baseline, not an exhaustive quality checker.

---

## Exercise A: Agent-driven engineering

**Goal:** practice delegating, reviewing and diagnosing.

1. Use this repository first, or choose a small public Python repo with tests.
2. Clone it, create a venv, install dependencies, run the tests. Note the baseline pass count.
3. With an AI coding agent, ask for one small change (add a function parameter, a CLI flag, or input validation).
4. **Review the diff line by line.** Write down: anything unrequested, anything missing, anything you don't understand.
5. Run tests. Deliberately ask the agent for something slightly ambiguous, observe the failure, then rewrite the request as an executable spec and compare results.
6. Create a git worktree and run a second, independent change there.

**Mentor lessons to capture:** where the agent over-reaches, what a vague request produced vs. a precise one, how long diagnosis took.

## Exercise B: Python reading and pytest

1. Read the Python lesson sections 1-5, then complete [the pytest tutorial](../lessons/03-pytest.md).
2. Run `python -m pytest tutorials/pytest -v` and explain a plain assertion, a parametrized case and `pytest.raises`.
3. Use fixtures and `tmp_path` to test retries and a denied write without touching your normal database.
4. Inspect the fake model transport and network guard. Explain which behavior they verify and what still needs a live test.
5. Introduce a bug in a disposable branch, read the failure and fix it. Add an independently justified regression case.

## Exercise C: A mini agent with a tool

1. Run the supplied agent with `--provider mock`; inspect `lookup_customer` (read), `search_policy` (read) and `flag_for_review` (write).
2. Make `flag_for_review` **idempotent** (calling twice creates one flag).
3. Make error messages tell the model how to recover (for example, expected ID format).
4. Add a max-iteration guard and log token usage per call.
5. Try to break it: ambiguous IDs, missing customer, user asks something that needs no tool.

Use `--allow-write --write-customer C-1001 --request-id practice-001` to authorize one customer's pending local review. These permissions come from the application, not the model's arguments. Repeat the request and inspect `reviews`; then change the payload with the same request ID and inspect the conflict.

## Exercise D: Starter eval suite

1. Run `python -m examples.ai_systems eval --provider mock`; inspect `data/eval_cases.json` and the completed harness.
2. Write 10 cases: 4 happy path, 3 edge cases, 2 adversarial (prompt injection in a document field, asking the agent to flag everyone), 1 out-of-scope.
3. Label every failure with a taxonomy category. Aim for 4-6 categories.
4. Change the tool description and re-run. Did the pass rate move? Which categories?
5. Add **trajectory** checks (which tools, in what order) and a **state** check (exactly one flag written).

The supplied twelve cases are starter checks. The mock is scripted and is not an accuracy baseline. Repeat with a configured live provider, record its model ID and inspect the checks' limitations. Add an injection test using `invoice-injection.pdf`; the model must treat document instructions as untrusted data and the application must still enforce write scope.

## Exercise E: Context engineering

1. Start with `data/policies/`, which includes active and obsolete policies, then expand to a longer policy corpus.
2. Version 1: stuff it all in the prompt and ask 5 questions. Record tokens and accuracy.
3. Version 2: chunk and retrieve only relevant sections (simple keyword or embedding search).
4. Version 3: give the agent a `search_policy(query)` tool for JIT retrieval.
5. Compare accuracy, tokens and cost. Write three sentences on when each wins.

## Exercise F: Azure Document Intelligence

1. Follow [Azure guide](../lessons/10-azure.md) in the learning path sandbox, or a suitable personal subscription after checking permissions and cost.
2. Use the three supplied synthetic PDFs in `data/documents/`: clean invoice, missing identifier and injected instructions. Render/scan a copy if you want to compare OCR quality; these initial PDFs are native text.
3. Run the Python extraction command, inspect raw output and normalize it into the lab contract.
4. Compare actual fields with `data/document_manifest.json`. The hand-authored JSON confidence fixtures are not captured Azure outputs.
5. Validate with the supplied fixture pipeline. Investigate 0.8 versus 0.9 against labels, missing confidence and invalid values before choosing thresholds.
6. Record data/PII decisions and the human-review route at every connection.

## Exercise G: Cost model and Autonomy Ladder

1. Using usage from Exercise C, estimate cost per request and monthly cost at 1,000, 10,000 and 100,000 requests/day (use current published prices).
2. Identify the biggest cost driver (input from repeated context? long outputs?).
3. Place each part of your mini agent on the Autonomy Ladder and justify. Which steps should simply be deterministic code?
4. Propose one routing rule (cheap model for X, strong model for Y).

## Exercise H: Risk and handoff

1. List every action your mini agent can take. Mark read vs. write and reversible vs. irreversible.
2. Mark where a human approval gate belongs.
3. Write the **model / software / human** ownership split in one table.
4. Write a one-page handoff brief: purpose, architecture, evals, known gaps, run instructions, cost, risks.

Also map the human workflow before and after the change: reviewer, evidence, approval/rejection, exceptions and owner. Use [the templates](project-templates.md).

## Exercise I: Interface and persistent state

1. Run the optional Streamlit interface described in README.
2. Inspect an extraction fixture, run a customer lookup and create a scoped pending review.
3. Stop and restart the interface; verify the review is still present.
4. Trace one request through interface, provider, tool and SQLite state. Diagnose one failure at each boundary.

## Exercise J: Deployment and recovery

1. Complete [the Azure lab](../lessons/10-azure.md), including identity and endpoint diagnosis.
2. Deploy only to an approved host and record the deployment choice and alternatives.
3. Inspect useful logs, request IDs, latency, token usage and costs. Exclude credentials and sensitive fields.
4. Inject a timeout, wrong configuration or denied permission; identify the first diagnostic check and an escalation route.
5. Review resources created and clean up the practice scope when finished. Budget alerts do not stop consumption.

## Exercise K: Later extension sessions blocks

- **Workflow:** persist pending/approved/rejected state, retry a request and resume after restart. The model must not perform the human decision.
- **Knowledge support:** answer the five questions in `data/answers/retrieval_questions.json`; verify retrieval, source versions, citations and abstention separately.
- **Integration rehearsal:** combine extraction, workflow and retrieval; explain user value, software quality, risks, data needs and deployment choices.

---

## Mentor support playbook

### When a learner says "the agent is wrong"

1. Capability problem or information problem? (Does it have what it needs in context?)
2. Look at the **trajectory**: tools called, arguments, results.
3. Re-read the spec: could a careful human misread it?
4. Check tool schema and error messages.
5. Check for an eval that would have caught it. If none, write one.
6. Check permissions, state and idempotency.

### Coaching questions (better than giving the answer)

- "What did you expect, and what happened instead?"
- "Which line of the diff worries you most?"
- "How would you know this is working? What test shows it?"
- "What's the smallest input that reproduces it?"
- "What does the model see at that step?"
- "Who owns this decision, the model, the code, or a human?"

### Feedback rubric for specs, PRDs and briefs

| Check | Strong | Weak |
|---|---|---|
| Testable | Each requirement has a pass/fail test | "Should be fast / accurate" |
| Edge cases | At least three realistic ones with expected behavior | Happy path only |
| Ownership | Clear who owns data, decisions, approvals | Implicit |
| Risk | Irreversible actions have gates | No mention |
| Cost | Tokens/request and volume estimated | "Cheap" |
| Scope | Explicit non-goals | Unbounded |

### Common learner traps

- Trusting the agent's summary instead of reading the diff.
- Evals that only check the final answer.
- Dumping whole documents into context.
- Write tools that duplicate on retry.
- Multi-agent designs where a workflow would do.
- Human approval placed after the irreversible step.
- Hard-coded API keys in the repo.
- Using real customer data in experiments.

---

## Self-check before a project review

- [ ] Run a Python repo's tests and diagnose a failure
- [ ] Review an agent's diff and name three issues
- [ ] Create and remove a git worktree
- [ ] Explain retrieval vs. JIT search and give a tradeoff
- [ ] Explain idempotency with a KYC example
- [ ] Show a small eval suite with failure categories
- [ ] Estimate monthly cost for a given workload
- [ ] Interpret Document Intelligence confidence scores
- [ ] Explain the running example; use the optional domain glossary only if relevant
- [ ] Profile messy data and write a data readiness note
- [ ] Trace a request across interface, model, tool and persistent state
- [ ] Reproduce a denied write and a retry without duplicate state
- [ ] Diagnose local versus Azure-hosted identity/configuration differences
- [ ] Coach a learner through one failure using staged hints
- [ ] Explain project outcomes against agreed acceptance criteria

## Decisions to record for yourself or with a study partner

1. Will you study independently, pair with someone or ask a Mentor to review evidence?
2. Which coding tool and application models can you access, and which exercises will remain offline?
3. Can you reproduce a baseline and keep expected outcomes separate from model inputs?
4. If you choose Azure, which subscription, resource scope, permissions, cost limit and cleanup plan will you use?
5. What requirements, forbidden actions and evidence will define success for your project?
