import sys
from pathlib import Path
import subprocess
import pandas as pd

# ------------------------
# Project Root
# ------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Paths
FEATURES_DATA_PATH = PROJECT_ROOT / "data" / "features" / "features_taxi_fares.csv"

# Scripts
BUILD_FEATURES_SCRIPT = PROJECT_ROOT / "src" / "features" / "build_features.py"
TRAIN_MODEL_SCRIPT = PROJECT_ROOT / "src" / "models" / "train_model.py"

# ------------------------
# Helper function to run scripts
# ------------------------
def run_script(script_path):
    print(f"[PIPELINE] Running {script_path.name} ...")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'  # replaces unprintable characters
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at {script_path.name}")
    
    print(f"[PIPELINE] {script_path.name} completed successfully.\n")

# ------------------------
# Pipeline Steps
# ------------------------
def main():
    print("[PIPELINE] Starting Training Pipeline ...\n")

    # Step 1: Build features
    print("[STEP 1] Building features")
    run_script(BUILD_FEATURES_SCRIPT)

    # Step 2: Train the model
    print("[STEP 2] Training the model")
    run_script(TRAIN_MODEL_SCRIPT)

    # Step 3: Optional - Load features to confirm pipeline output
    if FEATURES_DATA_PATH.exists():
        df = pd.read_csv(FEATURES_DATA_PATH)
        print(f"[STEP 3] Features shape: {df.shape}")
    else:
        print(f"[WARNING] Features file not found at {FEATURES_DATA_PATH}")

    print("\n[PIPELINE] Training pipeline completed successfully.")

# ------------------------
# Entry point
# ------------------------
if __name__ == "__main__":
    main()
