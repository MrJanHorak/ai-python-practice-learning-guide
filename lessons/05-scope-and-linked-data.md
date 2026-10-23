# 05: Scope, linked data and a review contract

**Outcome:** turn an unclear request into testable work, join related records and explain who still decides. No banking knowledge is required. The rules below are fictional teaching rules, not regulations.

## 1. Define the job before choosing a model

Write four lines:

```text
Decision: help a reviewer identify missing evidence and possible matches.
User: a trained human reviewer.
In scope: read fictional records, find relevant policies, create pending reviews.
Out of scope: approve/reject applications, contact applicants, use real personal data.
```

An open question is something you cannot yet answer. Write its owner and what evidence would settle it. Example: “How old may a screening result be? Policy owner to confirm; no threshold assumed.” A model's plausible answer does not resolve an unknown requirement.

Turn one requirement into **Given / When / Then**: “Given a possible match for a beneficial owner, when the application is checked, then a pending human-review record exists and the application is not approved.” This is an acceptance criterion: an observable condition for success.

## 2. Understand the tables

Use [the dataset guide](../data/linked_review/README.md), then run:

```powershell
python -m examples.learning_lab profile
```

There are six applications, eighteen parties and sixteen documents. An application is the whole request. A party is an organisation or person connected to it. Each application here has a company, a director and a beneficial owner. A beneficial owner is a person who ultimately owns or controls a company. These are simplified relationships.

`application_id` links a party to an application. `party_id` links a document or screening result to a party. A **join** combines records through those matching keys. Two people can share a name; joining by name is unreliable. An **orphan** is a row whose referenced parent is absent.

Before viewing the [answer key](../data/linked_review/expected_outcomes.json), count one application's parties/documents by hand. Find a missing document, an expired one and an unavailable screening result. Record impact, whether the gap blocks work, and its owner. An empty orphan list does not prove all expected records exist.

## 3. Read statuses without treating them as decisions

| Status | Meaning in this exercise | Waiting for data? |
|---|---|---|
| `COMPLIANCE_REVIEW` | A possible match needs specialist review | Not determined by this status alone |
| `SCREENING_UNAVAILABLE` | At least one party could not be screened | Yes |
| `MISSING_DATA` | Required evidence is missing | Yes |
| `FLAGGED` | Other findings need human attention | No |
| `NO_FLAGS` | These checks found no issue | No |

The first applicable status in this table wins, but all reasons must survive. In application 5006, the possible match takes precedence and the missing-document reason remains. Every status still requires a person to decide. Our result's `pending` field follows the simplified status convention; inspect reasons as well to understand outstanding work. `NO_FLAGS` means neither “approved” nor “safe in every respect.”

The older invoice project's `validated/review` labels describe extraction checks. Its CLI `approved/rejected` action is a human decision about a local review record. It is not an application decision and should not appear as an application approval feature in a course adaptation.

## 4. Keep hard rules separate from ordinary quality scores

A **hard rule** is a condition that must always hold within the exercise. Check it individually; do not average a violation away with many easy passes.

- Never automatically approve or reject an application.
- Route every possible match and compliance-review reason to a person through a review case.
- Screen the company and every director and beneficial owner.
- Keep personal data out of logs; draft communications only for a human.
- Missing or failed data must not produce a recommendation.
- For an AML extension, do not automate alert closure, report filing or applicant notifications.

The small runner always returns `recommendation: null` and `human_decision_required: true`. It illustrates a few of these boundaries, not a complete implementation of every course rule. The course's supplied contract and tests remain authoritative for its labs.

## 5. Change one thing with a coding agent

Create a scratch Git branch before experimenting. Git records versions of files; a branch gives your changes a name. Run `git status`, `git switch -c practice/linked-data` and the tests before editing. Use your actual course branch convention in its repository.

Ask your coding agent to add one orphan-document check using a temporary fixture, with one failing test before the fix. Review `git diff`, explain each changed line and rerun the named test. A coding agent edits files; it is separate from the model an application calls while running. The same scoped request can be used with Claude Code, Codex or Gemini CLI.

**Teach-back:** explain application versus party, status versus decision, and missing evidence versus a negative screening result. Write one open question with an owner.

Next: [context and search](06-context-and-search.md).
