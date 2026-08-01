"""Model loading and robust multi-output inference."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from mindbalance.config import CLASS_ORDER
from mindbalance.features import build_model_vector, engineer_features
from mindbalance.recommendations import build_profile_explanations
from mindbalance.schemas import AssessmentInput, PredictionResult

LOGGER = logging.getLogger(__name__)


@dataclass
class ModelBundle:
    model: Any | None
    path: Path | None
    error: str | None = None

    @property
    def available(self) -> bool:
        return self.model is not None


def load_keras_model(paths: tuple[Path, ...]) -> ModelBundle:
    """Load the first usable Keras model while keeping imports lazy."""
    try:
        import tensorflow as tf  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on runtime environment
        return ModelBundle(None, None, f"TensorFlow unavailable: {exc}")

    errors: list[str] = []
    for path in paths:
        if not path.exists():
            errors.append(f"Missing: {path.name}")
            continue
        try:
            model = tf.keras.models.load_model(str(path), compile=False, safe_mode=True)
            return ModelBundle(model=model, path=path)
        except TypeError:
            # Older TF/Keras versions may not expose safe_mode.
            try:
                model = tf.keras.models.load_model(str(path), compile=False)
                return ModelBundle(model=model, path=path)
            except Exception as exc:  # pragma: no cover
                errors.append(f"{path.name}: {exc}")
        except Exception as exc:  # pragma: no cover
            errors.append(f"{path.name}: {exc}")
    return ModelBundle(None, None, "; ".join(errors) or "No model paths were provided.")


def _to_numpy(value: Any) -> np.ndarray:
    if hasattr(value, "numpy"):
        value = value.numpy()
    return np.asarray(value)


def _extract_outputs(raw: Any) -> tuple[np.ndarray, float | None]:
    """Identify classification and regression heads by final dimension."""
    values: list[Any]
    if isinstance(raw, dict):
        values = list(raw.values())
    elif isinstance(raw, (list, tuple)):
        values = list(raw)
    else:
        values = [raw]

    class_probs: np.ndarray | None = None
    reg_score: float | None = None
    for value in values:
        arr = _to_numpy(value)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.ndim >= 2 and arr.shape[-1] == 3:
            class_probs = np.asarray(arr[0], dtype=float)
        elif arr.size >= 1 and arr.shape[-1] == 1:
            reg_score = float(arr.reshape(-1)[0])

    if class_probs is None:
        raise ValueError("The model did not return a 3-class probability output.")
    if not np.all(np.isfinite(class_probs)):
        raise ValueError("The model returned non-finite probabilities.")

    total = float(class_probs.sum())
    if total <= 0:
        raise ValueError("The model returned invalid probability mass.")
    class_probs = np.clip(class_probs / total, 0.0, 1.0)
    return class_probs, reg_score


def _heuristic_probabilities(composite: float, stress: int) -> np.ndarray:
    """Transparent fallback used only when TensorFlow/model loading fails."""
    signal = float(np.clip(0.75 * composite + 0.25 * ((stress - 1) / 9), 0.0, 1.0))
    centers = np.asarray([0.18, 0.50, 0.82])
    logits = -((signal - centers) ** 2) / 0.035
    logits -= logits.max()
    probs = np.exp(logits)
    return probs / probs.sum()


def _confidence_label(confidence: float) -> str:
    if confidence >= 0.80:
        return "Strong separation"
    if confidence >= 0.60:
        return "Moderate separation"
    return "Close call"


def predict_profile(data: AssessmentInput, bundle: ModelBundle) -> PredictionResult:
    engineered = engineer_features(data)
    vector = build_model_vector(data, engineered)

    model_mode = "TensorFlow model"
    regression_norm: float | None = None
    if bundle.available:
        try:
            raw = bundle.model(vector, training=False)
            probabilities, regression_norm = _extract_outputs(raw)
        except Exception as exc:  # pragma: no cover - runtime-specific
            LOGGER.exception("Model inference failed; using fallback.")
            probabilities = _heuristic_probabilities(engineered.anxiety_composite, data.stress_level)
            model_mode = f"Transparent fallback ({type(exc).__name__})"
    else:
        probabilities = _heuristic_probabilities(engineered.anxiety_composite, data.stress_level)
        model_mode = "Transparent fallback"

    index = int(np.argmax(probabilities))
    level = CLASS_ORDER[index]
    confidence = float(probabilities[index])
    if regression_norm is None or not np.isfinite(regression_norm):
        predicted_score = 1.0 + 9.0 * engineered.anxiety_composite
    else:
        predicted_score = 1.0 + 9.0 * float(np.clip(regression_norm, 0.0, 1.0))

    strengths, focus, actions = build_profile_explanations(data, engineered)
    return PredictionResult(
        level=level,
        probabilities={name: float(probabilities[i]) for i, name in enumerate(CLASS_ORDER)},
        predicted_score=round(float(np.clip(predicted_score, 1.0, 10.0)), 2),
        confidence=round(confidence, 4),
        confidence_label=_confidence_label(confidence),
        model_mode=model_mode,
        engineered=engineered,
        input_data=data,
        strengths=strengths,
        focus_areas=focus,
        action_plan=actions,
    )
