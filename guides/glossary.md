# Glossary: plain-language reference for AI systems

Use this as a reference while building the sample project. Explain terms in your own words and connect them to an observed behavior. The "Watch for" notes highlight common learner confusions.

---

## A. Learning and project roles

| Term | Meaning | Watch for |
|---|---|---|
| **Learner** | Person building understanding through reading, experiments and a working project. | Running a demo and explaining its behavior are different skills. |
| **Mentor** | Person who helps a learner reason, practise, diagnose failures and review evidence. | Use questions and staged hints so the learner retains ownership. |
| **Implementation team** | People who take a prototype toward a maintainable deployed system. | Agree what is demonstrated, what remains incomplete and who owns the next step. |
| **POC / POC floor** | Proof of concept / the project's minimum demonstration criteria. | A working data layer, agent and interface are a start; the reviewed course also names five evidence checks. Passing them is not production readiness. |
| **Review dimensions** | User value, experience, software quality, risk, data and deployment environment. | Use them to examine tradeoffs; they are not a certification framework. |
| **Running example** | Fictional onboarding/document review used to connect the lessons. | Its rules are invented for teaching, not domain requirements. |
| **Extension sessions** | Optional deeper practice in extraction, workflows, retrieval and deployment. | Choose a topic once the core system makes sense. |
| **Handoff brief** | Document that transfers scope, evidence, limitations and operating instructions to the next owner. | Explain what works, what was tested and what still needs engineering. |

## B. Discovery and specification

| Term | Meaning | Watch for |
|---|---|---|
| **Discovery checklist** | Questions that turn an ambiguous request into a scoped use case (users, data, constraints, success measures). | Learners skip "who owns the data?" |
| **Backlog** | Prioritized list of work items. | Each item needs **acceptance criteria**. |
| **Acceptance criteria** | Testable conditions that define "done" for a backlog item. | "Works well" is not testable. |
| **Data readiness note** | Written assessment of data gaps and who closes them. | Do this before relying on data in a build. |
| **Lineage** | Where data came from and how it was transformed. | Unknown lineage = risk. |
| **Latency / refresh cadence** | How stale the data can be, and how often it updates. | Constrains what can be built. |
| **Specification (spec)** | Instruction precise enough that an agent implements it correctly. | Vague: "make it robust". Executable: names inputs, outputs, errors, tests. |
| **PRD** | Product requirements document. Here: edge cases plus pseudocode-level detail. | At least three real edge cases. |
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
| **Hallucination** | Model states something unsupported or false. | Check whether important claims are supported by the retrieved source/version. |
| **Ground truth / golden set** | Verified correct answers used for scoring. | |
| **LLM-as-judge** | Using a model to grade outputs. | Needs calibration against human labels. |

## E. Context engineering

| Term | Meaning | Watch for |
|---|---|---|
| **Context window** | Everything the model can see in one call (instructions, history, documents, tool results). | Bigger is not better; relevance matters. |
| **Token** | Unit of text the model reads/writes (roughly 3/4 of an English word). | Drives cost and limits. |
| **Retrieval / RAG** | Retrieval fetches relevant information; retrieval-augmented generation uses that information when generating an answer. | Retrieval quality and answer quality need separate checks. |
| **JIT (just-in-time) search** | Fetching information when needed, often through an agent's search tool. | Can use retrieval too; compare measured quality, latency and cost. |
| **Memory / state** | Information carried across steps or sessions. | Where is it stored? What gets forgotten? |
| **Compaction** | Summarizing long history to free context. | Can drop critical details. |
| **File-system context** | Using files as external memory the agent reads and writes. | |
| **Tool output** | Results returned by tools; consume context too. | Oversized tool output is a common bug. |
| **Right capability, wrong information** | A model may have the required ability but lack relevant evidence or receive too much irrelevant context. | Inspect exactly what was provided at the failing step. |

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
| **Input / output / reasoning tokens** | Provider-specific usage categories; reasoning may be included within an output category. | Read the selected model's usage and pricing rules; avoid double-counting. |
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
| **Tenant / subscription** | Tenant: identity directory. Subscription: Azure resource/billing scope. | Confirm both when diagnosing access. |
| **Resource group / region** | Resource group organizes Azure resources; region is a deployment location. | Region, quota and service availability can constrain a lab. |
| **Endpoint / model deployment** | Endpoint: service URL. A deployment identifies a provisioned model on platforms that use deployments. | A public model name is not automatically the correct deployment name. |
| **Principal / Microsoft Entra ID** | A principal is an identity; Entra ID provides identity and token services. | Authenticate the app's identity, not merely your browser session. |
| **RBAC / data-plane permission** | Role-based access control assigns scoped permissions; service calls require appropriate service-data access. | Being able to see a resource does not prove you can call it. |
| **Managed identity** | Azure-managed application identity for supported service-to-service authentication. | Local developer credentials and hosted app identities differ. |
| **Quota / rate limit** | Quota bounds allocated capacity; rate limits bound request/token throughput. | Bounded retries do not fix missing quota. |
| **HTTP / JSON** | HTTP carries requests and responses; JSON is a common data format. | Inspect status, body shape and request ID separately. |
| **Timeout / backoff** | Timeout bounds a wait; backoff spaces retries. | Repeating a write after a timeout requires idempotency. |
| **Correlation ID** | Identifier connecting a user request with logs and downstream calls. | Trace failures without logging credentials or sensitive documents. |
| **Long-running operation / poller** | Service starts work and exposes progress/results later. SDK pollers wrap that process. | This is separate from Python's `async` syntax. |
| **Persistent workflow state** | Saved progress that survives process restart. | An in-memory variable is lost when the app restarts. |
| **Microsoft Foundry** | Current Microsoft branding for its AI application and agent platform. | Confirm which portal, SDK and resource type the learning path uses. |

