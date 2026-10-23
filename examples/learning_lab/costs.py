"""Arithmetic on authored usage, using invented prices; no billing API."""
import json
from .core import DATA, token_cost


def summarize(events, input_rate=2, output_rate=8):
    by_case = {}
    for event in events:
        cost = token_cost(event['input_tokens'], event['output_tokens'], input_rate, output_rate)
        by_case[event['case_id']] = by_case.get(event['case_id'], 0) + cost
    total = sum(by_case.values())
    return {'origin': 'invented_usage_and_prices', 'calls': len(events), 'cases': len(by_case), 'by_case': by_case, 'total': total, 'mean_per_case': total / len(by_case) if by_case else None, 'retry_call_fraction': sum(bool(e['retry']) for e in events) / len(events) if events else None}


if __name__ == '__main__':
    events = [json.loads(line) for line in (DATA / 'usage_sample.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    print(json.dumps(summarize(events), indent=2))
