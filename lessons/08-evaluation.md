# 08: Measure behavior and learn from errors

Learning outcome: design a small experiment that distinguishes useful performance from a demo that happened to work. Start with an expected outcome that was chosen independently of the implementation.

## 1. Different checks answer different questions

| Check | Question | Example |
|---|---|---|
| Unit test | Does one deterministic component meet its contract? | Invalid score raises ValueError |
| Integration/contract test | Do connected pieces exchange the expected data? | Provider response produces a correctly linked tool-result message |
| Model/system eval | Does the configured model/application perform representative tasks? | Correct lookup, grounded answer, safe state change and recovery |
| Usability observation | Can a person understand and complete the workflow? | Reviewer finds the evidence and handles an exception |

A fake network response makes tests repeatable. It cannot establish real model quality or endpoint compatibility. A live answer that looks correct cannot establish idempotency. Combine checks that target the different boundaries. [The pytest tutorial](03-pytest.md) covers the deterministic layers.

## 2. Define outcomes and baselines first

Specify the task, acceptable actions, correct final state, failure behavior and human-review route. Compare at least one simpler baseline: direct lookup, required-field rules, a keyword search or a fixed workflow. Measure quality, latency, cost and operational constraints using the same relevant tasks.

For agent tasks, evaluate final answers, tool choice/arguments, state changes, unauthorized actions and recovery. Avoid enforcing one exact tool sequence unless the order itself is required: several trajectories can produce the same valid result. The starter evaluator uses some strict sequences and substrings; human review should identify false positives and false negatives in its grading.

## 3. Confusion matrices and misleading accuracy

Suppose positive means "should be reviewed". True positives are correctly flagged cases; false positives are unnecessary flags; false negatives are missed cases; true negatives correctly remain unflagged.

- Precision = TP / (TP + FP): of the flags raised, how many were appropriate?
- Recall = TP / (TP + FN): of the cases needing review, how many were found?
- Accuracy = (TP + TN) / all cases: how many labels matched overall?

The tiny `classification_scores.csv` contains twenty invented labels and scores, with only two positives. A baseline that flags nobody has 90% accuracy and zero recall. It is therefore a poor choice if finding positives is essential. At threshold 0.5, the demo has TP=1, FP=3, FN=1, TN=15: precision 25%, recall 50%, accuracy 80%. Which tradeoff is useful depends on error costs and review capacity.

```powershell
python -m examples.ai_systems.learning_demos metrics --threshold 0.5
python -m examples.ai_systems.learning_demos metrics --threshold 0.35
python -m examples.ai_systems.learning_demos metrics --threshold 0.85
```

Scores are authored values, not predictions from a trained model. They are not calibrated probabilities. Undefined precision/recall is returned as null when its denominator is zero. Use this exercise to understand the arithmetic, not to choose a deployment threshold from twenty cases. See [scikit-learn's metric reference](https://scikit-learn.org/stable/modules/model_evaluation.html) for more metrics and their limitations.

## 4. Representative cases and held-out evaluation

Separate cases used for iteration from those reserved to assess the final design. In classical ML, training fits parameters, validation guides selection and a test set estimates performance after selection. Prompt and tool-description tuning can also overfit a known eval set.

Do not feed expected labels into context or use a held-out test set to repeatedly select prompts/thresholds while still calling it untouched. Keep related records together when splitting: pages of one document, repeated customers or paraphrases of the same case can leak information across splits. For a task that predicts future behavior, consider time ordering and data freshness.

The supplied twelve starter agent cases are visible and small. They are useful for development, not an independent estimate of broad performance. Author additional cases with a peer/mentor and preserve a separate final set. General guidance on [data leakage](https://scikit-learn.org/stable/common_pitfalls.html) also applies to how you prepare evaluation data.

## 5. An experiment you can reproduce

1. Write a hypothesis: e.g., a more specific tool description will reduce incorrect lookup calls without increasing unnecessary writes.
2. Freeze the relevant dataset/corpus, code revision, model/deployment, settings and grader.
3. Run the baseline and the changed version on the same cases.
4. Change one major factor at a time. Record latency, calls, usage, final state and failure categories.
5. Inspect individual regressions, not only the aggregate pass rate. Repeat relevant live cases when variability matters.
6. Review a held-out set once the design is selected and state what remains uncertain.

Twelve passes in twelve trials establish that those trials passed. They do not prove that all future requests are reliable. A larger, representative set and uncertainty estimates are needed for stronger claims; average quality alone can also hide a small class of serious failures.

## 6. Retrieval and answer evaluation are separate

Label which sources are relevant and whether the question is answerable. Check whether relevant sources appear among the retrieved results. Then check whether every important generated claim is supported by the returned source/version. Include missing evidence, obsolete policies, conflicting sources and documents the user cannot access.

An LLM judge is another fallible grader. Compare its judgments with human labels, keep a written rubric, inspect disagreements and account for its model/version. Do not assume its scores are ground truth or allow the judge to make business decisions outside its role.

## A small evidence report

Use the [evaluation template](../guides/project-templates.md). Include objective, baseline, cases and split, code/model/settings, rubric, results, worst failures, changes, repeated-run variation, cost/latency and unresolved limitations. Explain which findings come from deterministic tests, scripted fixtures or live models.

## End-to-end evaluation workshop

Start with the five practice cases: `python -m examples.learning_lab eval --split practice`. The runner prints JSONL with final status, tool events, review count and fingerprints. It checks only status, pending convention and review count. A passing row is not evidence that every hard rule was tested.

Extend the evaluator with independently authored requirements in these layers:

| Layer | Example check |
|---|---|
| Final answer | No unsupported approval or policy citation |
| Tool selection | Required tools called; forbidden tools absent |
| Arguments | Company, jurisdiction and date match the retrieved application |
| Trajectory | Every party screened; required calls happen before consequential writes; retries bounded |
| State | Exactly one review exists, with correct reasons; source application unchanged |
| Recovery | Unavailable data remains visible and does not create a recommendation |

Write a requirement ID, input, expected result and source for each new case. Classify observed failures as code, data, specification or unresolved ambiguity, citing the evidence. Keep a severity table separate from the failure category. Grade hard-rule checks individually before an aggregate score. `replay_missing` is an unexecuted scenario, not a pass.

If given messy evaluation data, inspect duplicate IDs, missing labels, invalid types, contradictory expected outcomes and unknown origins. Fix the evaluator data with a documented reason, preserve the original baseline, and version the corrected suite; do not quietly relabel failures to match the current implementation.

For a regression comparison, dataset and suite fingerprints must match. Record build, context variant, faults and actual dependencies too. Demonstrate one improvement and one unchanged control. The supplied runner fingerprints selected files, not the complete execution environment. After choosing changes, run `python -m examples.learning_lab eval --split holdout` once. If you use that result to tune, create a fresh holdout before claiming independent validation.

Continue with [MCP test examples](07-mcp-and-integration-tests.md) for spies and state checks, [oversight](11-oversight-permissions-and-red-teaming.md) for adversarial findings and [templates](../guides/project-templates.md) for evidence records.

The supplied split is educational: its labels and regression tests are visible. It is not a blind benchmark. Once you have seen them, obtain fresh independently authored cases for meaningful held-out validation.

## Check understanding

Why can 90% accuracy be poor? Why does a passing mock not prove model quality? Can a test set remain held out after using it to select ten successive prompts? How would you grade two different valid tool sequences?

Answer: consider the base rate and error costs; mocks supply authored behavior; repeated selection leaks test information into design; grade required outcomes and constraints while allowing valid alternatives unless order is part of the contract.
