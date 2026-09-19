# backend/main.py
"""Bank Arta Nusantara - API Skoring Kredit (Modul 19: Full-Stack ML).

Memuat model_gagal_bayar.joblib SEKALI saat startup (lifespan), memvalidasi
input lewat Pydantic, dan mengembalikan PROBABILITAS gagal bayar, bukan cuma
label biner. Menggabungkan Materi Inti dengan Latihan Mandiri Soal 1 (field
`catatan` opsional, dikembalikan apa adanya, tidak dipakai model) dan Soal 2
(endpoint batch /skor-kredit-batch).

PENTING: jalankan train_model.py dulu di folder ini (atau salin file .joblib
ke sini) sebelum menjalankan server, atau server akan gagal menyala dengan
pesan error yang jelas (lihat fungsi lifespan di bawah).

Jalankan dengan:
    uvicorn main:app --reload
"""
from contextlib import asynccontextmanager
from typing import Literal, Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

MODEL_PATH = "model_gagal_bayar.joblib"
AMBANG_BATAS = 0.60

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        raise RuntimeError(
            f"File model '{MODEL_PATH}' tidak ditemukan. Jalankan train_model.py dulu."
        )
    yield


app = FastAPI(title="Bank Arta Nusantara - API Skoring Kredit", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PengajuanKredit(BaseModel):
    pendapatan_juta: float = Field(gt=0, le=200, description="Pendapatan bulanan dalam juta Rupiah")
    usia: int = Field(ge=21, le=65, description="Usia pemohon dalam tahun")
    skor_kredit: float = Field(ge=0, le=100, description="Skor kredit internal, 0 sampai 100")
    jumlah_tanggungan: int = Field(ge=0, le=10, description="Jumlah tanggungan keluarga")
    rasio_cicilan_pendapatan: float = Field(gt=0, lt=1, description="Rasio cicilan terhadap pendapatan, 0 sampai 1")
    jenis_kredit: Literal["KPR", "UMKM"]
    catatan: Optional[str] = None


class HasilSkoring(BaseModel):
    probabilitas_gagal_bayar: float
    keputusan: Literal["Perlu Tinjauan Lanjut", "Lolos Penyaringan Awal"]
    ambang_batas_dipakai: float
    catatan: Optional[str] = None


def _skor_satu(pengajuan: PengajuanKredit) -> HasilSkoring:
    if model is None:
        raise HTTPException(status_code=503, detail="Model belum siap, coba lagi sesaat")

    data = pd.DataFrame([pengajuan.model_dump(exclude={"catatan"})])
    try:
        proba = model.predict_proba(data)[:, 1][0]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gagal memproses prediksi: {exc}")

    keputusan = "Perlu Tinjauan Lanjut" if proba >= AMBANG_BATAS else "Lolos Penyaringan Awal"
    return HasilSkoring(
        probabilitas_gagal_bayar=round(float(proba), 4),
        keputusan=keputusan,
        ambang_batas_dipakai=AMBANG_BATAS,
        catatan=pengajuan.catatan,
    )


@app.post("/skor-kredit", response_model=HasilSkoring)
def skor_kredit(pengajuan: PengajuanKredit):
    return _skor_satu(pengajuan)


@app.post("/skor-kredit-batch", response_model=list[HasilSkoring])
def skor_kredit_batch(pengajuan_list: list[PengajuanKredit]):
    if model is None:
        raise HTTPException(status_code=503, detail="Model belum siap, coba lagi sesaat")
    return [_skor_satu(p) for p in pengajuan_list]
