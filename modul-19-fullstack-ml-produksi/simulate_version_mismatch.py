# simulate_version_mismatch.py
"""Studi Kasus Modul 19: mendemonstrasikan InconsistentVersionWarning secara
terkontrol, dengan memuat model yang sama dua kali, sekali dengan metadata versi
scikit-learn yang cocok, sekali dengan metadata yang sengaja dibuat tidak cocok.

Jalankan dari folder backend/ (butuh model_gagal_bayar.joblib hasil train_model.py):

    cd backend
    python ../simulate_version_mismatch.py
"""
import joblib
import warnings
import pandas as pd
import sklearn.base as base

sample = pd.DataFrame([{
    "pendapatan_juta": 8, "usia": 30, "skor_kredit": 45, "jumlah_tanggungan": 3,
    "rasio_cicilan_pendapatan": 0.65, "jenis_kredit": "UMKM",
}])

model_normal = joblib.load("model_gagal_bayar.joblib")
proba_normal = model_normal.predict_proba(sample)[:, 1][0]

real_version = base.__version__
base.__version__ = "0.24.0"
joblib.dump(model_normal, "model_versi_lama_simulasi.joblib")
base.__version__ = real_version

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    model_mismatch = joblib.load("model_versi_lama_simulasi.joblib")
    jumlah_peringatan = len(w)
    for peringatan in w:
        print(peringatan.category.__name__, ":", str(peringatan.message)[:100], "...")

proba_mismatch = model_mismatch.predict_proba(sample)[:, 1][0]

print(f"Probabilitas (versi cocok)   : {proba_normal:.4f}")
print(f"Probabilitas (versi tidak cocok, {jumlah_peringatan} peringatan): {proba_mismatch:.4f}")
