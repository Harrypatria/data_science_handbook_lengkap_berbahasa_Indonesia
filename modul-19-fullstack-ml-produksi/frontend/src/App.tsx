import { useState } from 'react'

// Modul 19 (Full-Stack ML) - Skoring Kredit Bank Arta Nusantara. Menampilkan
// PROBABILITAS gagal bayar mentah dari API, bukan cuma label ya/tidak, sesuai
// permintaan eksplisit Bagas di Brief Klien.

interface HasilSkoring {
  probabilitas_gagal_bayar: number
  keputusan: string
  ambang_batas_dipakai: number
}

const API_BASE = 'http://127.0.0.1:8001'

function App() {
  const [pendapatan, setPendapatan] = useState('')
  const [usia, setUsia] = useState('')
  const [skorKredit, setSkorKredit] = useState('')
  const [tanggungan, setTanggungan] = useState('')
  const [rasioCicilan, setRasioCicilan] = useState('')
  const [jenisKredit, setJenisKredit] = useState<'KPR' | 'UMKM'>('KPR')

  const [hasil, setHasil] = useState<HasilSkoring | null>(null)
  const [error, setError] = useState('')
  const [memuat, setMemuat] = useState(false)

  async function ajukanSkoring() {
    setError('')
    setHasil(null)
    setMemuat(true)
    try {
      const res = await fetch(`${API_BASE}/skor-kredit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pendapatan_juta: Number(pendapatan),
          usia: Number(usia),
          skor_kredit: Number(skorKredit),
          jumlah_tanggungan: Number(tanggungan),
          rasio_cicilan_pendapatan: Number(rasioCicilan),
          jenis_kredit: jenisKredit,
        }),
      })
      if (res.status === 422) {
        const detail = await res.json()
        throw new Error(`Input tidak valid: ${detail.detail[0].msg}`)
      }
      if (!res.ok) {
        throw new Error('Server gagal memproses pengajuan ini')
      }
      const data: HasilSkoring = await res.json()
      setHasil(data)
    } catch (err) {
      if (err instanceof TypeError) {
        setError('Tidak bisa terhubung ke server skoring, pastikan backend berjalan')
      } else {
        setError((err as Error).message)
      }
    } finally {
      setMemuat(false)
    }
  }

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 480, margin: '2rem auto' }}>
      <h1>Skoring Kredit Bank Arta Nusantara</h1>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <input
          placeholder="Pendapatan (juta Rupiah)"
          value={pendapatan}
          onChange={(e) => setPendapatan(e.target.value)}
        />
        <input placeholder="Usia" value={usia} onChange={(e) => setUsia(e.target.value)} />
        <input
          placeholder="Skor kredit (0-100)"
          value={skorKredit}
          onChange={(e) => setSkorKredit(e.target.value)}
        />
        <input
          placeholder="Jumlah tanggungan"
          value={tanggungan}
          onChange={(e) => setTanggungan(e.target.value)}
        />
        <input
          placeholder="Rasio cicilan/pendapatan (0-1)"
          value={rasioCicilan}
          onChange={(e) => setRasioCicilan(e.target.value)}
        />
        <select value={jenisKredit} onChange={(e) => setJenisKredit(e.target.value as 'KPR' | 'UMKM')}>
          <option value="KPR">KPR</option>
          <option value="UMKM">UMKM</option>
        </select>
        <button onClick={ajukanSkoring} disabled={memuat}>
          {memuat ? 'Memproses...' : 'Ajukan Skoring'}
        </button>
      </div>

      {hasil && (
        <div style={{ marginTop: '1rem' }}>
          <p>Probabilitas gagal bayar: {(hasil.probabilitas_gagal_bayar * 100).toFixed(2)}%</p>
          <p>Keputusan: {hasil.keputusan}</p>
          <p>Ambang batas dipakai: {hasil.ambang_batas_dipakai}</p>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}

export default App
