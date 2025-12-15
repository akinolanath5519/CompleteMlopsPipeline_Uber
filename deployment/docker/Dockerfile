# Use a slim Python image
FROM python:3.10-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies for DVC and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir dvc[s3]  # change [s3] if needed

# Copy FastAPI app and DVC config files
COPY deployment/api/ ./deployment/api/
COPY dvc.yaml dvc.lock .dvc/config ./

# Pull models from DVC remote
RUN dvc pull -v

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "deployment.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
