"""Requests a wine prediction from the gRPC service."""

import os

import grpc

from grpc_service import wine_pb2, wine_pb2_grpc
from model.predictor import SAMPLE

GRPC_TARGET = os.getenv("GRPC_TARGET", "localhost:50051")


def predict_grpc(features: dict) -> dict:
    """Asks the gRPC service for a prediction with a unary call."""
    with grpc.insecure_channel(GRPC_TARGET) as channel:
        stub = wine_pb2_grpc.WinePredictorStub(channel)
        response = stub.Predict(wine_pb2.WineFeatures(**features), timeout=5)
    return {"label": response.label}


if __name__ == "__main__":
    print("gRPC:", predict_grpc(SAMPLE))
