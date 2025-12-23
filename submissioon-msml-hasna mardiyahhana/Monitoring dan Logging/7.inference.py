"""inference.py

Client test untuk bukti serving (Kriteria 4).
Pastikan service sudah jalan dulu:
python prometheus_exporter.py

Lalu:
python inference.py
"""

import requests

URL = "http://localhost:8000/predict"

payload = {
  "data": [
    {
      "Gender": "Male",
      "Married": "No",
      "Dependents": "0",
      "Education": "Graduate",
      "Self_Employed": "No",
      "ApplicantIncome": 3254,
      "CoapplicantIncome": 0,
      "LoanAmount": 50,
      "Loan_Amount_Term": 360,
      "Credit_History": 1,
      "Property_Area": "Urban"
    }
  ]
}

if __name__ == "__main__":
    r = requests.post(URL, json=payload, timeout=30)
    print("Status:", r.status_code)
    print("Response:", r.text)

    with open("1.bukti_serving/response_predict.json", "w", encoding="utf-8") as f:
        f.write(r.text)
