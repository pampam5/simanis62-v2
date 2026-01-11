# Spesifikasi Format KIB (Kartu Inventaris Barang)

**Versi:** 3.0 | **Tanggal:** 11 Januari 2026
**Sumber:** BPAD DKI Jakarta (Format Terverifikasi dari PDF Resmi)
**Referensi Utama:**
- **PDF KIB B BPAD DKI Jakarta** - https://bkddki.jakarta.go.id/download/detail/N3Q3NR1JDVVKMY9
- Permendagri No. 47 Tahun 2021 (Pengganti Permendagri 19/2016)
- Pergub DKI Jakarta No. 67 Tahun 2022
- Kepgub DKI Jakarta No. 734 Tahun 2022
- Kepgub DKI Jakarta No. 52 Tahun 2023
- Insekda DKI Jakarta No. 11 Tahun 2024 (Inventarisasi KIB B)
- Insekda DKI Jakarta No. 20 Tahun 2025 (Inventarisasi KIB E & ATB)

---

## 1. Ringkasan Format

| KIB | Nama | Kolom | Header Row | Data Start | Prioritas |
|-----|------|-------|------------|------------|-----------|
| A | Tanah | 14 | 6-8 | 10 | Post-MVP |
| B | Peralatan dan Mesin | **18** | 7-8 | 11 | **MVP** ⭐ |
| C | Gedung dan Bangunan | 17 | 6-7 | 10 | Post-MVP |
| D | Jalan, Irigasi, Jaringan | 16 | 6-7 | 10 | Post-MVP |
| E | Aset Tetap Lainnya | 16 | 6-7 | 10 | Post-MVP |
| F | Konstruksi Dalam Pengerjaan | 12 | 6-7 | 10 | Post-MVP |

---

## 2. Dasar Hukum (Hierarki DKI Jakarta)

### 2.1 Regulasi Nasional
| No | Regulasi | Tentang | Status |
|----|----------|---------|--------|
| 1 | PP No. 27/2014 | Pengelolaan BMN/BMD | Berlaku |
| 2 | Permendagri No. 19/2016 | Pedoman Pengelolaan BMD | **Diubah** |
| 3 | Permendagri No. 47/2021 | Perubahan Permendagri 19/2016 | **Berlaku** |
| 4 | Permendagri No. 7/2024 | Perubahan Kedua Permendagri 19/2016 | **Terbaru** |

### 2.2 Regulasi DKI Jakarta (PRIORITAS)
| No | Regulasi | Tentang | Status |
|----|----------|---------|--------|
| 1 | Pergub No. 67/2022 | Kebijakan Akuntansi DKI Jakarta | Berlaku |
| 2 | Kepgub No. 734/2022 | Pedoman Pelaksanaan Penyelesaian KDP | Berlaku |
| 3 | Kepgub No. 52/2023 | Tim Inventarisasi BMD | Berlaku |
| 4 | Insekda No. 11/2024 | Inventarisasi KIB B TA 2024 | **Aktif** |
| 5 | Insekda No. 20/2025 | Inventarisasi KIB E & ATB 2025 | **Aktif** |

> ⚠️ **PENTING:** Format KIB untuk DKI Jakarta mengikuti standar BPAD DKI Jakarta, BUKAN format generic Permendagri!

---

## 3. KIB B - Peralatan dan Mesin (18 Kolom) ⭐ PRIORITAS MVP

**Header:** "KARTU INVENTARIS BARANG (KIB) B - PERALATAN DAN MESIN"
**Sumber Resmi:** PDF BPAD DKI Jakarta (Update form: 07/04/2022, Rekon Semester 1 Tahun 2024)
**Status Verifikasi:** ✅ TERVERIFIKASI dari dokumen resmi BPAD DKI Jakarta

### 3.1 Struktur Kolom BPAD DKI Jakarta (TERVERIFIKASI)

**Sumber:** PDF Resmi BPAD DKI Jakarta (Update form: 07/04/2022, Rekon Semester 1 Tahun 2024)
**URL:** https://bkddki.jakarta.go.id/download/detail/N3Q3NR1JDVVKMY9

