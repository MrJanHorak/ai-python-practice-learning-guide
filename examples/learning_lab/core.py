"""Small observable tools and a constructed replay for beginner experiments."""
import csv
import hashlib
import json
import sqlite3
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / 'data' / 'linked_review'


def rows(name, root=DATA):
    with (root / f'{name}.csv').open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def read_json(name, root=DATA):
    return json.loads((root / name).read_text(encoding='utf-8'))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def verify_manifest(root=DATA):
    """A recording is only meaningful for its documented fixture bytes."""
    for name, entry in read_json('manifest.json', root).items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError(f'fixture_changed:{name}; this replay no longer matches')


def get_application(application_id, root=DATA):
    application = next((r for r in rows('applications', root) if r['application_id'] == application_id), None)
    if application is None:
        return {'error': 'not_found', 'retryable': False}
    parties = [r for r in rows('parties', root) if r['application_id'] == application_id]
    ids = {p['party_id'] for p in parties}
    return {**application, 'parties': parties, 'documents': [r for r in rows('documents', root) if r['party_id'] in ids]}


def screen_watchlist(party_id, root=DATA):
    result = next((r for r in rows('screening', root) if r['party_id'] == party_id), None)
    if result is None or result['result'] == 'unavailable':
        return {'error': 'unavailable', 'retryable': True}
    return {'result': result['result']}


def search_policy(query, entity_type, jurisdiction, as_of, root=DATA):
    date.fromisoformat(as_of)
    return [p for p in read_json('policies.json', root)
            if p['entity_type'] == entity_type and p['jurisdiction'] == jurisdiction
            and p['effective_from'] <= as_of < p['effective_to']
            and any(word in p['content'].lower() for word in query.lower().split())]


def shape_documents(documents):
    keys = ('party_id', 'doc_type', 'document_date', 'expiry_date')
    return [{key: document[key] for key in keys} for document in documents]


def compact_state(state):
    """Keep unresolved work even when chat history is dropped."""
    keys = ('application_id', 'as_of', 'reasons', 'open_questions')
    return {key: state[key] for key in keys}


class ReviewQueue:
    """Persistent, scoped demo writes; caller identity is not authenticated here."""
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute('CREATE TABLE IF NOT EXISTS reviews (request_id TEXT PRIMARY KEY, application_id TEXT NOT NULL, reason TEXT NOT NULL)')
        self.connection.commit()

    def close(self):
        self.connection.close()

    def count(self):
        return self.connection.execute('SELECT COUNT(*) FROM reviews').fetchone()[0]

    def open(self, application_id, reason, request_id, *, role='reader', allowed_application=None, fault=None):
        if role != 'analyst' or allowed_application != application_id:
            return {'error': 'permission_denied', 'retryable': False}
        if not request_id or not reason:
            return {'error': 'invalid_input', 'retryable': False}
        # unavailable means no work occurred; timeout below means reply lost AFTER commit.
        if fault == 'unavailable':
            return {'error': 'unavailable', 'retryable': True}
        with self.connection:
            self.connection.execute('INSERT OR IGNORE INTO reviews VALUES (?, ?, ?)', (request_id, application_id, reason))
            saved = self.connection.execute('SELECT application_id, reason FROM reviews WHERE request_id = ?', (request_id,)).fetchone()
            if saved != (application_id, reason):
                return {'error': 'idempotency_conflict', 'retryable': False}
        if fault == 'timeout_after_write':
            raise TimeoutError('Reply lost after commit; retry with the SAME request_id')
        return {'request_id': request_id, 'status': 'pending_human_review'}


def profile(root=DATA):
    apps, parties, documents = rows('applications', root), rows('parties', root), rows('documents', root)
    app_ids, party_ids = {a['application_id'] for a in apps}, {p['party_id'] for p in parties}
    return dict(applications=len(apps), parties=len(parties), documents=len(documents), orphan_parties=[p['party_id'] for p in parties if p['application_id'] not in app_ids], orphan_documents=[d['document_id'] for d in documents if d['party_id'] not in party_ids], parties_without_documents=sorted(party_ids - {d['party_id'] for d in documents}))


def run_case(application_id, queue, *, context='current', fault=None, call=None, root=DATA):
    """A fixed trajectory, NOT a model selecting actions or a course replay engine."""
    verify_manifest(root)
    recordings = read_json('recordings.json', root)
    if application_id not in recordings or context != 'current' or fault not in (None, 'search_unavailable'):
        return {'status': 'replay_missing', 'evaluated': False, 'reason': 'No authored script for this input/context/fault combination'}
    events = []
    def execute(name, function, **arguments):
        result = function(**arguments)
        # This trace records names/counts, never returned records or free text.
        events.append({'event': 'tool_call', 'tool': name, 'error': result.get('error') if isinstance(result, dict) else None})
        return result
    invoke = call or execute
    application = invoke('get_application', lambda **kw: get_application(root=root, **kw), application_id=application_id)
    if 'error' in application:
        return {'status': 'MISSING_DATA', 'pending': True, 'evaluated': True, 'events': events}
    reasons = []
    screening_missing = False
    for party in application['parties']:
        result = invoke('screen_watchlist', lambda **kw: screen_watchlist(root=root, **kw), party_id=party['party_id'])
        if result.get('error'):
            screening_missing = True
            reasons.append('SCREENING_UNAVAILABLE')
        elif result['result'] == 'possible_match':
            reasons.append('POSSIBLE_MATCH')
    document_party_ids = {d['party_id'] for d in application['documents']}
    if any(p['party_id'] not in document_party_ids for p in application['parties']):
        reasons.append('MISSING_DOCUMENT')
    if any(d['expiry_date'] < application['as_of'] for d in application['documents']):
        reasons.append('EXPIRED_DOCUMENT')
    if 'POSSIBLE_MATCH' in reasons:
        # One retry after the initial failure; every attempt remains observable.
        for _ in range(2):
            policies = invoke('search_policy', lambda **kw: {'error': 'unavailable', 'retryable': True} if fault else search_policy(root=root, **kw), query='review', entity_type=application['entity_type'], jurisdiction=application['jurisdiction'], as_of=application['as_of'])
            if not isinstance(policies, dict) or not policies.get('retryable'):
                break
        if isinstance(policies, dict):
            reasons.append('POLICY_UNAVAILABLE')
        saved = invoke('open_review_case', lambda **kw: queue.open(role='analyst', allowed_application=application_id, **kw), application_id=application_id, reason='POSSIBLE_MATCH', request_id=f'{application_id}:possible-match:v1')
        if 'error' in saved:
            reasons.append('REVIEW_WRITE_FAILED')
    # All reasons survive precedence. These are teaching rules, not legal advice.
    status = ('COMPLIANCE_REVIEW' if 'POSSIBLE_MATCH' in reasons else
              'SCREENING_UNAVAILABLE' if screening_missing else
              'MISSING_DATA' if 'MISSING_DOCUMENT' in reasons else
              'FLAGGED' if reasons else 'NO_FLAGS')
    record = recordings[application_id]
    return dict(status=status, pending=status in ('SCREENING_UNAVAILABLE', 'MISSING_DATA'), evaluated=True, reasons=reasons, recommendation=None, human_decision_required=True, events=events, usage={k: record[k] for k in ('input_tokens', 'output_tokens')}, origin=record['origin'], text=record['text'])


def token_cost(input_tokens, output_tokens, input_rate, output_rate):
    """Rates are currency units per million tokens, separately for input/output."""
    return (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000
