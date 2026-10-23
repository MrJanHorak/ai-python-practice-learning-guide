"""Create the independent, entirely fictional linked-record learning dataset."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'linked_review'


def generate(destination=OUT):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    applications, parties, documents, screening = [], [], [], []
    for number in range(1, 7):
        application = f'PRACTICE-APP-{5000 + number}'
        applications.append(dict(application_id=application, entity_type='COMPANY', jurisdiction='XA', as_of='2026-11-05'))
        for offset, role in enumerate(['company', 'director', 'beneficial_owner']):
            party = f'PRACTICE-PARTY-{number}{offset}'
            parties.append(dict(party_id=party, application_id=application, role=role, display_name=f'Invented party {number}-{offset}'))
            screening.append(dict(party_id=party, result=('possible_match' if number in (2, 6) and offset == 2 else 'unavailable' if number == 4 and offset == 1 else 'clear'), screened_on='2026-11-04', list_version='fictional-v1'))
            if not (number in (3, 6) and offset == 1):
                documents.append(dict(document_id=f'PRACTICE-DOC-{number}{offset}', party_id=party, doc_type='registration' if offset == 0 else 'identity', document_date='2025-01-01', expiry_date='2026-01-01' if number == 5 and offset == 1 else '2027-01-01', private_note='Invented private detail: exclude from context and logs'))
    policies = [
        dict(id='POL-COMPANY-XA-v1', entity_type='COMPANY', jurisdiction='XA', effective_from='2025-01-01', effective_to='2026-10-01', content='Review possible matches with a human. Superseded practice policy.'),
        dict(id='POL-COMPANY-XA-v2', entity_type='COMPANY', jurisdiction='XA', effective_from='2026-10-01', effective_to='2099-01-01', content='Review every possible match, including beneficial owners, with a human.'),
        dict(id='POL-PERSON-XA-v1', entity_type='PERSON', jurisdiction='XA', effective_from='2025-01-01', effective_to='2099-01-01', content='Review a personal application with a human.'),
        dict(id='POL-COMPANY-XB-v1', entity_type='COMPANY', jurisdiction='XB', effective_from='2025-01-01', effective_to='2099-01-01', content='Review a company under the fictional XB rules.'),
        dict(id='POL-COMPANY-XA-future', entity_type='COMPANY', jurisdiction='XA', effective_from='2027-01-01', effective_to='2099-01-01', content='Review under a future policy. Not yet in force.'),
    ]
    tables = {'applications': applications, 'parties': parties, 'documents': documents, 'screening': screening}
    for name, rows in tables.items():
        with (destination / f'{name}.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    def write_json(name, value):
        (destination / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    write_json('policies.json', policies)
    # Expectations are authored from the exercise specification, not the runner.
    statuses = ['NO_FLAGS', 'COMPLIANCE_REVIEW', 'MISSING_DATA', 'SCREENING_UNAVAILABLE', 'FLAGGED', 'COMPLIANCE_REVIEW']
    write_json('expected_outcomes.json', [dict(application_id=row['application_id'], status=status, review_count=int(index in (1, 5)), pending=index in (2, 3), split='holdout' if index == 5 else 'practice') for index, (row, status) in enumerate(zip(applications, statuses))])
    write_json('recordings.json', {row['application_id']: dict(origin='authored-script-not-a-live-model', model='none', input_tokens=100 + index * 20, output_tokens=30, text='A person must decide; this exercise makes no application decision.') for index, row in enumerate(applications)})
    manifest = {path.name: dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(), rows=len(tables[path.stem]) if path.stem in tables else None) for path in sorted(destination.iterdir()) if path.suffix in ('.csv', '.json') and path.name != 'manifest.json'}
    write_json('manifest.json', manifest)
    print(f'Wrote fictional fixtures to {destination}')


if __name__ == '__main__':
    generate()
