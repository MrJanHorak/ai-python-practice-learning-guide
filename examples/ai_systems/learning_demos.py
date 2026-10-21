"""Offline metric arithmetic; scores are authored examples, not model predictions."""
import argparse
import csv
import json
import math

from .core import DATA


def classification_metrics(rows, threshold=0.5):
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("Threshold must be finite and between zero and one")
    counts = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for row in rows:
        label, score = int(row["label"]), float(row["score"])
        if label not in (0, 1) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("Use binary labels and finite scores between zero and one")
        prediction = score >= threshold
        key = "tp" if label and prediction else "fn" if label else "fp" if prediction else "tn"
        counts[key] += 1
    total = sum(counts.values())
    def ratio(numerator, denominator):
        return numerator / denominator if denominator else None
    return {**counts, "total": total, "threshold": threshold,
            "precision": ratio(counts["tp"], counts["tp"] + counts["fp"]),
            "recall": ratio(counts["tp"], counts["tp"] + counts["fn"]),
            "accuracy": ratio(counts["tp"] + counts["tn"], total)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["metrics"])
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()
    with (DATA / "classification_scores.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    baseline = [{**row, "score": 0} for row in rows]
    print(json.dumps({"kind": "authored_scores_no_trained_model",
                      "selected_threshold": classification_metrics(rows, args.threshold),
                      "always_negative_baseline": classification_metrics(baseline)}, indent=2))


if __name__ == "__main__":
    main()
