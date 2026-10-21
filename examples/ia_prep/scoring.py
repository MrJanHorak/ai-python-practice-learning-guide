"""The bounded-score example used in the Python cheat sheet."""
from dataclasses import dataclass


@dataclass
class Customer:
    name: str
    risk_score: float = 0.0
    docs: list[str] | None = None


def score(customer: Customer, threshold: float = 0.7) -> str:
    if not 0 <= customer.risk_score <= 1 or not 0 <= threshold <= 1:
        raise ValueError("Scores and thresholds must be between 0 and 1")
    return "review" if customer.risk_score >= threshold else "clear"
