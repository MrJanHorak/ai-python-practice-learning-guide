# Verification record

Latest documentation verification: **24 October 2026**. Earlier results below are retained as historical checks.

## Standalone learning revision: executed 24 October

- Replaced the scheduled companion with self-study learning workshops and updated navigation. Removed private source links and audience/employer/schedule-specific wording from maintained material. Optional Mentor support remains available alongside independent study.
- Added a foundations checklist with processes/environments, value types, API/HTTP boundaries, SQL transactions, concurrency, probability/calibration and independent evaluation. Added a dataset coverage assessment that distinguishes supplied examples from extension work and unverified operating conditions.
- Executed all **3 new foundation Python examples** successfully. Verified linked dataset counts and confirmed its fixture byte hashes still match the manifest; data and expectations were not regenerated.
- Rechecked text and metadata of all **3 existing PDFs** for the removed organisation/audience labels; none found. The PDFs were not changed.
- `python scripts/check_learning_material.py`: **32 Markdown files, 183 local links, 24 Python blocks and 31 Python files; zero errors**. The wording audit excluded Git history, environments, caches and scratch/output folders. A public external tutorial URL retains its publisher's own path.
- `git diff --check` passed. Runtime behavior was not changed; two example docstrings were generalised. The previous 56-test integration run remains historical evidence from 23 October rather than a new full run for this documentation revision. No live model or Azure service was called.

## Linked-data and integration extension: executed 23 October

- Reorganised the fifteen root-level learning/reference Markdown files into numbered `lessons/` and unnumbered `guides/`; updated maintained local links. The root README remains the entry point.
- Added six beginner lessons, a workshop guide, expanded glossary, and extensions to evaluation, Azure, reliability, mentoring, templates and the workbook.
- Created the independent fictional linked-review fixtures: 6 applications, 18 parties, 16 documents, 18 screening rows and 5 policy versions. Recording text and token counts are authored, not captured live responses.
- Installed optional exercise dependencies into the separate ignored `.venv-learning` environment: Python **3.12.14**, pytest **9.1.1**, PyYAML **6.0.3**, MCP **1.30.0**, Pydantic **2.14.1**. Ranges in `requirements-learning.txt` are not a full dependency lockfile.
- `python -m pytest tests tutorials -q`: **56 passed, 18 subtests passed**. The MCP integration checks ran with real local stdio server processes and temporary SQLite databases. They verified listing/schema errors, not-found handling, denied writes, persistence across restart and repeated-write deduplication. The Windows sandbox blocked the subprocess exchange; the successful full run used an approved execution outside that sandbox.
- Replay tests verified actual local tool calls through a spy, all-party screening, policy scope/date, minimisation, must-keep questions, unsupported variants, fixture-byte mismatch rejection, bounded search failures and lost replies after committed writes.
- `python scripts/check_learning_material.py`: **30 Markdown files, 154 local links, 21 Python blocks and 31 Python files; zero errors**. This checks syntax and relative file existence, not external URL availability or semantic completeness.
- CLI checks: five practice replay cases matched authored status/pending/review-count expectations; per-call cost arithmetic reported total 0.008 at invented rates; original scripted provider evals remained **12/12**.
- `git diff --check` passed. The maintained lessons/guides were checked for the removed company and role labels and stale root filenames.

## Extension limitations

- No live model, local inference server, Azure Search, Azure Document Intelligence, Azure OpenAI or hosted deployment was invoked. The optional new Azure Search script was syntax-checked; its SDK integration and permissions remain unverified live.
- The small replay runner uses a fixed trajectory plus real local tools. It is not a model choosing actions, a general recorded-response replay engine, or a full implementation of every proposed workflow rule and minimum POC criterion.
- Visible answer keys and regression tests make the practice/holdout split educational, not a blind benchmark. Dataset/suite/build fingerprints cover selected inputs, not an attestation of the whole environment.
- The original interface was not started. Its renamed troubleshooting reference was updated; new document/interface material includes design exercises where runnable functionality is not provided.

## Historical verification: 21 October 2026

## Executed successfully

- Python source syntax checks for all project, generator and test files.
- Python code blocks in the Markdown lessons were syntax-checked.
- Local Markdown link checks: all relative file references resolved at the time of verification.
- `python -m unittest discover -s tests -v`: **24 passed** under bundled Python 3.12.14. Tests use scripted provider responses, not real model calls.
- Project virtual environment: installed pytest 9.1.1 and ran `python -m pytest tests tutorials/pytest -q` under Python 3.13.14: **41 passed**, plus **18 unittest subtests passed**. This includes 17 runnable pytest tutorial cases.
- Scripted agent starter evals: **12/12 passed**. This verifies sample wiring and authored cases, not LLM quality.
- CLI smoke checks: messy-data profiling, extraction validation, customer lookup, repeated scoped write, persisted review queue and saved human decision.
- Fixture checks: twelve messy rows matched the authored issue labels; twelve extraction cases matched the expected outcomes (two validated, ten review).
- Three generated PDFs were opened with pypdf and rendered for visual review. Each is one page; fields, tables and notes were legible. The missing-identifier version contains a blank identifier.
- `git diff --check`: passed for tracked changes.

## Not executed against a live service

- OpenAI, Anthropic and Gemini calls, including standalone SDK snippets.
- Ollama or another local model server; no model was downloaded.
- Live Azure Document Intelligence or Azure OpenAI calls, managed identity and deployment.
- Streamlit UI startup/browser interaction; its Python source was syntax-checked only.
- Other optional SDK/UI dependency installation, lockfile generation and cross-version SDK compatibility.

Official API documentation was consulted and linked in the lessons. Protocol fixture tests check the adapter's constructed requests and follow-up conversation state; they cannot establish account access, actual server compatibility, model availability, inference quality, cost or performance. Run one live smoke test for the selected environment before relying on a live-service example.

Core unittest verification used bundled Python 3.12.14; pytest verification used the existing project virtual environment's Python 3.13.14. The source targets Python 3.10+, but Python 3.10/3.11 were not executed here. Core eval/unittest scratch directories live under ignored `output/`. The pytest tutorial uses isolated `tmp_path` directories and blocks this module's real model transport.

The guide, commands, source imports and sample PDF metadata now use generic learner/mentor terminology and the `examples.ai_systems` package. The text/metadata audit excludes Git history, virtual environments, generated caches and temporary/output files. The added metrics lesson uses twenty authored scores; it does not train a classifier. External provider and cloud examples retain the live-service limitations listed above.

Latest content audit: 57 source/data files checked, 75 relative Markdown links resolved, 19 Python Markdown blocks parsed, all three PDF text/metadata checked, and the renamed package's scripted evals passed 12/12. No removed company/role labels or obsolete package/file references were found in the maintained material.
