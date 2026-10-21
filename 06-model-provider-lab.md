# Lesson 06: the same task with Anthropic, OpenAI, Gemini and a local LLM

Goal: run the same prompt, tools and evals across providers, then explain what changes in the protocol and what stays in application code. Examples were checked against official documentation on 21 October 2026; choose model IDs actually available to your account/server. No model choice is assumed to be the programme's requirement.

## 1. Two different uses of models

**Coding agent:** Claude Code, OpenAI Codex or Gemini CLI can help inspect and modify a repository. Use the same spec and acceptance tests from [lesson 10](10-project-templates.md); inspect the resulting diffs. Tool installation, authorization and billing depend on the product.

**Application model:** your running Python application calls a model API to answer a user or propose a tool call. An API SDK alone does not provide repository editing, a shell, MCP or deployment. This lesson implements that application side. A local chat model needs an additional coding-agent host if you want it to edit repos autonomously.

## 2. What is shared and what changes

| Backend | API used by runnable lab | Tool proposal | Tool result sent back | Main difference to notice |
|---|---|---|---|---|
| OpenAI | Responses | `function_call` with JSON-string arguments | `function_call_output` linked by `call_id` | Preserve response output items, including opaque reasoning context where returned |
| Anthropic | Messages | `tool_use` content block with input object | User message containing `tool_result` blocks | Preserve assistant content blocks and match tool-use IDs |
| Gemini | `generateContent` | Model part containing `functionCall` | User part containing `functionResponse` | Preserve original model parts, including any thought signatures and call IDs |
| Local Ollama | Native `/api/chat` | Message `tool_calls`, usually object arguments | Tool message with `tool_name` | Requires a running local server and downloaded model with tool support |
| Local compatible server | `/v1/chat/completions` | OpenAI-shaped `tool_calls` with JSON-string arguments | Tool message with `tool_call_id` | Compatibility is a subset; this is not the OpenAI Responses API |

The shared application validates names/arguments, authorizes one write scope, executes tools, stores state and limits steps. The model proposes calls; it does not execute Python or grant permission. The small schema uses required strings; advanced JSON Schema features vary by provider.

The Gemini adapter deliberately uses the documented `generateContent` API. Google's newer Interactions examples use a different conversation/result format; do not mix the two protocols. For native implementation details inspect `examples/ia_prep/providers.py`.

## 3. Configure a provider in PowerShell

Use only the block for the provider you are trying. Read-Host avoids typing the literal key into the command line, but stores it in the process environment. Do not paste keys into the chat, source files or test reports. `.env.example` is reference material; the CLI does not automatically load `.env`.

```powershell
# OpenAI direct API
$env:OPENAI_API_KEY = Read-Host "OpenAI API key" -MaskInput
$env:OPENAI_MODEL = Read-Host "Accessible OpenAI model ID with function tools"
python -m examples.ia_prep chat --provider openai --prompt "Explain a tool call in two sentences"
python -m examples.ia_prep agent --provider openai --prompt "What is the risk tier for C-1002?"
```

```powershell
# Anthropic direct API
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key" -MaskInput
$env:ANTHROPIC_MODEL = Read-Host "Accessible Claude model ID"
python -m examples.ia_prep chat --provider anthropic --prompt "Explain a tool call in two sentences"
python -m examples.ia_prep agent --provider anthropic --prompt "What is the risk tier for C-1002?"
```

```powershell
# Gemini Developer API (not a Vertex AI authentication example)
$env:GEMINI_API_KEY = Read-Host "Gemini API key" -MaskInput
$env:GEMINI_MODEL = Read-Host "Accessible Gemini model ID supporting generateContent tools"
python -m examples.ia_prep chat --provider gemini --prompt "Explain a tool call in two sentences"
python -m examples.ia_prep agent --provider gemini --prompt "What is the risk tier for C-1002?"
```

`-MaskInput` requires PowerShell 7. On Windows PowerShell 5.1, use your approved secret-management method or enter the environment value through your editor's secret configuration. Select a tool-capable model from the provider's current documentation/account, not a model name copied from an old course.

The runnable native REST examples use Python's standard library: no vendor SDK installation is required. They have a 45-second timeout per request, six model steps and ten tool calls by default, with no automatic HTTP retries. A timeout does not prove a server operation was cancelled.

## 4. Minimal SDK equivalents for plain text

These are independent snippets to run after installing the matching package. SDK client APIs and the lab's REST adapters are alternative ways to call the same provider; the snippets below do not implement the full tool loop.

### OpenAI: `python -m pip install openai`

```python
import os
from openai import OpenAI

with OpenAI(timeout=45.0, max_retries=0) as client:
    result = client.responses.create(
        model=os.environ["OPENAI_MODEL"],
        instructions="Explain concepts clearly for a learner.",
        input="Explain idempotency in two sentences.",
        store=False,
    )
    print(result.output_text)
```

### Anthropic: `python -m pip install anthropic`

```python
import os
from anthropic import Anthropic

with Anthropic(timeout=45.0, max_retries=0) as client:
    result = client.messages.create(
        model=os.environ["ANTHROPIC_MODEL"], max_tokens=500,
        system="Explain concepts clearly for a learner.",
        messages=[{"role": "user", "content": "Explain idempotency in two sentences."}],
    )
    print("\n".join(block.text for block in result.content if block.type == "text"))
```

