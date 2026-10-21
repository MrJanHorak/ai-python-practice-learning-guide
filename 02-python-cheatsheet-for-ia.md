# Python Cheat Sheet for the MTA Builder Programme

Goal: read Python fluently, run it, test it, and diagnose failures. You do not need to be an expert writer. Since you already work in JavaScript/TypeScript, each section maps Python to the JS/TS idea you know.

Runnable code now lives in `examples/ia_prep/`. Start at [README](README.md), then use [the provider lab](06-model-provider-lab.md) for Anthropic, OpenAI, Gemini and local-model equivalents. No provider is assumed to be the programme's final choice.

---

## 1. Environments and running code

| JS/TS world | Python world |
|---|---|
| `node_modules` + `package.json` | virtual environment + `requirements.txt` / `pyproject.toml` |
| `npm install` | `pip install -r requirements.txt` or `uv sync` |
| `npx` / `npm run` | `python -m ...` / `uv run ...` |
| `.env` + `dotenv` | `.env` + `python-dotenv`, or `os.environ` |

```bash
# classic venv
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py

# modern, faster (uv)
uv venv
uv pip install -r requirements.txt
uv run python main.py
uv run pytest
```

Common setup failures: wrong Python version (`python --version`), venv not activated, package installed in a different interpreter (`which python`, `pip --version`), missing env var for an API key.

On Windows PowerShell, from the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m examples.ia_prep agent --provider mock
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
# Optional dependencies only; choose packages needed by your lesson:
.\.venv\Scripts\python.exe -m pip install pytest pydantic
Get-Command python
```

Use the actual installed Python launcher/version if `py` is unavailable. Directly invoking the venv interpreter avoids activation policy changes. Core CLI and unittest checks require Python 3.10+ and no third-party packages. A `.env` file is not loaded automatically by these scripts.

## 2. Reading Python quickly

```python
from dataclasses import dataclass

@dataclass
class Customer:
    name: str
    risk_score: float = 0.0
    docs: list[str] | None = None      # type hints: like TS types, NOT enforced at runtime

def score(customer: Customer, threshold: float = 0.7) -> str:
    if not 0 <= customer.risk_score <= 1 or not 0 <= threshold <= 1:
        raise ValueError("Scores and thresholds must be between 0 and 1")
    if customer.risk_score >= threshold:
        return "review"
    return "clear"

customers = [Customer("SIM A", 0.2), Customer("SIM B", 0.8)]
results = [score(c) for c in customers]            # list comprehension (like .map)
flagged = [c for c in customers if c.risk_score > 0.7]   # like .filter
by_name = {c.name: c for c in customers}           # dict comprehension
```

Key reading tips:
- Indentation is syntax (no braces).
- `None` = `null`. `is None` to check.
- Falsy values: `None`, `0`, `""`, `[]`, `{}`.
- `x if cond else y` is the ternary.
- `f"Hello {name}"` is a template literal.
- `*args`, `**kwargs` collect positional/keyword arguments.
- `self` is `this`, passed explicitly.
- `with open(path) as f:` handles cleanup (like try/finally).
- `async def` / `await` works like JS but needs `asyncio.run(...)` to start.
- Modules: `from pkg.module import name` ~ ES imports. `if __name__ == "__main__":` is the entry-point guard.

## 3. Reading a traceback

```
Traceback (most recent call last):
  File "app/main.py", line 42, in run
    result = extract(doc)
  File "app/extract.py", line 17, in extract
    return data["fields"]["name"]
KeyError: 'name'
```

Read **bottom-up**: the last line is the error type and message (`KeyError: 'name'` = that dict key is missing). The lines above show the call path; the frame nearest the bottom is usually where the bug surfaces, but the cause may be earlier (bad input).

| Error | Usually means |
|---|---|
| `KeyError` | Dict key missing (data shape differs from assumption) |
| `AttributeError: 'NoneType' ...` | Something returned `None` unexpectedly |
| `TypeError` | Wrong argument type or count |
| `ModuleNotFoundError` | Package not installed or wrong environment |
| `JSONDecodeError` | Model/tool returned non-JSON or empty text |
| `ValidationError` (pydantic) | Data didn't match the schema |
| `AssertionError` (pytest) | Expected value differs from actual |

## 4. pytest essentials

```python
# tests/test_scoring.py
import pytest
from examples.ia_prep.scoring import score, Customer

def test_high_risk_goes_to_review():
    assert score(Customer("A", 0.9)) == "review"

@pytest.mark.parametrize("risk,expected", [(0.1, "clear"), (0.7, "review"), (1.0, "review")])
def test_threshold(risk, expected):
    assert score(Customer("A", risk)) == expected

def test_bad_input_raises():
    with pytest.raises(ValueError):
        score(Customer("A", -1))
