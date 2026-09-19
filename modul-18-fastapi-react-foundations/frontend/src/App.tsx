import { useState } from 'react'

// Modul 18 (Full-Stack Foundations) - solusi lengkap Lumina Tech, menggabungkan
// Materi Inti (cek status resi), Studi Kasus (riwayat pencarian sebagai array),
// dan Latihan Mandiri (hapus riwayat, form ongkir, penanganan error tiga skenario).

interface StatusResponse {
  id_resi: string
  status: string
}

interface OngkirResponse {
  biaya_rupiah: number
}

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [idResi, setIdResi] = useState('')
  const [hasil, setHasil] = useState<StatusResponse | null>(null)
  const [error, setError] = useState('')
  const [riwayat, setRiwayat] = useState<StatusResponse[]>([])

  const [berat, setBerat] = useState('')
  const [jarak, setJarak] = useState('')
  const [ongkir, setOngkir] = useState<number | null>(null)
  const [errorOngkir, setErrorOngkir] = useState('')

  async function cekStatus() {
    setError('')
    setHasil(null)
    try {
      const res = await fetch(`${API_BASE}/status/${idResi}`)
      if (res.status === 404) {
        throw new Error('Nomor resi tidak ditemukan, cek kembali penulisannya')
      }
      if (!res.ok) {
        throw new Error('Server mengembalikan error tak terduga')
      }
      const data: StatusResponse = await res.json()
      setHasil(data)
      setRiwayat((riwayatSebelumnya) => [data, ...riwayatSebelumnya])
    } catch (err) {
      if (err instanceof TypeError) {
        setError('Tidak bisa terhubung ke server, pastikan backend sedang berjalan')
      } else {
        setError((err as Error).message)
      }
    }
  }

  async function hapusRiwayat() {
    await fetch(`${API_BASE}/riwayat`, { method: 'DELETE' })
    setRiwayat([])
  }

  async function hitungOngkir() {
    setErrorOngkir('')
    setOngkir(null)
    try {
      const res = await fetch(`${API_BASE}/ongkir`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ berat_kg: Number(berat), jarak_km: Number(jarak) }),
      })
      if (!res.ok) {
        throw new Error('Input tidak valid, cek kembali berat dan jarak')
      }
      const data: OngkirResponse = await res.json()
      setOngkir(data.biaya_rupiah)
    } catch (err) {
      setErrorOngkir((err as Error).message)
    }
  }

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 480, margin: '2rem auto' }}>
      <h1>Lacak Paket Lumina Tech</h1>

      <input
        value={idResi}
        onChange={(e) => setIdResi(e.target.value)}
        placeholder="Contoh: LGX-1001"
      />
      <button onClick={cekStatus}>Cek Status</button>
      {hasil && (
        <p>
          {hasil.id_resi}: {hasil.status}
        </p>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h2>Riwayat Pencarian ({riwayat.length})</h2>
      <ul>
        {riwayat.map((item, index) => (
          <li key={index}>
            {item.id_resi}: {item.status}
          </li>
        ))}
      </ul>
      <button onClick={hapusRiwayat}>Hapus Riwayat</button>

      <hr />

      <h2>Hitung Ongkir</h2>
      <input value={berat} onChange={(e) => setBerat(e.target.value)} placeholder="Berat (kg)" />
      <input value={jarak} onChange={(e) => setJarak(e.target.value)} placeholder="Jarak (km)" />
      <button onClick={hitungOngkir}>Hitung</button>
      {ongkir !== null && <p>Estimasi ongkir: Rp{ongkir.toLocaleString('id-ID')}</p>}
      {errorOngkir && <p style={{ color: 'red' }}>{errorOngkir}</p>}
    </div>
  )
}

export default App
