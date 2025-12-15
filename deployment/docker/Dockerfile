# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (better caching)
COPY deployment/api/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app
COPY deployment/api/ ./deployment/api/

# Copy trained models
COPY models/saved/ ./models/saved/

# Expose port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "deployment.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
