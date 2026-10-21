# Verification record

Date: 21 October 2026.

## Executed successfully

- Python source syntax checks for all project, generator and test files.
- Syntax checks for all 14 Python code blocks in the Markdown lessons.
- Local Markdown link checks: all relative file references resolved at the time of verification.
- `python -m unittest discover -s tests -v`: **21 passed**. Tests use scripted provider responses, not real model calls.
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
- Optional dependency installation/lockfile generation and cross-version SDK compatibility.

Official API documentation was consulted and linked in the lessons. Protocol fixture tests check the adapter's constructed requests and follow-up conversation state; they cannot establish account access, actual server compatibility, model availability, inference quality, cost or performance. Run one live smoke test for the selected environment before using it in a class.

Core verification used the bundled Python 3.12.14 runtime; the source targets Python 3.10+. Other Python versions were not executed in this session. Windows sandbox restrictions affected the system temporary folder during the first eval attempt; eval/test scratch directories now live under the ignored repository `output/` directory.
