# Foundations checklist: build the missing mental models

This is a beginner companion, not an entrance exam. You can learn each idea when a practical exercise needs it. It explains the background that is easy to miss when a demonstration already runs. The main path is **applied AI application engineering**: using models within reliable software. Training a neural network from scratch is a separate extension.

Start with [the glossary](glossary.md) when a term is unfamiliar. For each topic, predict a result, run a small experiment and explain the observation without copying an AI tool's explanation.

## 1. Files, processes and environments

A **file** stores bytes on disk. A **process** is a running program with its own memory. A **path** identifies a file or directory. Relative paths start from the process's working directory; absolute paths include their starting location. This is why the guide's commands run from the repository root even though the lessons are in another folder.

A Python **interpreter** executes Python code. A virtual environment groups an interpreter with packages for one project. An import error can mean the wrong interpreter is running, not that the source code is wrong.

```powershell
python -c "import sys; from pathlib import Path; print(sys.executable); print(Path.cwd())"
python -m pip --version
```

Compare the interpreter and package paths. An environment variable is a setting inherited by a process; it is not a file and it does not automatically persist across every new terminal. A `.env` file only affects code that explicitly loads it. Continue with [Python](../lessons/02-python.md) and [configuration](../lessons/04-files-configuration-and-replay.md).

## 2. Values, types and validation

`"12"` is text; `12` is an integer. `None` means no value in Python; JSON represents it as `null`. An empty list means zero items, which differs from an unknown list. Decide whether missing, unreadable and explicitly empty values mean different things in your contract.

```python
import json

record = json.loads('{"amount": "12", "confidence": null, "owners": []}')
assert isinstance(record["amount"], str)
assert record["confidence"] is None
assert record["owners"] == []
```

Parsing proves that text has a recognised format. Validation checks your requirements: is amount numeric, is the date valid, is a required owner absent? Do not silently convert a missing confidence to zero or an absent amount to a real payment amount. See [pytest](../lessons/03-pytest.md) for independent expectations and boundary cases.

## 3. APIs, HTTP and failure boundaries

An **API** is a defined interface for requesting work. A Python function is one kind; a service API sends requests to another process or machine. **HTTP** is a common request/response protocol. **JSON** is a data format, not a transport. **MCP** is a tool/context protocol that can use transports such as local process streams; not every MCP exchange is an HTTP request.

An HTTP request has a method such as GET or POST, a destination, headers describing the request, and sometimes a body. A response has a status, headers and sometimes a body. Authentication credentials normally belong in the appropriate protected request mechanism, not a query string, log or model prompt.

| Observation | First question |
|---|---|
| Success status, wrong data | Did the application contract and source checks pass? |
| Authentication error, often 401 | Which credential or identity was presented? |
| Access denial, often 403 | Is that identity allowed this operation on this resource? |
| Not found, often 404 | Is the path, deployment or identifier correct? |
| Rate/capacity response, often 429 | Which limit was reached, and is retry appropriate? |
| Timeout | Did work finish even though the reply did not arrive? |

Status codes are clues, not complete diagnoses; read the service's error body and request ID. Retry only appropriate operations, bound the number of attempts and inspect saved state after uncertain writes. [MCP integration tests](../lessons/07-mcp-and-integration-tests.md) demonstrate the difference between failure before a write and a lost reply after it.

## 4. Tables, keys and database transactions

A **database** stores and queries structured data. SQL is one language for working with it. A primary key identifies a row; a foreign key references another row. A join combines related rows. Real databases enforce only the constraints that were actually configured.

```python
import sqlite3

with sqlite3.connect(":memory:") as database:
    database.execute("CREATE TABLE application (id TEXT PRIMARY KEY)")
    database.execute("CREATE TABLE party (id TEXT PRIMARY KEY, application_id TEXT)")
    database.execute("INSERT INTO application VALUES (?)", ("A-1",))
    database.execute("INSERT INTO party VALUES (?, ?)", ("P-1", "A-1"))
    related = database.execute(
        "SELECT p.id FROM party AS p JOIN application AS a ON a.id = p.application_id"
    ).fetchall()
    assert related == [("P-1",)]
database.close()
```

The `?` placeholders bind values rather than building SQL from input text. This tiny example intentionally has no enforced foreign-key constraint; add one and enable enforcement before relying on it to reject orphans. Close the connection when you finish; a connection's transaction context manager commits or rolls back work but does not itself close that connection.

