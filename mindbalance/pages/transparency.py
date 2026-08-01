"""Model card, data documentation, and limitations."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from mindbalance.charts import confusion_matrix_figure, model_metrics_bar
from mindbalance.config import DATA_DICTIONARY, FEATURE_ORDER, MODEL_METRICS
from mindbalance.model_engine import ModelBundle
from mindbalance.ui import footer, metric_card, notice, page_header, section_title


def render_transparency(df: pd.DataFrame, bundle: ModelBundle) -> None:
    page_header(
        "MODEL CARD AND DATA DOCUMENTATION",
        "How MindBalance works",
        "Review the feature pipeline, reported evaluation metrics, model limitations, and the exact data fields used by the dashboard.",
        "diagram-3",
    )
    notice(
        "The reported test performance comes from the included training notebook. It should not be interpreted as clinical validity or performance on a real-world patient population.",
        "warning",
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        metric_card("Architecture", "Multi-output", "3-class softmax plus 1 regression head", "share", "teal")
    with c2:
        metric_card("Test accuracy", f"{MODEL_METRICS['accuracy']:.1%}", "1,650 held-out records", "bullseye", "amber")
    with c3:
        metric_card("Weighted F1", f"{MODEL_METRICS['weighted_f1']:.1%}", "Balances precision and recall", "speedometer2", "blue")
    with c4:
        metric_card("Regression MAE", f"{MODEL_METRICS['regression_mae']:.3f}", "On the original 1–10 score scale", "graph-up", "rose")

    section_title("Runtime status", "The repository includes two Keras artifacts.", "01")
    if bundle.available:
        st.success(f"Loaded model: `{bundle.path.name if bundle.path else 'Keras model'}`")
    else:
        st.warning(f"The TensorFlow model is not loaded in this runtime. Reason: {bundle.error or 'Unknown error'}")
    st.code(
        "Raw 18-feature response\n"
        "        +\n"
        "3 engineered features\n"
        "        ↓\n"
        "RobustScaler embedded in deployment model\n"
        "        ↓\n"
        "Shared dense network\n"
        "     ↙          ↘\n"
        "3-class risk     Estimated 1–10 score",
        language="text",
    )

    section_title("Held-out test performance", "Per-class metrics reported by the training notebook.", "02")
    p1, p2 = st.columns(2, gap="large")
    with p1:
        st.plotly_chart(model_metrics_bar(), use_container_width=True, config={"displayModeBar": False})
    with p2:
        st.plotly_chart(confusion_matrix_figure(), use_container_width=True, config={"displayModeBar": False})
        st.caption("The matrix is an approximate visualization reconstructed from rounded recall values and reported supports. Use the per-class metrics as the authoritative reported values.")

    section_title("Feature engineering", "These formulas match the included notebook and deployment model contract.", "03")
    st.markdown(
        """
        **SleepEfficiencyScore**  
        `0.70 × normalized sleep + 0.30 × inverse normalized caffeine`

        **LifestyleRiskIndex**  
        Weighted combination of stress, smoking, alcohol, family history, recent life event, inverse activity, and inverse diet quality.

        **AnxietyCompositeScore**  
        Weighted combination of stress, heart rate, breathing rate, sweating, and family history.
        """
    )
    with st.expander("Show exact model feature order"):
        for index, feature in enumerate(FEATURE_ORDER, start=1):
            st.write(f"{index:02d}. {feature}")

    section_title("Data dictionary", f"{len(df):,} records and {len(df.columns)} columns are loaded in the dashboard.", "04")
    dictionary = pd.DataFrame(
        [
            {"Feature": name, "Type": info[0], "Range or values": info[1], "Description": info[2]}
            for name, info in DATA_DICTIONARY.items()
        ]
    )
    st.dataframe(dictionary, use_container_width=True, hide_index=True, height=520)

    section_title("Known limitations", "Use the system within the boundaries of its evidence.", "05")
    limitations = [
        "The source data are structured self-reports, not clinician-administered diagnostic interviews.",
        "The model may not generalize to populations, cultures, ages, or clinical settings not represented in training.",
        "Several input variables can change quickly and may be measured inaccurately by users.",
        "The test accuracy is below the notebook's original 85% target, with weaker recall for the Medium class than for Low and High.",
        "Category probabilities are model confidence scores, not probabilities that a person has a medical condition.",
        "The dashboard provides deterministic wellness suggestions and does not generate treatment or medication recommendations.",
    ]
    for limitation in limitations:
        st.markdown(f"<div class='mb-limit-item'><i class='bi bi-dot'></i>{limitation}</div>", unsafe_allow_html=True)

    section_title("Responsible-use checklist", "Recommended before presenting or extending the project.", "06")
    checks = [
        "Keep the educational-screening disclaimer visible.",
        "Do not store identifiable assessment data without explicit consent and appropriate controls.",
        "Validate the model on a relevant external dataset before claiming real-world performance.",
        "Add professional review before using the system in healthcare or institutional decision-making.",
        "Monitor fairness and calibration across relevant demographic groups.",
    ]
    for item in checks:
        st.checkbox(item, value=False, key=f"responsible_{item}")
    footer()
