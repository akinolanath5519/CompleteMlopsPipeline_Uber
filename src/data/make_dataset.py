import pandas as pd
from pathlib import Path

# ------------------------
# Project Root
# ------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # two levels up from src/data

# Paths
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "taxi_fares.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "processed_taxi_fares.csv"

# ------------------------
# Functions
# ------------------------
def load_raw_data():
    """
    Load raw taxi fare data from CSV files in 'data/raw/'.

    Columns: 'key', 'fare_amount', 'pickup_datetime', 
             'pickup_longitude', 'pickup_latitude', 
             'dropoff_longitude', 'dropoff_latitude', 'passenger_count'
    """
    if RAW_DATA_PATH.exists():
        df = pd.read_csv(RAW_DATA_PATH)
        print(f"[INFO] Loaded raw data with {len(df)} rows from {RAW_DATA_PATH}")
        return df
    else:
        print(f"[WARNING] Raw data file not found at {RAW_DATA_PATH}. Returning empty DataFrame.")
        return pd.DataFrame()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw taxi fare data.

    - Convert pickup_datetime to datetime
    - Ensure numeric columns are numeric
    - Remove rows with invalid coordinates (0,0)
    - Drop duplicates
    - Remove rows with missing fare_amount
    """
    if df.empty:
        return df

    # Drop duplicates
    df = df.drop_duplicates()

    # Convert pickup_datetime to datetime
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')

    # Ensure numeric columns
    numeric_cols = ['fare_amount', 'pickup_longitude', 'pickup_latitude',
                    'dropoff_longitude', 'dropoff_latitude', 'passenger_count']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove rows with missing fare or coordinates
    df = df.dropna(subset=['fare_amount', 'pickup_longitude', 'pickup_latitude',
                           'dropoff_longitude', 'dropoff_latitude'])

    # Remove invalid coordinates (0,0)
    df = df[(df['pickup_longitude'] != 0) & (df['pickup_latitude'] != 0)]

    print(f"[INFO] Cleaned data: {len(df)} rows remaining after cleaning.")
    return df

def save_processed_data(df: pd.DataFrame):
    """
    Save cleaned taxi fare data to 'data/processed/'.
    Creates the folder if it does not exist.
    """
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"[INFO] Processed data saved to {PROCESSED_DATA_PATH}")

# ------------------------
# Main
# ------------------------
if __name__ == "__main__":
    raw_df = load_raw_data()
    if not raw_df.empty:
        clean_df = clean_data(raw_df)
        save_processed_data(clean_df)
