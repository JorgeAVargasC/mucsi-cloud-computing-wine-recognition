#!/usr/bin/env bash
# Generates the gRPC Python stubs (wine_pb2.py, wine_pb2_grpc.py) from wine.proto
set -euo pipefail

cd "$(dirname "$0")"
python -m grpc_tools.protoc --proto_path=. ./wine.proto --python_out=. --grpc_python_out=.
echo "Stubs generated: wine_pb2.py, wine_pb2_grpc.py"
