import pytest

from examples.ai_systems.scoring import Customer, score


def test_high_score_requires_review():
    customer = Customer("SIM Example", 0.9)  # Arrange
    outcome = score(customer)               # Act
    assert outcome == "review"              # Assert


@pytest.mark.parametrize("risk,expected", [(0.0, "clear"), (0.69, "clear"),
    (0.7, "review"), (1.0, "review")], ids=["zero", "below", "boundary", "maximum"])
def test_threshold(risk, expected):
    assert score(Customer("SIM Example", risk)) == expected


@pytest.mark.parametrize("risk", [-0.1, 1.1, float("nan")])
def test_invalid_scores_raise(risk):
    with pytest.raises(ValueError, match="between 0 and 1"):
        score(Customer("SIM Example", risk))
