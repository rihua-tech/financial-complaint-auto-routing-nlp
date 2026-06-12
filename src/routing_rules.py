"""Placeholder routing policy helpers for complaint auto-routing.

The functions in this module are intentionally lightweight. They do not assume
that a trained model exists, and they should be expanded after baseline model
outputs and confidence behavior are available.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


DEFAULT_ROUTING_POLICY = {
    "auto_route_min_confidence": 0.75,
    "auto_route_min_margin": 0.15,
}


def _prediction_margin(top_predictions: Sequence[Mapping[str, Any]] | None) -> float | None:
    """Return the confidence gap between the top two predictions, if available."""
    if not top_predictions or len(top_predictions) < 2:
        return None

    try:
        first = float(top_predictions[0]["confidence"])
        second = float(top_predictions[1]["confidence"])
    except (KeyError, TypeError, ValueError):
        return None

    return first - second


def route_prediction(
    predicted_label: str | None,
    confidence: float | None,
    top_predictions: Sequence[Mapping[str, Any]] | None = None,
    policy: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Return a routing decision for a future model prediction.

    This placeholder policy sends missing, low-confidence, or ambiguous
    predictions to human review. It can be replaced or extended after baseline
    model evaluation defines realistic thresholds.
    """
    active_policy = dict(DEFAULT_ROUTING_POLICY)
    if policy:
        active_policy.update(policy)

    if not predicted_label:
        return {
            "decision": "human_review",
            "reason": "missing_prediction",
            "predicted_label": None,
            "confidence": confidence,
        }

    if confidence is None:
        return {
            "decision": "human_review",
            "reason": "missing_confidence",
            "predicted_label": predicted_label,
            "confidence": confidence,
        }

    margin = _prediction_margin(top_predictions)
    if confidence < active_policy["auto_route_min_confidence"]:
        return {
            "decision": "human_review",
            "reason": "low_confidence",
            "predicted_label": predicted_label,
            "confidence": confidence,
            "margin": margin,
        }

    if margin is not None and margin < active_policy["auto_route_min_margin"]:
        return {
            "decision": "human_review",
            "reason": "ambiguous_top_predictions",
            "predicted_label": predicted_label,
            "confidence": confidence,
            "margin": margin,
        }

    return {
        "decision": "auto_route_candidate",
        "reason": "meets_placeholder_policy",
        "predicted_label": predicted_label,
        "confidence": confidence,
        "margin": margin,
    }


def needs_human_review(routing_decision: Mapping[str, Any]) -> bool:
    """Return True when a routing decision should remain in a review queue."""
    return routing_decision.get("decision") != "auto_route_candidate"
