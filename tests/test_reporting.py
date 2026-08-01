from __future__ import annotations

from mindbalance.model_engine import ModelBundle, predict_profile
from mindbalance.reporting import result_html, result_json
from mindbalance.schemas import AssessmentInput


def test_reports_are_serializable() -> None:
    data = AssessmentInput(
        age=26,
        gender="Female",
        occupation="Student",
        sleep_hours=7.0,
        physical_activity=3.5,
        caffeine=100,
        alcohol=0,
        smoking="No",
        family_history="No",
        stress_level=4,
        heart_rate=72,
        breathing_rate=16,
        sweating_level=2,
        dizziness="No",
        medication="No",
        therapy_sessions=0,
        recent_life_event="No",
        diet_quality=7,
    )
    result = predict_profile(data, ModelBundle(None, None))
    assert '"level"' in result_json(result)
    html = result_html(result)
    assert "MindBalance Assessment Report" in html
    assert "not a diagnosis" in html