## Provider and local-model vocabulary

| Term | Meaning | Watch for |
|---|---|---|
| **Coding agent vs. application model** | Coding agent edits a repository; the application's model answers requests or proposes tool calls at runtime. | An API chat client alone is not a repository-editing coding agent. |
| **Tool call vs. MCP** | Tool call: model proposes a function. MCP: protocol connecting applications to tool servers and resources. | The sample's direct functions do not constitute an MCP integration. |
| **OpenAI-compatible endpoint** | Server implements some OpenAI-shaped requests and responses. | Compatibility can be partial; test tools and response formats separately. |
| **Local inference / model weights** | Inference runs a downloaded model on your machine using a model server. | Download size, RAM/VRAM, quantization, license and tool support vary. |
| **Mock / fixture** | Scripted behavior or saved data used for repeatable tests. | A passing mock test does not establish model accuracy or live access. |

## I. Optional domain vocabulary: AML/KYC

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

## J. First steps: files, configuration and connected records

| Term | Meaning | Example or common confusion |
|---|---|---|
| **Terminal / shell / PowerShell** | A terminal displays text commands; a shell interprets them. PowerShell is the shell used in this guide. | Commands for Bash may need different quoting on Windows. |
| **Repository root / working directory** | The root contains this project's README. The working directory is where a command starts looking for relative files. | Run the lesson commands from the root, even though the Markdown is in `lessons/`. |
| **Interpreter / virtual environment** | The interpreter runs Python; a virtual environment gives one project its own installed packages. | `python -m pip` installs for that Python, avoiding a different system `pip`. |
| **Dependency / version pin / lockfile** | A dependency is a package you need. A pin selects a version; a lockfile records a resolved set of versions. | A range such as `<2` is not a complete tested lockfile. |
| **CLI / flag / environment variable** | A CLI is a command-line interface. A flag is an option such as `--case`. An environment variable is a process setting. | A `.env` text file has no effect unless something loads it. |
| **CSV / YAML / JSON / JSONL** | CSV stores tables; YAML stores indented values; JSON stores structured values; JSONL stores one JSON value per line. | A whole JSONL file is not one JSON array. |
| **Boolean / null** | Boolean means true or false. Null means no value. | Missing confidence is not the number zero. |
| **Application / party** | Here, an application is one review request; a party is a company or person connected to it. | One application can have many parties to screen. |
| **Primary key / foreign key / join** | A primary key identifies a record; a foreign key refers to another record; a join matches the related records. | Join documents to `party_id`, not a possibly shared name. |
| **Orphan / duplicate / completeness** | An orphan has no referenced parent. A duplicate repeats a record/key. Completeness asks whether required evidence exists. | No orphans does not mean no missing documents. |
| **As-of date / validity interval / freshness** | The review date, the period a rule applies, and how up to date a source is. | A real policy may be superseded or not yet effective. |
| **Manifest / hash** | A manifest lists files and metadata. A hash fingerprints bytes to detect changes. | A matching hash proves matching bytes, not truthful data. |
| **Given / When / Then** | A way to state starting conditions, an action and its expected result. | Write the expected result independently of current code. |
| **Open question / owner** | An unresolved fact and the person/role responsible for settling it. | “Unknown” should lead to an evidence request, not a guess. |

## K. Replay, MCP and test evidence

