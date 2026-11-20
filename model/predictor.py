"""Loads the wine model once and exposes a single predict function."""

import os
from pathlib import Path

import joblib
import pandas as pd

DEFAULT_MODEL_PATH = Path(__file__).resolve().parent / "wine-model.joblib"
MODEL_PATH = Path(os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH))

# Loaded once, when the module is imported
model = joblib.load(MODEL_PATH)

# API field name -> column name used during training
FEATURES = {
    "alcohol": "alcohol",
    "malic_acid": "malic acid",
    "ash": "ash",
    "alcalinity_of_ash": "alcalinity of ash",
    "magnesium": "magnesium",
    "total_phenols": "total phenols",
    "flavanoids": "flavanoids",
    "nonflavanoid_phenols": "nonflavanoid phenols",
    "proanthocyanins": "proanthocyanins",
    "color_intensity": "color intensity",
    "hue": "hue",
    "od280_od315": "OD280/OD315 of diluted wines",
    "proline": "proline",
}

# First row of the dataset (expected label: 1)
SAMPLE = {
    "alcohol": 14.23,
    "malic_acid": 1.71,
    "ash": 2.43,
    "alcalinity_of_ash": 15.6,
    "magnesium": 127.0,
    "total_phenols": 2.80,
    "flavanoids": 3.06,
    "nonflavanoid_phenols": 0.28,
    "proanthocyanins": 2.29,
    "color_intensity": 5.64,
    "hue": 1.04,
    "od280_od315": 3.92,
    "proline": 1065.0,
}


def predict(features: dict) -> dict:
    """Returns the predicted wine class for one sample."""
    row = pd.DataFrame([{FEATURES[name]: features[name] for name in FEATURES}])
    # numpy.int64 is not JSON/protobuf serializable, so cast to int
    return {"label": int(model.predict(row)[0])}

