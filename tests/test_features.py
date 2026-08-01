from __future__ import annotations

import numpy as np

from mindbalance.features import (
    build_model_vector,
    engineer_features,
    normalized_wellness_scores,
    physiological_index_scores,
    validate_input,
)
from mindbalance.schemas import AssessmentInput


def sample_input(**overrides) -> AssessmentInput:
    values = {
        "age": 24,
        "gender": "Female",
        "occupation": "Student",
        "sleep_hours": 7.0,
        "physical_activity": 3.5,
        "caffeine": 120,
        "alcohol": 0,
        "smoking": "No",
        "family_history": "No",
        "stress_level": 4,
        "heart_rate": 72,
        "breathing_rate": 16,
        "sweating_level": 2,
        "dizziness": "No",
        "medication": "No",
        "therapy_sessions": 0,
        "recent_life_event": "No",
        "diet_quality": 7,
    }
    values.update(overrides)
    return AssessmentInput(**values)


def test_engineered_features_are_bounded() -> None:
    engineered = engineer_features(sample_input())
    assert 0 <= engineered.sleep_efficiency <= 1
    assert 0 <= engineered.lifestyle_risk <= 1
    assert 0 <= engineered.anxiety_composite <= 1


def test_model_vector_contract() -> None:
    vector = build_model_vector(sample_input())
    assert vector.shape == (1, 21)
    assert vector.dtype == np.float32
    assert vector[0, 0] == 24
    assert vector[0, 1] == 1  # Female encoding
    assert vector[0, 2] == 11  # Student encoding


def test_high_stress_profile_has_higher_composite() -> None:
    low = engineer_features(sample_input(stress_level=2, heart_rate=65, breathing_rate=14, sweating_level=1))
    high = engineer_features(sample_input(stress_level=9, heart_rate=110, breathing_rate=28, sweating_level=5))
    assert high.anxiety_composite > low.anxiety_composite
    assert high.lifestyle_risk > low.lifestyle_risk


def test_validation_reports_training_range_issue() -> None:
    issues = validate_input(sample_input(heart_rate=150, breathing_rate=35))
    fields = {issue.field for issue in issues}
    assert "Heart Rate (bpm)" in fields
    assert "Breathing Rate (breaths/min)" in fields
    assert "Heart rate" in fields


def test_dashboard_index_scores_and_labels() -> None:
    data = sample_input()
    engineered = engineer_features(data)
    indexes = physiological_index_scores(engineered)
    wellness = normalized_wellness_scores(data, engineered)

    assert set(indexes) == {"Sleep restfulness", "Lifestyle strain", "Physical tension"}
    assert all(0 <= value <= 100 for value in indexes.values())
    assert list(wellness) == ["Sleep", "Activity", "Low Stress", "Body Calm", "Mind Balance", "Diet Quality"]
