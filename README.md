# AI Systems Learning Guide

Learn to understand, build, evaluate and explain an AI-assisted application. This standalone guide supports self-study, pairing and mentor-led learning. It combines conceptual lessons, synthetic datasets and a runnable Python practice project, with a focus on language-model systems. All customer records, documents and policy rules in `data/` are fictional.

Begin with [Start here](guides/start-here.md) for prerequisites, a suggested reading order and understanding checks. The invoice project demonstrates engineering mechanics; its validation is not an identity or onboarding decision.

## Start here

From this repository's root in PowerShell, use Python 3.10 or later:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m examples.ai_systems profile
.\.venv\Scripts\python.exe -m examples.ai_systems validate
.\.venv\Scripts\python.exe -m examples.ai_systems agent --provider mock --prompt "What is the risk tier for C-1002?"
.\.venv\Scripts\python.exe -m examples.ai_systems eval --provider mock
```

Core CLI commands and unittest checks require no third-party packages, API keys or cloud account. The pytest tutorial requires pytest. If `py` is unavailable, use your installed Python executable. After selecting a venv interpreter in your terminal/editor, the lessons abbreviate that executable as `python`. Run commands from the root so the `examples` package is importable.

For the beginner testing path:

```powershell
.\.venv\Scripts\python.exe -m pip install "pytest>=8,<10"
.\.venv\Scripts\python.exe -m pytest tutorials/pytest -v
```

Follow [pytest](lessons/03-pytest.md) for assertions, exceptions, parametrization, fixtures, temporary databases and fake model calls. A second practice package, `examples.learning_lab`, adds linked data, authored replay and real MCP. Both use fictional data and generic Learner/Mentor language.

`mock` is a scripted offline double. Its pass rate verifies sample wiring and fixtures, not language-model capability. Cloud integrations, optional SDK snippets, the UI and Azure extraction need the corresponding setup. No cloud calls, model downloads or Azure resources are created by the offline commands.

## Read in this order

Lessons now live in `lessons/`, numbered in learning order. Reusable references live in `guides/`. Commands still run from this repository's root. The former root-level numbered Markdown files have moved; maintained links have been updated.

| File | Use it for |
|---|---|
| [01: Foundations](lessons/01-ai-systems-foundations.md) | Model, application and system; follow one request |
| [02: Python](lessons/02-python.md) | Read and run functions, dictionaries, files and errors |
| [03: pytest](lessons/03-pytest.md) | Assertions, fixtures, temporary state and test doubles |
| [04: Files, configuration and replay](lessons/04-files-configuration-and-replay.md) | CSV, YAML, JSONL, fingerprints and honest evidence |
| [05: Scope and linked data](lessons/05-scope-and-linked-data.md) | Requirements, joins, statuses and human decisions |
| [06: Context and search](lessons/06-context-and-search.md) | Policy scope, validity, minimisation, compaction and optional Azure Search |
| [07: MCP and integration tests](lessons/07-mcp-and-integration-tests.md) | A real local server/client, spies, permissions and failure injection |
| [08: Evaluation](lessons/08-evaluation.md) | Baselines, precision/recall, holdouts and experiments |
| [09: Model providers](lessons/09-model-providers.md) | Anthropic, OpenAI, Gemini, Ollama and local-compatible examples |
| [10: Azure](lessons/10-azure.md) | Identity, extraction, model hosting and deployment |
| [11: Oversight and red teaming](lessons/11-oversight-permissions-and-red-teaming.md) | Human roles, default-deny permissions and attack evidence |
| [12: Reliability and transfer](lessons/12-reliability-and-transfer.md) | Recovery, worked costs, monitoring and another domain |
| [13: Document pipelines and privacy](lessons/13-document-pipelines-and-privacy.md) | OCR, repeating fields, confidence and data boundaries |
| [14: Project workbook](lessons/14-project-workbook.md) | Put the ideas together through practice sessions |

Use [Start here](guides/start-here.md), [the glossary](guides/glossary.md), [learning routes](guides/learning-path.md), [preparation plan](guides/preparation-plan.md), [course companion](guides/course-companion.md), [Mentor playbook](guides/mentor-playbook.md), [templates](guides/project-templates.md) and [reading list](guides/reading-list.md) as references. The [original data guide](data/README.md) and [linked-data guide](data/linked_review/README.md) describe the independent practice datasets.

## New course preparation exercises

```powershell
py -3 -m venv .venv-learning
.\.venv-learning\Scripts\python.exe -m pip install -r requirements-learning.txt
.\.venv-learning\Scripts\python.exe -m examples.learning_lab profile
.\.venv-learning\Scripts\python.exe -m examples.learning_lab eval --split practice
.\.venv-learning\Scripts\python.exe -m examples.learning_lab.mcp_client list
.\.venv-learning\Scripts\python.exe -m pytest tutorials/integration -v
```

These commands use local tools and constructed replay, not a live model. The MCP client launches a real local subprocess. Optional Azure Search is a separate, explicitly live exercise in lesson 06. Start with lessons 01–07 and the course companion for the first-week bridge; defer cloud setup until the relevant service is available.

## One shared project, several model backends

`examples/ai_systems/core.py` holds customer lookup, policy retrieval, extraction validation and SQLite review state. `providers.py` contains the native provider protocols and bounded agent loop. `__main__.py` supplies the CLI. Provider changes reuse the same tools, data and eval cases.

```powershell
# A read-only request; writes are disabled by default.
python -m examples.ai_systems agent --provider mock --prompt "Create a review for C-1001"

