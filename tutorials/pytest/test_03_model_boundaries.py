import pytest

from examples.ai_systems import providers
from examples.ai_systems.core import TOOLS, ToolContext
from examples.ai_systems.providers import Conversation, MockConversation, run_agent


def test_missing_model_setting_is_actionable(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    with pytest.raises(providers.ProviderError, match="OPENAI_MODEL"):
        providers.required_env("OPENAI_MODEL")


def test_mock_agent_uses_lookup_and_does_not_write(review_store):
    result = run_agent(MockConversation("Look up C-1002"), ToolContext(review_store, "read-001"), TOOLS)
    assert result["status"] == "completed"
    assert [step["tool"] for step in result["trace"]] == ["lookup_customer"]
    assert result["trace"][0]["result"]["risk_tier"] == "medium"
    assert review_store.list() == []


def test_openai_response_parsing_uses_fake_transport(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-not-a-real-key")
    captured = []
    def fake_transport(url, payload, headers, timeout):
        captured.append(payload)
        return {"status": "completed", "output": [{"type": "message", "content": [
            {"type": "output_text", "text": "A scripted response"}]}]}
    conversation = Conversation("openai", "Explain a test double", model="test-model", transport=fake_transport)
    result = conversation.step([])
    assert result.text == "A scripted response"
    assert captured[0]["model"] == "test-model"
    assert captured[0]["store"] is False


def test_network_guard_prevents_an_accidental_live_call(monkeypatch):
    # This explicitly exercises the guard installed by the autouse fixture.
    with pytest.raises(AssertionError, match="must not call a real model"):
        providers.urlopen("https://example.test/not-a-real-provider")
