"""Focused tests for decision-score routing and class-order safety."""

import unittest

import numpy as np

from src.routing_rules import AUTO_ROUTE, HUMAN_REVIEW, needs_human_review, route_from_scores


USE_DEFAULT_LABELS = object()


class RoutingRulesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.labels = ["class_a", "class_b", "class_c"]
        self.thresholds = {"min_top_score": 0.50, "min_score_margin": 0.20}

    def route(self, scores, labels=USE_DEFAULT_LABELS, **threshold_overrides):
        thresholds = self.thresholds | threshold_overrides
        return route_from_scores(
            self.labels if labels is USE_DEFAULT_LABELS else labels,
            scores,
            **thresholds,
        )

    def test_exact_threshold_boundaries_auto_route(self):
        result = self.route([0.30, 0.50, 0.10])

        self.assertEqual(result["routing_decision"], AUTO_ROUTE)
        self.assertEqual(result["predicted_label"], "class_b")
        self.assertAlmostEqual(result["top_score"], 0.50)
        self.assertAlmostEqual(result["score_margin"], 0.20)
        self.assertIsNone(result["review_reason"])

    def test_values_above_both_thresholds_auto_route(self):
        result = self.route([0.05, 0.80, 0.30])

        self.assertEqual(result["routing_decision"], AUTO_ROUTE)
        self.assertFalse(needs_human_review(result))

    def test_values_immediately_above_both_thresholds_auto_route(self):
        epsilon = 1e-9
        result = self.route([0.30, 0.50 + epsilon, 0.10])

        self.assertEqual(result["routing_decision"], AUTO_ROUTE)
        self.assertIsNone(result["review_reason"])

    def test_value_below_top_score_threshold_requires_review(self):
        result = self.route([0.49, 0.20, -0.10])

        self.assertEqual(result["routing_decision"], HUMAN_REVIEW)
        self.assertEqual(result["review_reason"], "low_top_score")

    def test_value_below_margin_threshold_requires_review(self):
        result = self.route([0.60, 0.41, -0.20])

        self.assertEqual(result["routing_decision"], HUMAN_REVIEW)
        self.assertEqual(result["review_reason"], "low_score_margin")

    def test_both_threshold_conditions_failing_returns_combined_reason(self):
        result = self.route([0.49, 0.40, -0.10])

        self.assertEqual(result["routing_decision"], HUMAN_REVIEW)
        self.assertEqual(
            result["review_reason"],
            "low_top_score_and_low_score_margin",
        )

    def test_tied_top_scores_require_review_even_at_zero_margin_threshold(self):
        result = self.route([0.60, 0.60, 0.10], min_score_margin=0.0)

        self.assertEqual(result["routing_decision"], HUMAN_REVIEW)
        self.assertEqual(result["review_reason"], "tied_top_scores")

    def test_negative_scores_can_route_with_locked_negative_thresholds(self):
        result = self.route(
            [-0.60, -0.20, -0.50],
            min_top_score=-0.20,
            min_score_margin=0.30,
        )

        self.assertEqual(result["routing_decision"], AUTO_ROUTE)
        self.assertEqual(result["predicted_label"], "class_b")

    def test_nan_and_infinite_scores_require_review(self):
        for scores in ([0.7, np.nan, 0.1], [0.7, np.inf, 0.1], [0.7, -np.inf, 0.1]):
            with self.subTest(scores=scores):
                result = self.route(scores)
                self.assertEqual(result["routing_decision"], HUMAN_REVIEW)
                self.assertEqual(result["review_reason"], "non_finite_scores")

    def test_malformed_score_arrays_require_review(self):
        malformed_inputs = ([], [0.8], [[0.8, 0.2, 0.1]], ["bad", 0.2, 0.1], None)
        for scores in malformed_inputs:
            with self.subTest(scores=scores):
                result = self.route(scores)
                self.assertEqual(result["routing_decision"], HUMAN_REVIEW)

    def test_class_label_and_score_count_mismatch_requires_review(self):
        result = self.route([0.80, 0.20])

        self.assertEqual(result["routing_decision"], HUMAN_REVIEW)
        self.assertEqual(result["review_reason"], "class_score_count_mismatch")

    def test_duplicate_or_invalid_class_labels_require_review(self):
        invalid_labels = (
            ["class_a", "class_a", "class_c"],
            ["class_a", "", "class_c"],
            None,
            "class_a",
        )
        for labels in invalid_labels:
            with self.subTest(labels=labels):
                result = self.route([0.80, 0.20, 0.10], labels=labels)
                self.assertEqual(result["routing_decision"], HUMAN_REVIEW)
                self.assertEqual(result["review_reason"], "invalid_class_labels")

    def test_class_order_controls_score_to_label_mapping(self):
        scores = np.array([0.10, 0.20, 0.90])
        result = self.route(scores, labels=["third", "first", "second"])

        self.assertEqual(result["predicted_label"], "second")
        self.assertEqual(result["top_score"], 0.90)
        self.assertEqual(result["second_score"], 0.20)

    def test_invalid_thresholds_raise_configuration_error(self):
        for invalid_threshold in (np.nan, np.inf, "0.5", None, True):
            with self.subTest(invalid_threshold=invalid_threshold):
                with self.assertRaises(ValueError):
                    self.route([0.80, 0.20, 0.10], min_top_score=invalid_threshold)


if __name__ == "__main__":
    unittest.main()
