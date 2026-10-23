# Start here: learn to understand an AI system

This guide teaches applied AI systems through small, inspectable applications. You will follow data from a user request through a model, tools, stored state and a response, then evaluate what happened. You can study independently, pair with someone or work with a mentor. No AI, Azure, banking or MCP knowledge is assumed. New vocabulary is explained at first use or in [the glossary](glossary.md).

The main focus is language-model applications. You will also meet basic machine-learning ideas so that predictions, labels, metrics and uncertainty have a clear meaning. Advanced model training and the mathematics of deep learning are deeper follow-on topics.

## Before you start

You should be able to run a terminal command and read simple functions, lists and dictionaries. If those are unfamiliar, start with sections 1-5 of [the Python guide](../lessons/02-python.md) and the linked official Python tutorial. Use Python 3.10+ and run commands from the repository root.

The first exercises use generated data and scripted responses. They need no model account, API key or cloud subscription. Pytest requires a small package installation. Live model, UI and Azure exercises are clearly marked extensions.

## Choose a first route

| Your starting point | Read and do | First milestone |
|---|---|---|
| New to AI concepts | Lessons 01–05, then 06–08; use workbook sessions for practice | Explain a request, a linked record and a failing test |
| Comfortable programming | Foundations -> provider lab -> workbook -> evaluation | Compare a rule-based baseline with a model-assisted design |
| Interested in cloud | Complete the offline path, then the Azure lab | Trace identity, permissions, endpoint and state locally and in a host |
| Helping others learn | Complete a learner route, then the mentor playbook | Coach a diagnosis while the learner operates the keyboard |

Suggested resource order (the [root README](../README.md) links every lesson):

1. [AI systems foundations](../lessons/01-ai-systems-foundations.md): the mental model and a worked trace.
2. [Python](../lessons/02-python.md) and [pytest](../lessons/03-pytest.md): read, run and test small pieces.
3. Lessons [04: configuration/replay](../lessons/04-files-configuration-and-replay.md), [05: scope/data](../lessons/05-scope-and-linked-data.md), [06: context/search](../lessons/06-context-and-search.md) and [07: MCP](../lessons/07-mcp-and-integration-tests.md): understand the course's integration patterns with independent local exercises.
4. [08: evaluation](../lessons/08-evaluation.md): baselines, metrics, holdouts and error analysis.
5. [09: providers](../lessons/09-model-providers.md) and [10: Azure](../lessons/10-azure.md): optional live/local integrations after offline concepts make sense.
6. [11: oversight](../lessons/11-oversight-permissions-and-red-teaming.md), [12: reliability/transfer](../lessons/12-reliability-and-transfer.md) and [13: documents/privacy](../lessons/13-document-pipelines-and-privacy.md): control actions, measure operation and handle evidence.
7. [14: workbook](../lessons/14-project-workbook.md): combine the ideas. Use it earlier when a short practice session helps.
8. [Course companion](course-companion.md), [Mentoring](mentor-playbook.md) and [Templates](project-templates.md): prepare to support the actual exercises and explain evidence.

Lessons are numbered in the recommended learning order; reference guides are unnumbered. Use [the glossary](glossary.md) when a term blocks your understanding rather than memorizing it in advance.

## First 30-45 minutes

Follow the environment setup in README, then:

```powershell
python -m examples.ai_systems agent --provider mock --prompt "What is the risk tier for C-1002?"
python -m examples.ai_systems profile
python -m unittest discover -s tests -v
```

Predict the result before each command. Afterwards explain where the facts came from, which code ran and what state changed. The assigned risk tier is a fictional stored label; the mock did not infer it. Tests passing establish only the behavior those tests actually checked.

## A learning cycle that builds understanding

For each session: **predict -> run -> inspect -> explain -> change one thing -> compare**. Write down your prediction and evidence. If an AI coding tool helps, explain the resulting diff in your own words before accepting it.

Maintain a short notebook with the question, predicted behavior, command/input, observed result, explanation and next uncertainty. Use synthetic data. Never paste credentials into that notebook or the chat.

## Checkpoints

- Can you distinguish a model, an application and the system around it?
- Can you trace a tool proposal to the application's actual permission check and write?
- Can you explain a failed assertion and improve a test without changing the expected behavior merely to make it pass?
- Can you distinguish a missing source from an unsupported answer using a correct source?
- Can you measure a baseline, inspect errors and explain which outcomes remain untested?
- Can you propose recovery after a timeout, restart or denied permission?
- Can you choose a suitable design for a different small problem?

If one answer is weak, revisit the matching lesson and run another experiment. Completion time alone is not a useful measure of understanding.
