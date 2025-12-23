import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# =====================
# Load Dataset
# =====================
data = pd.read_csv("loan_prediction.csv")  # sesuaikan nama file dataset

X = data.drop("Loan_Status", axis=1)
y = data["Loan_Status"]

# =====================
# Split Data
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
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

    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("precision", prec)
    mlflow.log_metric("recall", rec)
    mlflow.log_metric("f1_score", f1)

    mlflow.sklearn.log_model(pipeline, "model")

