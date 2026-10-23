import pytest
from examples.learning_lab.costs import summarize


def test_case_cost_counts_every_call_including_retry():
    events = [dict(case_id='A', input_tokens=1200, output_tokens=100, retry=False), dict(case_id='A', input_tokens=100, output_tokens=20, retry=True), dict(case_id='A', input_tokens=800, output_tokens=50, retry=False), dict(case_id='B', input_tokens=900, output_tokens=80, retry=False)]
    report = summarize(events)
    assert report['by_case']['A'] == pytest.approx(0.00556)
    assert report['by_case']['B'] == pytest.approx(0.00244)
    assert report['total'] == pytest.approx(0.008)
    assert report['mean_per_case'] == pytest.approx(0.004)
    assert report['retry_call_fraction'] == 0.25
    assert summarize([])['mean_per_case'] is None
