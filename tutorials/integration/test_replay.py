"""Observe real local tools, not just an authored model answer."""
import json
import shutil
import pytest
from examples.learning_lab.core import DATA, ReviewQueue, compact_state, get_application, profile, run_case, search_policy, shape_documents


@pytest.fixture
def queue(tmp_path):
    database = ReviewQueue(tmp_path / 'reviews.sqlite3')
    yield database
    database.close()


def test_spy_preserves_real_work_and_checks_party_coverage(queue):
    calls = []
    def spy(name, function, **arguments):
        result = function(**arguments)
        calls.append((name, arguments.copy(), result))
        return result
    result = run_case('PRACTICE-APP-5002', queue, call=spy)
    application = calls[0][2]
    screened_ids = {arguments['party_id'] for name, arguments, _ in calls if name == 'screen_watchlist'}
    assert screened_ids == {p['party_id'] for p in application['parties']}
    policy_args = next(arguments for name, arguments, _ in calls if name == 'search_policy')
    assert policy_args['entity_type'] == application['entity_type']
    assert policy_args['jurisdiction'] == application['jurisdiction']
    assert next(value for name, _, value in calls if name == 'search_policy')[0]['id'] == 'POL-COMPANY-XA-v2'
    assert [name for name, _, _ in calls][-2:] == ['search_policy', 'open_review_case']
    assert result['status'] == 'COMPLIANCE_REVIEW'
    assert queue.count() == 1


def test_missing_data_does_not_hide_owner_match(queue):
    result = run_case('PRACTICE-APP-5006', queue)
    assert result['status'] == 'COMPLIANCE_REVIEW'
    assert set(result['reasons']) == {'POSSIBLE_MATCH', 'MISSING_DOCUMENT'}
    assert result['recommendation'] is None
    assert result['human_decision_required'] is True
    assert queue.count() == 1


@pytest.mark.parametrize('variant', ['changed', 'unknown'])
def test_unsupported_context_is_not_a_pass(queue, variant):
    result = run_case('PRACTICE-APP-5002', queue, context=variant)
    assert result['status'] == 'replay_missing'
    assert result['evaluated'] is False
    assert queue.count() == 0


def test_changed_fixture_bytes_cannot_reuse_replay(queue, tmp_path):
    copy = tmp_path / 'fixtures'
    shutil.copytree(DATA, copy)
    with (copy / 'applications.csv').open('a', encoding='utf-8') as stream:
        stream.write('\n')
    with pytest.raises(ValueError, match='fixture_changed:applications.csv'):
        run_case('PRACTICE-APP-5002', queue, root=copy)


def test_search_failure_is_bounded_and_still_reaches_human(queue):
    result = run_case('PRACTICE-APP-5002', queue, fault='search_unavailable')
    searches = [event for event in result['events'] if event['tool'] == 'search_policy']
    assert len(searches) == 2
    assert all(event['error'] == 'unavailable' for event in searches)
    assert 'POLICY_UNAVAILABLE' in result['reasons']
    assert queue.count() == 1
    assert result['recommendation'] is None


def test_lost_reply_after_commit_does_not_duplicate_on_retry(queue):
    args = dict(application_id='PRACTICE-APP-5002', reason='POSSIBLE_MATCH', request_id='one-operation', role='analyst', allowed_application='PRACTICE-APP-5002')
    with pytest.raises(TimeoutError, match='after commit'):
        queue.open(**args, fault='timeout_after_write')
    assert queue.count() == 1
    assert queue.open(**args)['status'] == 'pending_human_review'
    assert queue.count() == 1
    assert queue.open(**{**args, 'reason': 'different'})['error'] == 'idempotency_conflict'


def test_failure_before_write_and_denied_scope_leave_no_rows(queue):
    args = dict(application_id='PRACTICE-APP-5002', reason='POSSIBLE_MATCH', request_id='before-write', role='analyst', allowed_application='PRACTICE-APP-5002')
    assert queue.open(**args, fault='unavailable')['retryable'] is True
    assert queue.count() == 0
    assert queue.open(**{**args, 'allowed_application': 'PRACTICE-APP-5001'})['error'] == 'permission_denied'
    assert queue.count() == 0


def test_minimised_context_excludes_private_note_and_keeps_relationships():
    application = get_application('PRACTICE-APP-5002')
    shaped = shape_documents(application['documents'])
    assert all(set(row) == {'party_id', 'doc_type', 'document_date', 'expiry_date'} for row in shaped)
    assert {row['party_id'] for row in shaped} == {row['party_id'] for row in application['documents']}
    assert 'Invented private detail' not in json.dumps(shaped)


def test_compaction_keeps_unresolved_question():
    state = dict(application_id='PRACTICE-APP-5002', as_of='2026-11-05', reasons=['POSSIBLE_MATCH'], open_questions=['Owner: policy lead; screening age limit?'], history=['old message'] * 100)
    compacted = compact_state(state)
    assert compacted['open_questions'] == state['open_questions']
    assert compacted['reasons'] == ['POSSIBLE_MATCH']
    assert 'history' not in compacted


def test_policy_scope_date_and_future_version():
    assert [p['id'] for p in search_policy('review', 'COMPANY', 'XA', '2026-11-05')] == ['POL-COMPANY-XA-v2']
    assert [p['id'] for p in search_policy('review', 'COMPANY', 'XA', '2026-09-30')] == ['POL-COMPANY-XA-v1']
    assert search_policy('review', 'COMPANY', 'XX', '2026-11-05') == []
    assert profile()['parties_without_documents'] == ['PRACTICE-PARTY-31', 'PRACTICE-PARTY-61']
