# Laporan Riset: Format KIB B BPAD DKI Jakarta

**Tanggal:** 11 Januari 2026 (Koreksi Final: 11 Januari 2026)  
**Peneliti:** Kiro AI Assistant  
**Tujuan:** Verifikasi format KIB B yang digunakan oleh BPAD DKI Jakarta untuk sekolah
**Tools Verifikasi:** Exa Search, Tavily Search, Firecrawl, Fetch, Sequential Thinking, **Verifikasi Visual PDF**

---

## Executive Summary

Setelah melakukan **verifikasi visual langsung** dari PDF resmi BPAD DKI Jakarta (`KIB_B_BPAD_2024.pdf`), ditemukan bahwa format KIB B yang benar adalah **18 kolom** (bukan 20 kolom seperti yang sebelumnya didokumentasikan).

### Temuan Utama

| Aspek | Permendagri 19/2016 | BPAD DKI Jakarta |
|-------|---------------------|------------------|
| Jumlah Kolom KIB B | 16 kolom | **18 kolom** ✅ |
| Format Harga | Tidak spesifik | **Rupiah penuh (Rp.)** |
| Kolom Tambahan | - | SATUAN, TGL. BPKB/DOK, KAPITALISASI, TOTAL |
| Format Tanggal | Tidak spesifik | **DD/MM/YYYY** |

### Koreksi Penting (v3.0)

> ⚠️ **KOREKSI:** Versi sebelumnya (v2.x) menyatakan 20 kolom berdasarkan interpretasi teks. Setelah **verifikasi visual langsung** dari PDF, format yang benar adalah **18 kolom**. Perbedaan karena kolom "OLEH" digabung dengan kolom tanggal/asal, bukan kolom terpisah.

---

## 1. Sumber yang Diteliti

### 1.1 Sumber Resmi BPAD DKI Jakarta (Terverifikasi)

| No | Sumber | URL/Referensi | Status |
|----|--------|---------------|--------|
| 1 | **KIB B BPAD DKI Jakarta 2024** | bkddki.jakarta.go.id (PDF) | ✅ **TERVERIFIKASI VISUAL** |
| 2 | **KIB B BPAD DKI Jakarta 2025** | bkddki.jakarta.go.id (PDF) | ✅ **TERVERIFIKASI** |
| 3 | Insekda DKI Jakarta No. 11/2024 | bpad.jakarta.go.id | ✅ Aktif |
| 4 | Portal Sensus BMD DKI | sensus-kib-e-atb.crd.co | ✅ Aktif |
| 5 | Aplikasi JAK-ASET | jakaset.jakarta.go.id | ✅ Aktif |

### 1.2 File PDF yang Didownload

| File | Ukuran | Halaman | Sumber |
|------|--------|---------|--------|
| `KIB_B_BPAD_2024.pdf` | 1.55 MB | 215 | BKD DKI Jakarta |
| `KIB_B_BPAD_2025.pdf` | 11.34 MB | - | BKD DKI Jakarta |
| `KIB_B_Jakarta_Timur.pdf` | 0.83 MB | - | Jakarta Timur |

---

## 2. Struktur 18 Kolom KIB B (TERVERIFIKASI VISUAL)

### 2.1 Daftar Kolom Resmi

| No | Nama Kolom | Field Database | Keterangan |
|----|------------|----------------|------------|
| 1 | NO. | auto-increment | Nomor urut |
| 2 | KODE BARANG | kode_barang | Format: XX.XX.XX.XXXX (13 karakter) |
| 3 | REG. | nomor_register | Nomor Register/NUP |
| 4 | JENIS BARANG | nama_barang | Nama barang sesuai katalog |
| 5 | UKU-RAN | ukuran_cc | Ukuran/CC |
| 6 | SATU-AN | satuan | BH/Unit/Set/Buah |
| 7 | TGL. OLEH | tanggal_perolehan | Tanggal & sumber perolehan (digabung) |
| 8 | BA-HAN | bahan | Material/bahan |
| 9 | MEREK | merk | Merk barang |
| 10 | TYPE | tipe | Tipe/model |
| 11 | TGL. BPKB/TGL. DOK. | tanggal_dokumen | Tanggal dokumen kepemilikan |
| 12 | NO. CHASIS/NO. RANGKA | nomor_rangka | Untuk kendaraan |
| 13 | NO. MESIN/NO. PABRIK | nomor_mesin | Nomor mesin/pabrik |
| 14 | NOMOR POLISI | nomor_polisi | Untuk kendaraan |
| 15 | ASAL OLEH | asal_usul | Asal usul & sumber (digabung) |
| 16 | HARGA (Rp.) | harga | **Rupiah penuh** (bukan ribuan) |
| 17 | KAPITALISASI (Rp.) | kapitalisasi | Nilai kapitalisasi |
| 18 | TOTAL (Rp.) | total_harga | Total harga keseluruhan |

