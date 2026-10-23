# 06: Give the system the right context

**Outcome:** retrieve the right policy version, remove unnecessary fields and preserve unresolved work. Complete [linked data](05-scope-and-linked-data.md) first.

## 1. Context is what a model can see now

A model does not automatically know the database's latest contents. Its context is the information supplied for the current request. Chat history can contain an older value. Retrieve the current application and keep an explicit `as_of` date: the date against which the exercise checks validity.

Run `python -m examples.learning_lab context --case PRACTICE-APP-5002`. Inspect the document keys and policy ID. The command shapes context; it makes no model call.

## 2. Relevance needs scope as well as keywords

The dataset has company and personal policies, two invented jurisdictions, a superseded version and a future version. All may contain “review.” A jurisdiction is an area whose rules apply; XA and XB here are invented country codes.

The local `search_policy` requires a query plus `entity_type`, `jurisdiction` and `as_of`. Its date interval includes the start and excludes the end: `effective_from <= as_of < effective_to`. For COMPANY, XA and 2026-11-05, the result should be `POL-COMPANY-XA-v2`. This is a tiny keyword example, not vector search or a full version-resolution engine. Overlapping valid versions would need an explicit resolution rule.

Exercise: call the function from a Python scratch file with a different jurisdiction and date. Predict which record is eligible before checking. A relevant sentence from the wrong jurisdiction is still the wrong evidence.

## 3. Minimise document fields

`shape_documents` keeps only `party_id`, `doc_type`, `document_date` and `expiry_date`. It removes names and the fictional private note. An **allowlist** states what is permitted; extra fields are excluded by default. Do not pass a complete record merely because it is convenient.

This exercise does not anonymise the retained party IDs, and IDs can be personal data in real systems. Decide what each recipient needs, whether a reversible mapping is justified, and where it may be stored.

## 4. Compact without losing work

**Compaction** means shortening accumulated context. Preserve current facts, identifiers, decisions, reasons and open questions separately from long chat history. The `compact_state` example keeps `application_id`, `as_of`, `reasons` and `open_questions`. Its required keys intentionally raise an error if state is incomplete.

Write a test showing an unresolved question survives when chat history is removed. Then explain why a smaller token count is not success if a beneficial owner's possible match disappeared. Tokens are pieces of text processed by a model; fewer tokens help only when necessary information remains.

## 5. Optional live Azure AI Search

An **index** is a searchable collection. First use the local function; then use an existing approved Azure Search service and a practice index you own. No script below creates a service. Cloud access is optional.

```powershell
python -m pip install "azure-search-documents>=11.6,<13"
$env:AZURE_SEARCH_ENDPOINT = "https://YOUR-SERVICE.search.windows.net"
$env:AZURE_SEARCH_INDEX = "learning-policy-YOUR-ALIAS"
# Set AZURE_SEARCH_ADMIN_KEY using your approved secret method for indexing only.
python -m examples.learning_lab.azure_search upload
# Remove the admin key before the runtime query exercise.
Remove-Item Env:AZURE_SEARCH_ADMIN_KEY
# Set AZURE_SEARCH_QUERY_KEY using your approved secret method.
python -m examples.learning_lab.azure_search query
```

An upload creates a new index if its name does not already exist and sends only this guide's invented policies. It refuses an existing index instead of replacing another person's schema. Use a different name for a second upload. Delete only your own practice index through the approved portal workflow when finished. Search-service resources can still incur costs after an index is removed.

An admin key permits broad content changes. A query key permits reads and is not by itself per-user or per-document authorization; do not treat a configured index name as a security boundary. Where your environment uses Entra identities, use the course's approved role-based setup instead. The included optional script illustrates key authentication only. [Microsoft's key guidance](https://learn.microsoft.com/en-us/azure/search/search-security-api-keys)

The query filters entity type, jurisdiction and validity dates in Azure, independently of text relevance. Compare its IDs with the local expected ID. Missing credentials cause an explicit error: no silent switch to offline results. An unavailable live service is an unverified integration, even if local tests pass. See [SearchClient's reference](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python).

**Teach-back:** distinguish retrieval quality from answer quality. Show how a valid keyword result can still be out of scope. Explain what compaction must retain.

Next: [MCP and integration tests](07-mcp-and-integration-tests.md).
