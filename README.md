# IA preparation: learn, build, diagnose, explain

This workspace combines the programme scope, revised study guides, synthetic datasets and a runnable Python practice project. All customer records, documents and policy rules in `data/` are fictional. The project demonstrates engineering mechanics; invoice validation does not establish identity or approve onboarding.

## Start here

From this repository's root in PowerShell, use Python 3.10 or later:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m examples.ia_prep profile
.\.venv\Scripts\python.exe -m examples.ia_prep validate
.\.venv\Scripts\python.exe -m examples.ia_prep agent --provider mock --prompt "What is the risk tier for C-1002?"
.\.venv\Scripts\python.exe -m examples.ia_prep eval --provider mock
```

Core commands and tests require no third-party packages, API keys or cloud account. If `py` is unavailable, use your installed Python executable. After selecting a venv interpreter in your terminal/editor, the lessons abbreviate that executable as `python`. Run commands from the root so the `examples` package is importable.

`mock` is a scripted offline double. Its pass rate verifies sample wiring and fixtures, not language-model capability. Cloud integrations, optional SDK snippets, the UI and Azure extraction need the corresponding setup. No cloud calls, model downloads or Azure resources are created by the offline commands.

## Lesson map

| File | Use it for |
|---|---|
| [01: Vocabulary](01-vocabulary-glossary.md) | Programme, Python/agent, cloud and provider terminology |
| [02: Python cheat sheet](02-python-cheatsheet-for-ia.md) | Reading code, tests, debugging and bounded tool loops |
| [03: Reading list](03-reading-list-and-tutorials.md) | Short pre-Day-1 route plus specific official references |
| [04: Preparation exercises](04-prep-plan-and-exercises.md) | Programme-aligned tasks and readiness checks |
| [05: Readiness review](05-ia-readiness-review-and-azure-practice.md) | Original gap analysis and programme mapping |
| [06: Provider lab](06-model-provider-lab.md) | Anthropic, OpenAI, Gemini, Ollama and local OpenAI-compatible examples |
| [07: Azure lab](07-azure-hands-on-lab.md) | Identity, Document Intelligence, deployment and diagnosis |
| [08: Project workbook](08-project-workbook.md) | Eight practice sessions with commands and evidence |
| [09: IA support](09-ia-troubleshooting-and-assessment.md) | Staged hints, escalation and assessment evidence |
| [10: Templates](10-project-templates.md) | Specs, PRD, data readiness, architecture, evals and handoff |
| [Data guide](data/README.md) | Schema, defects, expected results and reuse rules |

## One shared project, several model backends

`examples/ia_prep/core.py` holds customer lookup, policy retrieval, extraction validation and SQLite review state. `providers.py` contains the native provider protocols and bounded agent loop. `__main__.py` supplies the CLI. Provider changes reuse the same tools, data and eval cases.

```powershell
# A read-only request; writes are disabled by default.
python -m examples.ia_prep agent --provider mock --prompt "Create a review for C-1001"

# Explicit application authorization for one customer, with an idempotency key.
python -m examples.ia_prep agent --provider mock --prompt "Create a review for C-1001" --allow-write --write-customer C-1001 --request-id demo-001
# Repeat that command: one review remains. Inspect the persisted queue.
python -m examples.ia_prep reviews

# Human decision, separate from model tools; use the actual ID from the queue.
python -m examples.ia_prep review --id 1 --decision approved --reviewer demo-reviewer
```

The SQLite store persists across restarts in `output/reviews.sqlite3`. Use a new request ID for a different operation. Reusing an ID with a different customer or reason returns a conflict. These local permissions illustrate an application boundary; the sample does not provide production authentication or multi-user access control.

## Optional interface and Azure

```powershell
python -m pip install streamlit
python -m streamlit run examples/ia_prep/ui.py
```

The interface displays extraction fixtures, calls the selected agent and shows the persistent review queue. Start with mock. It is a local single-user exercise and should not be exposed as a public service. The extraction panel displays saved fixtures; it does not silently call Azure or send a document to a model.

The three original sample invoices are in `data/documents/`. [Lesson 07](07-azure-hands-on-lab.md) explains the separate live Azure extraction command. `requirements-optional.txt` lists optional packages; install only what the chosen lesson needs. Ranges are not a tested lockfile: record actual versions once the programme environment is known.

## Verification and limits

See [the verification record](VERIFICATION.md) for checks actually executed and live-service limitations.

- Offline unit tests cover data labels, invalid inputs, permission boundaries, retry persistence, workflow transitions, loop budgets and protocol fixtures for all five live adapters.
- Starter agent evals check selected answer substrings, expected tool sequences and state changes. They are deliberately small and require human review when comparing real models.
- Provider protocol fixtures do not establish live SDK/server compatibility, account access, model support, latency or quality. Configure a model and run a live smoke test before a lesson.
- The comparison does not treat token counts or local hardware cost as directly interchangeable across providers. Record usage, time and actual published rates for the selected deployment.
- `output/`, temporary files, virtual environments, secrets and databases are ignored by Git.

To regenerate the authored datasets: `python scripts/generate_sample_data.py`. It overwrites the named fixture files, so save exercise changes first. To regenerate the PDF fixtures, install `reportlab` and run `python scripts/generate_sample_pdfs.py`.