| No | Kolom | Nama Field (Resmi BPAD) | Mapping Database | Wajib? | Keterangan |
|----|-------|-------------------------|------------------|--------|------------|
| 1 | A | NO. | (auto-increment) | Ya | Nomor urut |
| 2 | B | KODE BARANG | `kode_barang` | Ya | Sesuai Katalog Regional BPAD |
| 3 | C | REG. | `nomor_register` | Ya | Nomor Register/NUP |
| 4 | D | JENIS BARANG | `nama_barang` | Ya | Nama barang sesuai katalog |
| 5 | E | UKU-RAN | `ukuran_cc` | Tidak | Ukuran/CC |
| 6 | F | SATU-AN | `satuan` | Ya | BH/Unit/Set/Buah |
| 7 | G | TGL. OLEH (DD/MM/YYYY) | `tanggal_perolehan` | Ya | Tanggal perolehan |
| 8 | H | BA-HAN | `bahan` | Tidak | Material/bahan |
| 9 | I | MEREK | `merk` | Tidak | Merk barang |
| 10 | J | TYPE | `tipe` | Tidak | Tipe/model |
| 11 | K | TGL. BPKB/TGL. DOK. (DD/MM/YYYY) | `tanggal_dokumen` | Tidak | Tanggal dokumen |
| 12 | L | NO. CHASIS/NO. RANGKA | `nomor_rangka` | Tidak | Untuk kendaraan |
| 13 | M | NO. MESIN/NO. PABRIK | `nomor_mesin` | Tidak | Nomor mesin/pabrik |
| 14 | N | NOMOR POLISI | `nomor_polisi` | Tidak | Untuk kendaraan |
| 15 | O | ASAL OLEH | `asal_usul` | Ya | Asal usul (Pembelian/Hibah/dll) |
| 16 | P | HARGA (Rp.) | `harga` | Ya | **Rupiah penuh** (bukan ribuan) |
| 17 | Q | KAPITALISASI (Rp.) | `kapitalisasi` | Tidak | Nilai kapitalisasi (Rp.) |
| 18 | R | TOTAL (Rp.) | `total_harga` | Ya | Total harga

### 3.2 Perbedaan dengan Format Permendagri Generic

| Aspek | Permendagri Generic | BPAD DKI Jakarta |
|-------|---------------------|------------------|
| Jumlah Kolom | 17 kolom | **18 kolom** |
| Satuan Harga | Ribuan (Rp) | **Rupiah penuh (Rp.)** |
| Kolom SATUAN | Tidak ada | **Ada** |
| Kolom KAPITALISASI | Tidak ada | **Ada** |
| Format Tanggal | Tidak spesifik | **DD/MM/YYYY** |
| Kolom TGL. BPKB/DOK | Tidak ada | **Ada** |

### 3.3 Catatan Penting KIB B

1. **Harga dalam Rupiah penuh** - BUKAN ribuan seperti format lama
2. **Kolom SATUAN wajib diisi** - BH (Buah), Unit, Set, dll
3. **Format tanggal DD/MM/YYYY** - Konsisten untuk semua field tanggal
4. **Kolom 12-14 khusus kendaraan** - Bisa dikosongkan untuk non-kendaraan
5. **KAPITALISASI** - Nilai tambahan untuk aset yang dikapitalisasi
6. **Kolom "TGL. OLEH"** - Menggabungkan tanggal perolehan dan sumber perolehan

---

## 4. KIB A - Tanah (14 Kolom)

**Header:** "KARTU INVENTARIS BARANG (KIB) A - TANAH"

| No | Kolom | Nama Field | Mapping Database | Wajib? |
|----|-------|------------|------------------|--------|
| 1 | A | No Urut | (auto-increment) | Ya |
| 2 | B | Nama Barang/Jenis Barang | `item_name` | Ya |
| 3 | C | Kode Barang | `regional_code` | Ya |
| 4 | D | Register | `nup` | Ya |
| 5 | E | Luas (M²) | `land_area` | Ya |
| 6 | F | Tahun Pengadaan | `acquisition_year` | Ya |
| 7 | G | Letak/Alamat | `location_address` | Ya |
| 8 | H | Status Tanah - Hak | `land_right_status` | Ya |
| 9 | I | Sertifikat - Tanggal | `certificate_date` | Tidak |
| 10 | J | Sertifikat - Nomor | `certificate_number` | Tidak |
| 11 | K | Penggunaan | `usage` | Ya |
| 12 | L | Asal Usul | `source_fund` | Ya |
| 13 | M | Harga (Rp.) | `price` | Ya |
| 14 | N | Keterangan | `notes` | Tidak |

---

## 5. KIB C - Gedung dan Bangunan (17 Kolom)

**Header:** "KARTU INVENTARIS BARANG (KIB) C - GEDUNG DAN BANGUNAN"

