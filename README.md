# MLOps Project

This project is a **production-ready MLOps structure** with DVC, MLflow, deployment, and monitoring.  
It is designed to handle the **full lifecycle of machine learning projects** from raw data to deployment and monitoring.

---

## 1️⃣ Project Overview

- **Goal:** Predict product sales/revenue using machine learning.
- **Key Features:**
  - Automated data ingestion and preprocessing
  - Feature engineering
  - Model training and experiment tracking with MLflow
  - Pipeline orchestration with DVC
  - Deployment via FastAPI + Docker
  - Monitoring and logging
  - Unit tests and CI/CD integration

---

## 2️⃣ Folder Structure & Workflow

mlops_project/
├── data/ # Raw, processed, and external data
├── notebooks/ # Exploratory notebooks
├── src/ # Source code
│ ├── data/ # Load and save datasets
│ ├── features/ # Feature engineering
│ ├── models/ # Training & prediction
│ ├── pipelines/ # Orchestration scripts
│ └── utils/ # Helper functions
├── models/ # Saved models & registry
├── configs/ # Config & hyperparameters
├── dvc_artifacts/ # DVC tracked files
├── mlruns/ # MLflow experiment logs
├── mlflow_registry/ # MLflow model registry
├── deployment/ # API, Docker, Kubernetes
├── monitoring/ # Logs and metrics
├── tests/ # Unit tests
└── .github/workflows/ # CI/CD GitHub Actions

markdown
Copy code

---

## 3️⃣ Workflow Steps

1. **Data Ingestion (`data/` + `make_dataset.py`)**
   - Load raw CSVs or external data sources.
   - Clean and save processed data.
   - **Example:** Retail store collects daily sales CSVs → save as `processed_sales.csv`.

2. **Feature Engineering (`src/features/build_features.py`)**
   - Transform processed data to create features for ML models.
   - **Example:** Add `total_revenue = price * quantity` for each product.

3. **Model Training (`src/models/train_model.py`)**
   - Train ML model using features.
   - Log experiments with MLflow (`mlruns/`).
   - Save model to `models/saved/latest_model.pkl`.
   - **Example:** Predict next week's sales revenue.

4. **Pipeline Orchestration (`src/pipelines/training_pipeline.py`)**
   - Automate steps: data → features → model training.
   - Integrate with **DVC** for versioned pipeline execution.

5. **Experiment Tracking (`mlruns/` & `mlflow_registry/`)**
   - Track metrics, parameters, and models.
   - Compare multiple runs to choose the best model.

6. **Deployment (`deployment/api/app.py`)**
   - Wrap model in REST API using FastAPI.
   - Containerize with Docker for production.
   - **Example:** Retail manager sends product info → receives predicted revenue.
6️⃣ Using DVC with DagsHub (Data Versioning + Remote Storage)

This project supports full data versioning and pipeline orchestration using DVC integrated with DagsHub.
DagsHub acts as both:

a Git remote (for code + .dvc files)

a DVC storage backend (for actual datasets, models, and artifacts)

6.1 Why Use DVC + DagsHub?

Track every version of your datasets

Share data across machines and teammates

Reproduce pipelines consistently

Store large files outside GitHub

Visualize DVC pipelines and metrics directly on DagsHub

6.2 Step-by-Step Setup
1️⃣ Add DagsHub as a Git Remote

After creating an empty repos on DagsHub:

git remote add dagshub https://dagshub.com/<username>/<repo>.git
git push -u dagshub main


This pushes code only, not datasets.

2️⃣ Initialize DVC (if not already done)
dvc init
git add .
git commit -m "Initialize DVC"
git push dagshub main

3️⃣ Track Your Dataset with DVC

Example: tracking a raw dataset:

dvc add data/raw/dataset.csv


This creates:

dataset.csv.dvc → tracked by Git

The raw data file → added to .gitignore

Commit & push the metadata:

git add data/raw/dataset.csv.dvc .gitignore
git commit -m "Track raw dataset with DVC"
git push dagshub main

4️⃣ Configure DVC Remote Storage on DagsHub

On your DagsHub repo:

Repository → DVC → Configure Remote
Copy the generated storage URL:

https://dagshub.com/<username>/<repo>.dagshub.storage


Add it locally:

dvc remote add -d dagshub-storage https://dagshub.com/<username>/<repo>.dagshub.storage
dvc remote default dagshub-storage

5️⃣ Push Data to DagsHub Storage

Upload your actual dataset:

dvc push


Your files now appear under the DVC tab on DagsHub.

6.3 Full Command Summary
# Track data
dvc add data/raw/dataset.csv

# Commit metadata
git add data/raw/dataset.csv.dvc .gitignore
git commit -m "Track dataset"

# Push metadata
git push dagshub main

# Push actual data
dvc push

6.4 How DVC + DagsHub Works in This Project

Data ingestion outputs (raw → processed) are versioned using DVC

Feature files, trained models, and artifacts can be stored with DVC

DagsHub stores:

Dataset versions

Model binaries

Pipeline outputs

Git stores:

Code

Pipeline definitions

.dvc pointer files

This ensures full reproducibility of your ML pipeline.

6.5 DagsHub UI Benefits

You can now view directly on DagsHub:

Versioned datasets

Pipeline DAGs

Model files

Metrics

MLflow runs (optional integration)

7. **Monitoring (`monitoring/`)**
   - Collect logs and metrics to monitor model performance.
   - Detect errors, data drift, or performance degradation.

8. **Testing (`tests/`)**
   - Unit tests for data loading, feature engineering, model training, and API endpoints.

9. **CI/CD (`.github/workflows/mlops-ci.yml`)**
   - Run automated tests on GitHub push.
   - Ensure code quality before deployment.

---

## 4️⃣ Workflow Flowchart

Raw Data (data/raw/)
↓
Data Ingestion (make_dataset.py)
↓
Processed Data (data/processed/)
↓
Feature Engineering (build_features.py)
↓
Training Pipeline (training_pipeline.py)
↓
Trained Model (models/saved/) → MLflow logs (mlruns/)
↓
Deployment API (deployment/api/app.py)
↓
Monitoring & Logging (monitoring/)

yaml
Copy code

**Optional integrations:**  
- **DVC:** Version datasets & models automatically.  
- **GitHub Actions:** CI/CD for testing and deployment.  
- **Docker/Kubernetes:** Scalable production deployment.

---

## 5️⃣ How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
Run the training pipeline:

bash
Copy code
python src/pipelines/training_pipeline.py
Start API:

bash
Copy code
uvicorn deployment.api.app:app --reload
Track experiments:

bash
Copy code
mlflow ui
Run tests:

bash
Copy code
pytest
6️⃣ Real-Life Use Case Example
A retail chain collects daily sales data from multiple stores.

The MLOps pipeline:

Ingests daily sales CSVs.

Creates features like total_revenue.

Trains a model to predict next week's sales.

Logs all experiments with MLflow.

Deploys API to provide live predictions to store managers.

Monitors predictions to detect anomalies or data drift.