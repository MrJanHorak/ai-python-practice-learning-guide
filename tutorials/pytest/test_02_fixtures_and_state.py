from examples.ai_systems.core import ReviewStore, ToolContext, validate_extraction


def test_missing_confidence_requires_review(extraction):
    extraction["confidence"]["invoice_id"] = None
    result = validate_extraction(extraction)
    assert result["status"] == "review"
    assert "missing_confidence:invoice_id" in result["reasons"]


def test_a_different_test_receives_a_fresh_extraction(extraction):
    assert extraction["confidence"]["invoice_id"] == 0.98
    assert validate_extraction(extraction)["status"] == "validated"


def test_identical_retry_creates_one_review(review_store):
    first = review_store.create("C-1001", "Check source", "retry-001")
    second = review_store.create("C-1001", "Check source", "retry-001")
    assert first["id"] == second["id"]
    assert len(review_store.list()) == 1


def test_denied_write_leaves_state_unchanged(review_store):
    context = ToolContext(review_store, "denied-001", allow_write=False)
    outcome = context.dispatch("flag_for_review", {"customer_id": "C-1001", "reason": "Check source"})
    assert outcome["error"] == "approval_required"
    assert review_store.list() == []


def test_review_survives_a_new_connection(tmp_path):
    path = tmp_path / "restart.sqlite3"
    original = ReviewStore(path)
    try:
        created = original.create("C-1001", "Check source", "restart-001")
    finally:
        original.close()
    restarted = ReviewStore(path)
    try:
        assert restarted.list()[0]["id"] == created["id"]
        assert restarted.list()[0]["status"] == "pending"
    finally:
        restarted.close()
