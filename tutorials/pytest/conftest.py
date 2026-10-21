"""Shared fixtures for the optional pytest tutorials only."""
import copy
import pytest

from examples.ai_systems import providers
from examples.ai_systems.core import DATA, ReviewStore, read_json


@pytest.fixture
def review_store(tmp_path):
    store = ReviewStore(tmp_path / "reviews.sqlite3")
    yield store
    store.close()


@pytest.fixture
def extraction():
    return copy.deepcopy(read_json(DATA / "extraction_fixtures.json")[0])


@pytest.fixture(autouse=True)
def no_real_model_network(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("Tutorial tests must not call a real model endpoint")
    monkeypatch.setattr(providers, "urlopen", blocked)
