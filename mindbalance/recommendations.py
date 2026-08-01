"""Deterministic, explainable wellness guidance from assessment inputs."""
from __future__ import annotations

from mindbalance.schemas import AssessmentInput, EngineeredFeatures


def _item(title: str, detail: str, icon: str, priority: int = 0) -> dict[str, str | int]:
    return {"title": title, "detail": detail, "icon": icon, "priority": priority}


def build_profile_explanations(
    data: AssessmentInput,
    engineered: EngineeredFeatures,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    strengths: list[dict[str, str | int]] = []
    focus: list[dict[str, str | int]] = []

    if data.sleep_hours >= 7:
        strengths.append(_item("Sleep foundation", f"{data.sleep_hours:.1f} hours of sleep supports recovery.", "moon-stars"))
    elif data.sleep_hours < 6:
        focus.append(_item("Sleep duration", f"Current sleep is {data.sleep_hours:.1f} hours per night.", "moon-stars", 8))

    if data.physical_activity >= 3.5:
        strengths.append(_item("Regular movement", f"{data.physical_activity:.1f} hours of weekly activity is a protective habit.", "person-walking"))
    elif data.physical_activity < 2:
        focus.append(_item("Daily movement", "Low weekly activity may reduce opportunities for stress release.", "person-walking", 5))

    if data.caffeine <= 150:
        strengths.append(_item("Moderate caffeine", f"Daily intake is {data.caffeine} mg.", "cup-hot"))
    elif data.caffeine > 300:
        focus.append(_item("Caffeine load", f"Daily intake is {data.caffeine} mg, which is high relative to the dataset.", "cup-hot", 7))

    if data.stress_level <= 4:
        strengths.append(_item("Manageable stress", f"Self-reported stress is {data.stress_level}/10.", "wind"))
    elif data.stress_level >= 7:
        focus.append(_item("High perceived stress", f"Self-reported stress is {data.stress_level}/10.", "wind", 10))

    if data.heart_rate <= 80:
        strengths.append(_item("Settled resting pulse", f"Reported resting heart rate is {data.heart_rate} bpm.", "heart-pulse"))
    elif data.heart_rate >= 100:
        focus.append(_item("Elevated resting pulse", f"Reported resting heart rate is {data.heart_rate} bpm.", "heart-pulse", 9))

    if data.breathing_rate <= 18:
        strengths.append(_item("Calm breathing", f"Reported resting breathing rate is {data.breathing_rate}/min.", "lungs"))
    elif data.breathing_rate >= 24:
        focus.append(_item("Fast resting breathing", f"Reported breathing rate is {data.breathing_rate}/min.", "lungs", 8))

    if data.diet_quality >= 7:
        strengths.append(_item("Supportive diet pattern", f"Diet quality is rated {data.diet_quality}/10.", "apple-whole"))
    elif data.diet_quality <= 4:
        focus.append(_item("Diet consistency", f"Diet quality is rated {data.diet_quality}/10.", "apple-whole", 4))

    if data.recent_life_event == "Yes":
        focus.append(_item("Recent major life event", "A recent stressful event can temporarily increase emotional load.", "calendar-heart", 7))
    if data.family_history == "Yes":
        focus.append(_item("Family history", "Family history can increase sensitivity but does not determine an outcome.", "people", 3))

    focus.sort(key=lambda item: int(item["priority"]), reverse=True)
    strengths = strengths[:4]
    focus = focus[:5]

    actions: list[dict[str, str | int]] = []
    if data.stress_level >= 7 or data.breathing_rate >= 24:
        actions.append(_item("Regulate first", "Try five slow breathing cycles with a longer exhale before solving the next problem.", "activity", 10))
    if data.sleep_hours < 7:
        actions.append(_item("Protect tonight's sleep window", "Choose a realistic bedtime and reduce bright-screen stimulation during the final 30 minutes.", "moon-stars", 9))
    if data.caffeine > 200:
        actions.append(_item("Move caffeine earlier", "Reduce late-day caffeine first rather than making a sudden large change.", "cup-hot", 8))
    if data.physical_activity < 3.5:
        actions.append(_item("Add a small movement block", "Schedule a 10 to 20 minute walk or light activity on most days.", "person-walking", 7))
    if data.recent_life_event == "Yes" or data.stress_level >= 8:
        actions.append(_item("Use social support", "Tell a trusted person what feels hardest and what type of help would be useful.", "chat-heart", 8))
    if data.therapy_sessions == 0 and engineered.anxiety_composite >= 0.65:
        actions.append(_item("Consider professional support", "A qualified mental health professional can provide an individual assessment and care plan.", "person-hearts", 9))
    if not actions:
        actions.extend([
            _item("Maintain your current anchors", "Keep sleep, movement, and recovery routines consistent.", "check2-circle", 5),
            _item("Check in weekly", "Repeat the reflection when your routine or stress level changes.", "calendar-check", 4),
        ])

    actions.sort(key=lambda item: int(item["priority"]), reverse=True)

    def strip_priority(items: list[dict[str, str | int]]) -> list[dict[str, str]]:
        return [{k: str(v) for k, v in item.items() if k != "priority"} for item in items]

    return strip_priority(strengths), strip_priority(focus), strip_priority(actions[:5])