| No | Kolom | Nama Field | Mapping Database | Wajib? |
|----|-------|------------|------------------|--------|
| 1 | A | No Urut | (auto-increment) | Ya |
| 2 | B | Nama Barang/Jenis Barang | `item_name` | Ya |
| 3 | C | Kode Barang | `regional_code` | Ya |
| 4 | D | Nomor Register | `nup` | Ya |
| 5 | E | Kondisi Bangunan | `condition` | Ya |
| 6 | F | Konstruksi - Bertingkat | `is_multi_story` | Ya |
| 7 | G | Konstruksi - Beton | `is_concrete` | Ya |
| 8 | H | Luas Lantai (M²) | `floor_area` | Ya |
| 9 | I | Letak/Lokasi Alamat | `location_address` | Ya |
| 10 | J | Dokumen - Tanggal | `document_date` | Tidak |
| 11 | K | Dokumen - Nomor | `document_number` | Tidak |
| 12 | L | Luas Tanah (M²) | `land_area` | Tidak |
| 13 | M | Status Tanah | `land_status` | Tidak |
| 14 | N | Nomor Kode Tanah | `land_code` | Tidak |
| 15 | O | Asal Usul | `source_fund` | Ya |
| 16 | P | Harga (Rp.) | `price` | Ya |
| 17 | Q | Keterangan | `notes` | Tidak |

**Catatan Kondisi:**
- B = Baik
- KB = Kurang Baik
- RB = Rusak Berat

---

## 6. KIB D - Jalan, Irigasi, dan Jaringan (16 Kolom)

**Header:** "KARTU INVENTARIS BARANG (KIB) D - JALAN, IRIGASI DAN JARINGAN"

| No | Kolom | Nama Field | Mapping Database | Wajib? |
|----|-------|------------|------------------|--------|
| 1 | A | No Urut | (auto-increment) | Ya |
| 2 | B | Nama Barang/Jenis Barang | `item_name` | Ya |
| 3 | C | Kode Barang | `regional_code` | Ya |
| 4 | D | Nomor Register | `nup` | Ya |
| 5 | E | Konstruksi | `construction_type` | Ya |
| 6 | F | Panjang (Km) | `length_km` | Ya |
| 7 | G | Lebar (M) | `width_m` | Ya |
| 8 | H | Luas (M²) | `area_m2` | Ya |
| 9 | I | Letak/Alamat | `location_address` | Ya |
| 10 | J | Dokumen - Tanggal | `document_date` | Tidak |
| 11 | K | Dokumen - Nomor | `document_number` | Tidak |
| 12 | L | Status Tanah | `land_status` | Tidak |
| 13 | M | Nomor Kode Tanah | `land_code` | Tidak |
| 14 | N | Asal Usul | `source_fund` | Ya |
| 15 | O | Harga (Rp.) | `price` | Ya |
| 16 | P | Keterangan | `notes` | Tidak |

---

## 7. KIB E - Aset Tetap Lainnya (16 Kolom)

**Header:** "KARTU INVENTARIS BARANG (KIB) E - ASET TETAP LAINNYA"

| No | Kolom | Nama Field | Mapping Database | Wajib? |
|----|-------|------------|------------------|--------|
| 1 | A | No Urut | (auto-increment) | Ya |
| 2 | B | Nama Barang/Jenis Barang | `item_name` | Ya |
| 3 | C | Kode Barang | `regional_code` | Ya |
| 4 | D | Nomor Register | `nup` | Ya |
| 5 | E | Buku - Judul/Pencipta | `book_title_author` | Tidak |
| 6 | F | Buku - Spesifikasi | `book_specification` | Tidak |
| 7 | G | Barang Bercorak - Asal Daerah | `origin_region` | Tidak |
| 8 | H | Barang Bercorak - Pencipta | `creator` | Tidak |
| 9 | I | Barang Bercorak - Bahan | `material` | Tidak |
| 10 | J | Hewan/Ternak - Jenis | `animal_type` | Tidak |
| 11 | K | Hewan/Ternak - Ukuran | `animal_size` | Tidak |
| 12 | L | Jumlah | `quantity` | Ya |
| 13 | M | Tahun Cetak/Pembelian | `acquisition_year` | Ya |
| 14 | N | Asal Usul | `source_fund` | Ya |
| 15 | O | Harga (Rp.) | `price` | Ya |
| 16 | P | Keterangan | `notes` | Tidak |

---

## 8. KIB F - Konstruksi Dalam Pengerjaan (12 Kolom)

**Header:** "KARTU INVENTARIS BARANG (KIB) F - KONSTRUKSI DALAM PENGERJAAN"

