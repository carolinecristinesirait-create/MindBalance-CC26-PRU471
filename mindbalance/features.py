"""Feature engineering, validation, and model-vector construction."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from mindbalance.config import (
    BINARY_MAP,
    DATA_RANGES,
    FEATURE_ORDER,
    GENDER_MAP,
    OCCUPATION_MAP,
)
from mindbalance.schemas import AssessmentInput, EngineeredFeatures


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str
    severity: str = "warning"


def _bounded(value: float, lower: float, upper: float) -> float:
    return float(np.clip(value, lower, upper))


def _normalize(value: float, lower: float, upper: float) -> float:
    if upper <= lower:
        raise ValueError("Normalization upper bound must be greater than lower bound.")
    return _bounded((value - lower) / (upper - lower), 0.0, 1.0)


def validate_input(data: AssessmentInput) -> list[ValidationIssue]:
    """Return non-blocking domain and training-range warnings."""
    issues: list[ValidationIssue] = []

    checks = {
        "Age": data.age,
        "Sleep Hours": data.sleep_hours,
        "Physical Activity (hrs/week)": data.physical_activity,
        "Caffeine Intake (mg/day)": data.caffeine,
        "Alcohol Consumption (drinks/week)": data.alcohol,
        "Stress Level (1-10)": data.stress_level,
        "Heart Rate (bpm)": data.heart_rate,
        "Breathing Rate (breaths/min)": data.breathing_rate,
        "Sweating Level (1-5)": data.sweating_level,
        "Therapy Sessions (per month)": data.therapy_sessions,
        "Diet Quality (1-10)": data.diet_quality,
    }
    for field, value in checks.items():
        lower, upper = DATA_RANGES[field]
        if value < lower or value > upper:
            issues.append(
                ValidationIssue(
                    field=field,
                    message=(
                        f"Value {value} is outside the training-data range "
                        f"({lower} to {upper}). The estimate may be less reliable."
                    ),
                )
            )

    if data.sleep_hours < 4 and data.stress_level >= 8:
        issues.append(
            ValidationIssue(
                field="Sleep and stress",
                message="Very short sleep and high stress appear together in this profile.",
                severity="attention",
            )
        )
    if data.heart_rate >= 120:
        issues.append(
            ValidationIssue(
                field="Heart rate",
                message="A resting heart rate at or above 120 bpm is outside the model range.",
                severity="attention",
            )
        )
    if data.breathing_rate >= 30:
        issues.append(
            ValidationIssue(
                field="Breathing rate",
                message="A resting breathing rate at or above 30/min is outside the model range.",
                severity="attention",
            )
        )
    return issues


def engineer_features(data: AssessmentInput) -> EngineeredFeatures:
    """Reproduce the formulas used in the training notebook."""
    sleep_norm = _normalize(data.sleep_hours, 2.3, 11.3)
    caffeine_norm = _normalize(data.caffeine, 0, 599)
    sleep_efficiency = sleep_norm * 0.70 + (1.0 - caffeine_norm) * 0.30

    stress_norm = _normalize(data.stress_level, 1, 10)
    alcohol_norm = _normalize(data.alcohol, 0, 19)
    activity_norm = _normalize(data.physical_activity, 0, 10.1)
    diet_norm = _normalize(data.diet_quality, 1, 10)

    lifestyle_risk = (
        stress_norm * 0.25
        + BINARY_MAP[data.smoking] * 0.10
        + alcohol_norm * 0.10
        + BINARY_MAP[data.family_history] * 0.15
        + BINARY_MAP[data.recent_life_event] * 0.15
        + (1.0 - activity_norm) * 0.10
        + (1.0 - diet_norm) * 0.15
    )

    hr_norm = _normalize(data.heart_rate, 60, 119)
    br_norm = _normalize(data.breathing_rate, 12, 29)
    sweat_norm = _normalize(data.sweating_level, 1, 5)
    anxiety_composite = (
        stress_norm * 0.30
        + hr_norm * 0.20
        + br_norm * 0.20
        + sweat_norm * 0.15
        + BINARY_MAP[data.family_history] * 0.15
    )

    return EngineeredFeatures(
        sleep_efficiency=round(_bounded(sleep_efficiency, 0.0, 1.0), 4),
        lifestyle_risk=round(_bounded(lifestyle_risk, 0.0, 1.0), 4),
        anxiety_composite=round(_bounded(anxiety_composite, 0.0, 1.0), 4),
    )


def build_model_vector(data: AssessmentInput, engineered: EngineeredFeatures | None = None) -> np.ndarray:
    engineered = engineered or engineer_features(data)
    values = [
        data.age,
        GENDER_MAP[data.gender],
        OCCUPATION_MAP[data.occupation],
        data.sleep_hours,
        data.physical_activity,
        data.caffeine,
        data.alcohol,
        BINARY_MAP[data.smoking],
        BINARY_MAP[data.family_history],
        data.stress_level,
        data.heart_rate,
        data.breathing_rate,
        data.sweating_level,
        BINARY_MAP[data.dizziness],
        BINARY_MAP[data.medication],
        data.therapy_sessions,
        BINARY_MAP[data.recent_life_event],
        data.diet_quality,
        engineered.sleep_efficiency,
        engineered.lifestyle_risk,
        engineered.anxiety_composite,
    ]
    vector = np.asarray([values], dtype=np.float32)
    if vector.shape != (1, len(FEATURE_ORDER)):
        raise RuntimeError(f"Unexpected model vector shape: {vector.shape}")
    return vector


def normalized_wellness_scores(data: AssessmentInput, engineered: EngineeredFeatures) -> dict[str, int]:
    """Create presentation-friendly wellness dimensions for the radar chart."""
    stress_norm = _normalize(data.stress_level, 1, 10)
    hr_norm = _normalize(data.heart_rate, 60, 119)
    activity_norm = _normalize(data.physical_activity, 0, 10.1)
    scores = {
        "Sleep": engineered.sleep_efficiency,
        "Activity": activity_norm,
        "Low Stress": 1.0 - stress_norm,
        "Body Calm": 1.0 - hr_norm,
        "Mind Balance": 1.0 - engineered.lifestyle_risk,
        "Diet Quality": _normalize(data.diet_quality, 1, 10),
    }
    return {name: int(round(_bounded(value, 0.0, 1.0) * 100)) for name, value in scores.items()}


def physiological_index_scores(engineered: EngineeredFeatures) -> dict[str, int]:
    """Return the three headline index percentages used by the result dashboard.

    Sleep restfulness is a protective score, while lifestyle strain and physical
    tension are risk-oriented scores. All values are constrained to 0–100.
    """
    values = {
        "Sleep restfulness": engineered.sleep_efficiency,
        "Lifestyle strain": engineered.lifestyle_risk,
        "Physical tension": engineered.anxiety_composite,
    }
    return {name: int(round(_bounded(value, 0.0, 1.0) * 100)) for name, value in values.items()}
