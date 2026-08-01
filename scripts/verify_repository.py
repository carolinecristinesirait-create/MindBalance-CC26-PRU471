"""Verify critical MindBalance repository artifacts without importing TensorFlow."""
from __future__ import annotations

import csv
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "app.py",
    "requirements.txt",
    ".streamlit/config.toml",
    "data/cleaned_anxiety_data.csv",
    "models/mindbalance_model_preprocess.keras",
    "models/mindbalance_model_new.keras",
    "mindbalance/features.py",
    "mindbalance/model_engine.py",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def verify_files() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).exists()]
    if missing:
        fail(f"Missing required files: {', '.join(missing)}")
    print(f"[OK] {len(REQUIRED)} required paths found")


def verify_dataset() -> None:
    path = ROOT / "data" / "cleaned_anxiety_data.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if len(rows) != 11_000:
        fail(f"Expected 11,000 data rows, found {len(rows):,}")
    if len(reader.fieldnames or []) != 20:
        fail(f"Expected 20 columns, found {len(reader.fieldnames or [])}")
    categories = {row["Anxiety_Category"] for row in rows}
    if categories != {"Low", "Medium", "High"}:
        fail(f"Unexpected categories: {sorted(categories)}")
    print("[OK] Dataset: 11,000 rows, 20 columns, three expected classes")


def verify_model(name: str) -> None:
    path = ROOT / "models" / name
    with zipfile.ZipFile(path) as archive:
        required = {"metadata.json", "config.json", "model.weights.h5"}
        if not required.issubset(archive.namelist()):
            fail(f"{name} is missing one or more Keras archive entries")
        config = json.loads(archive.read("config.json"))
    input_layers = [
        layer for layer in config["config"]["layers"]
        if layer.get("class_name") == "InputLayer"
    ]
    shape = input_layers[0]["config"].get("batch_shape") if input_layers else None
    if shape != [None, 21]:
        fail(f"{name} input shape is {shape}, expected [None, 21]")
    print(f"[OK] {name}: valid Keras archive with 21-feature input")


def main() -> None:
    print(f"Verifying repository: {ROOT}")
    verify_files()
    verify_dataset()
    verify_model("mindbalance_model_preprocess.keras")
    verify_model("mindbalance_model_new.keras")
    print("[PASS] MindBalance repository verification complete")


if __name__ == "__main__":
    main()
