# Modul 19 — Full-Stack ML (Bank Arta Nusantara: Skoring Kredit)

Solusi lengkap: model klasifikasi gagal bayar (Modul 7) dilatih offline dan
disimpan lewat `joblib`, dimuat sekali saat startup FastAPI, dan probabilitasnya
(bukan cuma label) ditampilkan di frontend React. Mencakup training offline,
serving, penanganan version mismatch, containerization, dan CI dasar.

## Struktur folder

```
modul-19-fullstack-ml-produksi/
├── train_model.py                    # training offline, sekali jalan
├── simulate_version_mismatch.py      # Studi Kasus: InconsistentVersionWarning
├── backend/
│   ├── main.py                       # FastAPI + lifespan + endpoint skoring
│   ├── requirements.txt              # versi terkunci (==), bukan pip freeze biasa
│   ├── Dockerfile
│   └── model_gagal_bayar.joblib      # sudah dilatih, siap pakai langsung
├── frontend/                         # scaffold npm create vite@latest -- --template react-ts
│   ├── src/App.tsx
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
├── .github/workflows/ci.yml
└── .gitignore
```

## 1. Training offline

```bash
cd backend
python ../train_model.py
```

Menghasilkan `model_gagal_bayar.joblib` (sudah disertakan di folder ini, hasil
dijalankan nyata):

```
ROC-AUC data uji: 0.6657
Model disimpan ke model_gagal_bayar.joblib
```

## 2. Menjalankan backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Dijalankan dan diverifikasi lewat `curl` menghasilkan angka yang identik dengan
Modul 7:

```bash
curl -X POST http://127.0.0.1:8001/skor-kredit -H "Content-Type: application/json" -d '{
  "pendapatan_juta": 8, "usia": 30, "skor_kredit": 45, "jumlah_tanggungan": 3,
  "rasio_cicilan_pendapatan": 0.65, "jenis_kredit": "UMKM"
}'
# {"probabilitas_gagal_bayar":0.8799,"keputusan":"Perlu Tinjauan Lanjut","ambang_batas_dipakai":0.6,"catatan":null}
```

Endpoint tambahan dari Latihan Mandiri sudah digabung: field `catatan` opsional
(Soal 1) dan `POST /skor-kredit-batch` untuk banyak pengajuan sekaligus (Soal 2).

## 3. Menjalankan frontend

```bash
cd frontend
npm install
npm run dev
```

Buka `http://localhost:5173`. Antarmuka menampilkan probabilitas gagal bayar
sebagai persentase, keputusan, dan ambang batas yang dipakai, sesuai permintaan
eksplisit Bagas di Brief Klien: **jangan cuma tampilkan label ya/tidak**.

> Catatan port: contoh `curl` dan `App.tsx` di atas memakai port **8001** untuk
> menjalankan backend secara lokal lewat `uvicorn` langsung (menghindari bentrok
> kalau proyek Modul 18 juga sedang berjalan di port 8000 di komputer yang sama).
> Kalau dijalankan lewat Docker Compose (langkah 5), backend memakai port **8000**
> sesuai `Dockerfile`/`docker-compose.yml`, ganti `API_BASE` di `App.tsx` sesuai
> cara menjalankannya.

## 4. Simulasi version mismatch (Studi Kasus)

```bash
cd backend
python ../simulate_version_mismatch.py
```

Hasil nyata (7 `InconsistentVersionWarning`, probabilitas tetap sama pada kasus
spesifik ini, tapi TIDAK boleh dianggap jaminan umum, lihat Modul 19 bagian
Studi Kasus):

```
Probabilitas (versi cocok)   : 0.8799
Probabilitas (versi tidak cocok, 7 peringatan): 0.8799
```

## 5. Containerization dengan Docker

```bash
docker compose up --build
```

Backend di `http://localhost:8000`, frontend (dibangun jadi file statis,
disajikan Nginx) di `http://localhost:3000`. `backend/Dockerfile` menyalin
`requirements.txt` dan menjalankan `pip install` **sebelum** menyalin kode,
supaya cache layer Docker tidak perlu mengulang instalasi setiap kode berubah.
`frontend/Dockerfile` memakai *multi-stage build*: image Node lengkap untuk
membangun, image `nginx:alpine` yang jauh lebih ringan untuk menyajikan hasilnya.

> Dockerfile diverifikasi lewat pembacaan cermat dan konsisten dengan pola yang
> sama sudah dipakai `backend/requirements.txt`/`frontend/package.json` di folder
> ini, tapi build image sungguhan tidak dijalankan pada sesi penulisan solusi ini
> karena Docker Desktop daemon tidak aktif di lingkungan tersebut. Jalankan
> `docker compose up --build` di komputer kita untuk memverifikasi langsung.

## 6. CI dengan GitHub Actions

`.github/workflows/ci.yml` menjalankan dua job paralel setiap push/PR ke `main`:
memastikan `backend/main.py` bisa di-*import* tanpa error, dan
`frontend` bisa di-*build* (`npm run build`) tanpa error. Kedua langkah ini
diverifikasi bekerja secara lokal sebelum ditulis ke workflow.

## Verifikasi yang sudah dijalankan nyata

- `train_model.py`: ROC-AUC 0,6657 (identik Modul 7).
- `main.py`: `import main` berhasil; server gagal menyala dengan pesan jelas
  saat file model dihapus (perilaku `lifespan` diverifikasi langsung).
- Endpoint `/skor-kredit`, `/skor-kredit-batch`: diverifikasi lewat `curl`,
  termasuk kasus sukses, validasi gagal (422), dan field `catatan`.
- `simulate_version_mismatch.py`: 7 `InconsistentVersionWarning` nyata,
  probabilitas dibandingkan.
- Frontend: `npm run build` berhasil (16 modul, tanpa error TypeScript);
  `npm run dev` dan backend dijalankan bersamaan, CORS preflight diverifikasi
  mengembalikan header `access-control-allow-origin` yang benar.
