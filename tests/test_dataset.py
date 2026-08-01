from __future__ import annotations

from pathlib import Path

import pandas as pd

from mindbalance.config import CLASS_ORDER, FEATURE_ORDER


def test_dataset_contract() -> None:
    path = Path(__file__).resolve().parents[1] / "data" / "cleaned_anxiety_data.csv"
    df = pd.read_csv(path)
    assert len(df) == 11_000
    assert df.shape[1] == 20
    assert not df.isna().any().any()
    assert set(df["Anxiety_Category"].unique()) == set(CLASS_ORDER)


def test_model_feature_contract_has_21_items() -> None:
    assert len(FEATURE_ORDER) == 21
    assert len(set(FEATURE_ORDER)) == 21
