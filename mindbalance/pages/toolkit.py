"""Interactive, non-clinical wellness tools."""
from __future__ import annotations

from datetime import datetime

import streamlit as st

from mindbalance.suite import render_interactive_measurement_suite
from mindbalance.ui import footer, notice, page_header, section_title


def _grounding_exercise() -> None:
    section_title("5–4–3–2–1 grounding", "Use your senses to reconnect with the present moment.", "GROUND")
    prompts = [
        ("5", "things you can see"),
        ("4", "things you can feel"),
        ("3", "things you can hear"),
        ("2", "things you can smell"),
        ("1", "thing you can taste or appreciate"),
    ]
    cols = st.columns(5, gap="small")
    answers = {}
    for column, (number, label) in zip(cols, prompts):
        with column:
            st.markdown(f"<div class='mb-ground-number'>{number}</div>", unsafe_allow_html=True)
            answers[number] = st.text_area(label.capitalize(), key=f"ground_{number}", height=110)
    if st.button("Save grounding note in this session", use_container_width=True):
        st.session_state.grounding_note = {
            "created": datetime.now().isoformat(timespec="minutes"),
            "answers": answers,
        }
        st.success("Saved in this browser session.")


def _check_in() -> None:
    section_title("60-second check-in", "Name what is happening before deciding what to do next.", "CHECK")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        emotion = st.select_slider("Current emotional intensity", options=list(range(1, 11)), value=5)
    with c2:
        energy = st.select_slider("Current energy", options=list(range(1, 11)), value=5)
    with c3:
        control = st.select_slider("Sense of control", options=list(range(1, 11)), value=5)
    trigger = st.text_input("What seems to be driving the feeling?", placeholder="One sentence is enough")
    need = st.selectbox("What would help most right now?", ["A short pause", "Clarity", "Movement", "Connection", "Rest", "Professional support"])
    if st.button("Create a check-in summary", type="primary", use_container_width=True):
        st.session_state.toolkit_mood = {
            "intensity": emotion,
            "energy": energy,
            "control": control,
            "trigger": trigger,
            "need": need,
        }
    summary = st.session_state.get("toolkit_mood")
    if summary:
        st.markdown(
            f"""
            <div class="mb-checkin-summary">
              <strong>Current snapshot</strong>
              <p>Intensity <b>{summary['intensity']}/10</b> · Energy <b>{summary['energy']}/10</b> · Control <b>{summary['control']}/10</b></p>
              <p><b>Likely need:</b> {summary['need']}</p>
              <p><b>Trigger note:</b> {summary['trigger'] or 'Not specified'}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _routine_builder() -> None:
    section_title("Recovery-plan builder", "Create a realistic plan for the next 24 hours.", "PLAN")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        sleep = st.text_input("Sleep anchor", placeholder="Example: Put phone away at 10:30 PM")
        movement = st.text_input("Movement anchor", placeholder="Example: Walk for 15 minutes after lunch")
    with c2:
        connection = st.text_input("Connection anchor", placeholder="Example: Call a trusted friend")
        boundary = st.text_input("One boundary", placeholder="Example: Stop work messages after 8 PM")
    plan = {
        "Sleep": sleep,
        "Movement": movement,
        "Connection": connection,
        "Boundary": boundary,
    }
    content = "\n".join(f"{name}: {value or '[not set]'}" for name, value in plan.items())
    st.download_button(
        "Download my 24-hour plan",
        data=content,
        file_name="mindbalance_24_hour_plan.txt",
        mime="text/plain",
        use_container_width=True,
    )


def render_toolkit() -> None:
    page_header(
        "PRACTICAL TOOLS FOR A CALMER NEXT STEP",
        "Wellness toolkit",
        "Use these brief exercises independently of the AI assessment. None of the tools replace professional treatment or emergency support.",
        "activity",
    )
    notice(
        "Stop any breathing exercise that causes discomfort, dizziness, or worsening symptoms. Return to normal breathing and seek appropriate help when needed.",
        "warning",
    )

    tabs = st.tabs(["Breathing & measurements", "Grounding", "Quick check-in", "24-hour plan"])
    with tabs[0]:
        render_interactive_measurement_suite()
    with tabs[1]:
        _grounding_exercise()
    with tabs[2]:
        _check_in()
    with tabs[3]:
        _routine_builder()

    notice(
        "When distress feels unmanageable, keeps worsening, or includes immediate danger or thoughts of self-harm, contact local emergency services or a trusted crisis-support provider now.",
        "danger",
        "Know when to seek urgent help",
    )
    footer()
