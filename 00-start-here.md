# Start here: learn to understand an AI system

This guide teaches applied AI systems through one small, inspectable application. You will follow data from a user request through a model, tools, stored state and a response, then evaluate what happened. You can study independently, pair with someone or work with a mentor.

The main focus is language-model applications. You will also meet basic machine-learning ideas so that predictions, labels, metrics and uncertainty have a clear meaning. Advanced model training and the mathematics of deep learning are deeper follow-on topics.

## Before you start

You should be able to run a terminal command and read simple functions, lists and dictionaries. If those are unfamiliar, start with sections 1-5 of [the Python guide](02-python-cheatsheet.md) and the linked official Python tutorial. Use Python 3.10+ and run commands from the repository root.

The first exercises use generated data and scripted responses. They need no model account, API key or cloud subscription. Pytest requires a small package installation. Live model, UI and Azure exercises are clearly marked extensions.

## Choose a first route

| Your starting point | Read and do | First milestone |
|---|---|---|
| New to AI concepts | Foundations -> Python -> pytest -> workbook sessions 1-3 | Explain one request and one failing test |
| Comfortable programming | Foundations -> provider lab -> workbook -> evaluation | Compare a rule-based baseline with a model-assisted design |
| Interested in cloud | Complete the offline path, then the Azure lab | Trace identity, permissions, endpoint and state locally and in a host |
| Helping others learn | Complete a learner route, then the mentor playbook | Coach a diagnosis while the learner operates the keyboard |

Suggested resource order:

1. [11: AI systems foundations](11-ai-systems-foundations.md): the mental model and a worked trace.
2. [02: Python](02-python-cheatsheet.md) and [14: pytest](14-pytest-tutorial.md): read, run and test small pieces.
3. [08: Workbook](08-project-workbook.md): build understanding through the existing sample.
4. [06: Providers](06-model-provider-lab.md): repeat a task with a chosen live or local model when available.
5. [12: Evaluation](12-evaluation-and-experiments.md): baselines, metrics, holdouts and error analysis.
6. [07: Azure](07-azure-hands-on-lab.md) and [13: Reliability/transfer](13-reliability-and-transfer-project.md): deployment, recovery and a second problem.
7. [09: Mentoring](09-mentor-troubleshooting-and-assessment.md) and [10: Templates](10-project-templates.md): explain and review the evidence.

Resource numbers are identifiers, not a required reading order. Use [the glossary](01-vocabulary-glossary.md) when a term blocks your understanding rather than memorizing it in advance.

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
