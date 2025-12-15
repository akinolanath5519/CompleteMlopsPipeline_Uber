FROM python:3.10-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends git gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir dvc[s3]

COPY deployment/api/ ./deployment/api/
COPY dvc.yaml dvc.lock .dvc/config ./

EXPOSE 8000

CMD ["sh", "-c", "dvc pull -v && uvicorn deployment.api.app:app --host 0.0.0.0 --port 8000"]