```

```bash
pytest                      # run all
pytest -x                   # stop at first failure
pytest -k threshold         # run tests matching a name
pytest tests/test_scoring.py::test_threshold -vv   # one test, verbose
pytest --lf                 # re-run last failures
pytest -s                   # show print output
```

Diagnosis routine for a failing test: (1) read the assertion diff, (2) run just that test, (3) check fixtures/inputs, (4) ask: is the code wrong, the test wrong, or the environment wrong?

The runnable equivalent is `examples/ia_prep/scoring.py`. The range check makes the negative-score test meaningful. Learn pytest fixtures for repeated setup, `tmp_path` for isolated state, and `monkeypatch` for replacing network/configuration dependencies. Keep live model tests separate from offline checks; see the unittest examples in `tests/test_lab.py` for the same principles without additional packages.

## 5. Data shapes: JSON, dicts and Pydantic

```python
import json
from pydantic import BaseModel, Field, ValidationError

class Extraction(BaseModel):
    full_name: str
    date_of_birth: str | None = None
    confidence: float = Field(ge=0, le=1)

raw = '{"full_name": "Ada Lovelace", "confidence": 0.93}'
try:
    item = Extraction.model_validate_json(raw)   # pydantic v2
except ValidationError as e:
    print(e)                                      # shows which field failed and why
```

Pydantic is how many Python agent projects define the **output contract** and tool input schemas, similar to Zod in TypeScript. Generate JSON Schema with `Extraction.model_json_schema()`.

## 6. Calling models: four equivalent approaches

Use [lesson 06](06-model-provider-lab.md) for side-by-side SDK snippets and native REST implementations for OpenAI, Anthropic, Gemini and local Ollama. Start without credentials:

```powershell
python -m examples.ia_prep chat --provider mock --prompt "Explain what this lab does"
```

The following Anthropic snippet remains a vendor-specific illustration. Configure an accessible model rather than assuming one name.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...    # never commit keys
```

```python
from anthropic import Anthropic

client = Anthropic(timeout=45.0, max_retries=0)  # reads ANTHROPIC_API_KEY
import os
MODEL = os.environ["ANTHROPIC_MODEL"]

msg = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    system="You are a careful KYC analyst assistant.",
    messages=[{"role": "user", "content": "List 3 red flags in customer onboarding."}],
)
print(msg.content[0].text)
print(msg.usage.input_tokens, msg.usage.output_tokens)   # for cost-to-serve math
```

## 7. A bounded tool-use loop (the heart of an agent)

The complete shared loop is `run_agent` in `examples/ia_prep/providers.py`. It bounds model steps and tool calls, validates tool arguments in application code and returns a trace. Each provider's conversation class encodes native tool requests/results.

```python
from examples.ia_prep.core import ROOT, TOOLS, ReviewStore, ToolContext
from examples.ia_prep.providers import MockConversation, run_agent

store = ReviewStore(ROOT / "output/cheatsheet.sqlite3")
try:
    context = ToolContext(store, request_id="cheatsheet-read", allow_write=False)
    result = run_agent(MockConversation("What is the risk tier for C-1002?"),
                       context, TOOLS, max_steps=6, max_calls=10)
    print(result)
finally:
    store.close()
```

For comparison, this small Anthropic-specific loop illustrates the underlying protocol. It is a read-only teaching sketch; the project version supplies complete dispatch and error handling.

```python
import json
from anthropic import Anthropic

client = Anthropic(timeout=45.0, max_retries=0)
import os
MODEL = os.environ["ANTHROPIC_MODEL"]

tools = [{
    "name": "lookup_customer",
    "description": "Fetch a customer record by ID. Read-only. Returns name and risk tier.",
    "input_schema": {
        "type": "object",
        "properties": {"customer_id": {"type": "string", "description": "e.g. C-1042"}},
        "required": ["customer_id"],
    },
}]

def lookup_customer(customer_id: str) -> dict:
    db = {"C-1042": {"name": "Ada Lovelace", "risk_tier": "medium"}}
    return db.get(customer_id, {"error": f"No customer {customer_id}. Check the ID format C-####."})

messages = [{"role": "user", "content": "What is the risk tier for C-1042?"}]

for step in range(6):
    resp = client.messages.create(model=MODEL, max_tokens=1000, tools=tools, messages=messages)
    messages.append({"role": "assistant", "content": resp.content})

    if resp.stop_reason != "tool_use":
        print("\n".join(b.text for b in resp.content if b.type == "text"))
        break

    results = []
    for block in resp.content:
        if block.type == "tool_use":
            if block.name != "lookup_customer":
                output = {"error": "unknown_tool"}
            elif (not isinstance(block.input, dict) or set(block.input) != {"customer_id"}
                  or not isinstance(block.input["customer_id"], str)):
                output = {"error": "invalid_arguments"}
            else:
                output = lookup_customer(**block.input)
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": json.dumps(output)})
    messages.append({"role": "user", "content": results})
else:
    print("Stopped at the six-step budget; inspect the trace before retrying.")
```

What to notice: the **tool description is a prompt**, but permission checks and execution belong to application code. The runnable project also applies per-request timeouts, limits total tool calls and prevents a model from granting itself write permission.

