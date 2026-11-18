"""Requests the same wine prediction through each microservice."""

from model.predictor import SAMPLE
from rest_service.client import predict_rest
from grpc_service.client import predict_grpc
from kafka_service.client import predict_kafka

if __name__ == "__main__":
    print("REST:", predict_rest(SAMPLE))
    print("gRPC:", predict_grpc(SAMPLE))
    print("Kafka:", predict_kafka(SAMPLE))
