"""Placeholder prediction interface for complaint product classification.

This module defines the expected shape of future prediction code without
assuming that a trained model artifact already exists.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any


def load_model_artifacts(model_path: str | Path | None = None) -> Mapping[str, Any]:
    """Load future model artifacts.

    Raises:
        FileNotFoundError: Always raised until a baseline model artifact exists.
    """
    path_label = str(model_path) if model_path else "models/"
    raise FileNotFoundError(
        f"No trained model artifact is available at {path_label}. "
        "Train and evaluate a baseline model before enabling prediction."
    )


def predict_product_category(
    complaint_text: str,
    model_artifacts: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a placeholder prediction response for a complaint narrative.

    The function validates input text but does not run inference until future
    model artifacts are supplied and this function is implemented.
    """
    if not complaint_text or not complaint_text.strip():
        return {
            "status": "human_review_required",
            "reason": "missing_complaint_text",
            "predicted_label": None,
            "confidence": None,
            "top_predictions": [],
        }

    if model_artifacts is None:
        return {
            "status": "pending_model_artifacts",
            "reason": "baseline_model_not_trained",
            "predicted_label": None,
            "confidence": None,
            "top_predictions": [],
        }

    return {
        "status": "not_implemented",
        "reason": "prediction_logic_pending",
        "predicted_label": None,
        "confidence": None,
        "top_predictions": [],
    }
