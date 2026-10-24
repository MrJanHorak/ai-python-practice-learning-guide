# Synthetic data guide

All records, documents and policy rules here were authored for learning. They contain no sourced customer information and do not define regulatory or company policy. Company names begin with SIM; email addresses use the reserved example.test domain. Treat any accidental resemblance to a real organisation as coincidence.

## Inventory

The original customer/invoice fixtures below remain available. The separate [linked-review dataset](linked_review/README.md) adds applications, parties, documents, policy versions, scripted replay and usage examples for the linked-record learning path. It uses its own identifiers and manifest.

For a skill-by-skill assessment of these datasets and their limits, see [data coverage and next steps](../guides/data-coverage-and-next-steps.md). Small fixtures support inspection and debugging; realistic evaluation needs independently chosen variation and representative evidence.

| File | Contents | Exercise |
|---|---|---|
| `customers_clean.csv` | 12 valid rows under this demo's narrow checks | Customer lookup and joins |
| `customers_messy.csv` | 12 rows with deliberately planted defects | Data profiling and readiness note |
| `extraction_fixtures.json` | 12 hand-authored normalized invoice extractions | Validation, confidence, recovery and injected text |
| `eval_cases.json` | 12 prompts plus evaluator-only expectations | Tool trajectory, answer and state checks |
| `classification_scores.csv` | 20 invented binary labels and scores, including two positive cases | Precision, recall, thresholds and misleading accuracy in Evaluation guide |
| `policies/index.json` and four policy Markdown files | Three active documents and one obsolete version | Retrieval, citations, versioning and insufficient evidence |
| `document_manifest.json` | Known values for the three synthetic source PDFs | Manual comparison of actual Azure extraction |
| `documents/invoice-clean.pdf` | Original native-text invoice with fields/table | First live extraction |
| `documents/invoice-missing-number.pdf` | Invoice with missing identifier | Missing-field diagnosis |
| `documents/invoice-injection.pdf` | Invoice containing explicitly adversarial notes | Untrusted document context and application boundaries |
| `answers/` | Authored profile/extraction labels and five retrieval questions | Evaluator/Mentor reference; keep outside model context |

## CSV dictionary

| Field | Meaning and demo contract |
|---|---|
| `customer_id` | Unique `C-####` identifier; valid lookup IDs are C-1001 through C-1012 |
| `legal_name` | Synthetic organisation name; required |
| `country_code` | Two uppercase letters; the profiler checks format, not membership in a full country-code registry |
| `onboarding_date` | ISO date, not later than the comparison date |
| `risk_tier` | Assigned fictional label: low, medium or high; not a model-generated risk determination |
| `email` | Synthetic address ending @example.test; the profiler performs only a narrow demo check |
| `last_refreshed` | ISO date; more than 90 days old is stale under the invented teaching rule |
| `source` | Generated-data provenance; required |

The default comparison date is **2026-10-21**, which keeps the initial labels reproducible. The CLI supports `--as-of YYYY-MM-DD` for profiling and extraction validation. Expected labels assume the default date.

## Normalized extraction contract

Each record has `document_id`, caller-assigned `customer_id`, `invoice_id`, `supplier_name`, ISO `invoice_date`, numeric nonnegative `total_amount`, `currency` and a field-level `confidence` mapping. Supported demo currencies are USD, GBP and EUR. Notes are untrusted free text and must never become tool permissions.

The validator routes missing/invalid fields, unknown customers, supplier mismatches, future dates and low/missing/invalid confidence to human review. Its 0.85 threshold is a teaching setting, not a calibrated acceptance policy. A validated record is not proof of identity, a compliance decision or onboarding approval.

These JSON fixtures are not Azure SDK response objects. Their confidence values were authored to create predictable exercises. The Azure example writes raw service results separately and maps them into this application contract. Compare live extraction with the actual source PDF and manifest.

At the default settings, D-001 and D-009 validate; the other ten require review. D-009 contains injection text in its notes. Deterministic field validation does not execute or interpret that text; a separate model-context experiment tests agent behavior. Application write checks must remain effective regardless of the model's response.

## State, evals and ground truth

The runtime tools read the clean customers and active policy files only. The evaluator reads expected labels separately. Reviews are written to `output/reviews.sqlite3`, not into the source CSV. A temporary database isolates each eval case; repeated CLI/UI requests persist in the normal database.

The mock uses scripted responses to demonstrate known paths. It is not an LLM and does not measure resistance to prompt injection. Live model evals are opt-in and can incur usage charges. Their simple grading rules are a starting point for human-reviewed evaluation.

## Regeneration

```powershell
python scripts/generate_sample_data.py
# Optional package needed only to recreate PDF sources:
python -m pip install reportlab
python scripts/generate_sample_pdfs.py
```

Generation replaces the named sample fixtures. Keep your own experiments elsewhere or save changes before regenerating. The initial PDFs contain native text; for an OCR experiment, render/scan a copy and compare it with the same field labels. Do not introduce real customer records or identity documents into the exercise.
