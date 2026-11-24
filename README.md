# Wine Recognition · Microservicios

**[Jorge Andrés Vargas Cordoba](https://github.com/JorgeAVargasC)** · Cloud Computing · MUCSI, Universidad de Deusto

Clasificador de vinos expuesto por **REST**, **gRPC** y **Kafka**.

| Carpeta | Contenido |
|---|---|
| `model/` | modelo, notebook y `predictor.py` (compartido por los 3 servicios) |
| `rest_service/` | FastAPI · `GET /predict` |
| `grpc_service/` | `wine.proto`, stubs y servidor |
| `kafka_service/` | worker: `wine-requests` → `wine-predictions` |
| `test_client.py` | prueba las 3 vías |

## Instalar

```bash
./install-requirements.sh
source .venv/Scripts/activate
```

## Ejecutar sin Docker

| Terminal | Comando |
|---|---|
| 1 | `docker compose up -d` |
| 2 | `uvicorn rest_service.app:app --port 8000` |
| 3 | `python -m grpc_service.server` |
| 4 | `python -m kafka_service.worker` |
| 5 | `python test_client.py` |

Salida esperada: `{'label': 1}` en REST, gRPC y Kafka. Swagger: http://localhost:8000/docs

## Docker

Cada servicio tiene su imagen (`wine-rest`, `wine-grpc`, `wine-kafka-worker`, versión `1.0.0`) y Kafka usa `apache/kafka:3.9.1`. Se construyen desde la raíz del repo.

| Script | Qué hace |
|---|---|
| `./build-all.sh` | `docker pull` de Kafka y `docker build` de las 3 imágenes propias |
| `./run-all.sh` | crea la red `wine-net` y lanza Kafka, REST, gRPC y el worker |
| `./stop-all.sh` | para los contenedores y elimina la red |

```bash
./build-all.sh
./run-all.sh
KAFKA_BOOTSTRAP_SERVERS=127.0.0.1:29092 python test_client.py
./stop-all.sh
```

- El modelo no está dentro de las imágenes: se monta como volumen de solo lectura en `/models` y se localiza con `MODEL_PATH`. Cambiar el modelo no requiere reconstruir.
- Dentro de la red, los servicios se encuentran por alias: `kafka:9092`. Desde el equipo, el cliente usa `127.0.0.1:29092`, que es el segundo listener de Kafka.
- Los scripts y el `docker-compose.yml` usan los mismos nombres de contenedor (`kafka`, `wine-rest`, ...): no los ejecutes a la vez. Haz `./stop-all.sh` o `docker compose down` antes de cambiar de uno a otro.

### Variables de entorno

| Variable | Default | Servicio |
|---|---|---|
| `REST_HOST` / `REST_PORT` | `0.0.0.0` / `8000` | REST |
| `GRPC_PORT` | `50051` | gRPC |
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:9092` en la imagen, `127.0.0.1:9092` en local | worker y cliente |
| `REQUESTS_TOPIC` / `PREDICTIONS_TOPIC` | `wine-requests` / `wine-predictions` | worker y cliente |
| `CONSUMER_GROUP` | `wine-predictor` | worker |
| `KAFKA_CONNECT_RETRIES` / `KAFKA_CONNECT_WAIT_SECONDS` | `30` / `2` | worker |
| `MODEL_PATH` | `/models/wine-model.joblib` en la imagen | los 3 servicios |
| `REST_URL` / `GRPC_TARGET` | `http://localhost:8000` / `localhost:50051` | clientes |

La lista completa está en `.env.example`.

## Docker Compose

`docker-compose.yml` levanta todo el sistema: ZooKeeper, Kafka, Kafdrop y los 3 servicios. Equivale a los 3 scripts anteriores.

| Script | Compose |
|---|---|
| `./build-all.sh` | `docker compose build` |
| `./run-all.sh` | `docker compose up -d` |
| `./stop-all.sh` | `docker compose down` |

```bash
docker compose build
docker compose up -d
KAFKA_BOOTSTRAP_SERVERS=127.0.0.1:29092 python test_client.py
docker compose down
```

| Servicio | Contenedor | Puerto |
|---|---|---|
| `zookeeper` | `zookeeper` | `22181:2181` |
| `kafka` | `kafka` | `29092` (este equipo), `29093` (otros equipos); `9092` solo dentro de la red |
| `kafdrop` | `kafdrop` | `9000` · http://localhost:9000 |
| `rest` | `wine-rest` | `8000` |
| `grpc` | `wine-grpc` | `50051` |
| `kafka-worker` | `wine-kafka-worker` | ninguno |

- Rutas de build relativas (`context: .`): funciona igual en cualquier equipo.
- Los servicios se encuentran por nombre dentro de la red `wine-recognition_default` (`kafka:9092`).
- Kafka tiene `healthcheck` y el worker y Kafdrop esperan a que esté `healthy`.
- Los datos de Kafka y ZooKeeper se guardan en `Kafka/kafka-storage/` (ignorada por Git), así que sobreviven a `docker compose down`.
- Para clientes en otros equipos, define `KAFKA_HOST_IP` en un `.env` (ver `.env.example`); por defecto `127.0.0.1`.

Diferencias con el enunciado:
- Kafka publica `29092` y `29093`, no `22181:2181`: ese puerto ya es de ZooKeeper.
- `EXTERNAL_SAME_HOST` se anuncia como `127.0.0.1:29092` y no `localhost`, que en Windows resuelve primero a IPv6 y falla.
- La IP `192.168.5.242` del ejemplo se sustituye por `KAFKA_HOST_IP`.
- Imágenes fijas: `confluentinc/cp-zookeeper:7.6.1`, `confluentinc/cp-kafka:7.6.1` y `obsidiandynamics/kafdrop:4.0.2`.

## Notas

- Stubs de gRPC: `./generate-stubs.sh` (solo si cambia `wine.proto`).
- Windows: el broker se anuncia en `127.0.0.1` (no `localhost`, que va por IPv6 y falla); `kafka-python==2.3.1` con `api_version=(3, 9)`.

## Evidencias

Las 3 vías devuelven la misma predicción:

![test_client.py](evidence/05-test-client-output.png)

Swagger, `GET /predict`:

![Swagger](evidence/09-rest-swagger-response.png)

## Evidencias Docker

Construcción de las imágenes (`./build-all.sh`):

![build-all](evidence/docker/01-build-all.png)

Lanzamiento de los contenedores (`./run-all.sh`):

![run-all](evidence/docker/02-run-all.png)

Contenedores en ejecución y worker de Kafka escuchando:

![Contenedores](evidence/docker/03-containers-status.png)

Red `wine-net` con los 4 contenedores:

![Red](evidence/docker/04-network-inspect.png)

Docker Desktop:

![Docker Desktop](evidence/docker/05-docker-desktop.png)

Prueba con `test_client.py` contra los contenedores:

![test_client](evidence/docker/06-test-client.png)

Logs de los tres servicios tras la prueba:

![Logs](evidence/docker/07-service-logs.png)

Parada de los contenedores y borrado de la red (`./stop-all.sh`):

![stop-all](evidence/docker/08-stop-all.png)

## Evidencias Docker Compose

Stack de Kafka levantado (`docker compose up -d zookeeper kafka kafdrop`):

![Stack de Kafka levantado (`docker compose up -d zookeeper kafka kafdrop`)](evidence/compose/01-compose-up.png)

ZooKeeper, Kafka y Kafdrop en Docker Desktop:

![ZooKeeper, Kafka y Kafdrop en Docker Desktop](evidence/compose/02-docker-desktop.png)

Kafdrop con el broker:

![Kafdrop con el broker](evidence/compose/03-kafdrop-broker.png)

Construcción de las imágenes (`docker compose build`):

![Construcción de las imágenes (`docker compose build`)](evidence/compose/04-compose-build.png)

Los 6 contenedores levantados (`docker compose up -d`):

![Los 6 contenedores levantados (`docker compose up -d`)](evidence/compose/05-compose-up-all.png)

Proyecto `wine-recognition` en Docker Desktop:

![Proyecto `wine-recognition` en Docker Desktop](evidence/compose/06-docker-desktop-all.png)

Red `wine-recognition_default`:

![Red `wine-recognition_default`](evidence/compose/07-network-ls.png)

Prueba con `test_client.py`:

![Prueba con `test_client.py`](evidence/compose/08-test-client.png)

Logs de los tres servicios tras la prueba:

![Logs de los tres servicios tras la prueba](evidence/compose/09-service-logs.png)

Kafdrop con los topics `wine-requests` y `wine-predictions`:

![Kafdrop con los topics `wine-requests` y `wine-predictions`](evidence/compose/10-kafdrop-topics.png)

Swagger, `GET /predict`:

![Swagger, `GET /predict`](evidence/compose/11-swagger-response.png)

## Anexos

### A1 · Kafka levantado con Docker Compose

![Kafka levantado con Docker Compose](evidence/01-kafka-compose-up.png)

### A2 · Servicio REST arrancado

![Servicio REST arrancado](evidence/02-rest-service-running.png)

### A3 · Servidor gRPC arrancado

![Servidor gRPC arrancado](evidence/03-grpc-server-running.png)

### A4 · Worker de Kafka arrancado

![Worker de Kafka arrancado](evidence/04-kafka-worker-running.png)

### A5 · Log REST de la petición

![Log REST de la petición](evidence/06-rest-request-log.png)

### A6 · Log gRPC de la petición

![Log gRPC de la petición](evidence/07-grpc-request-log.png)

### A7 · Log del worker de Kafka

![Log del worker de Kafka](evidence/08-kafka-request-log.png)

### A8 · Contenedor Kafka en Docker Desktop

![Contenedor Kafka en Docker Desktop](evidence/10-docker-kafka-container.png)
