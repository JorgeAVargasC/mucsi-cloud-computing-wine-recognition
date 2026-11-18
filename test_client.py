"""Requests the same wine prediction through each microservice."""

from grpc_service.test_grpc import predict_grpc
from kafka_service.test_kafka import predict_kafka
from model.predictor import SAMPLE
from rest_service.test_rest import predict_rest

if __name__ == "__main__":
    print("REST:", predict_rest(SAMPLE))
    print("gRPC:", predict_grpc(SAMPLE))
    print("Kafka:", predict_kafka(SAMPLE))
