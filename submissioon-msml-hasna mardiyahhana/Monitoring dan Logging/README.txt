MONITORING DAN LOGGING
Nama: Hasna Mardiyahhana
Submission: Proyek Akhir MSML Dicoding

==================================================
1. Tujuan
==================================================
Monitoring dan Logging bertujuan untuk memantau performa sistem inference
machine learning secara real-time, memastikan layanan berjalan dengan baik,
serta mendeteksi potensi masalah melalui metrik dan alerting.

Sistem monitoring ini dibangun menggunakan Prometheus dan Grafana.

==================================================
2. Arsitektur Monitoring
==================================================
Alur monitoring yang digunakan adalah sebagai berikut:

1. File inference.py menjalankan service inference berbasis Flask.
2. File prometheus_exporter.py menambahkan endpoint /metrics
   yang mengekspor metrik inference.
3. Prometheus melakukan scraping metrik dari endpoint /metrics
   sesuai konfigurasi pada prometheus.yml.
4. Grafana digunakan untuk memvisualisasikan metrik dari Prometheus
   dalam bentuk dashboard.
5. Grafana Alerting digunakan untuk membuat aturan alert (alert rules)
   berdasarkan metrik tertentu.

==================================================
3. Prometheus
==================================================
File konfigurasi Prometheus terdapat pada:
- 2.prometheus.yml

Konfigurasi ini mendefinisikan:
- scrape_interval dan evaluation_interval
- job_name: loan_inference_service
- metrics_path: /metrics
- target: localhost:8000

Bukti monitoring Prometheus disertakan pada folder:
- 4.bukti monitoring Prometheus

Screenshot menunjukkan target Prometheus berstatus UP
dan metrik dapat di-scrape dengan baik.

==================================================
4. Metrics yang Dimonitor
==================================================
Metrics yang diekspor melalui prometheus_exporter.py meliputi:

1. inference_requests_total
   - Total jumlah request ke endpoint inference

2. inference_request_latency_seconds
   - Waktu latency inference (dalam detik)

3. inference_predictions_total
   - Total jumlah prediksi berdasarkan label

4. inference_inprogress_requests
   - Jumlah request inference yang sedang diproses

Metrics ini digunakan sebagai dasar visualisasi dan alerting.

==================================================
5. Grafana Dashboard
==================================================
Grafana digunakan untuk memvisualisasikan metrik dari Prometheus.

Dashboard menampilkan panel:
- CPU / Memory / Resource (demo)
- Request inference
- Latency inference
- Distribusi prediksi

Nama dashboard disesuaikan dengan username Dicoding:
dashboard-hasna_mardiyahhana_r6W5

Bukti monitoring Grafana disertakan pada folder:
- 5.bukti monitoring Grafana

==================================================
6. Alerting Grafana
==================================================
Grafana Alerting digunakan untuk membuat alert rules
berdasarkan kondisi metrik tertentu.

Alert rules ditampilkan pada menu:
Alerts & IRM → Alert rules

Bukti alerting Grafana disertakan pada folder:
- 6.bukti alerting Grafana

Screenshot menunjukkan daftar alert rules yang terdaftar
dan dapat digunakan untuk notifikasi jika kondisi tertentu terpenuhi.

==================================================
7. Kesimpulan
==================================================
Dengan adanya sistem Monitoring dan Logging ini,
layanan inference machine learning dapat dipantau secara real-time,
memudahkan deteksi masalah, serta meningkatkan keandalan sistem
dalam proses deployment dan operasional.
