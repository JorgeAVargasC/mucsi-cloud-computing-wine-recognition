"""Requests a wine prediction from the REST service."""

import os

import requests

from model.predictor import SAMPLE

REST_URL = os.getenv("REST_URL", "http://localhost:8000")


def predict_rest(features: dict) -> dict:
    """Asks the REST service for a prediction with a GET request."""
    response = requests.get(f"{REST_URL}/predict", params=features, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("REST:", predict_rest(SAMPLE))
