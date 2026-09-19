# Modul 18 — Full-Stack Foundations (FastAPI + React/TypeScript)

Solusi lengkap arsitektur dua-proyek-terpisah untuk Lumina Tech: backend REST API
(FastAPI + Pydantic) dan frontend (React + TypeScript + Vite) yang berkomunikasi
lewat kontrak API bervalidasi, tanpa satu pun model machine learning (itu Modul 19).

## Struktur folder

```
modul-18-fastapi-react-foundations/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/               (scaffold npm create vite@latest -- --template react-ts)
│   ├── src/App.tsx
│   ├── package.json
│   └── ...
└── .gitignore
```

## Menjalankan backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend berjalan di `http://127.0.0.1:8000`. Dokumentasi interaktif otomatis di
`http://127.0.0.1:8000/docs`.

## Menjalankan frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend berjalan di `http://localhost:5173`, port yang sudah didaftarkan di
`CORSMiddleware` backend. Jalankan backend dan frontend di dua terminal terpisah
secara bersamaan.

## Endpoint API

| Method | Path | Deskripsi |
|---|---|---|
| GET | `/` | Cek server aktif |
| GET | `/status/{id_resi}` | Cek status pengiriman (404 kalau tidak ditemukan) |
| POST | `/ongkir` | Hitung ongkir (`berat_kg`, `jarak_km`, 422 kalau tidak valid) |
| DELETE | `/riwayat` | Placeholder hapus riwayat (dipanggil dari tombol frontend) |

## Fitur frontend yang sudah digabung dari seluruh bab

- Form cek status resi dengan `useState` dan `fetch`.
- Riwayat pencarian sebagai array (Studi Kasus), dengan tombol Hapus Riwayat (Soal 1).
- Form hitung ongkir terpisah dengan validasi `jarak_km <= 5000` di Pydantic (Soal 2).
- Penanganan error tiga skenario: resi tidak ditemukan (404), server tak terjangkau
  (`err instanceof TypeError`), dan sukses (Soal 3).

## Verifikasi

Seluruh endpoint dijalankan nyata lewat `uvicorn` dan diverifikasi lewat `curl`
(sukses 200, gagal 404, validasi gagal 422, preflight CORS), dan frontend
dijalankan nyata lewat `npm run dev` (HTTP 200) serta `npm run build` (build
production berhasil, 16 modul, tanpa error TypeScript).
