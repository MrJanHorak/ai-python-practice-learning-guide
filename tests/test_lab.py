"""Offline invariants, provider protocol fixtures and recovery checks. No network."""
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

from examples.ai_systems.__main__ import evaluate
from examples.ai_systems.azure_extract import normalize_document
from examples.ai_systems.core import DATA, ROOT, TOOLS, ReviewStore, ToolContext, profile_csv, read_json, search_policy, validate_extraction
from examples.ai_systems.providers import Conversation, MockConversation, ProviderError, ToolCall, Turn, local_url, run_agent
from examples.ai_systems.scoring import Customer, score


class LabTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / "output/test-scratch"
        scratch.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=scratch)
        self.path = Path(self.directory.name) / "reviews.sqlite3"
        self.store = ReviewStore(self.path)
        self.context = ToolContext(self.store, "test-request", True, "C-1001")

    def tearDown(self):
        self.store.close()
        self.directory.cleanup()

    def test_score_threshold_and_invalid_input(self):
        self.assertEqual(score(Customer("SIM", 0.7)), "review")
        for value in (-1, 1.1, float("nan")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                score(Customer("SIM", value))

    def test_clean_and_messy_profiles_match_authored_labels(self):
        self.assertEqual(profile_csv(DATA / "customers_clean.csv")["issues"], [])
        actual = profile_csv(DATA / "customers_messy.csv")
        expected = read_json(DATA / "answers/profile_expected.json")
        self.assertEqual(actual["rows"], expected["rows"])
        self.assertEqual({str(x["csv_line"]): x["issues"] for x in actual["issues"]}, expected["issues_by_csv_line"])

    def test_extraction_cases_match_independent_expected_results(self):
        expected = {x["document_id"]: x for x in read_json(DATA / "answers/extraction_expected.json")}
        for item in read_json(DATA / "extraction_fixtures.json"):
            with self.subTest(item=item["document_id"]):
                result = validate_extraction(item)
                self.assertEqual(result["status"], expected[item["document_id"]]["status"])
                self.assertEqual(result["reasons"], expected[item["document_id"]]["reasons"])

    def test_invalid_confidence_and_boolean_amount_are_not_accepted(self):
        item = read_json(DATA / "extraction_fixtures.json")[0]
        item["total_amount"] = True
        item["confidence"]["invoice_id"] = float("nan")
        reasons = validate_extraction(item)["reasons"]
        self.assertIn("invalid_total_amount", reasons)
        self.assertIn("invalid_confidence:invoice_id", reasons)

    def test_obsolete_policy_is_excluded(self):
        matches = search_policy("confidence threshold")
        self.assertEqual(matches[0]["source_id"], "POL-REVIEW-v2")
        self.assertNotIn("POL-REVIEW-v1", [x["source_id"] for x in matches])
        self.assertEqual(search_policy("quantum neutrino"), [])

    def test_write_requires_application_approval_and_customer_scope(self):
        args = {"customer_id": "C-1001", "reason": "demo"}
        denied = ToolContext(self.store, "x", False, "C-1001")
        self.assertEqual(denied.dispatch("flag_for_review", args)["error"], "approval_required")
        args["customer_id"] = "C-1002"
        self.assertEqual(self.context.dispatch("flag_for_review", args)["error"], "write_scope_denied")
        self.assertEqual(self.store.list(), [])

    def test_model_cannot_supply_approval_argument(self):
        result = self.context.dispatch("flag_for_review", {"customer_id": "C-1001", "reason": "demo", "approved": True})
        self.assertEqual(result["error"], "invalid_arguments")
        self.assertEqual(self.store.list(), [])

    def test_malformed_and_unknown_tools_recover(self):
        for name, args, error in [("delete_everything", {}, "unknown_tool"),
                                  ("lookup_customer", [], "invalid_arguments"),
                                  ("lookup_customer", {"customer_id": "oops"}, "invalid_customer_id"),
                                  ("lookup_customer", {"customer_id": "C-9999"}, "customer_not_found")]:
            self.assertEqual(self.context.dispatch(name, args)["error"], error)

    def test_idempotency_persists_and_detects_payload_conflict(self):
        first = self.store.create("C-1001", "demo", "retry-key")
        self.store.close()
        self.store = ReviewStore(self.path)
        self.assertEqual(first["id"], self.store.create("C-1001", "demo", "retry-key")["id"])
        self.assertEqual(len(self.store.list()), 1)
        self.assertEqual(self.store.create("C-1002", "demo", "retry-key")["error"], "idempotency_conflict")

    def test_human_workflow_blocks_conflicting_decision(self):
        row = self.store.create("C-1001", "demo", "human-key")
        approved = self.store.decide(row["id"], "approved", "demo-reviewer")
        self.assertEqual(approved["status"], "approved")
        self.assertEqual(self.store.decide(row["id"], "approved", "demo-reviewer"), approved)
        with self.assertRaises(ValueError):
            self.store.decide(row["id"], "rejected", "demo-reviewer")

    def test_loop_budget_and_call_budget(self):
        class Loop:
            def step(self, tools, results):
                return Turn(calls=[ToolCall("x", "lookup_customer", {"customer_id": "C-1001"})])
        result = run_agent(Loop(), self.context, TOOLS, max_steps=2)
        self.assertEqual(result["status"], "budget_exhausted")
        self.assertEqual(len(result["trace"]), 2)
        self.assertEqual(run_agent(Loop(), self.context, TOOLS, max_calls=1)["status"], "budget_exhausted")

    def test_truncated_response_does_not_execute_partial_tool(self):
        class Truncated:
            def step(self, tools, results):
                return Turn(calls=[ToolCall("x", "flag_for_review", {"customer_id": "C-1001", "reason": "x"})], stop="incomplete")
        self.assertEqual(run_agent(Truncated(), self.context, TOOLS)["status"], "truncated_or_failed")
        self.assertEqual(self.store.list(), [])

    def test_mock_eval_is_labeled_scripted(self):
        report = evaluate("mock")
        self.assertEqual((report["passed"], report["total"]), (12, 12))
        self.assertEqual(report["kind"], "scripted_offline")

    def test_local_endpoint_rejects_remote_and_embedded_credentials(self):
        for url in ("https://example.com/v1", "http://user:secret@localhost:1234", "http://localhost:1234?key=x"):
            with self.subTest(url=url), self.assertRaises(ProviderError):
                local_url(url)

    def test_azure_mapping_handles_missing_fields_and_confidence(self):
        document = NS(fields={"InvoiceId": NS(confidence=None, value_string="INV-X", content="INV-X")})
        result = normalize_document(document, "C-1001", "demo-doc")
        self.assertIsNone(result["total_amount"])
        self.assertIsNone(result["confidence"]["invoice_id"])
        self.assertEqual(validate_extraction(result)["status"], "review")


class ProtocolTests(unittest.TestCase):
    def conversation(self, provider, frames):
        calls = []
        def transport(url, payload, headers, timeout):
            calls.append({"url": url, "payload": copy.deepcopy(payload), "timeout": timeout})
            return frames.pop(0)
        env = {"OPENAI_API_KEY": "test-only", "ANTHROPIC_API_KEY": "test-only", "GEMINI_API_KEY": "test-only"}
        with patch.dict(os.environ, env, clear=True):
            session = Conversation(provider, "Look up C-1001", model="test-model", transport=transport)
        return session, calls

    def test_openai_preserves_reasoning_and_call_id(self):
        session, calls = self.conversation("openai", [
            {"status": "completed", "output": [{"type": "reasoning", "encrypted_content": "opaque"},
              {"type": "function_call", "call_id": "call-7", "name": "lookup_customer", "arguments": '{"customer_id":"C-1001"}'}]},
            {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "low"}]}]}])
        turn = session.step(TOOLS)
        session.step(TOOLS, [(turn.calls[0], {"risk_tier": "low"})])
        payload = calls[-1]["payload"]
        self.assertFalse(payload["store"])
        self.assertEqual(payload["input"][1]["encrypted_content"], "opaque")
        self.assertEqual(payload["input"][-1]["call_id"], "call-7")
        self.assertTrue(payload["tools"][0]["strict"])

    def test_anthropic_preserves_blocks_and_groups_results(self):
        session, calls = self.conversation("anthropic", [
            {"content": [{"type": "tool_use", "id": "a1", "name": "lookup_customer", "input": {"customer_id": "C-1001"}}], "stop_reason": "tool_use"},
            {"content": [{"type": "text", "text": "missing"}], "stop_reason": "end_turn"}])
        turn = session.step(TOOLS)
        session.step(TOOLS, [(turn.calls[0], {"error": "customer_not_found"})])
        result = calls[-1]["payload"]["messages"][-1]["content"][0]
        self.assertEqual(result["tool_use_id"], "a1")
        self.assertTrue(result["is_error"])
        self.assertIn("input_schema", calls[0]["payload"]["tools"][0])

    def test_gemini_preserves_signature_and_function_response_id(self):
        content = {"role": "model", "parts": [{"thoughtSignature": "opaque-signature", "functionCall":
                   {"id": "g1", "name": "lookup_customer", "args": {"customer_id": "C-1001"}}}]}
        session, calls = self.conversation("gemini", [
            {"candidates": [{"content": content, "finishReason": "STOP"}]},
            {"candidates": [{"content": {"role": "model", "parts": [{"text": "low"}]}, "finishReason": "STOP"}]}])
        turn = session.step(TOOLS)
        session.step(TOOLS, [(turn.calls[0], {"risk_tier": "low"})])
        contents = calls[-1]["payload"]["contents"]
        self.assertEqual(contents[1], content)
        self.assertEqual(contents[2]["parts"][0]["functionResponse"]["id"], "g1")

    def test_ollama_uses_native_arguments_and_tool_name(self):
        session, calls = self.conversation("ollama", [
            {"message": {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": "lookup_customer", "arguments": {"customer_id": "C-1001"}}}]}},
            {"message": {"role": "assistant", "content": "low"}, "done_reason": "stop"}])
        turn = session.step(TOOLS)
        session.step(TOOLS, [(turn.calls[0], {"risk_tier": "low"})])
        self.assertTrue(calls[0]["url"].endswith("/api/chat"))
        self.assertEqual(calls[-1]["payload"]["messages"][-1]["tool_name"], "lookup_customer")

    def test_local_openai_uses_json_arguments_and_tool_call_id(self):
        session, calls = self.conversation("local-openai", [
            {"choices": [{"message": {"role": "assistant", "content": None, "tool_calls": [
               {"id": "l1", "type": "function", "function": {"name": "lookup_customer", "arguments": '{"customer_id":"C-1001"}'}}]}, "finish_reason": "tool_calls"}]},
            {"choices": [{"message": {"role": "assistant", "content": "low"}, "finish_reason": "stop"}]}])
        turn = session.step(TOOLS)
        session.step(TOOLS, [(turn.calls[0], {"risk_tier": "low"})])
        self.assertTrue(calls[0]["url"].endswith("/v1/chat/completions"))
        self.assertEqual(calls[-1]["payload"]["messages"][-1]["tool_call_id"], "l1")

    def test_malformed_model_json_is_passed_to_validator(self):
        session, _ = self.conversation("openai", [{"output": [{"type": "function_call", "name": "lookup_customer", "call_id": "bad", "arguments": "not-json"}]}])
        self.assertIsNone(session.step(TOOLS).calls[0].arguments)


if __name__ == "__main__":
    unittest.main()
