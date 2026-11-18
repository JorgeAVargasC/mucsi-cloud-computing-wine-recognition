"""Kafka microservice: reads prediction requests and publishes the results."""

import json

from kafka import KafkaConsumer, KafkaProducer

from model.predictor import predict

KAFKA_BOOTSTRAP_SERVERS = "127.0.0.1:9092"
REQUESTS_TOPIC = "wine-requests"
PREDICTIONS_TOPIC = "wine-predictions"
# Fixed protocol version: automatic version detection fails against this broker
KAFKA_API_VERSION = (3, 9)


def serve() -> None:
    """Consumes requests forever and answers each one on the predictions topic."""
    consumer = KafkaConsumer(
        REQUESTS_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        api_version=KAFKA_API_VERSION,
        group_id="wine-predictor",
        auto_offset_reset="earliest",
        value_deserializer=json.loads,
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        api_version=KAFKA_API_VERSION,
        value_serializer=lambda value: json.dumps(value).encode(),
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
