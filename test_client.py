"""Requests the same wine prediction through each microservice."""

import grpc
import requests

import wine_pb2
import wine_pb2_grpc
from predictor import SAMPLE

REST_URL = "http://localhost:8000"
GRPC_TARGET = "localhost:50051"


def predict_rest(features: dict) -> dict:
    """Asks the REST service for a prediction with a GET request."""
    response = requests.get(f"{REST_URL}/predict", params=features, timeout=5)
    response.raise_for_status()
    return response.json()


def predict_grpc(features: dict) -> dict:
    """Asks the gRPC service for a prediction with a unary call."""
    with grpc.insecure_channel(GRPC_TARGET) as channel:
        stub = wine_pb2_grpc.WinePredictorStub(channel)
        response = stub.Predict(wine_pb2.WineFeatures(**features), timeout=5)
    return {"label": response.label}


if __name__ == "__main__":
    print("REST:", predict_rest(SAMPLE))
    print("gRPC:", predict_grpc(SAMPLE))