# Explicit application authorization for one customer, with an idempotency key.
python -m examples.ai_systems agent --provider mock --prompt "Create a review for C-1001" --allow-write --write-customer C-1001 --request-id demo-001
# Repeat that command: one review remains. Inspect the persisted queue.
python -m examples.ai_systems reviews

# Human decision, separate from model tools; use the actual ID from the queue.
python -m examples.ai_systems review --id 1 --decision approved --reviewer demo-reviewer
```

The SQLite store persists across restarts in `output/reviews.sqlite3`. Use a new request ID for a different operation. Reusing an ID with a different customer or reason returns a conflict. These local permissions illustrate an application boundary; the sample does not provide production authentication or multi-user access control.

## Optional interface and Azure

```powershell
python -m pip install streamlit
python -m streamlit run examples/ai_systems/ui.py
```

The interface displays extraction fixtures, calls the selected agent and shows the persistent review queue. Start with mock. It is a local single-user exercise and should not be exposed as a public service. The extraction panel displays saved fixtures; it does not silently call Azure or send a document to a model.

The three original sample invoices are in `data/documents/`. [Azure guide](lessons/10-azure.md) explains the separate live Azure extraction command. `requirements-optional.txt` lists optional packages; install only what the chosen lesson needs. Ranges are not a tested lockfile: record actual versions once the learning path environment is known.

## Verification and limits

See [the verification record](VERIFICATION.md) for checks actually executed and live-service limitations.

- Offline unit tests cover data labels, invalid inputs, permission boundaries, retry persistence, workflow transitions, loop budgets and protocol fixtures for all five live adapters.
- Starter agent evals check selected answer substrings, expected tool sequences and state changes. They are deliberately small and require human review when comparing real models.
- Provider protocol fixtures do not establish live SDK/server compatibility, account access, model support, latency or quality. Configure a model and run a live smoke test before a lesson.
- The comparison does not treat token counts or local hardware cost as directly interchangeable across providers. Record usage, time and actual published rates for the selected deployment.
- `output/`, temporary files, virtual environments, secrets and databases are ignored by Git.

To regenerate the authored datasets: `python scripts/generate_sample_data.py`. It overwrites the named fixture files, so save exercise changes first. To regenerate the PDF fixtures, install `reportlab` and run `python scripts/generate_sample_pdfs.py`.
