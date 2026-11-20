#!/usr/bin/env bash
# Creates the network and starts Kafka and the three services
set -euo pipefail

cd "$(dirname "$0")"

# Git Bash on Windows rewrites paths in docker arguments; pwd -W gives the Windows path
export MSYS_NO_PATHCONV=1
MODEL_DIR="$(pwd -W 2>/dev/null || pwd)/model"

NETWORK="wine-net"
KAFKA_IMAGE="apache/kafka:3.9.1"
VERSION="1.0.0"

docker network inspect "$NETWORK" >/dev/null 2>&1 || docker network create "$NETWORK"

# INTERNAL is for containers (kafka:9092), EXTERNAL for the test client on the host (127.0.0.1:29092)
docker run -d --rm --name kafka --network "$NETWORK" --network-alias kafka \
  -p 29092:29092 \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_LISTENERS=INTERNAL://:9092,EXTERNAL://:29092,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=INTERNAL://kafka:9092,EXTERNAL://127.0.0.1:29092 \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT \
  -e KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
  "$KAFKA_IMAGE"

docker run -d --rm --name wine-rest --network "$NETWORK" --network-alias rest \
  -p 8000:8000 \
  -e REST_PORT=8000 \
  -e MODEL_PATH=/models/wine-model.joblib \
  -v "$MODEL_DIR:/models:ro" \
  "wine-rest:$VERSION"

docker run -d --rm --name wine-grpc --network "$NETWORK" --network-alias grpc \
  -p 50051:50051 \
  -e GRPC_PORT=50051 \
  -e MODEL_PATH=/models/wine-model.joblib \
  -v "$MODEL_DIR:/models:ro" \
  "wine-grpc:$VERSION"

docker run -d --rm --name wine-kafka-worker --network "$NETWORK" --network-alias kafka-worker \
  -e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
  -e REQUESTS_TOPIC=wine-requests \
  -e PREDICTIONS_TOPIC=wine-predictions \
  -e MODEL_PATH=/models/wine-model.joblib \
  -v "$MODEL_DIR:/models:ro" \
  "wine-kafka-worker:$VERSION"

docker ps
