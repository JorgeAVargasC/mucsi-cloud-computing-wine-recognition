"""gRPC microservice that exposes the wine model through a unary call."""

from concurrent import futures

import grpc

import wine_pb2
import wine_pb2_grpc
from predictor import FEATURES, predict

GRPC_PORT = 50051


class WinePredictor(wine_pb2_grpc.WinePredictorServicer):
    """Implements the WinePredictor service defined in wine.proto."""

    def Predict(self, request, context):
        """Receives a WineFeatures message and returns a Prediction message."""
        features = {name: getattr(request, name) for name in FEATURES}
        result = predict(features)
        print(f"gRPC request -> {result}")
        return wine_pb2.Prediction(**result)


def serve() -> None:
    """Starts the gRPC server and blocks until it is stopped."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    wine_pb2_grpc.add_WinePredictorServicer_to_server(WinePredictor(), server)
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    server.start()
    print(f"gRPC server listening on port {GRPC_PORT}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
