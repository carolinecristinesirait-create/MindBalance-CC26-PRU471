from __future__ import annotations

import math

from mindbalance.model_engine import ModelBundle, predict_profile
from mindbalance.schemas import AssessmentInput


def sample_input(stress_level: int = 5) -> AssessmentInput:
    return AssessmentInput(
        age=30,
        gender="Male",
        occupation="Engineer",
        sleep_hours=6.5,
        physical_activity=2.0,
        caffeine=220,
        alcohol=2,
        smoking="No",
        family_history="No",
        stress_level=stress_level,
        heart_rate=84,
        breathing_rate=19,
        sweating_level=3,
        dizziness="No",
        medication="No",
        therapy_sessions=0,
        recent_life_event="No",
        diet_quality=6,
    )


def test_fallback_prediction_is_complete() -> None:
    result = predict_profile(sample_input(), ModelBundle(model=None, path=None, error="test"))
    assert result.level in {"Low", "Medium", "High"}
    assert set(result.probabilities) == {"Low", "Medium", "High"}
    assert math.isclose(sum(result.probabilities.values()), 1.0, rel_tol=1e-6)
    assert 1 <= result.predicted_score <= 10
    assert result.model_mode == "Transparent fallback"
    assert result.action_plan


def test_higher_stress_does_not_reduce_fallback_score() -> None:
    low = predict_profile(sample_input(stress_level=2), ModelBundle(None, None))
    high = predict_profile(sample_input(stress_level=9), ModelBundle(None, None))
    assert high.predicted_score >= low.predicted_score