## 8. A tiny eval harness

```python
import json

cases = [
    {"id": "t1", "input": "Is C-1002 high risk?", "expect_tool": "lookup_customer", "expect_substr": "medium"},
    {"id": "t2", "input": "What's the weather?", "expect_tool": None, "expect_substr": None},
]

def run_agent(prompt):
    """Return (final_text, [tool_names_called]). Wrap your agent loop here."""
    from examples.ia_prep.core import TOOLS, ReviewStore, ToolContext
    from examples.ia_prep.providers import MockConversation, run_agent as execute
    store = ReviewStore(":memory:")
    try:
        result = execute(MockConversation(prompt), ToolContext(store, "tiny-eval"), TOOLS)
        return result["text"], [step["tool"] for step in result["trace"]]
    finally:
        store.close()

def grade(case, text, tools_called):
    failures = []
    if case["expect_tool"] and case["expect_tool"] not in tools_called:
        failures.append("wrong_tool")                       # failure taxonomy label
    if case["expect_tool"] is None and tools_called:
        failures.append("unneeded_tool_call")
    if case["expect_substr"] and case["expect_substr"] not in text.lower():
        failures.append("wrong_answer")
    return failures

report = []
for c in cases:
    text, tools_called = run_agent(c["input"])
    report.append({"id": c["id"], "failures": grade(c, text, tools_called)})

passed = sum(1 for r in report if not r["failures"])
print(f"{passed}/{len(report)} passed")
print(json.dumps(report, indent=2))
```

This one file demonstrates: eval set, trajectory check (tool selection), failure taxonomy labels, and a pass rate you can track across changes (regression).

The standalone Anthropic sketch uses illustrative customer C-1042; the runnable dataset and harness use C-1001 through C-1012. Run the complete starter evals with `python -m examples.ia_prep eval --provider mock`; replace the provider only after configuring it. A scripted pass verifies wiring, not model quality. The live checks use simple expected tool sequences and selected answer substrings; inspect false positives/negatives manually.

## 9. A minimal MCP server (Python)

```bash
pip install "mcp[cli]"
```

```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("kyc-demo")

@mcp.tool()
def lookup_customer(customer_id: str) -> dict:
    """Read-only. Fetch a customer record by ID (format C-####)."""
    return {"customer_id": customer_id, "risk_tier": "medium"}

if __name__ == "__main__":
    mcp.run()
```

Verify against the current MCP Python SDK docs, since the API evolves. Concepts to practice explaining: tool schema, read vs. write, auth/scoping, idempotency, error text.

## 10. Cost-to-serve calculator

```python
def monthly_cost(requests_per_day, in_tokens, out_tokens, in_price_per_mtok, out_price_per_mtok, days=30):
    per_request = (in_tokens * in_price_per_mtok + out_tokens * out_price_per_mtok) / 1_000_000
    return per_request * requests_per_day * days

# Example with made-up prices: always use current pricing for the model you use
print(monthly_cost(2000, 6000, 800, in_price_per_mtok=3.0, out_price_per_mtok=15.0))
```

This simplified calculator uses aggregate per-request token counts. Agent runs can include multiple model calls, repeated context and retries. Record actual usage per call. Cached input, reasoning usage and tool charges differ by provider/model; avoid counting reasoning twice if already included in output totals. Add document-processing, retrieval, hosting and monitoring costs separately.

## 11. Git worktree quick reference

```bash
git worktree add ../mta-feature-a -b feature-a   # new dir + new branch
git worktree list
cd ../mta-feature-a                              # run a second agent session here
git worktree remove ../mta-feature-a             # when done
```

## 12. Python debugging toolkit

```python
print(repr(value))            # see exact value, including whitespace
import pdb; pdb.set_trace()   # or: breakpoint()
import logging; logging.basicConfig(level=logging.DEBUG)
```

```bash
python -m pdb script.py
pytest --pdb                  # drop into debugger on failure
```

## 13. Practice drills (30 min each)

1. Clone any small public Python repo, create a venv, run its tests, break one on purpose, then fix it.
2. Write a Pydantic model for an ID document (name, DOB, expiry, confidence) and validate good and bad JSON.
3. Run the shared agent with a read and a scoped write; repeat the same request ID and verify one stored record.
4. Run the supplied 12-case eval suite, then add a new case with an independently chosen expected outcome.
5. Create two git worktrees and run two experiments side by side.

## 14. HTTP, service operations and asynchronous code

Trace one request through URL, method, authentication, JSON body, HTTP status and response schema. A 401, 403, 429 or timeout suggests different first checks; see [the troubleshooting playbook](09-ia-troubleshooting-and-assessment.md). Do not blindly retry non-idempotent writes. The sample model transport uses a 45-second per-request timeout and no automatic retries.

An SDK poller waits for a long-running server operation. Python `async def` controls concurrency in the client. Understand both before trying to fix latency by adding `async`. Add bounded backoff only after reproducing the error and deciding whether a retry is appropriate.