### 2.2 Penjelasan Koreksi 20 → 18 Kolom

Kesalahan sebelumnya terjadi karena interpretasi teks yang menghitung "OLEH" sebagai kolom terpisah:

| Interpretasi Lama (Salah) | Interpretasi Baru (Benar) |
|---------------------------|---------------------------|
| Kolom 7: TGL. | Kolom 7: TGL. OLEH (digabung) |
| Kolom 8: OLEH | - |
| Kolom 9: TGL. BPKB/DOK. | Kolom 11: TGL. BPKB/TGL. DOK. |
| Kolom 10: OLEH | - |
| Kolom 11: ASAL | Kolom 15: ASAL OLEH (digabung) |

**Hasil:** 20 - 2 = **18 kolom**

---

## 3. Perbandingan Format

### 3.1 Permendagri 19/2016 vs BPAD DKI Jakarta

| Aspek | Permendagri 19/2016 | BPAD DKI Jakarta |
|-------|---------------------|------------------|
| Jumlah Kolom | 16 kolom | **18 kolom** |
| Kolom SATUAN | ❌ Tidak ada | ✅ Ada |
| Kolom TGL. BPKB/DOK | ❌ Tidak ada | ✅ Ada |
| Kolom KAPITALISASI | ❌ Tidak ada | ✅ Ada |
| Kolom TOTAL | ❌ Tidak ada | ✅ Ada |
| Format Harga | Tidak spesifik | Rupiah penuh |
| Format Tanggal | Tidak spesifik | DD/MM/YYYY |

### 3.2 Kolom Tambahan BPAD DKI Jakarta (vs Permendagri)

| Kolom | Posisi | Fungsi |
|-------|--------|--------|
| SATU-AN | 6 | Satuan barang (BH/Unit/Set) |
| KAPITALISASI (Rp.) | 17 | Nilai kapitalisasi aset |
| TOTAL (Rp.) | 18 | Total harga keseluruhan |

---

## 4. Klarifikasi: BKD vs BPAD

### 4.1 Perbedaan Instansi

| Instansi | Nama Lengkap | Fungsi |
|----------|--------------|--------|
| **BKD** | Badan Kepegawaian Daerah | Mengelola kepegawaian PNS |
| **BPAD** | Badan Pengelolaan Aset Daerah | Mengelola aset/BMD daerah |

### 4.2 Mengapa File Ada di BKD?

File KIB B yang ditemukan di website BKD adalah **contoh penggunaan format BPAD** oleh BKD sebagai salah satu SKPD di DKI Jakarta. Semua SKPD/UKPD di DKI Jakarta (termasuk BKD, Dinas Pendidikan, dan sekolah-sekolah) menggunakan format KIB yang sama dari BPAD.

### 4.3 Relevansi untuk Sekolah

- Sekolah di DKI Jakarta adalah **UPB (Unit Pengguna Barang)** di bawah Dinas Pendidikan
- Dinas Pendidikan adalah **SKPD** yang menggunakan format BPAD
- Oleh karena itu, sekolah **WAJIB** menggunakan format KIB B 18 kolom dari BPAD

---

## 5. Regulasi yang Berlaku

