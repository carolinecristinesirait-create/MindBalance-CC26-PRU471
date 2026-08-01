"""Central configuration and immutable project metadata."""
from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models"
NOTEBOOK_DIR = ROOT_DIR / "notebooks"

DATASET_PATH = DATA_DIR / "cleaned_anxiety_data.csv"
MODEL_PATHS = (
    MODEL_DIR / "mindbalance_model_preprocess.keras",
    MODEL_DIR / "mindbalance_model_new.keras",
)

APP_NAME = "MindBalance"
APP_TAGLINE = "AI-assisted anxiety risk screening and wellness intelligence"
APP_VERSION = "2.0.0"
TEAM_ID = "CC26-PRU471"
TEAM_MEMBERS = (
    "Caroline Cristine Sirait",
    "Vincentius Tanujaya",
    "Nabillah Indah Tsuraya",
)

CLASS_ORDER = ("Low", "Medium", "High")
CLASS_COLORS = {
    "Low": "#2DD4BF",
    "Medium": "#FBBF24",
    "High": "#FB7185",
}
CLASS_DESCRIPTIONS = {
    "Low": "Current inputs resemble the lower-risk patterns in the training data.",
    "Medium": "Current inputs show several stress-related patterns worth monitoring.",
    "High": "Current inputs resemble higher-risk patterns and may warrant added support.",
}

MODEL_METRICS = {
    "test_records": 1650,
    "accuracy": 0.7570,
    "weighted_f1": 0.7573,
    "regression_mae": 0.8780,
    "regression_rmse": 1.1081,
    "regression_r2": 0.7249,
    "class_report": {
        "Low": {"precision": 0.88, "recall": 0.89, "f1": 0.88, "support": 171},
        "Medium": {"precision": 0.82, "recall": 0.69, "f1": 0.75, "support": 780},
        "High": {"precision": 0.68, "recall": 0.80, "f1": 0.74, "support": 699},
    },
    # Reconstructed from the reported support and rounded recall values.
    # It is intentionally labelled as an approximate visualization in the UI.
    "approx_confusion_matrix": [
        [152, 15, 4],
        [13, 538, 229],
        [8, 132, 559],
    ],
}

FEATURE_ORDER = (
    "Age",
    "Gender",
    "Occupation",
    "Sleep Hours",
    "Physical Activity (hrs/week)",
    "Caffeine Intake (mg/day)",
    "Alcohol Consumption (drinks/week)",
    "Smoking",
    "Family History of Anxiety",
    "Stress Level (1-10)",
    "Heart Rate (bpm)",
    "Breathing Rate (breaths/min)",
    "Sweating Level (1-5)",
    "Dizziness",
    "Medication",
    "Therapy Sessions (per month)",
    "Recent Major Life Event",
    "Diet Quality (1-10)",
    "SleepEfficiencyScore",
    "LifestyleRiskIndex",
    "AnxietyCompositeScore",
)

GENDER_MAP = {"Male": 0, "Female": 1, "Other": 2}
OCCUPATIONS = (
    "Artist",
    "Athlete",
    "Chef",
    "Doctor",
    "Engineer",
    "Freelancer",
    "Lawyer",
    "Musician",
    "Nurse",
    "Other",
    "Scientist",
    "Student",
    "Teacher",
)
OCCUPATION_MAP = {name: index for index, name in enumerate(OCCUPATIONS)}
BINARY_MAP = {"No": 0, "Yes": 1}

DATA_RANGES = {
    "Age": (18, 64),
    "Sleep Hours": (2.3, 11.3),
    "Physical Activity (hrs/week)": (0.0, 10.1),
    "Caffeine Intake (mg/day)": (0, 599),
    "Alcohol Consumption (drinks/week)": (0, 19),
    "Stress Level (1-10)": (1, 10),
    "Heart Rate (bpm)": (60, 119),
    "Breathing Rate (breaths/min)": (12, 29),
    "Sweating Level (1-5)": (1, 5),
    "Therapy Sessions (per month)": (0, 12),
    "Diet Quality (1-10)": (1, 10),
}

DATA_DICTIONARY = {
    "Age": ("Numeric", "18–64", "Respondent age in years."),
    "Gender": ("Categorical", "Male, Female, Other", "Self-reported gender category."),
    "Occupation": ("Categorical", "13 categories", "Primary occupation or activity."),
    "Sleep Hours": ("Numeric", "2.3–11.3", "Average nightly sleep duration."),
    "Physical Activity (hrs/week)": ("Numeric", "0–10.1", "Weekly physical activity duration."),
    "Caffeine Intake (mg/day)": ("Numeric", "0–599", "Average daily caffeine intake."),
    "Alcohol Consumption (drinks/week)": ("Numeric", "0–19", "Average weekly alcohol intake."),
    "Smoking": ("Binary", "Yes / No", "Current smoking status."),
    "Family History of Anxiety": ("Binary", "Yes / No", "First-degree family history of anxiety."),
    "Stress Level (1-10)": ("Ordinal", "1–10", "Self-assessed general stress level."),
    "Heart Rate (bpm)": ("Numeric", "60–119", "Self-reported resting heart rate."),
    "Breathing Rate (breaths/min)": ("Numeric", "12–29", "Self-reported resting breathing rate."),
    "Sweating Level (1-5)": ("Ordinal", "1–5", "Self-assessed sweating intensity."),
    "Dizziness": ("Binary", "Yes / No", "Regular dizziness or lightheadedness."),
    "Medication": ("Binary", "Yes / No", "Current anxiety-related medication use."),
    "Therapy Sessions (per month)": ("Numeric", "0–12", "Monthly counseling or therapy sessions."),
    "Recent Major Life Event": ("Binary", "Yes / No", "Major stressful event within six months."),
    "Diet Quality (1-10)": ("Ordinal", "1–10", "Self-assessed diet quality."),
    "Anxiety Level (1-10)": ("Target", "1–10", "Self-reported anxiety severity."),
    "Anxiety_Category": ("Target", "Low / Medium / High", "Derived classification label."),
    "SleepEfficiencyScore": ("Engineered", "0–1", "Sleep duration and inverse caffeine composite."),
    "LifestyleRiskIndex": ("Engineered", "0–1", "Weighted lifestyle and contextual risk composite."),
    "AnxietyCompositeScore": ("Engineered", "0–1", "Weighted physiological and stress composite."),
}

NAV_ITEMS = (
    ("Home", "house-heart"),
    ("Assessment", "clipboard2-pulse"),
    ("Insights", "bar-chart-line"),
    ("Wellness Toolkit", "activity"),
    ("Model & Data", "diagram-3"),
    ("About", "info-circle"),
)
