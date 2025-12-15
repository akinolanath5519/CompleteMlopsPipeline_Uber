import os

folders = [
    "data/raw",
    "data/processed",
    "data/interim",
    "data/external",

    "notebooks",
    "src",
    "src/data",
    "src/features",
    "src/models",
    "src/visualization",
    "src/pipelines",
    "src/utils",

    "models/saved",
    "models/registry",

    "configs",
    "configs/params",
    "configs/pipeline",

    "dvc_artifacts",
    "mlruns",                      # MLflow experiment directory
    "mlflow_registry",

    "deployment",
    "deployment/api",
    "deployment/docker",
    "deployment/kubernetes",

    "monitoring",
    "monitoring/logs",
    "monitoring/metrics",

    "tests",
    ".github/workflows"
]

files = {
    "README.md": "# MLOps Project\n\nGenerated folder structure.",
    "requirements.txt": "",
    "setup.py": "from setuptools import setup, find_packages\n\nsetup(name='mlops_project', packages=find_packages())",
    "dvc.yaml": "stages: {}",
    ".gitignore": "mlruns/\n__pycache__/\nmodels/\n.env",
    ".github/workflows/mlops-ci.yml": """
name: MLOps CI Pipeline

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Python
        uses: actions/setup-python@v3
        with:
          python-version: 3.10
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
""",
    "src/data/make_dataset.py": "def load_raw_data():\n    pass",
    "src/features/build_features.py": "def create_features():\n    pass",
    "src/models/train_model.py": "def train():\n    pass",
    "src/models/predict_model.py": "def predict():\n    pass",
    "src/pipelines/training_pipeline.py": "def run_training_pipeline():\n    pass",
    "deployment/api/app.py": "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {'message': 'ML Model API Running'}",
    "deployment/docker/Dockerfile": """
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "deployment.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
"""
}

def create_project():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content)

    print("🎉 MLOps project structure created successfully!")


if __name__ == "__main__":
    create_project()
