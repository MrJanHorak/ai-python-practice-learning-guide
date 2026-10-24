# Reading List and Tutorials

Links are grouped by learning path topic, with a suggested priority:
**[Must]** complete the short preparation route below, **[Should]** use for the relevant lab, **[Later]** reference or depth. Vendor-specific items apply only to your selected tool/provider.

> Core provider references checked 21 October 2026. Start with [Providers guide](../lessons/09-model-providers.md), which includes equivalent examples across providers. Use [Azure guide](../lessons/10-azure.md) for Azure access and deployment practice.

New to the concepts? Begin with [the start-here guide](start-here.md) and [foundations](../lessons/01-ai-systems-foundations.md). Use [the pytest tutorial](../lessons/03-pytest.md) for hands-on testing and [evaluation](../lessons/08-evaluation.md) for model-quality experiments.

## Short route before the first project

1. Read [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents); explain when deterministic code is enough.
2. Use the [Python tutorial](https://docs.python.org/3/tutorial/) alongside the local scoring example; run the offline tests.
3. Read [Git worktrees](https://git-scm.com/docs/git-worktree), then create an isolated experiment and inspect its diff.
4. Run the shared agent and evals from [README](../README.md). Inspect one tool trajectory and one denied write.
5. Complete local [configuration/replay](../lessons/04-files-configuration-and-replay.md), [context/search](../lessons/06-context-and-search.md) and [MCP/testing](../lessons/07-mcp-and-integration-tests.md) exercises. Use [the learning workshops](learning-workshops.md) to choose what is needed next. Live Document Intelligence is a later step once sandbox access is ready.

## References for the new practical lessons

- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation): loading standard YAML values; our lesson adds application validation.
- [MCP Python SDK 1.x](https://py.sdk.modelcontextprotocol.io/v1/): API line deliberately used by this practice server/client. Record and verify the dependency versions you choose.
- [Pytest skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html): interpret missing execution evidence.
- [Azure SearchClient](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python) and [key permissions](https://learn.microsoft.com/en-us/azure/search/search-security-api-keys): optional live query exercise, separate from extraction/model credentials.

Everything else is just-in-time reading for the upcoming lab. Reserve practice time rather than treating every vendor's documentation as required reading.

---

## 1. AI agents and architecture

- **[Must] Building Effective Agents** (Anthropic Engineering): workflows vs. agents, when to add complexity. https://www.anthropic.com/engineering/building-effective-agents
- **[Should] Writing effective tools for agents** (Anthropic Engineering): https://www.anthropic.com/engineering/writing-tools-for-agents ; use it to improve one tool description and rerun evals.
- **[Later] Native tool protocols and equivalent examples:** [Providers guide](../lessons/09-model-providers.md), with direct official references for each provider.

## 2. AI-assisted coding

- **[Should, Claude Code] Best practices:** https://code.claude.com/docs/en/best-practices
- **[Should, OpenAI Codex] Quickstart:** https://developers.openai.com/codex/quickstart/
- **[Should, Gemini CLI] Getting started:** https://geminicli.com/docs/get-started/
- **Practice across tools:** use the same executable spec, change scope and tests in [Templates guide](project-templates.md). Compare diffs, not just explanations. Coding-agent access/billing is separate from the application's API integration.
- **[Should] Git worktree docs:** https://git-scm.com/docs/git-worktree
- **[Should] Pro Git book (free):** branching, merging, rebasing chapters. https://git-scm.com/book
- **[Later] GitHub Docs, resolving merge conflicts:** https://docs.github.com

## 3. Specs, PRDs and prompts

- **[Must] Local executable-spec and PRD templates:** [Templates guide](project-templates.md). Supply inputs, outputs, constraints, failure cases and tests to any coding agent.
- **[Should] OpenAI prompt engineering:** https://developers.openai.com/api/docs/guides/prompt-engineering
- **[Should] Gemini prompting strategies:** https://ai.google.dev/gemini-api/docs/prompting-strategies
- **[Should] Claude prompting:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview

## 4. Evals

- **[Must] Your AI product needs evals** (Hamel Husain): error analysis, failure categories, practical workflow. https://hamel.dev/blog/posts/evals/
- **[Should] Eugene Yan on LLM evaluation:** patterns and pitfalls. https://eugeneyan.com
- **[Should] Apply the local eval template:** [Templates guide](project-templates.md), then run and inspect the shared provider evals.
- **[Later] OpenAI evaluation best practices:** https://developers.openai.com/api/docs/guides/evaluation-best-practices ; compare automated scores with your own labels before trusting a judge.

## 5. Context engineering

- **[Should] Effective context engineering for AI agents** (Anthropic Engineering): compare the recommendations with an actual request trace. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **[Should] Compare actual per-call usage metadata:** [Providers guide](../lessons/09-model-providers.md). Follow the selected provider's current context/cache limits and pricing rules.
- **[Should] Local retrieval exercise:** [Workbook guide](../lessons/14-project-workbook.md), including obsolete-policy exclusion and unsupported-answer checks. Compare retrieval and answer failures separately.

## 6. Tools and MCP

- **[Must] Model Context Protocol, introduction and concepts:** https://modelcontextprotocol.io
- **[Must] MCP Python SDK on GitHub:** README and examples. https://github.com/modelcontextprotocol/python-sdk
- **[Should] Provider tool references and runnable examples:** [Providers guide](../lessons/09-model-providers.md).
- **[Later] Stripe idempotent requests:** https://docs.stripe.com/api/idempotent_requests ; compare with the local SQLite retry exercise.

## 7. Python

- **[Must] Official Python tutorial** (read quickly, focus on sections 3-9): https://docs.python.org/3/tutorial/
- **[Must] Local pytest tutorial:** [pytest guide](../lessons/03-pytest.md), with runnable examples. Pair it with [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html).
- **[Should] pytest references:** [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html), [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) and [temporary paths](https://docs.pytest.org/en/stable/how-to/tmp_path.html).
- **[Should] uv docs:** https://docs.astral.sh/uv/
- **[Should] Pydantic docs, Models and Validators:** https://docs.pydantic.dev
- **[Should] Real Python, tracebacks, virtual environments, type hints:** https://realpython.com
- **[Should] Anthropic Python SDK:** https://github.com/anthropics/anthropic-sdk-python
- **[Later] Python `asyncio` docs:** https://docs.python.org/3/library/asyncio.html

## 8. Azure (extension sessions Block 1 and deployment)

- **[Must] Azure AI Document Intelligence overview** (Microsoft Learn): models, OCR vs. layout, confidence. https://learn.microsoft.com/azure/ai-services/document-intelligence/
- **[Must] Document Intelligence Studio:** upload a sample PDF and inspect output and confidence. https://documentintelligence.ai.azure.com
- **[Should] Azure Container Apps overview:** https://learn.microsoft.com/azure/container-apps/overview
- **[Should] Azure Key Vault overview:** https://learn.microsoft.com/azure/key-vault/general/overview
- **[Should] Microsoft Foundry documentation:** https://learn.microsoft.com/en-us/azure/foundry/ ; confirm the actual resource, model deployment and SDK with a study partner or project owner.
- **[Should] Python authentication:** https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview ; explain how local and deployed identities differ.
- **[Should] Microsoft agent labs:** https://microsoftlearning.github.io/mslearn-ai-agents/ ; select the basic agent, function and MCP exercises if this matches the learning path stack.
- **[Later] Azure pricing calculator:** https://azure.microsoft.com/pricing/calculator
- **[Later] Current study maps:** [AI-901](https://learn.microsoft.com/en-us/credentials/certifications/exams/ai-901/) and [AI-103](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/AI-103). Use selected topics rather than making certification a prerequisite.

## 9. Risk, responsible AI and governance

- **[Should] Anthropic Responsible Scaling and usage policies** (for general framing): https://www.anthropic.com
- **[Must] Write a small project risk checklist and review criteria.** State permitted data, forbidden actions, required human decisions and evidence needed. If you work within an organisation, include its applicable requirements; for self-study, use the fictional project contract and identify its limits.
- **[Should] Microsoft responsible AI resources:** https://www.microsoft.com/en-us/ai/responsible-ai
- **[Later] NIST AI Risk Management Framework:** https://www.nist.gov/itl/ai-risk-management-framework

## 10. Optional AML/KYC domain background

- **[Optional] FATF, "What is money laundering" and risk-based approach pages:** https://www.fatf-gafi.org
- **[Should] FinCEN, CDD rule and SAR overview (US):** https://www.fincen.gov
- **[Should] Map your chosen review workflow:** identify the owner, required evidence and escalation at each step. The local fictional invoice project does not establish regulatory requirements.
- **[Later] Wolfsberg Group guidance:** https://www.wolfsberg-group.org

## 11. Presentation and handoff

- **[Should] Architecture, handoff and runbook templates:** [Templates guide](project-templates.md). Defend one architecture choice using measured results.

---

## Additional topic blocks (optional, about 10 hours total)

| Block | Items | Time |
|---|---|---|
| 1 | Building Effective Agents; Context engineering article | 1 hr |
| 2 | Your chosen coding agent's practices; Git worktree docs | 1 hr |
| 3 | Hamel Husain evals article; Anthropic test-case docs | 1.5 hrs |
| 4 | MCP intro; build the tiny MCP server from the cheat sheet | 2 hrs |
| 5 | Python tutorial skim; pytest get-started; Pydantic basics | 2 hrs |
| 6 | Document Intelligence overview plus Studio experiment | 1.5 hrs |
| 7 | FATF/FinCEN basics | 1 hr |

## Newsletters and communities worth following

- Anthropic Engineering blog: https://www.anthropic.com/engineering
- Latent Space (AI engineering podcast/newsletter): https://www.latent.space
- Simon Willison's blog (practical LLM tooling): https://simonwillison.net

## Local model reference

- [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling): run the same customer lookup with a downloaded tool-capable model.
- [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility): compare native `/api/chat` with `/v1/chat/completions`; test feature support instead of assuming full compatibility.
