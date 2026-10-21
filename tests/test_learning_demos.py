import csv
import unittest

from examples.ai_systems.core import DATA
from examples.ai_systems.learning_demos import classification_metrics


class MetricsTests(unittest.TestCase):
    def setUp(self):
        with (DATA / "classification_scores.csv").open(encoding="utf-8", newline="") as stream:
            self.rows = list(csv.DictReader(stream))

    def test_rare_event_accuracy_can_hide_all_missed_positives(self):
        baseline = classification_metrics([{**r, "score": 0} for r in self.rows])
        self.assertEqual(baseline["accuracy"], 0.9)
        self.assertEqual(baseline["recall"], 0)
        self.assertIsNone(baseline["precision"])

    def test_threshold_tradeoff_matches_authored_example(self):
        middle = classification_metrics(self.rows, 0.5)
        self.assertEqual([middle[k] for k in ("tp", "fp", "fn", "tn")], [1, 3, 1, 15])
        self.assertEqual(middle["precision"], 0.25)
        self.assertEqual(classification_metrics(self.rows, 0.35)["recall"], 1)
        self.assertEqual(classification_metrics(self.rows, 0.85)["precision"], 1)

    def test_empty_and_invalid_scores_do_not_report_perfect_quality(self):
        self.assertIsNone(classification_metrics([])["accuracy"])
        with self.assertRaises(ValueError):
            classification_metrics([{"label": 1, "score": float("nan")}])


if __name__ == "__main__":
    unittest.main()
