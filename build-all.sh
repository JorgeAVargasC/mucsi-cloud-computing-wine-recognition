#!/usr/bin/env bash
# Pulls third-party images and builds the service images
set -euo pipefail

cd "$(dirname "$0")"

KAFKA_IMAGE="apache/kafka:3.9.1"
VERSION="1.0.0"

docker pull "$KAFKA_IMAGE"

docker build -f rest_service/Dockerfile -t "wine-rest:$VERSION" .
docker build -f grpc_service/Dockerfile -t "wine-grpc:$VERSION" .
docker build -f kafka_service/Dockerfile -t "wine-kafka-worker:$VERSION" .

docker images | grep -E "wine-|apache/kafka"
