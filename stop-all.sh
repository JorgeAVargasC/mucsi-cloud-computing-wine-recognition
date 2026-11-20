#!/usr/bin/env bash
# Stops the containers and removes the network
set -uo pipefail

NETWORK="wine-net"

# --rm removes each container when it stops
docker stop wine-kafka-worker wine-grpc wine-rest kafka 2>/dev/null || true

docker network rm "$NETWORK"

docker ps -a
docker network ls
