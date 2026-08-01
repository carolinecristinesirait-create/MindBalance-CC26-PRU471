"""Typed domain objects used across the application."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class AssessmentInput:
    age: int
    gender: str
    occupation: str
    sleep_hours: float
    physical_activity: float
    caffeine: int
    alcohol: int
    smoking: str
    family_history: str
    stress_level: int
    heart_rate: int
    breathing_rate: int
    sweating_level: int
    dizziness: str
    medication: str
    therapy_sessions: int
    recent_life_event: str
    diet_quality: int

    def to_public_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EngineeredFeatures:
    sleep_efficiency: float
    lifestyle_risk: float
    anxiety_composite: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


@dataclass
class PredictionResult:
    level: str
    probabilities: dict[str, float]
    predicted_score: float
    confidence: float
    confidence_label: str
    model_mode: str
    engineered: EngineeredFeatures
    input_data: AssessmentInput
    strengths: list[dict[str, str]] = field(default_factory=list)
    focus_areas: list[dict[str, str]] = field(default_factory=list)
    action_plan: list[dict[str, str]] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["engineered"] = self.engineered.to_dict()
        payload["input_data"] = self.input_data.to_public_dict()
        return payload
