# 13: Documents, extraction and privacy boundaries

**Outcome:** design a document-to-review pipeline without confusing legible text, confident extraction and verified facts. Complete [Azure](10-azure.md) first for the optional live extractor.

## 1. Inspect before choosing an extractor

A native-text PDF contains selectable text. A scanned PDF or PNG contains an image; OCR converts visible marks into text. OCR can misread a date even when the page looks sharp. Native text can also be incomplete or have a poor reading order. “PDF” alone does not tell you whether OCR is needed.

The three existing [invoice PDFs](../data/documents/) are native-text starting points. These three PDFs do not cover scanned pages, several document types or repeating owner lists. The exercises below explain those extensions; create or obtain suitable synthetic inputs before evaluating them. No Azure results are fabricated for the supplied PDFs.

Create an inventory with document ID, type, native/scan, readable fields, missing pages, repeated groups, chosen extraction route and human-review reason. A repeated group is a list, such as several owners on one page. Do not flatten it into a single owner and silently lose the rest.

## 2. Define the output before calling a service

Write a contract for four fictional types: company registration, personal identity, ownership statement and address evidence. For each, specify required fields, field type, source page, missing-value representation, confidence and validation rules. This is a design exercise, not a claim that the included invoice extractor implements four models.

Use a list for owners: `owners: [{party_id: ..., ownership_percent: ...}, ...]`. A missing field is `null` with a reason, not a guessed value or a confidence of zero invented by the application. Check expiry using an explicit review date. Treat model-specific field names as an external format to normalise into your own contract.

## 3. Keep extraction origin visible

Record `native_text`, `simulated_ocr` or `azure:<model-id>` beside the result. Simulated OCR is authored practice text, not service evidence. A high extraction confidence says something about the extractor's field prediction; it does not establish that the source document is genuine or sufficient for a business decision.

Compare extracted fields with manually authored labels. Test unreadable dates, absent confidence, an expired identity document, a missing owner and a repeating list. If many documents require review, investigate document quality and field mapping before lowering a threshold. Choose thresholds with a stated error tradeoff and representative evidence.

## 4. Decide what crosses every connection

| Boundary | Ask | Possible decision |
|---|---|---|
| Upload to extractor | Is the complete page necessary and allowed? | Pass approved synthetic page; block unsupported real data |
| Extractor to application | Which fields does validation need? | Minimise to the contract |
| Application to model | Can identifiers replace names? | Redact unneeded details, preserving required relationships |
| Application to tools | Which arguments are essential? | Pass scoped IDs, not a full document |
| Application to logs | Is this useful operational evidence? | Log event IDs, counts and error codes; omit personal values |

**Pass** sends data unchanged; **minimise** retains only needed fields; **redact** removes or masks specific values; **block** prevents transfer. Redaction can fail and IDs can remain linkable. Describe residual risks and access/retention decisions rather than declaring all transformed data anonymous.

## 5. Test the full route

Run one clean case, one missing/low-confidence case and one owner-list case. Inspect every boundary and resulting review state. Add a synthetic canary such as `DO_NOT_LOG_PRIVATE_7` in a field that should never leave extraction; scan captured logs and model/tool requests for it. A clean log alone does not prove the model request excluded it. Keep a separate test showing necessary owner relationships survive minimisation.

For the interface, escape document text before inserting it into HTML, show pending human-review states plainly, handle unknown IDs without unnecessary model calls, and avoid application approve/reject controls. A functioning UI does not prove authorization or privacy boundaries work.

**Teach-back:** distinguish extraction from validation and a human decision. Explain why a privacy filter that discards an owner can create a correctness failure.

Next: [project workbook](14-project-workbook.md), applying these lessons to a complete small system.
