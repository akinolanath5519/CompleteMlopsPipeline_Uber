from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
import uvicorn
import numpy as np
from datetime import datetime

# ------------------------
# Config
# ------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # adjust to project root
MODEL_PATH = PROJECT_ROOT / "models" / "saved" / "linear_regression_taxi_fare.pkl"

# Load the trained model
model = joblib.load(MODEL_PATH)

# ------------------------
# FastAPI app
# ------------------------
app = FastAPI(title="Taxi Fare Prediction API", version="1.0")

# Request model
class TaxiFareRequest(BaseModel):
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    passenger_count: int
    pickup_datetime: str  # Pass as ISO string: "YYYY-MM-DD HH:MM:SS"

# Response model
class TaxiFareResponse(BaseModel):
    fare_amount: float

# ------------------------
# Helper: calculate distance
# ------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6371 * c
    return km

# ------------------------
# Prediction endpoint
# ------------------------
@app.post("/predict", response_model=TaxiFareResponse)
def predict_fare(request: TaxiFareRequest):
    # Calculate trip distance
    trip_distance = haversine_distance(
        request.pickup_latitude,
        request.pickup_longitude,
        request.dropoff_latitude,
        request.dropoff_longitude
    )
    
    # Extract time features
    dt = pd.to_datetime(request.pickup_datetime)
    hour_of_day = dt.hour
    day_of_week = dt.dayofweek
    month = dt.month
    
    # Cap passenger count if needed
    passenger_count = min(request.passenger_count, 6)
    
    # Build input DataFrame with all features
    X = pd.DataFrame([[
        trip_distance,
        hour_of_day,
        day_of_week,
        month,
        passenger_count
    ]], columns=[
        "trip_distance_km",
        "hour_of_day",
        "day_of_week",
        "month",
        "passenger_count"
    ])
    
    # Predict fare
    fare_pred = model.predict(X)[0]
    return TaxiFareResponse(fare_amount=float(fare_pred))

# ------------------------
# Health check
# ------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------
# Run locally
# ------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
