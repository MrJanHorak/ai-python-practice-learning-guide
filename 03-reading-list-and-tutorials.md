# Reading List and Tutorials

Links are grouped by programme topic, with a suggested priority:
**[Must]** read before Day 1, **[Should]** read in the first week, **[Later]** reference or depth.

> Verify links before relying on them. Sites reorganize, and Azure product names change often. If a link is dead, search the title.

---

## 1. AI agents and architecture (Autonomy Ladder, Day 6)

- **[Must] Building Effective Agents** (Anthropic Engineering): workflows vs. agents, when to add complexity. https://www.anthropic.com/engineering/building-effective-agents
- **[Should] Writing effective tools for agents** (Anthropic Engineering): tool design, descriptions, error messages. Search the title on https://www.anthropic.com/engineering
- **[Later] Anthropic docs, agents and tool use sections:** https://docs.claude.com

## 2. AI-assisted coding (Day 2)

- **[Must] Claude Code best practices** (Anthropic Engineering): how to direct an agent in a repo. https://www.anthropic.com/engineering/claude-code-best-practices
- **[Must] Claude Code documentation:** workflows, worktrees, subagents. https://docs.claude.com
- **[Should] Git worktree docs:** https://git-scm.com/docs/git-worktree
- **[Should] Pro Git book (free):** branching, merging, rebasing chapters. https://git-scm.com/book
- **[Later] GitHub Docs, resolving merge conflicts:** https://docs.github.com

## 3. Specs, PRDs and prompts (Days 2-3)

- **[Must] Anthropic prompt engineering docs:** be clear and direct, use examples, structure with tags. https://docs.claude.com
- **[Should] Search for "writing a good PRD" from Atlassian or Product School**, then compare to the programme's "pseudocode-level" standard.
- **[Later] Anthropic docs: defining success criteria:** ties specs to evals. https://docs.claude.com

## 4. Evals (Days 2, 3, 7)

- **[Must] Your AI product needs evals** (Hamel Husain): error analysis, failure categories, practical workflow. https://hamel.dev/blog/posts/evals/
- **[Should] Eugene Yan on LLM evaluation:** patterns and pitfalls. https://eugeneyan.com
- **[Should] Anthropic docs: develop test cases / empirical evaluations:** https://docs.claude.com
- **[Later] Search "LLM-as-a-judge calibration"** for limits of automated graders.

## 5. Context engineering (Day 4)

- **[Must] Effective context engineering for AI agents** (Anthropic Engineering): the core Day 4 article. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **[Should] Anthropic docs on context windows, prompt caching, token counting:** https://docs.claude.com
- **[Later] Search "retrieval augmented generation vs agentic search"** for the retrieval-vs-JIT debate (Block 3 depth).

## 6. Tools and MCP (Day 5)

- **[Must] Model Context Protocol, introduction and concepts:** https://modelcontextprotocol.io
- **[Must] MCP Python SDK on GitHub:** README and examples. https://github.com/modelcontextprotocol/python-sdk
- **[Should] Anthropic docs, tool use overview:** https://docs.claude.com
- **[Later] Search "idempotency keys API design"** (Stripe's API docs explain it well): https://docs.stripe.com

## 7. Python

- **[Must] Official Python tutorial** (read quickly, focus on sections 3-9): https://docs.python.org/3/tutorial/
- **[Must] pytest docs, "Get started" and "How-to guides":** https://docs.pytest.org
- **[Should] uv docs:** https://docs.astral.sh/uv/
- **[Should] Pydantic docs, Models and Validators:** https://docs.pydantic.dev
- **[Should] Real Python, tracebacks, virtual environments, type hints:** https://realpython.com
- **[Should] Anthropic Python SDK:** https://github.com/anthropics/anthropic-sdk-python
- **[Later] Python `asyncio` docs:** https://docs.python.org/3/library/asyncio.html

## 8. Azure (Protected Learning Block 1 and deployment)

- **[Must] Azure AI Document Intelligence overview** (Microsoft Learn): models, OCR vs. layout, confidence. https://learn.microsoft.com/azure/ai-services/document-intelligence/
- **[Must] Document Intelligence Studio:** upload a sample PDF and inspect output and confidence. https://documentintelligence.ai.azure.com
- **[Should] Azure Container Apps overview:** https://learn.microsoft.com/azure/container-apps/overview
- **[Should] Azure Key Vault overview:** https://learn.microsoft.com/azure/key-vault/general/overview
- **[Should] Microsoft Learn, search "Azure AI Foundry" or "Azure OpenAI"** for model hosting, whichever the programme uses (ask the lead).
- **[Later] Azure pricing calculator:** https://azure.microsoft.com/pricing/calculator
- **[Later] Microsoft Learn learning paths for AI-900 and AI-102:** https://learn.microsoft.com/credentials

## 9. Risk, responsible AI and governance (Day 8)

- **[Should] Anthropic Responsible Scaling and usage policies** (for general framing): https://www.anthropic.com
- **[Should] Microsoft Responsible AI Standard overview:** search the title on https://www.microsoft.com/ai/responsible-ai
- **[Later] NIST AI Risk Management Framework:** https://www.nist.gov/itl/ai-risk-management-framework

## 10. AML/KYC domain

- **[Must] FATF, "What is money laundering" and risk-based approach pages:** https://www.fatf-gafi.org
- **[Should] FinCEN, CDD rule and SAR overview (US):** https://www.fincen.gov
- **[Should] Search "KYC onboarding process steps"** from a major bank or vendor for a practical walk-through.
- **[Later] Wolfsberg Group guidance:** https://www.wolfsberg-group.org

## 11. Presentation and handoff (Day 10)

- **[Should] Search "architecture decision record (ADR)"**: a model for defending decisions.
- **[Later] Search "runbook template"** for what CTD will expect in a handoff.

---

## Suggested reading order (about 10 hours)

| Block | Items | Time |
|---|---|---|
| 1 | Building Effective Agents; Context engineering article | 1 hr |
| 2 | Claude Code best practices; Git worktree docs | 1 hr |
| 3 | Hamel Husain evals article; Anthropic test-case docs | 1.5 hrs |
| 4 | MCP intro; build the tiny MCP server from the cheat sheet | 2 hrs |
| 5 | Python tutorial skim; pytest get-started; Pydantic basics | 2 hrs |
| 6 | Document Intelligence overview plus Studio experiment | 1.5 hrs |
| 7 | FATF/FinCEN basics | 1 hr |

## Newsletters and communities worth following

- Anthropic Engineering blog: https://www.anthropic.com/engineering
- Latent Space (AI engineering podcast/newsletter): https://www.latent.space
- Simon Willison's blog (practical LLM tooling): https://simonwillison.net
