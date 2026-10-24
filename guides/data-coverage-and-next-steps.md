# Data coverage: what you can learn and what needs more evidence

**The supplied data is sufficient for introductory, inspectable exercises in most of this guide's engineering patterns. It is not sufficient to establish realistic model quality, OCR robustness, performance at scale or production readiness.** More rows help only if they add relevant variation and independently chosen expected behavior.

All supplied records, rules and confidence/usage fixtures are fictional. Some advanced topics are design exercises rather than completed runnable features. This page separates those cases so you can plan a standalone project honestly.

## What is included

| Material | Size | Useful for |
|---|---:|---|
| Clean and messy customer CSVs | 12 rows each | Profiling, duplicate/missing/stale values, lookup and basic contracts |
| Normalised extraction fixtures | 12 | Missing fields, invalid values, confidence boundaries and review reasons |
| Native-text invoice PDFs | 3 | Field inspection, a missing identifier and untrusted document notes |
| Original policy documents | 4, including an obsolete version | Basic retrieval, version selection and citations |
| Original agent cases | 12 | Scripted response handling, tool trajectories and state checks |
| Authored binary labels/scores | 20, with 2 positives | Precision, recall, class imbalance and thresholds |
| Linked-record set | 6 applications, 18 parties, 16 documents, 18 screening rows | Joins, screening every related party, missing evidence and status precedence |
| Linked policy records | 5 | Entity/jurisdiction filters and past/current/future validity |
| Linked replay scenarios | 6 with visible labels | Repeatable tool execution, recorded-evidence limits and coverage gaps |
| Per-call usage sample | 4 calls across 2 cases | Summing multi-call cost and including a chargeable retry |

See [the original data dictionary](../data/README.md) and [the linked-data dictionary](../data/linked_review/README.md). The replay runner and original model adapters are different examples; neither is a benchmark for the other's model quality.

## What is sufficient now?

| Learning objective | Current coverage | Important limit |
|---|---|---|
| Python, pytest, file formats and error handling | Enough for a first pass | Handling visible fixtures is narrower than general robustness |
| Scope, linked data and required-field rules | Enough for small exercises | Similar party structures; little real-world ambiguity |
| MCP, tool schemas, scoped writes and retries | Runnable local examples and integration tests | Transport/authorization coverage comes from code tests, not just data volume; no authenticated multi-user environment |
| Context minimisation and policy filters | Small, inspectable examples | No large corpus, embedding index or implemented general history-compaction strategy |
| Evaluation design and hard-rule checks | Enough to practise checks and failure analysis | Visible labels and fixed scripts cannot estimate live LLM accuracy or independent holdout performance |
| Cost arithmetic and monitoring design | Enough to understand units and requirements | Usage is invented; no representative demand, latency or incident history |
| Document extraction and privacy | Some field-level rules and three native PDFs | No supplied scanned-document pack, repeating ownership-document pack or measured live extractor outputs |
| Azure identity/search/extraction | Optional example code and setup walkthroughs | Local data cannot establish account permissions, live SDK compatibility or successful deployment |

## Add these inputs next, in this order

### 1. More varied, independent behavioral cases

Author cases for duplicate IDs, orphan references, invalid dates, stale screening, multiple directors/owners, conflicting records and unavailable tools. Include clean controls, combinations of problems and boundary dates. Put expected behavior and its justification in evaluator-only files; do not generate expected answers by asking the current implementation what it would do.

Reserve new cases for independent evaluation. The visible `holdout` row is a learning aid, not a secret test. Increasing the same generator from six to thousands of similarly structured applications would not establish diversity, realistic frequency or correctness of labels. The current profiler and runner would need extensions for some of these checks.

### 2. A synthetic document-quality pack

Create several layouts across registration, identity, ownership and address evidence. Include native text and image scans, skewed/blurred/cropped pages, unreadable or ambiguous dates, missing pages and repeating owner groups. Retain manually checked field/page labels and expected review reasons. A lossless image made from a clean PDF tests the OCR route, not realistic scan damage by itself.

Separate original document labels, simulated extraction and measured service output. Do not fabricate confidence values as though they came from a live extractor. Keep the existing PDFs unchanged as clean controls.

### 3. A richer retrieval and attack collection

Add documents with overlapping wording, related but incorrect jurisdictions, superseded and contradictory versions, unanswerable questions and synthetic instruction-injection attempts. Label expected source IDs before running retrieval. Use access labels for a future authenticated-user exercise; metadata alone does not enforce access.

The five policy records already teach filters. Embedding search, chunking, reranking and citation evaluation need both a richer corpus and additional implementation; extra text files alone do not provide those capabilities.

### 4. Measured operating evidence

After local checks pass, collect deliberately bounded live examples for the backend you choose. Record sanitized per-call usage, tool attempts, elapsed times and final state. Include retries, unavailable services, restart recovery and reviewer work. Make the collection mode and environment explicit.

Use measured volumes and a defined time window for a cost/performance estimate. Do not present the four-line usage fixture as demand history or the local environment-variable gate as production authentication. Concurrency, role enforcement, deployment and restore exercises require code and infrastructure work as well as data.

## What foundations need attention?

The concepts are present, but beginners benefit from slower explanations of processes/environments, typed values, HTTP/API errors, database transactions, asynchronous waiting, probabilities and independent evaluation. [The foundations checklist](foundations-checklist.md) now provides those explanations and small exercises.

Classical model training and advanced neural-network mathematics remain separate deeper tracks. This learning project concentrates on understanding, building and evaluating applications around models. Use [the learning workshops](learning-workshops.md) to apply the foundations and [project templates](project-templates.md) to record evidence and limitations.
