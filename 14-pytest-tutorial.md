# Lesson 14: pytest from a first assertion to testing an AI application

Learning outcome: write a useful deterministic test, read a failure, reuse safe setup and test model boundaries without calling a paid service. The runnable examples are in `tutorials/pytest/`; the existing `tests/` suite uses Python's built-in unittest framework and can also be run by pytest.

## 1. What is a test?

A test compares observed behavior with an independently chosen expectation. It is useful when it protects a real requirement or failure boundary. For this project, examples include rejecting an invalid score, blocking a write and avoiding duplicate state after a retry.

Use **Arrange, Act, Assert**: set up the input, perform the operation, then check its observable outcome. Write the expected behavior first. Avoid rewriting the expected answer merely to match a bug.

## 2. Install and run one test

From the repository root, using your selected Python 3.10+ environment:

```powershell
# If you have not created a virtual environment yet:
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "pytest>=8,<10"
.\.venv\Scripts\python.exe -m pytest tutorials/pytest/test_01_basics.py::test_high_score_requires_review -v
```

The remaining commands abbreviate the selected venv interpreter as `python`. Using `python -m pytest` helps keep the runner and interpreter aligned. If import discovery fails, check your working directory and interpreter before changing imports.

Pytest discovers files/functions with test naming conventions; our `pytest.ini` selects `tests/` and `tutorials/pytest/`. A name such as `test_high_score_requires_review` explains the behavior, not merely the function being exercised. See the official [getting-started guide](https://docs.pytest.org/en/stable/getting-started.html).

## 3. Your first assertion

The first runnable test is:

```python
from examples.ai_systems.scoring import Customer, score

def test_high_score_requires_review():
    customer = Customer("SIM Example", 0.9)
    outcome = score(customer)
    assert outcome == "review"
```

`assert` states an observable expectation. It is more useful here to check the decision than to duplicate the entire implementation inside the test. Also test the threshold boundary and invalid inputs: a single happy path is limited evidence.

Predict what would fail if the comparison in `score` changed from `>=` to `>`. The high-score test would still pass; a boundary test is needed to catch that regression.

## 4. Read a failure

Run a single test with `-v`, locate the failing assertion, compare actual and expected values, then inspect the smallest relevant code path. A failed assertion differs from an import/fixture error: the latter may prevent the behavior from being tested at all.

For a controlled exercise, copy a small test into your scratch branch and intentionally expect `clear` for a score of 0.9. Observe the failure explanation, then restore the correct expectation. Do not weaken the application or leave a deliberately failing test in the normal suite.

Useful commands:

```powershell
python -m pytest tutorials/pytest -q
python -m pytest tutorials/pytest/test_01_basics.py -v
python -m pytest tutorials/pytest -k threshold -v
python -m pytest tutorials/pytest -x --tb=short
python -m pytest --lf -v
python -m pytest --collect-only -q
```

`-k` filters names, `-x` stops at the first failure, `--lf` selects previously failing tests and `--collect-only` lists what would run. If there were no previous failures, `--lf` can run the normal selection; inspect the collected output. A green run with zero intended tests is not evidence that the intended behavior was checked.

## 5. Exceptions are part of the contract

```python
import pytest
from examples.ai_systems.scoring import Customer, score

def test_invalid_score_is_rejected():
    with pytest.raises(ValueError, match="between 0 and 1"):
        score(Customer("SIM Example", -0.1))
```

Put the operation expected to raise inside the context manager. If it does not raise, the test fails. Check meaningful exception type/message behavior; avoid a broad `except Exception` that makes the test succeed for an unrelated error.

Exercise: include a value above one and NaN. Explain why rejecting non-finite input matters for a numeric boundary.

## 6. Parametrization: several cases, one rule

```python
import pytest
from examples.ai_systems.scoring import Customer, score

@pytest.mark.parametrize("risk,expected", [(0.69, "clear"), (0.7, "review"), (1.0, "review")])
def test_threshold(risk, expected):
    assert score(Customer("SIM Example", risk)) == expected
```

Each row becomes a separate collected case. The supplied examples use readable IDs such as `boundary` so failures are easier to locate. Include meaningful boundaries and error cases; a long list of almost identical happy paths adds little confidence. See [parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html).

## 7. Fixtures: repeatable setup and cleanup

A fixture supplies setup to a test through a named parameter. The default function scope creates a new fixture for each test. `conftest.py` shares fixtures with tests in its directory/subdirectories without explicit imports.

```python
import pytest
from examples.ai_systems.core import ReviewStore

@pytest.fixture
def review_store(tmp_path):
    store = ReviewStore(tmp_path / "reviews.sqlite3")
    yield store
    store.close()
```

Setup occurs before `yield`; cleanup runs afterwards, including when a test assertion fails. Keep teardown reliable and avoid sharing mutable databases between unrelated cases. Broader fixture scopes can speed expensive setup but also create order-dependent tests if state leaks. See [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html).

`tmp_path` supplies an isolated temporary Path for each test. It prevents a retry test from overwriting your real local review queue. Never point a test at a production database or use your normal `output/reviews.sqlite3` as disposable test state. See [temporary paths](https://docs.pytest.org/en/stable/how-to/tmp_path.html).

## 8. Test retries and persistence

```python
def test_identical_retry_creates_one_review(review_store):
    first = review_store.create("C-1001", "Check source", "retry-001")
    second = review_store.create("C-1001", "Check source", "retry-001")
    assert first["id"] == second["id"]
    assert len(review_store.list()) == 1
```

This tests a requirement: retrying the same operation produces one stored review. A separate supplied test closes/reopens the database to check restart persistence. Another verifies that a denied write leaves the database empty. These are observable state checks, not just assertions about the final explanation text.

Exercise: add a different payload with the same request ID. Expect `idempotency_conflict` and one original record. Add a denied customer-scope case and confirm no new write occurs.

## 9. Monkeypatch and a fake model transport

`monkeypatch` temporarily replaces configuration or attributes and restores them after the test. Use `setenv`/`delenv` for configuration checks and `setattr` for controlled dependencies. Patch where the application looks up the dependency; patching a different module's original definition may not replace an already imported reference. See [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html).

The model conversation accepts a `transport` function. The tutorial passes an authored fake response into that boundary and inspects the parsed result and request. No SDK, server or valid API key is needed. This is **dependency injection**: the test supplies the dependency explicitly instead of invoking the network.

The tutorial's `conftest.py` also installs an autouse guard replacing the provider's `urlopen` reference. An accidental real model call fails immediately. It is a guard for this module's transport, not a system-wide network sandbox.

Run:

```powershell
python -m pytest tutorials/pytest/test_03_model_boundaries.py -v
```

Explain what these tests establish: local parsing, configuration handling, tool dispatch and state boundaries. They do not establish live model correctness, provider availability or current server behavior. Live inference needs separately configured, explicitly selected tests/evals.

## 10. Organize a useful suite

| Test layer | Keep deterministic? | Typical evidence |
|---|---|---|
| Core contracts | Yes | Input/output, boundaries, exceptions |
| Stored state | Yes, isolated database | Retry, conflict, restart, denied write |
| Provider protocol fixtures | Yes, fake responses | Message format and tool-result linkage |
| Live integration | Opt in, controlled access | Real endpoint/authentication/compatibility |
| Model/task eval | Record variation and model/data versions | Representative answers, actions and failures |

Markers label test categories; they do not automatically prevent a live call. This repository declares `integration` and `live` for extensions, but its included tests are offline. Design explicit configuration/selection before adding live tests. Avoid sleeps, uncontrolled timestamps, shared mutable data or arbitrary external services in a fast deterministic suite.

Pytest can run the existing unittest suite too:

```powershell
python -m pytest tests tutorials/pytest -q
# Standard-library path still works without installing pytest:
python -m unittest discover -s tests -v
```

Optional later topic: coverage can help locate unexecuted paths, but a coverage percentage does not prove that assertions are meaningful. Prioritize the boundaries and outcomes that matter.

## Practice and mentor prompts

1. Add one threshold boundary and one invalid input case; explain why each matters.
2. Add the retry-conflict and wrong-customer-scope tests described above.
3. Use a fresh extraction fixture to test a supplier mismatch.
4. Add a fake provider response containing a malformed tool argument; verify no write occurs.
5. Convert one unittest example into a standalone pytest function and compare the setup style.

Before reviewing a proposed fix, ask: Which requirement failed? What would make this test fail for the wrong reason? Does it inspect the state that matters? Would it accidentally use the network? Can a different valid implementation satisfy it?

You are ready to move on when you can explain a failure, add an independently justified case and demonstrate that a blocked operation leaves state unchanged. Continue with [evaluation](12-evaluation-and-experiments.md) to distinguish these tests from broader model-quality evidence.
