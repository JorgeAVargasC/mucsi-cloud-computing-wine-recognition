# Wine Recognition · Microservicios

Clasificador de vinos (`model/wine-model.joblib`, entrenado en `model/wine_recognition.ipynb`) expuesto por **REST**, **gRPC** y **Kafka**.

## Kafka (Docker Compose)

Requiere Docker Desktop abierto. `docker-compose.yml` levanta el broker (`kafka`) y un contenedor de un solo uso (`kafka-init`) que crea los topics `wine-requests` y `wine-predictions` cuando el broker está listo.

| Paso | Comando |
|---|---|
| Levantar el broker y crear los topics | `docker compose up -d` |
| Ver el estado | `docker compose ps -a` (`kafka-init` debe salir con `Exited (0)`) |
| Listar los topics | `docker exec kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092` |
| Apagar (conserva los mensajes) | `docker compose stop` |
| Borrar todo | `docker compose down` |

### Probar a mano

| Terminal | Comando |
|---|---|
| Productor (escribe un mensaje por línea) | `docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic wine-requests --bootstrap-server localhost:9092` |
| Consumidor (lee desde el inicio) | `docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic wine-requests --from-beginning --bootstrap-server localhost:9092` |
