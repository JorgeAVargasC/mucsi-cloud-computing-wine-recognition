FROM python:3.14-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Model mounted as a volume, not copied
ENV MODEL_PATH=/models/wine-model.joblib
ENV REST_HOST=0.0.0.0
ENV REST_PORT=8000

COPY rest_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY model/__init__.py model/predictor.py ./model/
COPY rest_service/ ./rest_service/

EXPOSE 8000
ENTRYPOINT ["python", "-m", "rest_service.app"]
