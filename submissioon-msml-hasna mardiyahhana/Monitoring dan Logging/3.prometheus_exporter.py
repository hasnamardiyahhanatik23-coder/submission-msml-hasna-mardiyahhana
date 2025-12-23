"""prometheus_exporter.py

Jalankan service inference + metrics untuk dipantau Prometheus.
Endpoint:
- POST /predict  -> prediksi
- GET  /health   -> healthcheck
- GET  /metrics  -> metrik Prometheus

Cara run (lokal):
1) pip install -r requirements.txt
2) python prometheus_exporter.py

Lalu jalankan Prometheus (lihat 2.prometheus.yml):
- prometheus --config.file=2.prometheus.yml

Catatan:
- File model yang dipakai default: model.pkl (ubah di ENV MODEL_PATH kalau perlu).
"""

import os
import time
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# =========
# Prometheus metrics
# =========
REQUEST_COUNT = Counter(
    "inference_requests_total",
    "Total request ke endpoint inference",
    ["endpoint", "http_status"],
)
REQUEST_LATENCY = Histogram(
    "inference_request_latency_seconds",
    "Latency request inference (detik)",
    ["endpoint"],
)
PREDICTION_COUNT = Counter(
    "inference_predictions_total",
    "Total prediksi per label",
    ["label"],
)
INPROGRESS = Gauge(
    "inference_inprogress_requests",
    "Jumlah request inference yang sedang diproses"
)

MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

app = Flask(__name__)

def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file '{path}' tidak ditemukan. "
            "Simpan model kamu sebagai model.pkl di folder ini "
            "atau set ENV MODEL_PATH."
        )
    return joblib.load(path)

model = None

@app.before_request
def _before():
    INPROGRESS.inc()

@app.after_request
def _after(resp):
    INPROGRESS.dec()
    return resp

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}, 200

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.post("/predict")
def predict():
    start = time.time()
    endpoint = "/predict"

    try:
        payload = request.get_json(force=True, silent=False)

        data = payload.get("data")
        if data is None:
            raise ValueError("Format salah. Harus ada key 'data'.")

        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)

        y_pred = model.predict(df)

        for lbl in y_pred:
            PREDICTION_COUNT.labels(label=str(lbl)).inc()

        resp = {"predictions": [str(x) for x in y_pred]}
        REQUEST_COUNT.labels(endpoint=endpoint, http_status="200").inc()
        return jsonify(resp), 200

    except Exception as e:
        REQUEST_COUNT.labels(endpoint=endpoint, http_status="500").inc()
        return jsonify({"error": str(e)}), 500

    finally:
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - start)

if __name__ == "__main__":
    model = load_model(MODEL_PATH)
    app.run(host="0.0.0.0", port=8000, debug=False)

"""
CONTOH CURL:
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"data\": [{\"Gender\":\"Male\",\"Married\":\"No\",\"Dependents\":\"0\",\"Education\":\"Graduate\",\"Self_Employed\":\"No\",\"ApplicantIncome\":3254,\"CoapplicantIncome\":0,\"LoanAmount\":50,\"Loan_Amount_Term\":360,\"Credit_History\":1,\"Property_Area\":\"Urban\"}]}"
"""
