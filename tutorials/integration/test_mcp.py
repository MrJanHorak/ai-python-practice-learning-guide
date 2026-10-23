"""A real local stdio subprocess exchange; no external account required."""
import asyncio
import pytest

pytest.importorskip('mcp', reason='Install requirements-learning.txt for MCP integration checks')
from examples.learning_lab.mcp_client import exchange


pytestmark = pytest.mark.integration


def payload(response):
    import json
    return json.loads(next(block['text'] for block in response['content'] if block['type'] == 'text'))


def test_server_lists_exact_tools_and_validates_required_arguments():
    listed = asyncio.run(exchange())
    assert {tool['name'] for tool in listed['tools']} == {'get_application', 'screen_watchlist', 'search_policy', 'open_review_case'}
    schema = next(tool['inputSchema'] for tool in listed['tools'] if tool['name'] == 'search_policy')
    assert set(schema['required']) == {'query', 'entity_type', 'jurisdiction', 'as_of'}
    invalid = asyncio.run(exchange('search_policy', {'query': 'review'}))
    assert invalid['isError'] is True
    assert payload(asyncio.run(exchange('get_application', {'application_id': 'not-found'})))['error'] == 'not_found'


def test_permission_retry_and_restart_across_real_stdio(monkeypatch, tmp_path):
    import sqlite3
    path = tmp_path / 'stdio.sqlite3'
    monkeypatch.setenv('LEARNING_REVIEW_DB', str(path))
    monkeypatch.setenv('LEARNING_REVIEW_ROLE', 'reader')
    monkeypatch.delenv('LEARNING_REVIEW_APPLICATION', raising=False)
    args = {'application_id': 'PRACTICE-APP-5002', 'reason': 'POSSIBLE_MATCH', 'request_id': 'stdio-1'}
    assert payload(asyncio.run(exchange('open_review_case', args)))['error'] == 'permission_denied'
    monkeypatch.setenv('LEARNING_REVIEW_ROLE', 'analyst')
    monkeypatch.setenv('LEARNING_REVIEW_APPLICATION', args['application_id'])
    # Each exchange starts a new server; the database must survive restart.
    assert payload(asyncio.run(exchange('open_review_case', args)))['status'] == 'pending_human_review'
    assert payload(asyncio.run(exchange('open_review_case', args)))['request_id'] == args['request_id']
    with sqlite3.connect(path) as connection:
        assert connection.execute('SELECT COUNT(*) FROM reviews').fetchone()[0] == 1
