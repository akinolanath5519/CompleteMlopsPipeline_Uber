from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Two levels up from src/configs

# Data paths
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "taxi_fares.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "processed_taxi_fares.csv"

# Logs
LOG_DIR = PROJECT_ROOT / "monitoring" / "logs"
LOG_FILE = LOG_DIR / "app.log"

# Models
MODEL_DIR = PROJECT_ROOT / "models" / "saved"
