# tests/test_app.py
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from deployment.api.app import app  # import your FastAPI apps

client = TestClient(app)

# ------------------------
# Health endpoint tests
# ------------------------
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# ------------------------
# Predict endpoint test
# ------------------------
def test_predict():
    payload = {
        "pickup_longitude": -73.985428,
        "pickup_latitude": 40.748817,
        "dropoff_longitude": -73.985428,
        "dropoff_latitude": 40.748817,
        "passenger_count": 1,
        "hour_of_day": 12,
        "day_of_week": 2,
        "month": 6
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "fare_amount" in data
    assert isinstance(data["fare_amount"], float)
