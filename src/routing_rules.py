"""Decision-score routing rules for the locked Linear SVM baseline.

Linear SVM decision scores and score margins are model signals, not
probabilities. Threshold values must be selected outside this module and passed
explicitly so that exploratory or placeholder values cannot silently become a
routing policy.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Any

import numpy as np


AUTO_ROUTE = "auto_route"
HUMAN_REVIEW = "human_review"


def _review_decision(reason: str) -> dict[str, Any]:
    """Return a consistent human-review response for unusable score input."""
    return {
        "routing_decision": HUMAN_REVIEW,
        "review_reason": reason,
        "predicted_label": None,
        "top_score": None,
        "second_score": None,
        "score_margin": None,
    }


def _valid_threshold(value: object) -> bool:
    """Return whether a routing threshold is a finite real number."""
    return (
        isinstance(value, Real)
        and not isinstance(value, bool)
        and np.isfinite(value)
    )


def route_from_scores(
    class_labels: Sequence[str] | None,
    decision_scores: Sequence[float] | np.ndarray | None,
    *,
    min_top_score: float,
    min_score_margin: float,
) -> dict[str, Any]:
    """Return an automatic-routing or human-review decision.

    The score array must be a one-dimensional score vector aligned with the
    fitted pipeline's ``classes_`` order. Both locked thresholds are inclusive:
    a row is an automatic-route candidate when ``top_score >= min_top_score``
    and ``score_margin >= min_score_margin``. Tied or invalid scores always go
    to human review.
    """
    if not _valid_threshold(min_top_score) or not _valid_threshold(min_score_margin):
        raise ValueError("Routing thresholds must be finite real numbers.")

    if class_labels is None or isinstance(class_labels, (str, bytes)):
        return _review_decision("invalid_class_labels")
    if decision_scores is None:
        return _review_decision("invalid_scores")

    try:
        labels = list(class_labels)
    except TypeError:
        return _review_decision("invalid_class_labels")

    if len(labels) < 2 or any(not isinstance(label, str) or not label for label in labels):
        return _review_decision("invalid_class_labels")
    if len(set(labels)) != len(labels):
        return _review_decision("invalid_class_labels")

    try:
        scores = np.asarray(decision_scores, dtype=float)
    except (TypeError, ValueError):
        return _review_decision("invalid_scores")

    if scores.ndim != 1 or scores.size < 2:
        return _review_decision("malformed_score_array")
    if scores.size != len(labels):
        return _review_decision("class_score_count_mismatch")
    if not np.isfinite(scores).all():
        return _review_decision("non_finite_scores")

    descending_indices = np.argsort(scores, kind="stable")[::-1]
    top_index = int(descending_indices[0])
    second_index = int(descending_indices[1])
    top_score = float(scores[top_index])
    second_score = float(scores[second_index])
    score_margin = top_score - second_score
    predicted_label = labels[top_index]

    result = {
        "routing_decision": HUMAN_REVIEW,
        "review_reason": None,
        "predicted_label": predicted_label,
        "top_score": top_score,
        "second_score": second_score,
        "score_margin": score_margin,
    }

    low_top_score = top_score < min_top_score
    low_score_margin = score_margin < min_score_margin

    if score_margin == 0.0:
        result["review_reason"] = "tied_top_scores"
    elif low_top_score and low_score_margin:
        result["review_reason"] = "low_top_score_and_low_score_margin"
    elif low_top_score:
        result["review_reason"] = "low_top_score"
    elif low_score_margin:
        result["review_reason"] = "low_score_margin"
    else:
        result["routing_decision"] = AUTO_ROUTE
        result["review_reason"] = None

    return result


def needs_human_review(routing_decision: Mapping[str, Any]) -> bool:
    """Return whether a routing result belongs in the human-review queue."""
    return routing_decision.get("routing_decision") != AUTO_ROUTE
