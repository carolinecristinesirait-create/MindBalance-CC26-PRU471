"""Home dashboard."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from mindbalance.charts import category_distribution
from mindbalance.config import CLASS_ORDER, MODEL_METRICS
from mindbalance.state import navigate
from mindbalance.ui import footer, metric_card, notice, page_header, section_title, step_card


def render_home(df: pd.DataFrame, model_available: bool) -> None:
    page_header(
        "CALMER DECISIONS START WITH A CLEARER PICTURE",
        "Understand your wellbeing signals",
        "MindBalance combines a structured self-reflection, a trained TensorFlow model, and explainable wellness guidance in one private session.",
        "heart-pulse",
    )

    notice(
        "MindBalance estimates patterns from self-reported inputs. It cannot diagnose an anxiety disorder, replace clinical assessment, or determine whether medication is appropriate.",
        "warning",
        "Educational screening only",
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        metric_card("Survey records", f"{len(df):,}", "Anonymized rows available for exploration", "database", "teal")
    with c2:
        metric_card("Input features", "21", "18 original plus 3 engineered features", "sliders", "blue")
    with c3:
        metric_card("Test accuracy", f"{MODEL_METRICS['accuracy']:.1%}", "Held-out test set reported in the notebook", "bullseye", "amber")
    with c4:
        metric_card("Runtime", "AI ready" if model_available else "Fallback", "Graceful operation when the model cannot load", "cpu", "rose")

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        section_title("Three steps to a useful result", "The assessment is designed to take only a few minutes.")
        a, b, c = st.columns(3, gap="small")
        with a:
            step_card("01", "Reflect", "Enter recent sleep, stress, lifestyle, and body signals.", "clipboard2-heart")
        with b:
            step_card("02", "Estimate", "The model compares the 21-feature profile with learned patterns.", "cpu")
        with c:
            step_card("03", "Act", "Review strengths, focus areas, and practical next steps.", "check2-circle")
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if st.button("Start my assessment", type="primary", use_container_width=True):
            navigate("Assessment")

    with right:
        st.plotly_chart(category_distribution(df), use_container_width=True, config={"displayModeBar": False})

    section_title("What this dashboard includes", "Built for demonstration, presentation, and further development.")
    f1, f2, f3 = st.columns(3, gap="medium")
    feature_cards = [
        (f1, "Assessment intelligence", "Multi-output prediction, class probabilities, estimated score, profile strengths, and priority focus areas.", "stars"),
        (f2, "Exploratory analytics", "Interactive filtering, category signatures, demographic comparisons, correlations, and raw-data export.", "bar-chart-line"),
        (f3, "Wellness toolkit", "Guided breathing, grounding prompts, a quick check-in, and a simple recovery-plan builder.", "activity"),
    ]
    for column, title, text, icon_name in feature_cards:
        with column:
            st.markdown(
                f"""
                <div class="mb-feature-card">
                  <div class="mb-feature-symbol"><i class="bi bi-{icon_name}"></i></div>
                  <h3>{title}</h3><p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    section_title("Dataset snapshot", "A quick view of the source data used by the analytics page.")
    preview_cols = [
        "Age",
        "Gender",
        "Occupation",
        "Sleep Hours",
        "Stress Level (1-10)",
        "Heart Rate (bpm)",
        "Anxiety_Category",
    ]
    available = [column for column in preview_cols if column in df.columns]
    st.dataframe(
        df[available].head(12),
        use_container_width=True,
        hide_index=True,
        column_config={"Anxiety_Category": st.column_config.TextColumn("Category")},
    )
    st.caption(f"Categories available: {', '.join(CLASS_ORDER)}. Full filtering and downloads are available under Insights.")
    footer()
