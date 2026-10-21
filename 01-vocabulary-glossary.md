# Vocabulary Glossary: Business Language and Frequent Words

Skim this twice before Day 1 and once more at the end of each week. Terms are grouped by the order you'll meet them. The "Watch for" notes are the most common learner confusions.

---

## A. Programme framing

| Term | Meaning | Watch for |
|---|---|---|
| **MTA** | This cohort the learners are a "MTA Graduate" = a learner who builds a POC. | Learners are *not* expected to learn Python from scratch. |
| **CTD** | The downstream engineering team that receives the handoff and takes the POC toward production. | The **ownership line** between MTA Graduate and CTD is a Day 1 topic. |
| **POC** | Proof of concept. | The **POC floor** = working data layer + agent + interface. |
| **Six lenses** | Business, Customer, Code, Risk, Data, Environment. The shared framework for every decision. | Full six-lens mastery is reserved for the Capstone. |
| **Anchor case** | The AML/KYC use case used across the programme. | Learners are assigned specific use cases within it. |
| **Protected Learning (PL)** | Four-hour Friday sessions after the 10-day phase, in four blocks. | Block 1 uses Azure Document Intelligence. |
| **Handoff brief** | Document that transfers the solution to CTD. | Peer-reviewed and defended live on Day 10. |

## B. Discovery and specification

| Term | Meaning | Watch for |
|---|---|---|
| **Discovery checklist** | Questions that turn an ambiguous request into a scoped use case (users, data, constraints, success measures). | Learners skip "who owns the data?" |
| **Backlog** | Prioritized list of work items. | Each item needs **acceptance criteria**. |
| **Acceptance criteria** | Testable conditions that define "done" for a backlog item. | "Works well" is not testable. |
| **Data readiness note** | Written assessment of data gaps and who closes them. | Day 1 deliverable. |
| **Lineage** | Where data came from and how it was transformed. | Unknown lineage = risk. |
| **Latency / refresh cadence** | How stale the data can be, and how often it updates. | Constrains what can be built. |
| **Specification (spec)** | Instruction precise enough that an agent implements it correctly. | Vague: "make it robust". Executable: names inputs, outputs, errors, tests. |
| **PRD** | Product requirements document. Here: edge cases plus pseudocode-level detail. | At least three real edge cases (Day 3). |
| **Edge case** | Unusual but realistic input or state (blank field, name transliteration, expired ID). | Learners list only happy paths. |
| **Pseudocode** | Plain-language logic outline, close to code but not tied to a language. | |

## C. AI-native engineering

| Term | Meaning | Watch for |
|---|---|---|
| **AI coding agent** | A tool that reads a repo, edits files, runs commands/tests and iterates (e.g. Claude Code). | Learners over-trust it; the skill is *reviewing*. |
| **Diff** | The change between two versions of files. | Review line by line, not just the summary. |
| **Repo** | Repository: a project's code under version control. | |
| **Branch** | Parallel line of development in Git. | |
| **Worktree** | A second working directory attached to the same repo, on a different branch. Lets parallel agent sessions run without clobbering each other. | `git worktree add ../feature-x feature-x` |
| **Merge conflict** | Two changes touch the same lines; a human or agent must choose. | |
| **Test suite** | Automated tests for code. In Python usually `pytest`. | Read the traceback bottom-up. |
| **Failing test** | A test whose result doesn't match the expectation. | Is the code wrong, or the test? |
| **Prompt / instruction** | Text given to the model. | |

## D. Evals and quality

| Term | Meaning | Watch for |
|---|---|---|
| **Eval** | Automated check of system behavior against expected results. | Not just "does the answer look right". |
| **Eval set** | A collection of test cases (input plus expected behavior). | Needs variety and hard cases. |
| **Baseline eval** | First measurement before improvements, used for comparison. | Without it you can't prove progress. |
| **Failure taxonomy** | Named categories of failure (wrong tool, hallucinated field, stale data, missed escalation). | Makes patterns visible. |
| **Regression test** | Re-run evals after a change to check nothing got worse. | |
| **Trajectory** | The sequence of steps/tool calls the agent took. | Evals can check the path, not only the answer. |
| **Tool selection eval** | Did the model choose the right tool? | |
| **State change eval** | Did the system end in the correct state (record created once, not twice)? | |
| **Recovery behavior** | What happens after an error or timeout. | |
| **Red-teaming** | Deliberately attacking the system with adversarial or odd inputs. | Log every gap found. |
| **Hallucination** | Model states something unsupported or false. | Block 3 covers detection and citation accuracy. |
| **Ground truth / golden set** | Verified correct answers used for scoring. | |
| **LLM-as-judge** | Using a model to grade outputs. | Needs calibration against human labels. |

## E. Context engineering

