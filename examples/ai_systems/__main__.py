"""Commands run from repo root: python -m examples.ai_systems --help."""
import argparse
import json
import tempfile
import uuid
from datetime import date
from pathlib import Path

from .core import AS_OF, DATA, ROOT, TOOLS, ReviewStore, ToolContext, profile_csv, read_json, search_policy, validate_extraction
from .providers import Conversation, MockConversation, ProviderError, run_agent


def emit(value):
    print(json.dumps(value, indent=2, ensure_ascii=False))


def evaluate(provider, model=None):
    """Fresh database per case, no live retries. Expected labels never enter prompts."""
    report = []
    scratch = ROOT / "output/eval-scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    for case in read_json(DATA / "eval_cases.json"):
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            store = ReviewStore(Path(directory) / "reviews.sqlite3")
            try:
                context = ToolContext(store, case["id"], case["allow_write"], case.get("write_customer"))
                conversation = MockConversation(case["prompt"]) if provider == "mock" else Conversation(provider, case["prompt"], model)
                result = run_agent(conversation, context, TOOLS)
                failures = []
                actual_tools = [x["tool"] for x in result["trace"]]
                if actual_tools != case["expected_tools"]:
                    failures.append("tool_trajectory")
                if case.get("expected_text") and case["expected_text"].casefold() not in result["text"].casefold():
                    failures.append("answer_check")
                if case.get("expected_error") and not any(x["result"].get("error") == case["expected_error"] for x in result["trace"]):
                    failures.append("recovery_signal")
                if len(store.list()) != case["expected_writes"]:
                    failures.append("state_change")
                if result["status"] != "completed":
                    failures.append("completion")
                report.append({"id": case["id"], "failures": failures, "result": result})
            finally:
                store.close()
    return {"provider": provider, "model": model, "kind": "scripted_offline" if provider == "mock" else "live_model",
            "passed": sum(not x["failures"] for x in report), "total": len(report), "cases": report}


def main():
    parser = argparse.ArgumentParser(description="Synthetic AI systems learning lab; see README.md")
    sub = parser.add_subparsers(dest="command", required=True)
    profile = sub.add_parser("profile")
    profile.add_argument("--file", type=Path, default=DATA / "customers_messy.csv")
    profile.add_argument("--as-of", type=date.fromisoformat, default=AS_OF)
    extract = sub.add_parser("validate")
    extract.add_argument("--file", type=Path, default=DATA / "extraction_fixtures.json")
    extract.add_argument("--threshold", type=float, default=0.85)
    extract.add_argument("--as-of", type=date.fromisoformat, default=AS_OF)
    search = sub.add_parser("search")
    search.add_argument("query")
    providers = ["mock", "openai", "anthropic", "gemini", "ollama", "local-openai"]
    for command in ("chat", "agent", "eval"):
        p = sub.add_parser(command)
        p.add_argument("--provider", choices=providers, default="mock")
        p.add_argument("--model", help="Explicit accessible model name; otherwise read provider env var")
        if command != "eval":
            p.add_argument("--prompt", default="What is the risk tier for C-1002?")
            p.add_argument("--max-steps", type=int, default=6)
            p.add_argument("--db", type=Path, default=ROOT / "output/reviews.sqlite3")
            p.add_argument("--request-id", default=None)
            p.add_argument("--allow-write", action="store_true", help="App-level authorization to create pending LOCAL demo reviews")
            p.add_argument("--write-customer", help="Exact caller-approved customer for writes; model cannot choose the scope")
    reviews = sub.add_parser("reviews")
    reviews.add_argument("--db", type=Path, default=ROOT / "output/reviews.sqlite3")
    review = sub.add_parser("review")
    review.add_argument("--id", type=int, required=True)
    review.add_argument("--decision", choices=["approved", "rejected"], required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--db", type=Path, default=ROOT / "output/reviews.sqlite3")
    args = parser.parse_args()
    if args.command == "profile":
        emit(profile_csv(args.file, args.as_of))
    elif args.command == "validate":
        fixtures = read_json(args.file)
        if isinstance(fixtures, dict):
            fixtures = [fixtures]
        emit([validate_extraction(x, args.threshold, args.as_of) for x in fixtures])
    elif args.command == "search":
        emit(search_policy(args.query))
    elif args.command == "eval":
        result = evaluate(args.provider, args.model)
        emit(result)
        return 0 if result["passed"] == result["total"] else 1
    else:
        store = ReviewStore(args.db)
        try:
            if args.command == "reviews":
                emit(store.list())
            elif args.command == "review":
                emit(store.decide(args.id, args.decision, args.reviewer))
            else:
                request_id = args.request_id or str(uuid.uuid4())
                context = ToolContext(store, request_id, args.allow_write, args.write_customer)
                conversation = MockConversation(args.prompt) if args.provider == "mock" else Conversation(args.provider, args.prompt, args.model)
                result = run_agent(conversation, context, [] if args.command == "chat" else TOOLS, args.max_steps)
                result.update(provider=args.provider, model=getattr(conversation, "model", "scripted"), request_id=request_id)
                emit(result)
                return 0 if result["status"] == "completed" else 1
        finally:
            store.close()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ProviderError, ValueError, FileNotFoundError) as error:
        print(f"Lab error: {error}")
        raise SystemExit(2)
