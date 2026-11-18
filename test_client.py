"""Requests the same wine prediction through each microservice."""

import requests

from predictor import SAMPLE

REST_URL = "http://localhost:8000"


def predict_rest(features: dict) -> dict:
    """Asks the REST service for a prediction with a GET request."""
    response = requests.get(f"{REST_URL}/predict", params=features, timeout=5)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("REST:", predict_rest(SAMPLE))