A **transaction** makes a group of database changes succeed or roll back together. **Atomicity** means that group is not partly committed. **Idempotency** addresses a different question: does repeating the same intended operation duplicate its effect? A transaction alone does not make a retried request idempotent. The review examples use a stable request ID and a uniqueness constraint as part of that mechanism. See [linked data](../lessons/05-scope-and-linked-data.md).

## 5. Waiting, concurrency and durable work

**Synchronous** code waits for an operation before proceeding. **Asynchronous** code can yield while waiting so other tasks may progress. **Concurrency** means tasks overlap in progress; it does not always mean CPU work is running simultaneously. Adding `async` does not make a remote model generate faster or remove a service limit.

A queue tracks waiting work. In-memory state disappears when a process stops; durable state survives in an appropriate store. If two workers can act on the same case, both may try a write. Practice duplicate prevention, locking/transaction choices and restart recovery before introducing more workers. The supplied local examples do not establish multi-user or distributed-system correctness.

**Exercise:** run the retry/restart tests, then explain which state is in Python memory and which is stored in SQLite. Predict what would happen if two different request IDs were used for the same intended review.

## 6. Probability, scores and small samples

A probability describes uncertainty under stated assumptions. A score of 0.8 is not automatically an 80% chance of correctness. A model's confident wording, its next-token probabilities and an extractor's field score are different signals. **Calibration** asks whether predicted probabilities agree with observed frequencies across suitable labelled examples.

Suppose 10 of 100 cases need review. A system catches 8 and incorrectly flags 12 others: it creates 20 reviews, of which only 8 were necessary. Precision is 8/20 = 40%; recall is 8/10 = 80%. Which error matters more depends on consequences and review capacity. See [evaluation](../lessons/08-evaluation.md) for a runnable metrics example.

```python
true_positives, false_positives, false_negatives = 8, 12, 2
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
assert precision == 0.4
assert recall == 0.8
```

With tiny samples, one changed outcome can move a percentage substantially. Do not infer a dependable rare-failure rate from six easy cases. Report counts, error types, case selection and uncertainty. Latency/cost averages can also hide slow or expensive tails; use the operating exercise in [reliability](../lessons/12-reliability-and-transfer.md).

## 7. Evaluation design and evidence leakage

Choose expected outcomes from requirements and source evidence before inspecting the implementation's answer. Use development cases for improvements; reserve independently authored cases for a later check. If you use those later results to tune, they are no longer untouched evidence.

Repeated records, pages from the same document or paraphrases of the same question can leak information across a split. Keep related examples together. The supplied answer keys and tests are visible, so the split here teaches the workflow; it is not a blind benchmark. A larger set of generated near-duplicates does not solve that problem.

**Exercise:** ask a partner to write three new cases from the stated contract without seeing the runner's logic. Without a partner, create cases first, seal their expected outcomes in a separate file and record that the same person authored and evaluated them. Describe this limitation honestly.

## 8. Trust, privacy and identity

**Authentication** establishes identity. **Authorization** checks that identity's permission for an action and resource. Input validation checks structure/content; none replaces the others. Local environment flags illustrate a boundary but do not authenticate a user.

Treat retrieved text, document notes and model output as untrusted input. Software must enforce access and actions even when a model follows an injected instruction. Minimise data at each connection, keep credentials separate, and test both privacy and preservation of necessary facts. Hashing an identifier does not automatically make linked data anonymous. Continue with [oversight](../lessons/11-oversight-permissions-and-red-teaming.md) and [document privacy](../lessons/13-document-pipelines-and-privacy.md).

## 9. What belongs in a deeper learning track?

The guide introduces features (input properties), labels (expected targets), training, inference, embeddings and evaluation. It does not provide a full machine-learning training curriculum. If that is your goal, extend it with train/validation/test splits, preprocessing fitted only on training data, a simple learned baseline, optimisation, overfitting and model lifecycle experiments. Neural-network mathematics and fine-tuning come after those foundations.

For retrieval depth, add a larger labelled corpus, chunking, embedding search and independent retrieval metrics. For operating depth, add authenticated users, scoped access, concurrency, deployment and restore testing. These are meaningful extensions, not prerequisites for running your first local example.

## Check your understanding

- Can you locate your interpreter and working directory?
- Can you distinguish parsing, validation, authentication and authorization?
- Can you explain a transaction versus an idempotent retry?
- Can you identify what survives restart and what asynchronous code changes?
- Can you distinguish a score, a probability and measured correctness?
- Can you state what your dataset and chosen tests do not demonstrate?

If an answer is unclear, return to the linked lesson and run one small experiment. Use [the data coverage guide](data-coverage-and-next-steps.md) to choose useful next inputs.
