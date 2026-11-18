"""Requests a wine prediction through Kafka and waits for the matching answer."""

import json
import uuid

from kafka import KafkaConsumer, KafkaProducer

from kafka_service.worker import (
    KAFKA_API_VERSION,
    KAFKA_BOOTSTRAP_SERVERS,
    PREDICTIONS_TOPIC,
    REQUESTS_TOPIC,
)
from model.predictor import SAMPLE


def predict_kafka(features: dict) -> dict:
    """Sends a request to the worker and returns the prediction with the same request_id."""
    request_id = str(uuid.uuid4())

    # Created before sending so the answer cannot arrive before we listen
    consumer = KafkaConsumer(
        PREDICTIONS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        api_version=KAFKA_API_VERSION,
        group_id=f"test-client-{request_id}",
        auto_offset_reset="earliest",
        consumer_timeout_ms=10000,
        value_deserializer=json.loads,
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        api_version=KAFKA_API_VERSION,
        value_serializer=lambda value: json.dumps(value).encode(),
    )
    producer.send(REQUESTS_TOPIC, {"request_id": request_id, "features": features})
    producer.flush()

    try:
        for message in consumer:
            response = message.value
            if response["request_id"] == request_id:
                return {"label": response["label"]}
    finally:
        consumer.close()
        producer.close()

    raise TimeoutError(f"No Kafka answer for request {request_id} after 10 s")


if __name__ == "__main__":
    print("Kafka:", predict_kafka(SAMPLE))
