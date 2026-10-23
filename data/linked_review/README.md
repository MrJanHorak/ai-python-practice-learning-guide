# Linked review practice data

Every record, name, rule, identifier, screening result and token count is invented for this guide. These are independent practice fixtures, not copies of the supplied course data and not regulatory requirements. Do not mix the two repositories' IDs or manifests.

| File | Rows | Meaning and links |
|---|---:|---|
| applications.csv | 6 | One request per `application_id`; scope and review date |
| parties.csv | 18 | Company, director and beneficial owner; joins on `application_id` |
| documents.csv | 16 | Joins on `party_id`; includes missing/expired evidence and a field to minimise |
| screening.csv | 18 | Fictional result, check date and list version per party |
| policies.json | 5 | Company/person, jurisdiction and validity-window distractors |
| expected_outcomes.json | 6 | Authored answer key; five practice cases and one holdout |
| recordings.json | 6 | Authored narrative/token counts, NOT captured model responses |
| manifest.json | — | Fixture byte hashes and CSV row counts |
| context.yaml | — | YAML reading exercise; not the runner's configuration input |
| usage_sample.jsonl | 4 | Authored per-call usage for two cases; separate cost-arithmetic exercise |

Run `python -m examples.learning_lab profile` from the repository root. Explain why 18 parties and 16 documents indicate missing evidence but not necessarily orphan rows. Investigate manually before viewing the answer key.

The practice cases cover clear checks, a possible owner match, missing document, unavailable screening and expired document. The holdout combines a possible match with missing evidence. This split teaches the process: the labels and regression tests are visible, so it is not a blind independent benchmark. After reading those answers or using a result to guide a fix, ask a partner to author fresh unseen cases before claiming independent validation.

Regenerate with `python scripts/generate_linked_data.py`. This overwrites the named generated CSV/JSON fixtures and updates their hashes, preserving this README and YAML exercise. Save your experimental changes elsewhere first. Regeneration creates a new fixture baseline; it does not validate the correctness of a change. The replay refuses mismatched fixture bytes until a deliberate new baseline is made.

For more advanced data profiling, copy tables into `output/` and add one duplicate ID, an orphan, an invalid date and a stale screening result. The current profiler checks a few counts and relationships, not every defect. Extend tests and quality checks independently; the runner does not implement a screening-age rule.

See [scope/data](../../lessons/05-scope-and-linked-data.md), [context](../../lessons/06-context-and-search.md) and [replay](../../lessons/04-files-configuration-and-replay.md).