| No | Regulasi | Tentang | Status |
|----|----------|---------|--------|
| 1 | Permendagri No. 19/2016 | Pedoman Pengelolaan BMD | Berlaku (Nasional) |
| 2 | Permendagri No. 47/2021 | Perubahan Permendagri 19/2016 | Berlaku |
| 3 | Permendagri No. 7/2024 | Perubahan Kedua | Terbaru |
| 4 | Pergub DKI No. 67/2022 | Kebijakan Akuntansi DKI Jakarta | **Berlaku (DKI)** |
| 5 | Kepgub DKI No. 52/2023 | Tim Inventarisasi BMD | **Berlaku (DKI)** |
| 6 | Insekda DKI No. 11/2024 | Inventarisasi KIB B TA 2024 | **Aktif (DKI)** |
| 7 | Insekda DKI No. 20/2025 | Inventarisasi KIB E & ATB 2025 | **Terbaru (DKI)** |

---

## 6. Kesimpulan dan Rekomendasi

### 6.1 Kesimpulan

1. **Format 18 kolom BPAD DKI Jakarta TERVERIFIKASI** dari PDF resmi (verifikasi visual)
2. **Harga dalam Rupiah penuh** (bukan ribuan) - sesuai format BPAD
3. **Format tanggal DD/MM/YYYY** - konsisten dengan standar BPAD
4. **Kode barang 13 karakter** - format XX.XX.XX.XXXX

### 6.2 Dokumentasi yang Sudah Diupdate

| File | Status | Perubahan |
|------|--------|-----------|
| `docs/format_kib_spesifikasi.md` | ✅ Updated | 20 → 18 kolom |
| `docs/data_schema.md` | ✅ Updated | Hapus 2 field, update mapping |
| `docs/api_contract.md` | ✅ Updated | 20 → 18 kolom |
| `AGENTS.md` | ✅ Updated | 20 → 18 kolom |
| `.kiro/steering/product.md` | ✅ Updated | 20 → 18 kolom |
| `.kiro/specs/simanis62-v2/design.md` | ✅ Updated | 20 → 18 kolom |
| `.kiro/specs/simanis62-v2/requirements.md` | ✅ Updated | 20 → 18 kolom |

---

## 7. Referensi

### 7.1 Dokumen Resmi (Downloaded)

1. **KIB_B_BPAD_2024.pdf** - `docs/KIB_B_BPAD_2024.pdf`
2. **KIB_B_BPAD_2025.pdf** - `docs/KIB_B_BPAD_2025.pdf`
3. **KIB_B_Jakarta_Timur.pdf** - `docs/KIB_B_Jakarta_Timur.pdf`

### 7.2 URL Sumber

- https://bkddki.jakarta.go.id/download/detail/N3Q3NR1JDVVKMY9 (KIB B 2024)
- https://bkddki.jakarta.go.id/download/detail/3K6YNQNP7P62M9P (KIB B 2025)

### 7.3 Portal Resmi

- BPAD DKI Jakarta: https://bpad.jakarta.go.id/
- JAK-ASET: https://jakaset.jakarta.go.id/
- Portal Sensus BMD: https://sensus-kib-e-atb.crd.co/

---

## 8. Catatan Revisi

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 1.0 | 10 Jan 2026 | Initial version - kesimpulan format 16 kolom |
| 2.0 | 11 Jan 2026 | REVISI - Ditemukan bukti format 20 kolom (interpretasi teks) |
| 2.1 | 10 Jan 2026 | RE-VERIFIKASI - URL dan regulasi diverifikasi |
| **3.0** | **11 Jan 2026** | **KOREKSI FINAL** - Format dikoreksi menjadi **18 kolom** setelah verifikasi visual PDF resmi. Kolom "OLEH" digabung dengan kolom tanggal/asal, bukan terpisah. |

---

## 9. Disclaimer

> ✅ **TERVERIFIKASI VISUAL:** Format KIB B **18 kolom** telah diverifikasi langsung dari PDF resmi BPAD DKI Jakarta (`KIB_B_BPAD_2024.pdf`).

> ⚠️ **PELAJARAN:** Verifikasi teks/OCR dari PDF tidak selalu akurat. Verifikasi visual langsung dari dokumen asli adalah metode paling reliable.

---

*Dokumen ini dibuat sebagai bagian dari proses quality assurance dokumentasi proyek SIMANIS62 V2.*
*Riset dilakukan menggunakan: Tavily Search, Exa Search, Firecrawl, **Verifikasi Visual PDF***
