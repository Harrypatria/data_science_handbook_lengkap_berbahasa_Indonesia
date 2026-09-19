# backend/main.py
"""Lumina Tech API - Modul 18 (Full-Stack Foundations).

Backend FastAPI + Pydantic murni arsitektur (tanpa machine learning, itu Modul 19),
menggabungkan Materi Inti (endpoint status resi dan ongkir, CORS) dengan Latihan
Mandiri (endpoint DELETE /riwayat, validasi jarak_km <= 5000 km).

Jalankan dengan:
    uvicorn main:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Lumina Tech API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_RESI = {
    "LGX-1001": "Dalam perjalanan, estimasi tiba 2 hari lagi",
    "LGX-1002": "Terkirim pada 14 September 2026",
    "LGX-1003": "Tertahan di gudang transit Surabaya",
}


@app.get("/")
def root():
    return {"message": "Lumina Tech API aktif"}


class StatusResponse(BaseModel):
    id_resi: str
    status: str


@app.get("/status/{id_resi}", response_model=StatusResponse)
def cek_status(id_resi: str):
    status = DATA_RESI.get(id_resi.upper())
    if status is None:
        raise HTTPException(status_code=404, detail="Nomor resi tidak ditemukan")
    return StatusResponse(id_resi=id_resi.upper(), status=status)


class OngkirRequest(BaseModel):
    berat_kg: float = Field(gt=0, description="Berat paket dalam kg, harus lebih dari 0")
    jarak_km: float = Field(gt=0, le=5000, description="Jarak pengiriman dalam km, 0 sampai 5000")


class OngkirResponse(BaseModel):
    biaya_rupiah: float


@app.post("/ongkir", response_model=OngkirResponse)
def hitung_ongkir(req: OngkirRequest):
    tarif_dasar = 5000
    biaya = tarif_dasar + (req.berat_kg * 2000) + (req.jarak_km * 500)
    return OngkirResponse(biaya_rupiah=biaya)


@app.delete("/riwayat")
def hapus_riwayat():
    return {"message": "Riwayat dihapus"}
