# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Non-interactive environment
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies for DVC
RUN apt-get update && \
    apt-get install -y --no-install-recommends git gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python packages and DVC
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir dvc[s3]  # replace [s3] with your remote type if needed

# Copy FastAPI app and DVC pipeline config
COPY deployment/api/ ./deployment/api/
COPY dvc.yaml dvc.lock .dvc/config ./

# Expose FastAPI port
EXPOSE 8000

# CMD: pull models from DVC at runtime, then run FastAPI
CMD ["sh", "-c", "dvc pull -v && uvicorn deployment.api.app:app --host 0.0.0.0 --port 8000"]
