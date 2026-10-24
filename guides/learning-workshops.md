# Learning workshops: build, inspect and explain

Use these workshops independently, with a study partner or with a Mentor. Choose your pace and return to an exercise when you need more practice. Begin with [Start here](start-here.md) and use [the glossary](glossary.md) when a word is unfamiliar.

## Two projects, deliberately separate

The original `examples.ai_systems` project teaches provider protocols, invoices and a local review queue. The new `examples.learning_lab` project teaches linked records, scoped context, constructed replay and real MCP. Its IDs begin `PRACTICE-`. Keep each project's fixtures together; their identifiers and contracts differ. Neither project automatically makes a real-world onboarding decision.

A coding agent edits repositories; an application model handles requests at runtime. Choose a coding tool you can access and review its changes. The local exercises work without a live model or Azure. Use [provider equivalents](../lessons/09-model-providers.md) later to compare application integrations. Scripted responses do not demonstrate live model quality.

## Workshops and completion evidence

| Workshop topic | Read and do | Produce and explain |
|---|---|---|
| scope and data readiness | [Scope and linked data](../lessons/05-scope-and-linked-data.md), [templates](project-templates.md) | Four-line scope, unresolved questions with owners, table joins and readiness findings |
| unfamiliar code, specs and tests | [Python](../lessons/02-python.md), [pytest](../lessons/03-pytest.md) | Baseline command, small reviewed diff, independent acceptance test and failure classification |
| PRD, eval data and costs | [Evaluation](../lessons/08-evaluation.md), [operational costs](../lessons/12-reliability-and-transfer.md) | Requirement-to-test map, independent labels, precision/error interpretation, per-call cost calculation |
| context and retrieval | [Configuration/replay](../lessons/04-files-configuration-and-replay.md), [context/search](../lessons/06-context-and-search.md) | Current state versus history, scoped policy retrieval, minimised fields, before/after evidence |
| MCP and tool misuse | [MCP/integration tests](../lessons/07-mcp-and-integration-tests.md) | Tool list/schema, client/server exchange, spy assertions, bounded failure path and duplicate prevention |
| autonomy and interface | [Oversight](../lessons/11-oversight-permissions-and-red-teaming.md), workbook | Per-step human oversight, honest status display, safe rendering and unknown-ID behavior |
| evaluation and attacks | Evaluation and oversight lessons | Answer/tool/trajectory/state/recovery checks, comparable baseline, all attack attempts recorded |
| gates and ownership | Oversight, templates | Permission table, model/software/human ownership, PASS/FAIL/UNVERIFIED control evidence |
| deployment, cost and monitoring | [Azure](../lessons/10-azure.md), reliability lesson | Justified hosting choice, peak/average demand, limits, monitoring owner and action |
| handoff and explanation | [Templates](project-templates.md), [Mentor playbook](mentor-playbook.md) | Reproducible evidence, runbook, claim-to-evidence links and clearly stated limitations |
| document intelligence | [Document pipelines](../lessons/13-document-pipelines-and-privacy.md) | Document inventory, repeating fields, extraction origin, confidence validation and per-boundary privacy decisions |

## Before each experiment: make the baseline explicit

1. Identify the selected project and its starting files. Read the commands before running them.
2. Record OS, Python/package versions, working directory, branch, commit and recording/build variant. Record the versions actually installed; compatibility ranges are not a complete lockfile.
3. Check coding-tool login separately from application API credentials. Do not copy a coding-tool key into the application's `.env` or MCP tool arguments.
4. Run the named baseline command. Record passed, failed, skipped and deselected counts plus reasons. Some failures and unfinished tests are intentional. A different folder's count is not your baseline.
5. Check the smallest MCP read exchange and, only when needed, the approved Azure endpoint/index access. Separate local, replay and live evidence.
6. Define a small change and its expected result. For a configuration-only experiment, preserve code, prompts, recordings and tests so you can explain the cause of a difference.
7. Save a clean starting branch and use a separate rehearsal branch. Rehearse a failure and an escalation route, not just the happy path.

## Mentor responsibilities

**Own:** explain instructions, help reproduce a failure, offer staged hints and collect sanitized evidence. **Share:** scope interpretation and ambiguous evaluation criteria with a study partner or project owner. **Hand off:** credential changes, missing platform permissions, production/client access, policy exceptions or unresolved ownership decisions to the authorized owner.

Use **Signal / Evidence / Ask**: “Signal: Search query denied. Evidence: sanitized 403, command, time and request ID; local query works. Ask: platform owner to verify data access for this identity.” Never turn an unknown policy fact into a plausible model-generated answer.

For self-study, record a two-minute explanation of a failure and its evidence. Ask a partner to reproduce your result using only the instructions, or retry it yourself from a clean branch. Label constructed responses and invented token counts honestly.

## What to learn next

Use [the foundations checklist](foundations-checklist.md) to find missing prerequisites and [the data coverage guide](data-coverage-and-next-steps.md) to distinguish supplied examples from extension work. For independent study, write a question, prediction, command, observation, explanation and next uncertainty after each workshop.
