# Wine Recognition · Microservicios

Clasificador de vinos (`model/wine-model.joblib`, entrenado en `model/wine_recognition.ipynb`) expuesto por **REST**, **gRPC** y **Kafka**.

## Kafka (Docker Compose)

Requiere Docker Desktop abierto. `docker-compose.yml` levanta un broker Kafka de un nodo. Los topics `wine-requests` y `wine-predictions` se crean solos la primera vez que se usan.

> **Git Bash en Windows:** antepón `MSYS_NO_PATHCONV=1` a los comandos `docker exec` (o usa `//opt/...`); si no, Git Bash convierte `/opt/...` en `C:/Program Files/Git/opt/...`.

| Paso | Comando |
|---|---|
| Levantar el broker | `docker compose up -d` |
| Ver el estado | `docker compose ps` |
| Listar los topics | `docker exec kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092` |
| Apagar (conserva los mensajes) | `docker compose stop` |
| Borrar todo | `docker compose down` |

### Probar a mano

| Terminal | Comando |
|---|---|
| Productor (escribe un mensaje por línea) | `docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic wine-requests --bootstrap-server localhost:9092` |
| Consumidor (lee desde el inicio) | `docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic wine-requests --from-beginning --bootstrap-server localhost:9092` |
