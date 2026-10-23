"""Read configuration and reject assumptions about its meaning."""
from pathlib import Path
import pytest

yaml = pytest.importorskip('yaml', reason='Install requirements-learning.txt for YAML exercises')


def test_yaml_types_are_not_all_strings():
    root = Path(__file__).resolve().parents[2]
    settings = yaml.safe_load((root / 'data/linked_review/context.yaml').read_text(encoding='utf-8'))
    assert settings['context']['include_current_state'] is True
    assert settings['context']['history_limit'] == 2
    assert settings['fault'] == 'search_policy:unavailable'
