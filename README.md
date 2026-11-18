# Wine Recognition · Microservicios

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

## Ejecutar

| Terminal | Comando |
|---|---|
| 1 | `docker compose up -d` |
| 2 | `uvicorn rest_service.app:app --port 8000` |
| 3 | `python -m grpc_service.server` |
| 4 | `python -m kafka_service.worker` |
| 5 | `python test_client.py` |

Salida esperada: `{'label': 1}` en REST, gRPC y Kafka. Swagger: http://localhost:8000/docs

## Notas

- Stubs de gRPC: `./generate-stubs.sh` (solo si cambia `wine.proto`).
- Windows: el broker se anuncia en `127.0.0.1` (no `localhost`, que va por IPv6 y falla); `kafka-python==2.3.1` con `api_version=(3, 9)`.

## Evidencias

Las 3 vías devuelven la misma predicción:

![test_client.py](evidence/05-test-client-output.png)

Swagger, `GET /predict`:

![Swagger](evidence/09-rest-swagger-response.png)

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
