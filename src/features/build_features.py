import pandas as pd
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

# ------------------------
# Project Root
# ------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # two levels up

RAW_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_taxi_fares.csv"
FEATURES_DATA_DIR = PROJECT_ROOT / "data" / "features"
FEATURES_DATA_PATH = FEATURES_DATA_DIR / "features_taxi_fares.csv"

# ------------------------
# Helper functions
# ------------------------
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance (km) between two points on the Earth.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

# ------------------------
# Main feature engineering
# ------------------------
def build_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    # Trip distance in km
    df['trip_distance_km'] = df.apply(
        lambda row: haversine(row['pickup_longitude'], row['pickup_latitude'],
                              row['dropoff_longitude'], row['dropoff_latitude']), axis=1
    )

    # Time features
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
    df['hour_of_day'] = df['pickup_datetime'].dt.hour
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['month'] = df['pickup_datetime'].dt.month

    # Optionally cap passenger count
    df['passenger_count'] = df['passenger_count'].clip(upper=6)

    print(f"[INFO] Feature engineering complete. Dataset now has {df.shape[1]} columns.")
    return df

def save_features(df: pd.DataFrame):
    FEATURES_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEATURES_DATA_PATH, index=False)
    print(f"[INFO] Features saved to {FEATURES_DATA_PATH}")

# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    if RAW_DATA_PATH.exists():
        df = pd.read_csv(RAW_DATA_PATH)
        df = build_features(df)
        save_features(df)
    else:
        print(f"[WARNING] Processed data not found at {RAW_DATA_PATH}. Run make_dataset.py first.")
