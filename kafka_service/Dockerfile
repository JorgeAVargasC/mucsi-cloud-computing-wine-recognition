FROM python:3.14-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Model mounted as a volume, not copied
ENV MODEL_PATH=/models/wine-model.joblib
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092
ENV REQUESTS_TOPIC=wine-requests
ENV PREDICTIONS_TOPIC=wine-predictions
ENV CONSUMER_GROUP=wine-predictor
ENV KAFKA_CONNECT_RETRIES=30
ENV KAFKA_CONNECT_WAIT_SECONDS=2

COPY kafka_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY model/__init__.py model/predictor.py ./model/
COPY kafka_service/ ./kafka_service/

ENTRYPOINT ["python", "-m", "kafka_service.worker"]
