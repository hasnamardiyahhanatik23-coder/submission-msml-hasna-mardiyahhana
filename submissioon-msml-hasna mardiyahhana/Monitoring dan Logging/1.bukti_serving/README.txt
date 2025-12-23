# 1.bukti_serving (WAJIB)

Masukkan bukti bahwa inference service berjalan.

Minimal isi folder ini:
- screenshot_serving_terminal.png
  - terminal menjalankan: `python prometheus_exporter.py`
  - terlihat "Running on http://0.0.0.0:8000"

- screenshot_request_predict.png
  - bukti request POST /predict via Postman / curl
  - terlihat response JSON `predictions`

Bonus (otomatis dibuat kalau kamu run `python inference.py`):
- response_predict.json