| No | Kolom | Nama Field | Mapping Database | Wajib? |
|----|-------|------------|------------------|--------|
| 1 | A | No Urut | (auto-increment) | Ya |
| 2 | B | Nama Barang/Jenis Barang | `item_name` | Ya |
| 3 | C | Kode Barang | `regional_code` | Ya |
| 4 | D | Nomor Register | `nup` | Ya |
| 5 | E | Bangunan | `building_type` | Ya |
| 6 | F | Konstruksi - Bertingkat | `is_multi_story` | Ya |
| 7 | G | Konstruksi - Beton | `is_concrete` | Ya |
| 8 | H | Luas (M²) | `area_m2` | Ya |
| 9 | I | Letak/Alamat | `location_address` | Ya |
| 10 | J | Dokumen - Tanggal/Nomor | `document_info` | Tidak |
| 11 | K | Asal Usul | `source_fund` | Ya |
| 12 | L | Harga (Rp.) | `price` | Ya |

---

## 9. Struktur Layout Excel BPAD DKI Jakarta

### 9.1 Header Section (Row 1-6)

```text
Row 1: PROVINSI          : DKI JAKARTA
Row 2: UNIT ORGANISASI   : [Nama SKPD/UKPD]
Row 3: SUB UNIT ORGANISASI: [Nama Sub Unit]
Row 4: KODE SKPD/UKPD    : [Kode]
Row 5: [Kosong]
Row 6: KARTU INVENTARIS BARANG (KIB) B
       (Peralatan dan Mesin) BPAD
       BADAN PENGELOLAAN ASET DAERAH
       JAYA RAYA
```

### 9.2 Column Header Section (Row 7-10)

- Row 7-8: Header utama dengan merged cells
- Row 9: Sub-header (jika ada)
- Row 10: Nomor kolom (1, 2, 3, ...)

### 9.3 Data Section (Row 11+)

- Data dimulai dari row 11
- Setiap baris = 1 aset
- Format tanggal: DD/MM/YYYY

### 9.4 Footer Section

```text
- KAPITALISASI TOTAL (Rp.)
- Update form: [tanggal]
- Rekon Semester [X] Tahun [YYYY]
- Tanda tangan:
  * Mengetahui, Kepala SKPD/UKPD
  * Pengurus Barang
```

---

## 10. Database Schema Update

### 10.1 Field Tambahan untuk KIB B (BPAD DKI Jakarta)

```sql
-- Tambahan field untuk KIB B format BPAD DKI Jakarta
ALTER TABLE Asset ADD COLUMN unit VARCHAR(20) DEFAULT 'BH';
ALTER TABLE Asset ADD COLUMN acquired_by VARCHAR(100);
ALTER TABLE Asset ADD COLUMN document_date DATE;
ALTER TABLE Asset ADD COLUMN document_issuer VARCHAR(100);
ALTER TABLE Asset ADD COLUMN brand VARCHAR(100);
ALTER TABLE Asset ADD COLUMN type VARCHAR(100);
ALTER TABLE Asset ADD COLUMN capitalization DECIMAL(18,2) DEFAULT 0;
ALTER TABLE Asset ADD COLUMN total_price DECIMAL(18,2);

-- Catatan: price sekarang dalam Rupiah penuh, BUKAN ribuan
-- Perlu migrasi data jika sebelumnya dalam ribuan
```

### 10.2 Enum untuk Satuan

```sql
-- Nilai yang valid untuk kolom unit
-- BH = Buah
-- Unit = Unit
-- Set = Set
-- Paket = Paket
-- Rim = Rim
-- Dus = Dus
```

---

## 11. Export Strategy (Contract-Based)

### 11.1 Pendekatan Hardcoded untuk BPAD DKI Jakarta

```csharp
public class KibBExporterBPAD
{
    // Header info
    private const string PROVINSI = "DKI JAKARTA";
    private const string BPAD_HEADER = "BADAN PENGELOLAAN ASET DAERAH";
    private const string JAYA_RAYA = "JAYA RAYA";

    // Layout
    private const int HEADER_START_ROW = 1;
    private const int COLUMN_HEADER_ROW = 7;
    private const int DATA_START_ROW = 11;

    // 18 Kolom BPAD DKI Jakarta
    private readonly string[] COLUMNS = {
        "NO.",
        "KODE BARANG",
        "REG.",
        "JENIS BARANG",
        "UKU-RAN",
        "SATU-AN",
        "TGL. OLEH (DD/MM/YYYY)",
        "BA-HAN",
        "MEREK",
        "TYPE",
        "TGL. BPKB/TGL. DOK. (DD/MM/YYYY)",
        "NO. CHASIS/NO. RANGKA",
        "NO. MESIN/NO. PABRIK",
        "NOMOR POLISI",
        "ASAL OLEH",
        "HARGA (Rp.)",
        "KAPITALISASI (Rp.)",
        "TOTAL (Rp.)"
    };

    // Format tanggal
    private const string DATE_FORMAT = "dd/MM/yyyy";

    // Harga dalam Rupiah penuh (BUKAN ribuan)
    private decimal FormatPrice(decimal price) => price;
}
```

