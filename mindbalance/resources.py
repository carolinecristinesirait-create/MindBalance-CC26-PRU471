"""Cached access to data and the trained model."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from mindbalance.config import DATASET_PATH, MODEL_PATHS
from mindbalance.model_engine import ModelBundle, load_keras_model


@st.cache_resource(show_spinner=False)
def get_model_bundle() -> ModelBundle:
    return load_keras_model(MODEL_PATHS)


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    if DATASET_PATH.exists():
        df = pd.read_csv(DATASET_PATH)
        if not df.empty:
            return df
    return generate_demo_dataset()


def generate_demo_dataset(n: int = 1200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    categories = rng.choice(["Low", "Medium", "High"], n, p=[0.47, 0.42, 0.11])
    center = {"Low": 2.1, "Medium": 5.0, "High": 8.1}
    anxiety = np.clip(np.asarray([center[x] for x in categories]) + rng.normal(0, 0.9, n), 1, 10)
    return pd.DataFrame({
        "Age": rng.integers(18, 65, n),
        "Gender": rng.choice(["Female", "Male", "Other"], n, p=[0.50, 0.48, 0.02]),
        "Occupation": rng.choice(["Student", "Engineer", "Teacher", "Freelancer", "Other"], n),
        "Sleep Hours": np.clip(8.4 - anxiety * 0.34 + rng.normal(0, 0.9, n), 2.3, 11.3),
        "Physical Activity (hrs/week)": np.clip(5.2 - anxiety * 0.28 + rng.normal(0, 1.2, n), 0, 10.1),
        "Caffeine Intake (mg/day)": np.clip(80 + anxiety * 35 + rng.normal(0, 65, n), 0, 599).round(),
        "Alcohol Consumption (drinks/week)": np.clip(anxiety + rng.normal(3, 2, n), 0, 19).round(),
        "Smoking": rng.choice(["No", "Yes"], n, p=[0.8, 0.2]),
        "Family History of Anxiety": rng.choice(["No", "Yes"], n, p=[0.7, 0.3]),
        "Stress Level (1-10)": np.clip(anxiety + rng.normal(0.7, 1, n), 1, 10).round(),
        "Heart Rate (bpm)": np.clip(62 + anxiety * 5.5 + rng.normal(0, 7, n), 60, 119).round(),
        "Breathing Rate (breaths/min)": np.clip(12 + anxiety * 1.5 + rng.normal(0, 2, n), 12, 29).round(),
        "Sweating Level (1-5)": np.clip(1 + anxiety * 0.42 + rng.normal(0, 0.5, n), 1, 5).round(),
        "Dizziness": rng.choice(["No", "Yes"], n, p=[0.76, 0.24]),
        "Medication": rng.choice(["No", "Yes"], n, p=[0.9, 0.1]),
        "Therapy Sessions (per month)": rng.integers(0, 13, n),
        "Recent Major Life Event": rng.choice(["No", "Yes"], n, p=[0.62, 0.38]),
        "Diet Quality (1-10)": np.clip(8 - anxiety * 0.32 + rng.normal(0, 1.2, n), 1, 10).round(),
        "Anxiety Level (1-10)": anxiety.round(),
        "Anxiety_Category": categories,
    })
