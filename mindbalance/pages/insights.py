"""Exploratory analytics dashboard."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from mindbalance.charts import (
    anxiety_histogram,
    category_distribution,
    correlation_heatmap,
    demographic_bar,
    feature_boxplot,
    feature_profile,
    occupation_ranking,
    sleep_caffeine_heatmap,
)
from mindbalance.config import CLASS_ORDER
from mindbalance.ui import footer, metric_card, notice, page_header, section_title

NUMERIC_FEATURES = [
    "Age",
    "Sleep Hours",
    "Physical Activity (hrs/week)",
    "Caffeine Intake (mg/day)",
    "Alcohol Consumption (drinks/week)",
    "Stress Level (1-10)",
    "Heart Rate (bpm)",
    "Breathing Rate (breaths/min)",
    "Sweating Level (1-5)",
    "Therapy Sessions (per month)",
    "Diet Quality (1-10)",
    "Anxiety Level (1-10)",
]


def _filters(df: pd.DataFrame) -> pd.DataFrame:
    with st.expander("Filter the dataset", expanded=True):
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            categories = st.multiselect("Anxiety category", list(CLASS_ORDER), default=list(CLASS_ORDER))
            genders = st.multiselect("Gender", sorted(df["Gender"].dropna().astype(str).unique()), default=sorted(df["Gender"].dropna().astype(str).unique()))
        with c2:
            occupations = st.multiselect("Occupation", sorted(df["Occupation"].dropna().astype(str).unique()), default=[])
            age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
            age_range = st.slider("Age range", age_min, age_max, (age_min, age_max))
        with c3:
            stress_min, stress_max = int(df["Stress Level (1-10)"].min()), int(df["Stress Level (1-10)"].max())
            stress_range = st.slider("Stress range", stress_min, stress_max, (stress_min, stress_max))
            family = st.multiselect("Family history", sorted(df["Family History of Anxiety"].astype(str).unique()), default=sorted(df["Family History of Anxiety"].astype(str).unique()))

    filtered = df[
        df["Anxiety_Category"].isin(categories)
        & df["Gender"].isin(genders)
        & df["Age"].between(age_range[0], age_range[1])
        & df["Stress Level (1-10)"].between(stress_range[0], stress_range[1])
        & df["Family History of Anxiety"].isin(family)
    ]
    if occupations:
        filtered = filtered[filtered["Occupation"].isin(occupations)]
    return filtered.copy()


def render_insights(df: pd.DataFrame) -> None:
    page_header(
        "EXPLORE 11,000 ANONYMIZED SURVEY RECORDS",
        "Population insights",
        "Filter the source data, compare groups, and inspect the lifestyle and physiological patterns associated with each anxiety category.",
        "bar-chart-line",
    )
    filtered = _filters(df)
    if filtered.empty:
        notice("The selected filters return no records. Widen one or more filters to continue.", "warning")
        footer()
        return

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        metric_card("Visible records", f"{len(filtered):,}", f"{len(filtered) / len(df):.1%} of the full dataset", "funnel", "teal")
    with c2:
        metric_card("Mean anxiety", f"{filtered['Anxiety Level (1-10)'].mean():.2f}", "Self-reported score on a 1–10 scale", "activity", "amber")
    with c3:
        metric_card("Mean sleep", f"{filtered['Sleep Hours'].mean():.1f} h", "Average nightly sleep", "moon-stars", "blue")
    with c4:
        metric_card("Mean stress", f"{filtered['Stress Level (1-10)'].mean():.2f}", "Average perceived stress", "wind", "rose")

    section_title("Overview", "Category balance and the distribution of self-reported anxiety scores.", "01")
    a, b = st.columns(2, gap="large")
    with a:
        st.plotly_chart(category_distribution(filtered), use_container_width=True, config={"displayModeBar": False})
    with b:
        st.plotly_chart(anxiety_histogram(filtered), use_container_width=True, config={"displayModeBar": False})

    section_title("Category signatures", "Compare the average profile and inspect one feature in detail.", "02")
    signature_features = [
        "Sleep Hours",
        "Physical Activity (hrs/week)",
        "Caffeine Intake (mg/day)",
        "Stress Level (1-10)",
        "Heart Rate (bpm)",
        "Diet Quality (1-10)",
    ]
    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.plotly_chart(feature_profile(filtered, signature_features), use_container_width=True, config={"displayModeBar": False})
    with right:
        selected_feature = st.selectbox("Feature to compare", NUMERIC_FEATURES, index=5)
        st.plotly_chart(feature_boxplot(filtered, selected_feature), use_container_width=True, config={"displayModeBar": False})

    section_title("Lifestyle interaction", "Explore how sleep and caffeine combinations align with average anxiety.", "03")
    st.plotly_chart(sleep_caffeine_heatmap(filtered), use_container_width=True, config={"displayModeBar": False})
    st.caption("This is an observational comparison. It does not prove that changing one variable will cause a specific anxiety outcome.")

    section_title("Demographic context", "Identity does not determine anxiety. These views only describe patterns in this dataset.", "04")
    d1, d2 = st.columns(2, gap="large")
    with d1:
        demographic = st.selectbox("Stacked comparison", ["Gender", "Family History of Anxiety", "Recent Major Life Event"])
        st.plotly_chart(demographic_bar(filtered, demographic), use_container_width=True, config={"displayModeBar": False})
    with d2:
        st.plotly_chart(occupation_ranking(filtered), use_container_width=True, config={"displayModeBar": False})

    section_title("Correlation explorer", "Linear relationships among selected numeric variables.", "05")
    default_corr = [
        "Sleep Hours",
        "Caffeine Intake (mg/day)",
        "Stress Level (1-10)",
        "Heart Rate (bpm)",
        "Breathing Rate (breaths/min)",
        "Diet Quality (1-10)",
        "Anxiety Level (1-10)",
    ]
    corr_columns = st.multiselect("Variables", NUMERIC_FEATURES, default=default_corr, max_selections=10)
    if len(corr_columns) >= 2:
        st.plotly_chart(correlation_heatmap(filtered, corr_columns), use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Select at least two variables.")

    section_title("Data explorer", "Search the filtered rows and download the current view.", "06")
    search = st.text_input("Search text values", placeholder="Example: Student, Female, Yes")
    table = filtered
    if search.strip():
        mask = table.astype(str).apply(lambda column: column.str.contains(search, case=False, na=False)).any(axis=1)
        table = table[mask]
    st.dataframe(table.head(500), use_container_width=True, hide_index=True, height=420)
    st.caption("The on-screen table is limited to 500 rows for responsiveness. The CSV download contains all filtered rows.")
    st.download_button(
        "Download filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="mindbalance_filtered_data.csv",
        mime="text/csv",
    )
    footer()
