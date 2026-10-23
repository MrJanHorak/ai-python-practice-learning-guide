# 04: Files, configuration and replay

**Outcome:** read a configuration file, follow a request through a log, and explain what a replay proves. First complete [Python](02-python.md) and [pytest](03-pytest.md). Allow one or two practice sessions; stop to explain each result.

All commands run from the repository root, the folder containing `README.md`. A terminal is the window where you type commands. The `python` command below means your selected virtual environment's Python, not whichever installation happens to be first on your computer.

## 1. Install the optional learning packages

```powershell
py -3 -m venv .venv-learning
.\.venv-learning\Scripts\python.exe -m pip install -r requirements-learning.txt
```

Select this interpreter in your editor. In later commands, replace `python` with `.\.venv-learning\Scripts\python.exe` if the environment is not activated. A virtual environment is a project-specific package folder. These packages are for this guide; use the supplied requirements file when working in the actual course repository.

## 2. Three formats, three jobs

| Format | What it looks like | Use here |
|---|---|---|
| CSV | One table, with a header and rows | Applications, parties and documents |
| YAML | Indented keys, values and lists | Human-editable settings |
| JSON / JSONL | Objects in braces; JSONL has one complete object per line | Saved fixtures / event logs |

Create a scratch folder for your own outputs with `New-Item -ItemType Directory -Force output`. Read [the YAML example](../data/linked_review/context.yaml):

```yaml
context:
  include_current_state: true
  history_limit: 2
  required_scope: [entity_type, jurisdiction, as_of]
fault: "search_policy:unavailable"
```

Two spaces indent the settings under `context`. `true` is a Boolean, `2` is a number, and `required_scope` is a list. Quote dates and strings with punctuation when you mean text. Use spaces, not tabs. A syntactically valid value can still be wrong for the application: `history_limit: -2` needs application validation.

Read it in Python:

```python
from pathlib import Path
import yaml

settings = yaml.safe_load(Path("data/linked_review/context.yaml").read_text(encoding="utf-8"))
assert settings["context"]["include_current_state"] is True
assert settings["context"]["history_limit"] >= 0
```

`safe_load` reads standard YAML values without constructing arbitrary Python objects. It does not validate your application's expected fields. See [PyYAML's documentation](https://pyyaml.org/wiki/PyYAMLDocumentation).

Exercise: copy the file into `output/`, change the history limit, and predict the loaded type. Then remove one level of indentation and inspect the parsed object or error. This YAML is a reading exercise; the small runner's context variant is selected with `--context`, not loaded from this file.

## 3. Read a JSONL log

Run:

```powershell
python -m examples.learning_lab run --case PRACTICE-APP-5002
python -m examples.learning_lab eval --split practice | Set-Content -Encoding utf8 output/practice.jsonl
```

The first command prints one JSON object. The second writes five objects, one per line. `|` sends one command's output to another command. `Set-Content` writes a file and replaces existing contents. Inspect the file before running more commands.

```python
import json
from pathlib import Path

for line in Path("output/practice.jsonl").read_text(encoding="utf-8-sig").splitlines():
    event = json.loads(line)
    print(event["correlation_id"], event["result"]["status"], event["passed"])
```

`utf-8-sig` accepts the optional byte-order mark some PowerShell versions write. A correlation ID connects the events for one request. This runner uses repeatable demo IDs; a real application needs an ID unique to each run. Never use an applicant's name as a correlation ID.

## 4. Fake, replay and live are different evidence

| Mode | What happens | What a pass establishes |
|---|---|---|
| Fake model | Your code returns an authored answer | Your application handles that answer |
| This guide's authored replay | A fixed Python trajectory runs real local tools and attaches scripted text/usage | The specified tools, state and fixture checks work together |
| Course replay | The supplied harness uses its recorded responses and checks its expected signatures | The course's supported recorded path behaves as checked |
| Live model | A configured model generates a new response | Evidence for that model/configuration on those inputs |

The new runner is deliberately small: it does not ask a model which tool to use and is not interchangeable with the course's harness. Read the `origin` and `mode` fields. Token numbers are invented, not measured model usage.

Try `python -m examples.learning_lab run --context changed`. It returns `replay_missing` with `evaluated: false`. An unsupported case/context/fault combination is a coverage gap, not a successful evaluation. Supported variants are `current`, the six authored IDs, and the optional `search_unavailable` fault. The manifest also rejects changed fixture bytes. It does not attest to every dependency, prompt or environment setting.

## 5. Compare like with like

A hash is a short fingerprint calculated from bytes. Logs include dataset, suite and build fingerprints. Compare baseline and candidate results only after checking dataset and suite match. Record configuration/fault variants and actual dependency versions separately. A build hash changing is expected when code changes; a suite changing means you may be asking a different question.

**Teach-back:** explain why a recorded response cannot show that your model account works. Show one case ID, its tool events and its saved review count. Name one unsupported variation.

Next: [scope and linked data](05-scope-and-linked-data.md).
