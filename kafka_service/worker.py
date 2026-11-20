"""Kafka microservice: reads prediction requests and publishes the results."""

import json
import os
import time

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

from model.predictor import predict

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
REQUESTS_TOPIC = os.getenv("REQUESTS_TOPIC", "wine-requests")
PREDICTIONS_TOPIC = os.getenv("PREDICTIONS_TOPIC", "wine-predictions")
CONSUMER_GROUP = os.getenv("CONSUMER_GROUP", "wine-predictor")
# Fixed protocol version: automatic version detection fails against this broker
KAFKA_API_VERSION = (3, 9)
CONNECT_RETRIES = int(os.getenv("KAFKA_CONNECT_RETRIES", "30"))
CONNECT_WAIT_SECONDS = int(os.getenv("KAFKA_CONNECT_WAIT_SECONDS", "2"))


def connect(create):
    """Calls create() until the broker answers, because the container may start before Kafka is ready."""
    for attempt in range(1, CONNECT_RETRIES + 1):
        try:
            return create()
        except NoBrokersAvailable:
            print(f"Kafka not ready at {KAFKA_BOOTSTRAP_SERVERS} (attempt {attempt}/{CONNECT_RETRIES})")
            time.sleep(CONNECT_WAIT_SECONDS)
    raise RuntimeError(f"Kafka not reachable at {KAFKA_BOOTSTRAP_SERVERS} after {CONNECT_RETRIES} attempts")


def serve() -> None:
    """Consumes requests forever and answers each one on the predictions topic."""
    consumer = connect(
        lambda: KafkaConsumer(
            REQUESTS_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            api_version=KAFKA_API_VERSION,
            group_id=CONSUMER_GROUP,
            auto_offset_reset="earliest",
            value_deserializer=json.loads,
        )
    )
    producer = connect(
        lambda: KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            api_version=KAFKA_API_VERSION,
            value_serializer=lambda value: json.dumps(value).encode(),
        )
    )
    print(f"Kafka worker listening on '{REQUESTS_TOPIC}'")

    for message in consumer:
        request = message.value
        result = predict(request["features"])
        response = {"request_id": request["request_id"], **result}
        producer.send(PREDICTIONS_TOPIC, response)
        producer.flush()
        print(f"Kafka request {request['request_id']} -> {result}")


if __name__ == "__main__":
    serve()
