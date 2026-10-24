# 07: MCP, real tools and integration tests

**Outcome:** connect a client to a tool server, inspect a tool contract and prove what was called. First complete [pytest](03-pytest.md) and [configuration/replay](04-files-configuration-and-replay.md).

## 1. Name the pieces

**MCP**, the Model Context Protocol, is a standard way for an application to connect to tools and other context. A **host** is the application using the connection. A **client** manages the connection. A **server** publishes tools. A **transport** carries their messages. This exercise uses **stdio**: the client starts a child process and exchanges messages through its standard input/output streams.

You do not need a model to test that connection. The manual client requests a tool directly. A model-assisted host adds another step: a model proposes a tool, then the host validates and dispatches it.

## 2. List the tools

Install `requirements-learning.txt` as explained in lesson 04, then run:

```powershell
python -m examples.learning_lab.mcp_client list
```

Find `get_application`, `screen_watchlist`, `search_policy` and `open_review_case`. Read their descriptions and `inputSchema` fields. A schema describes expected argument names and types. It does not prove the caller is allowed to perform the action.

The client uses its own Python interpreter to launch the server, avoiding an accidental different interpreter. If you start `python -m examples.learning_lab.mcp_server` alone, waiting silently is normal: it expects protocol messages. Use Ctrl+C to stop it. Do not add `print()` debugging to the server's stdout; it carries protocol messages. Use stderr/logging for sanitized diagnostics.

These examples deliberately use the Python SDK's 1.x API and an upper bound `<2`. SDK major versions can change APIs; this is an exercise compatibility choice. [Official 1.x documentation](https://py.sdk.modelcontextprotocol.io/v1/)

A coding-agent host also needs server configuration. The common shape is a server name plus executable and arguments; [this illustrative file](../data/linked_review/mcp-host.example.json) is not automatically activated. Replace its executable with your environment's absolute Python path, use your host's supported schema, and ensure its working directory is this repository root. Hosts differ in configuration filenames and how they set the working directory. Do not put model keys into a tool's description or arguments. The manual client avoids that host setup so you can learn the protocol first.

## 3. Call a read tool

PowerShell and native programs can disagree about quotes in inline JSON. Use a file:

```powershell
New-Item -ItemType Directory -Force output
'{"application_id":"PRACTICE-APP-5002"}' | Set-Content -Encoding utf8 output/mcp-arguments.json
python -m examples.learning_lab.mcp_client call --tool get_application --arguments-file output/mcp-arguments.json
```

Inspect both the protocol result and the tool result. MCP's `isError` describes protocol/tool execution errors; a returned object with `error: permission_denied` is this example's application-level error. A successful exchange is not necessarily a successful business operation.

Try an unknown ID and then omit a required argument. Explain the difference between `not_found` and schema validation. Do not save full live application records as debugging logs.

## 4. Call a write with explicit local permission

The default role is `reader`, so writes are denied. Create an arguments file containing an application ID, reason and request ID:

```powershell
'{"application_id":"PRACTICE-APP-5002","reason":"POSSIBLE_MATCH","request_id":"practice-5002-match-v1"}' | Set-Content -Encoding utf8 output/mcp-write.json
python -m examples.learning_lab.mcp_client call --tool open_review_case --arguments-file output/mcp-write.json
$env:LEARNING_REVIEW_ROLE = "analyst"
$env:LEARNING_REVIEW_APPLICATION = "PRACTICE-APP-5002"
python -m examples.learning_lab.mcp_client call --tool open_review_case --arguments-file output/mcp-write.json
```

Repeat the last command: it keeps one record in `output/mcp-learning.sqlite3`. A changed payload with the same request ID returns `idempotency_conflict`. A different application remains denied. Clean up the session's permission settings afterwards:

```powershell
Remove-Item Env:LEARNING_REVIEW_ROLE
Remove-Item Env:LEARNING_REVIEW_APPLICATION
```

This is a local permission demonstration, not authenticated multi-user security: anyone controlling the process can change its environment. A real host obtains roles and scope from verified identity. Never accept an `approved=true` or role argument from the model as proof of authorization. There is no application approval/rejection tool here.

## 5. Observe calls without replacing their work

A **spy** records a call and passes it to the real function. A **fake** replaces behavior. In `tutorials/integration/test_replay.py`, the spy copies the arguments, invokes the real function and keeps the result. The test asserts each party was screened, the company/jurisdiction arguments came from the application, and one review was persisted.

```powershell
python -m pytest tutorials/integration/test_replay.py -v
python -m pytest tutorials/integration/test_mcp.py -v
```

The second command launches a real local server process. It needs MCP installed, but no API key, model, HTTP server or Azure account. Tests use temporary databases. Required optional packages missing? Pytest reports skips; check the summary rather than treating them as passes.

## 6. Fail before work versus lose the reply after work

`unavailable` returns an error before a review is written. `timeout_after_write` commits the row and then raises `TimeoutError`, simulating a lost reply. A timeout alone cannot tell you whether work happened. Retry with the same request ID and identical payload; assert one row remains. A new ID would represent a new operation and can create a duplicate.

The replay's `search_unavailable` fault demonstrates a different rule: bounded read retries, no invented policy citation, and a human-review record still created. Run:

```powershell
python -m examples.learning_lab run --case PRACTICE-APP-5002 --fault search_unavailable
```

Inspect two search attempts, `POLICY_UNAVAILABLE`, and `review_count: 1`. This retry budget is an explicit example choice; other workflows need their own justified limit.

## 7. Read the test summary honestly

| Result | Meaning |
|---|---|
| passed | Executed assertions succeeded |
| failed | An assertion or tested behavior failed |
| error | Setup, collection or execution prevented the intended check |
| skipped | Check was not executed; inspect its reason |
| deselected | Your command/configuration excluded the check |
| xfailed / xpassed | An expected failure occurred / unexpectedly passed; inspect the marker policy |

Run `python -m pytest tutorials/integration --collect-only -q` and compare with `python -m pytest tutorials/integration -ra`. `-ra` explains non-passing outcomes. An unfamiliar project may skip tests when dependencies are absent or exclude checks through configuration. Record the exact folder, build/recording variant, command and selected test names. Do not copy a pass count from a different project or test selection. [Pytest skip/xfail guidance](https://docs.pytest.org/en/stable/how-to/skipping.html)

**Practice:** on a scratch branch, make search use the wrong jurisdiction. Watch a meaningful argument/result test fail, then fix the implementation without weakening the expectation. Explain what the MCP test proves that a direct-function test does not.

Next: [evaluation](08-evaluation.md).
