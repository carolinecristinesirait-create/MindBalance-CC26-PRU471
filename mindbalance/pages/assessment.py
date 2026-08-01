"""Assessment form and results dashboard."""
from __future__ import annotations

import time

import streamlit as st

from mindbalance.charts import probability_donut, wellness_radar
from mindbalance.config import CLASS_DESCRIPTIONS, OCCUPATIONS
from mindbalance.features import normalized_wellness_scores, physiological_index_scores, validate_input
from mindbalance.model_engine import ModelBundle, predict_profile
from mindbalance.reporting import result_html, result_json
from mindbalance.schemas import AssessmentInput, PredictionResult
from mindbalance.ui import (
    footer,
    guidance_panel,
    list_cards,
    notice,
    page_header,
    physiological_index_cards,
    result_banner,
    section_title,
)


def _render_form() -> AssessmentInput | None:
    with st.form("mindbalance_assessment", clear_on_submit=False, border=True):
        st.markdown("<div class='mb-form-intro'><strong>Use your recent typical pattern</strong><span>Choose values that best represent the past one to two weeks.</span></div>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["1 · Lifestyle", "2 · Body signals", "3 · Context"])

        with tab1:
            st.caption("Sleep, movement, stimulants, and daily routines.")
            c1, c2 = st.columns(2, gap="large")
            with c1:
                sleep_hours = st.slider("Average sleep per night", 2.0, 12.0, 7.0, 0.1, help="Average duration during the past one to two weeks.")
                physical_activity = st.slider("Physical activity per week", 0.0, 14.0, 3.5, 0.5, help="Walking, exercise, sport, or other moderate activity.")
                diet_quality = st.slider("Diet quality", 1, 10, 7, help="A personal consistency and nutrition rating.")
            with c2:
                caffeine = st.number_input("Caffeine per day (mg)", min_value=0, max_value=1000, value=120, step=10, help="Coffee, tea, energy drinks, and other sources.")
                alcohol = st.number_input("Alcoholic drinks per week", min_value=0, max_value=50, value=0, step=1)
                smoking = st.selectbox("Current smoking or vaping", ["No", "Yes"])

        with tab2:
            st.caption("Use resting measurements where possible. Avoid measuring immediately after exercise.")
            c1, c2 = st.columns(2, gap="large")
            with c1:
                stress_level = st.slider("Perceived stress", 1, 10, 4, help="1 means very calm and 10 means extremely stressed.")
                heart_rate = st.number_input("Resting heart rate (bpm)", min_value=40, max_value=180, value=72, step=1)
                breathing_rate = st.number_input("Resting breathing rate (per minute)", min_value=8, max_value=45, value=16, step=1)
            with c2:
                sweating_level = st.slider("Sweating tendency", 1, 5, 2)
                dizziness = st.selectbox("Frequent dizziness or lightheadedness", ["No", "Yes"])
                medication = st.selectbox("Currently using anxiety-related medication", ["No", "Yes"])
            with st.expander("How to estimate resting pulse and breathing rate"):
                st.markdown(
                    "Sit quietly for a few minutes. Count pulse beats for 30 seconds and multiply by two. For breathing, count each full rise and fall of the chest for 60 seconds. These measurements are optional self-reports, not clinical readings."
                )

        with tab3:
            st.caption("Contextual factors help the model interpret the same body signals more carefully.")
            c1, c2 = st.columns(2, gap="large")
            with c1:
                age = st.number_input("Age", min_value=18, max_value=100, value=26, step=1)
                gender = st.selectbox("Gender category", ["Female", "Male", "Other"])
                occupation = st.selectbox("Primary occupation or activity", list(OCCUPATIONS), index=list(OCCUPATIONS).index("Student"))
            with c2:
                family_history = st.selectbox("Family history of anxiety", ["No", "Yes"])
                recent_life_event = st.selectbox("Major stressful life event in the past six months", ["No", "Yes"])
                therapy_sessions = st.number_input("Therapy or counseling sessions this month", min_value=0, max_value=30, value=0, step=1)

        consent = st.checkbox(
            "I understand that this is an educational screening estimate, not a medical diagnosis.",
            value=False,
        )
        submitted = st.form_submit_button("Analyze my profile", type="primary", use_container_width=True)

    if not submitted:
        return None
    if not consent:
        st.error("Please confirm the screening disclaimer before continuing.")
        return None

    return AssessmentInput(
        age=int(age),
        gender=gender,
        occupation=occupation,
        sleep_hours=float(sleep_hours),
        physical_activity=float(physical_activity),
        caffeine=int(caffeine),
        alcohol=int(alcohol),
        smoking=smoking,
        family_history=family_history,
        stress_level=int(stress_level),
        heart_rate=int(heart_rate),
        breathing_rate=int(breathing_rate),
        sweating_level=int(sweating_level),
        dizziness=dizziness,
        medication=medication,
        therapy_sessions=int(therapy_sessions),
        recent_life_event=recent_life_event,
        diet_quality=int(diet_quality),
    )


def _render_result(result: PredictionResult) -> None:
    result_banner(
        result.level,
        result.predicted_score,
        result.confidence,
        CLASS_DESCRIPTIONS[result.level],
    )

    if result.model_mode != "TensorFlow model":
        notice(
            "The trained TensorFlow model was unavailable in this runtime, so the app used its documented transparent fallback. Deploy with the included TensorFlow dependency to use the trained model.",
            "warning",
            "Fallback inference active",
        )

    scores = normalized_wellness_scores(result.input_data, result.engineered)
    index_scores = physiological_index_scores(result.engineered)

    balance_col, index_col = st.columns([1.08, 1], gap="large")
    with balance_col:
        st.markdown("<div class='mb-result-subheading'><h3>Wellness Factor Balance</h3><p>A normalized view of six protective wellbeing dimensions.</p></div>", unsafe_allow_html=True)
        st.plotly_chart(
            wellness_radar(scores),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with index_col:
        st.markdown("<div class='mb-result-subheading'><h3>Key Physiological Indexes</h3><p>Headline indicators derived from the values submitted.</p></div>", unsafe_allow_html=True)
        physiological_index_cards(
            [
                {
                    "label": "SLEEP RESTFULNESS",
                    "value": index_scores["Sleep restfulness"],
                    "detail": "Adjusted for sleep duration and daily caffeine intake.",
                    "direction": "higher-protection",
                },
                {
                    "label": "LIFESTYLE STRAIN",
                    "value": index_scores["Lifestyle strain"],
                    "detail": "Routine stressors, habits, movement, diet, and recent context.",
                    "direction": "higher-risk",
                },
                {
                    "label": "PHYSICAL TENSION",
                    "value": index_scores["Physical tension"],
                    "detail": "Combined stress, pulse, breathing, sweating, and history signal.",
                    "direction": "higher-risk",
                },
            ]
        )

    guidance_panel(result.action_plan, "No restorative strategy was generated.")

    section_title(
        "How the result was formed",
        "Review the model confidence alongside the strongest protective and risk signals.",
        "DETAIL",
    )
    probability_col, explanation_col = st.columns([0.82, 1.18], gap="large")
    with probability_col:
        st.markdown("#### Probability profile")
        st.plotly_chart(
            probability_donut(result.probabilities),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.caption(
            f"Interpretation: {result.confidence_label}. Similar class probabilities mean the profile sits near a decision boundary."
        )
    with explanation_col:
        signal_tab, focus_tab = st.tabs(["Protective signals", "Priority focus areas"])
        with signal_tab:
            list_cards(result.strengths, "No specific protective signal met the dashboard thresholds.")
        with focus_tab:
            list_cards(result.focus_areas, "No high-priority focus area met the dashboard thresholds.")

    if result.level == "High" or result.input_data.stress_level >= 9:
        notice(
            "Consider speaking with a qualified mental health professional, especially if distress is persistent, worsening, or interfering with daily life. Seek urgent local help when there is immediate danger or a risk of self-harm.",
            "danger",
            "Additional support may be appropriate",
        )

    section_title("Download or start again", "Reports contain the values submitted in this session.")
    d1, d2, d3 = st.columns([1, 1, 0.8], gap="small")
    with d1:
        st.download_button(
            "Download HTML report",
            data=result_html(result),
            file_name="mindbalance_assessment_report.html",
            mime="text/html",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "Download JSON data",
            data=result_json(result),
            file_name="mindbalance_assessment.json",
            mime="application/json",
            use_container_width=True,
        )
    with d3:
        if st.button("Clear result", use_container_width=True):
            st.session_state.assessment_result = None
            st.rerun()


def render_assessment(bundle: ModelBundle) -> None:
    page_header(
        "PRIVATE, SESSION-BASED SELF-REFLECTION",
        "MindBalance assessment",
        "Complete three short sections. The dashboard will estimate a risk pattern and explain the strongest signals behind it.",
        "clipboard2-pulse",
    )
    notice(
        "For more reliable comparisons, enter typical recent values rather than the best or worst day you can remember.",
        "info",
    )

    submitted_data = _render_form()
    if submitted_data is not None:
        issues = validate_input(submitted_data)
        attention = [issue for issue in issues if issue.severity == "attention"]
        warnings = [issue for issue in issues if issue.severity != "attention"]
        for issue in attention:
            st.warning(f"{issue.field}: {issue.message}")
        if warnings:
            with st.expander(f"{len(warnings)} training-range note(s)"):
                for issue in warnings:
                    st.write(f"- **{issue.field}:** {issue.message}")
        with st.spinner("Analyzing the 21-feature profile..."):
            time.sleep(0.25)
            st.session_state.assessment_result = predict_profile(submitted_data, bundle)
            st.session_state.assessment_count += 1
        st.toast("Assessment complete", icon="✅")
        st.rerun()

    result = st.session_state.get("assessment_result")
    if isinstance(result, PredictionResult):
        _render_result(result)
    footer()
