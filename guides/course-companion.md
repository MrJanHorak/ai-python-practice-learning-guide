# Course companion: prepare, practise and mentor

This maps the reviewed Days 1–12 material into this generic learning guide. It is a preparation aid, not an official marking scheme or a replacement for current lab instructions. Keep learner and Mentor terminology. The reviewed folder is a draft; validate provisioned resources and starter versions with the lead before teaching.

## Two projects, deliberately separate

The original `examples.ai_systems` project teaches provider protocols, invoices and a local review queue. The new `examples.learning_lab` project teaches linked records, scoped context, constructed replay and real MCP. Its IDs begin `PRACTICE-`; the supplied labs use different specimen IDs and manifests. Neither practice project is a complete implementation of the course system.

The course names Claude Code as the coding tool in the reviewed instructions. Coding tools edit repositories; an application model handles requests at runtime. Several labs use replay instead of live model inference. Keep [provider equivalents](../lessons/09-model-providers.md) for a later comparison, rather than changing course recordings to another provider during a constrained exercise.

## A day-by-day bridge

| Course day | Prepare with | Produce and explain |
|---|---|---|
| 1: scope and data readiness | [Scope and linked data](../lessons/05-scope-and-linked-data.md), [templates](project-templates.md) | Four-line scope, unresolved questions with owners, table joins and readiness findings |
| 2: unfamiliar code, specs and tests | [Python](../lessons/02-python.md), [pytest](../lessons/03-pytest.md) | Baseline command, small reviewed diff, independent acceptance test and failure classification |
| 3: PRD, eval data and costs | [Evaluation](../lessons/08-evaluation.md), [operational costs](../lessons/12-reliability-and-transfer.md) | Requirement-to-test map, independent labels, precision/error interpretation, per-call cost calculation |
| 4: context and retrieval | [Configuration/replay](../lessons/04-files-configuration-and-replay.md), [context/search](../lessons/06-context-and-search.md) | Current state versus history, scoped policy retrieval, minimised fields, before/after evidence |
| 5: MCP and tool misuse | [MCP/integration tests](../lessons/07-mcp-and-integration-tests.md) | Tool list/schema, client/server exchange, spy assertions, bounded failure path and duplicate prevention |
| 6: autonomy and interface | [Oversight](../lessons/11-oversight-permissions-and-red-teaming.md), workbook | Per-step human oversight, honest status display, safe rendering and unknown-ID behavior |
| 7: evaluation and attacks | Evaluation and oversight lessons | Answer/tool/trajectory/state/recovery checks, comparable baseline, all attack attempts recorded |
| 8: gates and ownership | Oversight, templates | Permission table, model/software/human ownership, PASS/FAIL/UNVERIFIED control evidence |
| 9: deployment, cost and monitoring | [Azure](../lessons/10-azure.md), reliability lesson | Justified hosting choice, peak/average demand, limits, monitoring owner and action |
| 10: handoff and explanation | [Templates](project-templates.md), [Mentor playbook](mentor-playbook.md) | Reproducible evidence, runbook, claim-to-evidence links and clearly stated limitations |
| 11–12: document intelligence | [Document pipelines](../lessons/13-document-pipelines-and-privacy.md) | Document inventory, repeating fields, extraction origin, confidence validation and per-boundary privacy decisions |

## Before each lab: make the baseline explicit

1. Identify the exact `lesson` or `lab` starter folder; they may differ. Read its current instructions.
2. Record OS, Python/package versions, working directory, branch, commit and recording/build variant. Use the repository's pinned dependencies, not this guide's optional ranges.
3. Check coding-tool login separately from application API credentials. Do not copy a coding-tool key into the application's `.env` or MCP tool arguments.
4. Run the named baseline command. Record passed, failed, skipped and deselected counts plus reasons. Some failures and unfinished tests are intentional. A different folder's count is not your baseline.
5. Check the smallest MCP read exchange and, only when needed, the approved Azure endpoint/index access. Separate local, replay and live evidence.
6. Confirm the day's allowed edit scope. Some exercises prohibit changes to prompts, recordings, code or tests and require a configuration-only repair.
7. Save a clean starting branch and use a separate rehearsal branch. Rehearse a failure and an escalation route, not just the happy path.

## Mentor responsibilities

**Own:** explain instructions, help reproduce a failure, offer staged hints and collect sanitized evidence. **Share:** scope interpretation and ambiguous evaluation criteria with the lead. **Hand off:** credential changes, missing platform permissions, production/client access, policy exceptions or unresolved ownership decisions to the authorized owner.

Use **Signal / Evidence / Ask**: “Signal: Search query denied. Evidence: sanitized 403, command, time and request ID; local query works. Ask: platform owner to verify data access for this identity.” Never turn an unknown policy fact into a plausible model-generated answer.

The reviewed Day 1 instructor notes explicitly skip one decision exercise while its lab brief still contains it. Confirm the current instruction with the lead. Some later replay material is marked constructed or awaiting live re-recording. Label those limitations; do not present authored token counts as measured live performance.

## Sources reviewed

The Drive files remain unchanged. These links support the mapping; check for updates before delivery:

- [Course index](https://drive.google.com/file/d/1cDIpZNe2IaafLI1OFu8Inpmyy8vHAAuy/view)
- [Day 1 instructor notes](https://drive.google.com/file/d/1Gg3mcvf7qIdnvlIJw0EqtlWmDmAE-3Ip/view)
- [Context repair](https://drive.google.com/file/d/19QjwhnZPnTmcnQ5EK-gEO4XnQR1xyF94/view) and [context strategy](https://drive.google.com/file/d/1mpdhaA1YyfxId4Sq-OAZvP6oVH_7mYXR/view)
- [MCP implementation](https://drive.google.com/file/d/1fqZq0tg1sMwHH6ZVRSzKOcRLOuEsJTui/view) and [tool-use tests](https://drive.google.com/file/d/1cLhMP3kQjjmq4798unYURoa9Ow2mfA6I/view)
- [Hard rules/statuses](https://drive.google.com/file/d/1UmpvRJDppxg4U35jclNBm3FtFjpcnafA/view), [evaluation lab](https://drive.google.com/file/d/1pdGnCUkLR1Anz7vaKyE-_s-w6Yqfly4u/view) and [cost/monitoring](https://drive.google.com/file/d/1J5Vek_m5O1d-e8wmt0zuwEnIYiguEdIG/view)
- [Document scope](https://drive.google.com/file/d/1v17IaM3nqLM-ozXL3-rL0F4HCcNC8xMN/view) and [end-to-end document lab](https://drive.google.com/file/d/13olNfsPyBWFj8IShwB_GXLTlJSnI-Q8Q/view)
