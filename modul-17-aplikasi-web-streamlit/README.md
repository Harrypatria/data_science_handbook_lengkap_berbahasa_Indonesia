# Modul 17 — Aplikasi Web Interaktif dengan Streamlit

Solusi lengkap untuk studi kasus Lumina Tech: membungkus fungsi `cek_status_pengiriman`
dan `hitung_ongkir` (Modul 16) jadi aplikasi web satu file yang bisa dipakai staf
customer service non-teknis.

## Isi folder

- `app.py` — aplikasi Streamlit lengkap (Materi Inti + Studi Kasus + Latihan Mandiri).
- `requirements.txt` — dependency terkunci (`streamlit==1.64.0`).

## Menjalankan

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Buka `http://localhost:8501` di browser. Coba nomor resi `LGX-1001`, `LGX-1002`,
`LGX-1003` (valid) atau nomor lain (menampilkan kotak merah, bukan hijau).

## Fitur yang sudah digabung dari seluruh bab

- Dua tab: Cek Status Pengiriman dan Hitung Ongkir.
- `st.session_state` untuk riwayat pencarian yang bertahan antar-interaksi.
- Peringatan visual merah (`st.error`) khusus untuk resi tidak ditemukan (Studi Kasus).
- Validasi format nomor resi harus diawali `LGX-` sebelum diproses (Latihan Soal 2).
- Tombol "Hapus Riwayat" yang mengosongkan `st.session_state` dan memanggil
  `st.rerun()` (Latihan Soal 1).

## Verifikasi

Dijalankan headless dan dikonfirmasi merespons HTTP 200:

```bash
streamlit run app.py --server.headless true --server.port 8511
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8511
# HTTP 200
```
