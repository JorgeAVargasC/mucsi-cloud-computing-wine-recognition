#!/usr/bin/env bash
# Prints the predictions published by the worker
MSYS_NO_PATHCONV=1 docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh \
  --topic wine-predictions --from-beginning --bootstrap-server localhost:9092
