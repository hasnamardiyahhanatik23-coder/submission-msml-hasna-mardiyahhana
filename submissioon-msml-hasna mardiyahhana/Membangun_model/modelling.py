import os
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# =====================
# Load Dataset (PREPROCESSED)
# =====================
# Dicoding biasanya minta dataset yang dipakai untuk training adalah hasil preprocessing, bukan raw.
# Simpan dataset siap-latih di salah satu path berikut (pilih salah satu dan pastikan file-nya ada).
CANDIDATE_PATHS = [
    "namadataset_preprocessing/loan_preprocessed.csv",
    "namadataset_preprocessing.csv",
    "loan_preprocessed.csv",
    "loan_prediction.csv",  # fallback kalau kamu memang pakai ini (pastikan file ada)
]

dataset_path = None
for p in CANDIDATE_PATHS:
    if os.path.exists(p):
        dataset_path = p
        break

if dataset_path is None:
    raise FileNotFoundError(
        "Dataset tidak ditemukan. Taruh dataset hasil preprocessing di salah satu path ini:\n"
        + "\n".join([f"- {p}" for p in CANDIDATE_PATHS])
    )

data = pd.read_csv(dataset_path)

# Pastikan kolom target ada
if "Loan_Status" not in data.columns:
    raise ValueError("Kolom target 'Loan_Status' tidak ditemukan di dataset.")

X = data.drop("Loan_Status", axis=1)
y = data["Loan_Status"]

# =====================
# Split Data
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =====================
# Model Pipeline
# =====================
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=200))
])

# =====================
# MLflow Experiment
# =====================
mlflow.set_experiment("Loan Prediction Experiment")

with mlflow.start_run():
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label="Y")
    rec = recall_score(y_test, y_pred, pos_label="Y")
    f1 = f1_score(y_test, y_pred, pos_label="Y")

    mlflow.log_param("dataset_path", dataset_path)
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("max_iter", 200)

    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("precision", prec)
    mlflow.log_metric("recall", rec)
    mlflow.log_metric("f1_score", f1)

    mlflow.sklearn.log_model(pipeline, "model")

    print("Training selesai ✅")
    print("Dataset:", dataset_path)
    print("Accuracy:", acc)