### 11.2 Validasi Sebelum Export

| Check | Deskripsi | Aksi Jika Gagal |
|-------|-----------|-----------------|
| Field Wajib | NO, KODE BARANG, REG, JENIS BARANG, SATUAN, TGL OLEH, ASAL OLEH, HARGA, TOTAL | Blokir export |
| Kode Barang | Sesuai Katalog Regional BPAD | Warning |
| Format Tanggal | DD/MM/YYYY | Error |
| Harga | > 0, dalam Rupiah penuh | Warning |
| Status Aset | Hanya status 'Aktif' | Filter otomatis |
| Backup | Dalam 7 hari terakhir | Blokir export |
| Sign-off | Wajib sebelum export | Blokir export |

---

## 12. Asal Usul (Source Fund) - Nilai Valid

| Kode | Deskripsi |
|------|-----------|
| 1 | Pembelian |
| 2 | Hibah |
| 3 | Sumbangan |
| 4 | Tukar Menukar |
| 5 | Rampasan |
| 6 | Sitaan |
| 7 | Lainnya |

---

## 13. Kondisi Barang - Nilai Valid

| Kode | Deskripsi | Warna UI |
|------|-----------|----------|
| B | Baik | 🟢 Hijau |
| KB | Kurang Baik | 🟡 Kuning |
| RB | Rusak Berat | 🔴 Merah |

---

## 14. MVP Scope untuk SMAN 62 Jakarta

### 14.1 Sprint 4 (Reporting) - PRIORITAS

- ✅ **KIB B (Peralatan & Mesin)** - Format BPAD DKI Jakarta 18 kolom
- ✅ **Raw CSV Export** - Fallback jika Excel bermasalah

### 14.2 Post-Pilot

- KIB A (Tanah)
- KIB C (Gedung dan Bangunan)
- KIB D (Jalan, Irigasi, Jaringan)
- KIB E (Aset Tetap Lainnya)
- KIB F (Konstruksi Dalam Pengerjaan)

---

## 15. Referensi & Sumber

### 15.1 Sumber Resmi

| Sumber | URL | Keterangan |
|--------|-----|------------|
| BPAD DKI Jakarta | bpad.jakarta.go.id | Portal resmi BPAD |
| BKD DKI Jakarta | bkddki.jakarta.go.id | Contoh KIB B |
| Sensus BMD DKI | sensus-kib-e-atb.crd.co | Portal inventarisasi |
| Peraturan BPK | peraturan.bpk.go.id | Database regulasi |
| JDIH DKI Jakarta | jdih.jakarta.go.id | Produk hukum DKI |

### 15.2 Aplikasi Terkait

- **JAK-ASET** - Aplikasi inventarisasi BMD DKI Jakarta
- **SIMDA BMD** - Sistem Informasi Manajemen Daerah BMD

---

## 16. Catatan Revisi

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 1.0 | 4 Jan 2026 | Initial version berdasarkan analisis file Excel |
| 2.0 | 4 Jan 2026 | Update format KIB B sesuai BPAD DKI Jakarta, tambah dasar hukum terkini, update referensi Insekda 2024/2025 |
| 3.0 | 11 Jan 2026 | VERIFIKASI RESMI - Format dikonfirmasi dari PDF resmi BPAD DKI Jakarta |
| **3.1** | **11 Jan 2026** | **KOREKSI** - Format KIB B dikoreksi menjadi **18 kolom** (bukan 20) sesuai PDF resmi. Kolom "OLEH" digabung dengan "TGL." dan "ASAL" |

---

## 17. Status Verifikasi

> ✅ **FORMAT 18 KOLOM TERVERIFIKASI**
> 
> Format KIB B **18 kolom** telah diverifikasi dari dokumen resmi BPAD DKI Jakarta yang di-host di website BKD DKI Jakarta. Dokumen ini digunakan untuk Rekon Semester 1 Tahun 2024.
>
> **Sumber:** https://bkddki.jakarta.go.id/download/detail/N3Q3NR1JDVVKMY9
>
> **Catatan Koreksi (v3.1):** Sebelumnya tercatat 20 kolom, setelah verifikasi ulang dari PDF ternyata **18 kolom**. Perbedaan karena kolom "OLEH" digabung dengan kolom tanggal/asal.

---

## Akhir Dokumen
