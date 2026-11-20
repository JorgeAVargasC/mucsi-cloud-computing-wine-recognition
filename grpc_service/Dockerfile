FROM python:3.14-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Model mounted as a volume, not copied
ENV MODEL_PATH=/models/wine-model.joblib
ENV GRPC_PORT=50051

COPY grpc_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY model/__init__.py model/predictor.py ./model/
COPY grpc_service/ ./grpc_service/

EXPOSE 50051
ENTRYPOINT ["python", "-m", "grpc_service.server"]
