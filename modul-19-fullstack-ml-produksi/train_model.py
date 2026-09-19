# train_model.py
"""Training offline untuk model skoring kredit Bank Arta Nusantara (Modul 19).

Skrip ini TIDAK PERNAH dijalankan oleh server API (backend/main.py), hanya
dijalankan manual oleh data scientist saat model perlu dilatih atau dilatih ulang.
Murni mengulang Modul 7, dengan satu tambahan: menyimpan hasilnya ke disk lewat
joblib supaya bisa dimuat kembali oleh backend/main.py saat startup.

Jalankan dari dalam folder backend/ (supaya file .joblib berada di tempat yang
dicari MODEL_PATH di main.py):

    cd backend
    python ../train_model.py
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import joblib

np.random.seed(42)
n = 800

pendapatan_juta = np.clip(np.random.normal(14, 6, n), 4, 60)
usia = np.clip(np.random.normal(37, 9, n), 21, 65).round().astype(int)
skor_kredit = np.clip(0.7 * pendapatan_juta + np.random.normal(55, 10, n), 20, 100)
jumlah_tanggungan = np.clip(np.random.poisson(1.8, n), 0, 6)
rasio_cicilan_pendapatan = np.clip(np.random.normal(0.32, 0.12, n), 0.05, 0.9)
jenis_kredit = np.random.choice(["KPR", "UMKM"], size=n, p=[0.55, 0.45])

logit = (
    -3.2 - 0.05 * (skor_kredit - 60) + 4.5 * (rasio_cicilan_pendapatan - 0.3)
    + 0.18 * jumlah_tanggungan - 0.01 * (usia - 37)
    + np.where(jenis_kredit == "UMKM", 0.4, 0.0)
)
prob_gagal = 1 / (1 + np.exp(-logit))
gagal_bayar = np.random.binomial(1, prob_gagal)

df = pd.DataFrame({
    "pendapatan_juta": pendapatan_juta.round(2), "usia": usia,
    "skor_kredit": skor_kredit.round(1), "jumlah_tanggungan": jumlah_tanggungan,
    "rasio_cicilan_pendapatan": rasio_cicilan_pendapatan.round(3),
    "jenis_kredit": jenis_kredit, "gagal_bayar": gagal_bayar,
})

fitur_numerik = ["pendapatan_juta", "usia", "skor_kredit", "jumlah_tanggungan", "rasio_cicilan_pendapatan"]
fitur_kategorikal = ["jenis_kredit"]
X = df[fitur_numerik + fitur_kategorikal]
y = df["gagal_bayar"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), fitur_numerik),
    ("cat", OneHotEncoder(drop="first"), fitur_kategorikal),
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
pipeline.fit(X_train, y_train)

y_proba = pipeline.predict_proba(X_test)[:, 1]
print(f"ROC-AUC data uji: {roc_auc_score(y_test, y_proba):.4f}")

joblib.dump(pipeline, "model_gagal_bayar.joblib")
print("Model disimpan ke model_gagal_bayar.joblib")
