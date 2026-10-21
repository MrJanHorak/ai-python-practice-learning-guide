# Verification record

Date: 21 October 2026.

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

Official API documentation was consulted and linked in the lessons. Protocol fixture tests check the adapter's constructed requests and follow-up conversation state; they cannot establish account access, actual server compatibility, model availability, inference quality, cost or performance. Run one live smoke test for the selected environment before using it in a class.

Core unittest verification used bundled Python 3.12.14; pytest verification used the existing project virtual environment's Python 3.13.14. The source targets Python 3.10+, but Python 3.10/3.11 were not executed here. Core eval/unittest scratch directories live under ignored `output/`. The pytest tutorial uses isolated `tmp_path` directories and blocks this module's real model transport.

The guide, commands, source imports and sample PDF metadata now use generic learner/mentor terminology and the `examples.ai_systems` package. The text/metadata audit excludes Git history, virtual environments, generated caches and temporary/output files. The added metrics lesson uses twenty authored scores; it does not train a classifier. External provider and cloud examples retain the live-service limitations listed above.

Latest content audit: 57 source/data files checked, 75 relative Markdown links resolved, 19 Python Markdown blocks parsed, all three PDF text/metadata checked, and the renamed package's scripted evals passed 12/12. No removed company/role labels or obsolete package/file references were found in the maintained material.