| Term | Meaning | Watch for |
|---|---|---|
| **Context window** | Everything the model can see in one call (instructions, history, documents, tool results). | Bigger is not better; relevance matters. |
| **Token** | Unit of text the model reads/writes (roughly 3/4 of an English word). | Drives cost and limits. |
| **Retrieval (RAG)** | Fetch relevant documents ahead of time and add them to context. | |
| **JIT (just-in-time) search** | The agent fetches information only when it decides it needs it, via tools. | Cheaper, but needs good tools. |
| **Memory / state** | Information carried across steps or sessions. | Where is it stored? What gets forgotten? |
| **Compaction** | Summarizing long history to free context. | Can drop critical details. |
| **File-system context** | Using files as external memory the agent reads and writes. | |
| **Tool output** | Results returned by tools; consume context too. | Oversized tool output is a common bug. |
| **Right capability, wrong information** | The Day 4 diagnosis: model could do it but lacked or was swamped by the right data. | |

## F. Tools and MCP

| Term | Meaning | Watch for |
|---|---|---|
| **Tool** | A function the model can ask to call, defined by name, description and input schema. | Descriptions are prompts too. |
| **Schema** | Structured definition of inputs/outputs (JSON Schema, Pydantic). | |
| **MCP** | Model Context Protocol: an open standard for connecting models to tools and data sources. | An MCP *server* exposes tools; the *client* is inside the app/agent. |
| **Auth / permissions** | Who/what is allowed to do what. | Least privilege. |
| **Read vs. write action** | Reading doesn't change anything; writing does. | Writes need guardrails and often approval. |
| **Idempotent** | Repeating the call has the same effect as once. | Retries must not duplicate records. |
| **Error semantics** | How a tool reports failure so the model can recover. | "Error" alone is useless; say what to do next. |
| **Scoped** | Limited to only the data/actions needed. | |

## G. Architecture, cost and risk

| Term | Meaning | Watch for |
|---|---|---|
| **Deterministic workflow** | Fixed code path; the model is used for narrow steps or not at all. | Often the right answer. |
| **Single agent + tools** | One model loop choosing tools. | |
| **Parallel workers** | Several model calls in parallel on independent subtasks. | |
| **Multi-agent** | Multiple agents coordinating. | Only when measurably better. |
| **Autonomy Ladder** | The progression above; climb only with evidence. | |
| **Input / output / reasoning tokens** | Three billed token types, priced differently. | Output and reasoning usually cost more. |
| **Cost-to-serve** | Tokens/request x requests/day x price. | |
| **Model routing** | Send easy tasks to cheaper models. | |
| **Cost blowout** | Runaway usage (loops, huge contexts) causing unexpected spend. | Operational risk; add limits and alerts. |
| **Human approval gate** | Point requiring human sign-off before an action. | Before the irreversible step. |
| **Permission boundary** | Limit on what the system can touch. | |
| **Responsible-AI review** | Checks for fairness, privacy, safety, transparency. | |
| **Ownership split** | What the model owns, what software owns, what stays human. | Must be defended. |

## H. Deployment and Azure

| Term | Meaning | Watch for |
|---|---|---|
| **Platform vs. raw agents** | Managed agent platform vs. building the agent loop yourself. | |
| **Cloud / on-prem / hybrid** | Where the system runs. | Driven by data sensitivity. |
| **Container** | Packaged app with its dependencies (Docker). | |
| **Observability** | Logs, metrics, traces to see what the system is doing. | |
| **Circuit breaker** | Stops calls to a failing dependency to prevent cascades. | |
| **Azure AI Document Intelligence** | Azure service that extracts text, tables and fields from documents. | Returns **confidence scores**. |
| **OCR** | Optical character recognition: reading text from images/scans. | Native PDFs often don't need OCR. |
| **Extraction schema / output contract** | Defined fields the pipeline must produce. | |
| **Confidence threshold** | Cutoff below which a human reviews. | |
| **PII** | Personally identifiable information. | Decide handling at each connection. |
| **Key Vault** | Azure service for secrets (keys, connection strings). | Never hard-code secrets. |

## I. AML/KYC domain

| Term | Meaning |
|---|---|
| **KYC** | Know Your Customer: verifying identity and assessing risk at onboarding. |
| **AML** | Anti-Money Laundering: detecting and preventing laundering of illicit funds. |
| **CDD / EDD** | Customer Due Diligence / Enhanced Due Diligence for higher-risk customers. |
| **PEP** | Politically Exposed Person; higher risk. |
| **UBO** | Ultimate Beneficial Owner: the real person behind a company. |
| **Sanctions screening** | Checking names against government watchlists. |
| **SAR** | Suspicious Activity Report filed with regulators. |
| **False positive** | A legitimate case flagged as suspicious; drives analyst workload. |
| **Transaction monitoring** | Ongoing rules/models that flag unusual activity. |
| **Adverse media** | Negative news about a customer. |

---

## Quick self-test

Explain each in one sentence without looking: worktree, idempotent, JIT search, compaction, failure taxonomy, trajectory eval, Autonomy Ladder, cost-to-serve, human approval gate, confidence threshold, UBO.
