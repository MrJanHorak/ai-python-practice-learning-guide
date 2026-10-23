"""Run from the repository root: python -m examples.learning_lab --help."""
import argparse
import json
from pathlib import Path
from .core import DATA, ReviewQueue, digest, get_application, profile, read_json, run_case, search_policy, shape_documents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['profile', 'context', 'run', 'eval'])
    parser.add_argument('--case', default='PRACTICE-APP-5002')
    parser.add_argument('--context', default='current')
    parser.add_argument('--fault', choices=['search_unavailable'])
    parser.add_argument('--split', choices=['practice', 'holdout'], default='practice')
    args = parser.parse_args()
    if args.command == 'profile':
        print(json.dumps(profile(), indent=2))
        return
    if args.command == 'context':
        application = get_application(args.case)
        if 'error' in application:
            parser.error('Unknown application ID')
        print(json.dumps({'documents': shape_documents(application['documents']), 'policies': search_policy('review', application['entity_type'], application['jurisdiction'], application['as_of'])}, indent=2))
        return
    cases = [r for r in read_json('expected_outcomes.json') if r['split'] == args.split] if args.command == 'eval' else [{'application_id': args.case}]
    for expected in cases:
        queue = ReviewQueue(':memory:')
        try:
            result = run_case(expected['application_id'], queue, context=args.context, fault=args.fault)
            event = dict(correlation_id=expected['application_id'] + ':demo', mode='authored_replay', dataset_hash=digest(read_json('manifest.json')), suite_hash=digest(read_json('expected_outcomes.json')), build_hash=digest({'core': Path(__file__).with_name('core.py').read_text(encoding='utf-8'), 'cli': Path(__file__).read_text(encoding='utf-8')}), context=args.context, fault=args.fault, result=result, review_count=queue.count())
            if args.command == 'eval':
                event['passed'] = result['evaluated'] and all(result[key] == expected[key] for key in ('status', 'pending')) and queue.count() == expected['review_count']
            print(json.dumps(event))
        finally:
            queue.close()


if __name__ == '__main__':
    main()
