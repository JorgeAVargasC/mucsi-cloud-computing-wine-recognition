#!/usr/bin/env bash
# Generates the gRPC Python stubs (grpc_service/wine_pb2*.py) from grpc_service/wine.proto
set -euo pipefail

cd "$(dirname "$0")"
python -m grpc_tools.protoc --proto_path=. ./grpc_service/wine.proto --python_out=. --grpc_python_out=.
echo "Stubs generated in grpc_service/"
