# app.py
"""Lumina Tech - Lacak Kiriman.

Solusi lengkap Modul 17 (Aplikasi Web Interaktif dengan Streamlit), menggabungkan
Materi Inti, Studi Kasus (peringatan visual merah untuk resi tidak ditemukan),
dan Latihan Mandiri (tombol Hapus Riwayat + validasi format nomor resi).

Jalankan dengan:
    streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="Lumina Tech - Lacak Kiriman", page_icon="📦")
st.title("📦 Lumina Tech: Lacak Kiriman")
st.write("Selamat datang! Cek status pengiriman atau hitung ongkir di bawah ini.")


def cek_status_pengiriman(id_resi):
    data_resi = {
        "LGX-1001": "Dalam perjalanan, estimasi tiba 2 hari lagi",
        "LGX-1002": "Terkirim pada 14 September 2026",
        "LGX-1003": "Tertahan di gudang transit Surabaya",
    }
    return data_resi.get(id_resi, "Nomor resi tidak ditemukan")


def hitung_ongkir(berat_kg, jarak_km):
    tarif_dasar = 5000
    return tarif_dasar + (berat_kg * 2000) + (jarak_km * 500)


if "riwayat_pencarian" not in st.session_state:
    st.session_state.riwayat_pencarian = []

tab1, tab2 = st.tabs(["Cek Status Pengiriman", "Hitung Ongkir"])

with tab1:
    st.subheader("Cek Status Pengiriman")
    id_resi = st.text_input("Masukkan nomor resi (contoh: LGX-1001)")

    col1, col2 = st.columns([1, 1])
    with col1:
        cek_diklik = st.button("Cek Status")
    with col2:
        if st.button("Hapus Riwayat"):
            st.session_state.riwayat_pencarian = []
            st.rerun()

    if cek_diklik:
        id_resi_bersih = id_resi.strip().upper()
        if not id_resi_bersih:
            st.warning("Masukkan nomor resi dulu.")
        elif not id_resi_bersih.startswith("LGX-"):
            st.warning("Format nomor resi tidak dikenali, harus diawali 'LGX-'.")
        else:
            hasil = cek_status_pengiriman(id_resi_bersih)
            if hasil == "Nomor resi tidak ditemukan":
                st.error(hasil)  # kotak MERAH, bukan hijau
            else:
                st.success(hasil)
            st.session_state.riwayat_pencarian.append(id_resi_bersih)

    if st.session_state.riwayat_pencarian:
        st.caption("Riwayat pencarian sesi ini:")
        st.write(", ".join(st.session_state.riwayat_pencarian))

with tab2:
    st.subheader("Hitung Estimasi Ongkir")
    berat = st.number_input("Berat paket (kg)", min_value=0.1, value=1.0, step=0.5)
    jarak = st.number_input("Jarak pengiriman (km)", min_value=1.0, value=10.0, step=1.0)
    if st.button("Hitung"):
        biaya = hitung_ongkir(berat, jarak)
        st.success(f"Estimasi ongkir: Rp{biaya:,.0f}")
