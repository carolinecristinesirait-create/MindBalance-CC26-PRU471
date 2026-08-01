from __future__ import annotations

import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _config(name: str) -> dict:
    path = ROOT / "models" / name
    assert path.exists()
    with zipfile.ZipFile(path) as archive:
        assert {"metadata.json", "config.json", "model.weights.h5"}.issubset(archive.namelist())
        return json.loads(archive.read("config.json"))


def test_deployment_model_input_contract() -> None:
    config = _config("mindbalance_model_preprocess.keras")
    input_layers = [layer for layer in config["config"]["layers"] if layer["class_name"] == "InputLayer"]
    assert input_layers[0]["config"]["batch_shape"] == [None, 21]


def test_base_model_output_contract() -> None:
    config = _config("mindbalance_model_new.keras")
    assert config["config"]["output_layers"] == [
        ["class_output", 0, 0],
        ["reg_reshape", 0, 0],
    ]