### Gemini: `python -m pip install google-genai`

```python
import os
from google import genai
from google.genai import types

with genai.Client(api_key=os.environ["GEMINI_API_KEY"],
                  http_options=types.HttpOptions(timeout=45000)) as client:
    result = client.models.generate_content(
        model=os.environ["GEMINI_MODEL"],
        contents="Explain idempotency in two sentences.",
        config=types.GenerateContentConfig(
            system_instruction="Explain concepts clearly for a learner.", max_output_tokens=500),
    )
    print(result.text)
```

The Google client timeout is expressed in milliseconds. The examples preserve each SDK's natural response shape rather than assuming every result has `.text`.

## 5. Local LLM with Ollama

1. Install Ollama using its official instructions and start the local server.
2. Choose an explicitly local, tool-capable model that fits your RAM/VRAM, storage and license requirements. Model downloads can be large; none are performed by this repository.
3. Pull that exact model and verify its installed tag. For example, the official tool-calling documentation uses `qwen3`; choose the specific size/tag appropriate for your machine.

```powershell
$env:OLLAMA_MODEL = Read-Host "Local tool-capable model tag to download"
ollama pull $env:OLLAMA_MODEL
ollama list
$env:OLLAMA_HOST = "http://localhost:11434"
python -m examples.ia_prep chat --provider ollama --prompt "Explain idempotency in two sentences"
python -m examples.ia_prep agent --provider ollama --prompt "What is the risk tier for C-1002?"
```

The lab's local adapters permit only loopback URLs and reject `:cloud` tags. Still verify the model is downloaded and executes locally; a local UI/server can offer cloud-backed models too. Check the runtime's cloud/network configuration if offline operation is required. Logs, external tools and other services remain separate data paths.

Local differences to measure: cold-load time versus warm latency, model size/quantization, context capacity, tool reliability and memory use. A smaller local model may answer text questions but fail to emit valid tool calls. Do not replace a missing tool call by treating arbitrary generated Python as executable code.

## 6. Local server through an OpenAI-compatible endpoint

Ollama also exposes an OpenAI-shaped endpoint. Other local servers, such as LM Studio, can offer a similar interface; confirm their actual URL and tool support first.

```powershell
$env:LOCAL_OPENAI_BASE_URL = "http://localhost:11434/v1"
$env:LOCAL_OPENAI_MODEL = $env:OLLAMA_MODEL
python -m examples.ia_prep agent --provider local-openai --prompt "What is the risk tier for C-1002?"
```

Equivalent plain-text SDK call, using the `openai` package against the local server:

```python
import os
from openai import OpenAI

with OpenAI(base_url=os.environ["LOCAL_OPENAI_BASE_URL"], api_key="local-unused",
            timeout=90.0, max_retries=0) as client:
    result = client.chat.completions.create(
        model=os.environ["LOCAL_OPENAI_MODEL"],
        messages=[{"role": "user", "content": "Explain idempotency in two sentences."}],
    )
    print(result.choices[0].message.content)
```

The placeholder key is for an unauthenticated loopback server, never a real remote service. This uses Chat Completions; do not assume a local server also supports Responses, hosted tools, structured outputs or identical usage metadata.

## 7. Compare behavior with the same exercise

```powershell
python -m examples.ia_prep eval --provider mock
# After configuring ONE provider; live eval makes several billable model calls.
python -m examples.ia_prep eval --provider openai
# Repeat with anthropic, gemini, ollama or local-openai when configured.
```

Record provider, exact model/tag, SDK/runtime version, date, model settings, pass/failure categories, tool arguments, resulting state, latency and usage. Keep the prompts/data/tool definitions constant. Tokenizers and reasoning/cache accounting differ; convert usage to actual cost using the chosen provider's rates rather than comparing raw token totals as identical units.

The starter evaluator has exact trajectory and simple substring checks, so manually inspect alternative correct answers and refusals. Add tests for repeated writes, malformed arguments, exhausted budgets and injected document instructions. Tests of application permissions must still pass even if the model follows an injected instruction.

Do not put `data/answers/` or expected labels into model context. `mock` is scripted to exercise known paths and cannot be ranked alongside real models for quality.

## 8. Azure-hosted models are another deployment choice

Direct OpenAI, Azure OpenAI and other Foundry deployments can differ in endpoint, authentication, deployment name, model availability and API support. The `openai` CLI adapter above targets the direct OpenAI API. Use the Azure-specific SDK example and guidance in [lesson 07](07-azure-hands-on-lab.md) for an Azure OpenAI deployment; do not swap only the API key.

## Official references

- [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling) and [Responses reference](https://developers.openai.com/api/reference/python/resources/responses/methods/create).
- [Anthropic tool definitions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) and [tool-result handling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls).
- [Gemini generateContent reference](https://ai.google.dev/api/generate-content) and [Google Python SDK](https://googleapis.github.io/python-genai/). [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling) also documents the separate Interactions approach.
- [Ollama native tools](https://docs.ollama.com/capabilities/tool-calling) and [OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility).
- Coding agents: [Codex quickstart](https://developers.openai.com/codex/quickstart/), [Claude Code practices](https://code.claude.com/docs/en/best-practices), [Gemini CLI](https://geminicli.com/docs/get-started/).