| Term | Meaning | Example or common confusion |
|---|---|---|
| **Host / client / server** | The host is the tool-using application; its client manages an MCP connection; the server exposes tools/context. | A server can run locally without a web address. |
| **Transport / stdio / subprocess** | Transport carries messages. Stdio uses process input/output. A subprocess is a program launched by another program. | Ordinary debug prints on a stdio server's stdout can corrupt protocol messages. |
| **Input schema / argument / default** | Schema defines allowed input structure; arguments are actual supplied values; a default fills an omitted value. | A bad default can select the wrong jurisdiction even when input types are valid. |
| **Authentication / authorization / least privilege** | Authentication verifies identity; authorization checks allowed actions; least privilege grants only needed access. | Successful login does not establish permission to read an index. |
| **Spy / fake / mock** | A spy records calls while preserving real work; a fake implements substitute behavior; mock terminology often includes replacements with programmed expectations. | State which behavior was replaced instead of relying on the label. |
| **Replay / live / provenance** | Replay uses recorded or authored behavior; live makes a new service/model call; provenance says where evidence came from. | This guide's replay is authored and does not demonstrate model reasoning. |
| **Replay missing / divergence** | Missing means no supported recorded variant. Divergence means observed work differs from the replay's expectation. | Neither should be silently counted as a successful live evaluation. |
| **Fault injection / timeout after commit** | Deliberately cause a failure. A timeout after commit means saved work exists even though the reply was lost. | Retry the same operation with the same idempotency key. |
| **Unit / integration test** | A unit test checks a small piece; an integration test checks interactions between pieces. | A real local MCP exchange tests a boundary a direct-function call bypasses. |
| **Collected / skipped / deselected / xfail** | Found by pytest / not executed / excluded by selection / marked as expected to fail. | Passing selected tests says nothing about excluded assignment tests. |
| **Allowlist / minimisation / must-keep state** | Explicit allowed fields/actions; only retain needed data; preserve required facts and unresolved work when shortening context. | Smaller context is not better if an owner or open question disappears. |
| **Index / metadata filter / query key** | A searchable collection; a restriction by fields such as jurisdiction; a read credential for Azure Search. | Relevance ranking does not replace scope or access checks. |

## L. Oversight, privacy and operating evidence

| Term | Meaning | Example or common confusion |
|---|---|---|
| **Hard rule / status precedence** | A condition that must hold; the order for selecting one headline status when several apply. | Keep every reason even when only one status is displayed. |
| **HITL / HOTL / HOOTL / HITC** | Human in the loop / on the loop / out of the loop / in command. | See [oversight](../lessons/11-oversight-permissions-and-red-teaming.md) for examples; classify each step. |
| **Default deny / scoped approval** | Reject actions unless explicitly permitted; permission covers a particular action/resource/payload and applicable time. | A model-provided “approved” flag is not verified approval. |
| **PASS / FAIL / UNVERIFIED** | Required evidence succeeded / failed / is missing. | An unavailable Azure account leaves live integration unverified. |
| **Redact / minimise / block / pass** | Mask specific values / retain needed fields / stop transfer / allow transfer unchanged. | An ID can still identify someone; redaction does not guarantee anonymity. |
| **Native text / scanned image / repeated group** | Embedded selectable text / pixels needing OCR / multiple similar records such as owners. | Do not collapse several owners into a single extracted field. |
| **p95 / peak / mean** | A percentile near which 95% of observations fall; highest measured demand; arithmetic average. | Report the calculation convention and sample size; two requests cannot establish normal tail behavior. |
| **Per-call / per-case cost** | One model request's charge / all calls and service work for a user case. | Include repeated input and chargeable failed attempts. |
| **Alert / cap / kill switch** | A notification / enforced consumption limit / way to stop a capability. | A billing alert does not automatically prevent spending. |
| **Claim → evidence → limitation** | Say what works, point to a reproducible check, and state what it does not establish. | Local MCP passing does not establish live model quality. |
| **Runbook / escalation** | Operating and recovery instructions / transferring an unresolved issue to its responsible owner. | Identify a role, diagnostic command and required evidence. |

## Quick self-test

See [foundations](../lessons/01-ai-systems-foundations.md) for model/application/system, training/inference, tokens, embeddings and retrieval; [evaluation](../lessons/08-evaluation.md) for precision/recall, holdouts and leakage; and [pytest](../lessons/03-pytest.md) for fixtures, parametrization and test doubles.

Explain each in one sentence without looking: worktree, idempotent, JIT search, compaction, failure taxonomy, trajectory eval, Autonomy Ladder, cost-to-serve, human approval gate, confidence threshold, UBO.
