# Dokumentasi Proyek Simanis62 V2


## Alur Kerja dan Aturan Main

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 5 Januari 2026 | Architecture Engineer | Dokumen awal |

---

## 1. Pendahuluan

Dokumen ini menjelaskan alur kerja operasional dan aturan main (business rules) sistem Simanis62 V2. Dokumen ini melengkapi:

- **Dokumen 1:** Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala dan Asumsi
- **Dokumen 2:** Pemilik Kebenaran, Masalah Inti yang Diselesaikan, Konteks dan Batasan

### 1.1 Tujuan Dokumen

Dokumen ini bertujuan untuk:

1. Mendefinisikan alur kerja untuk setiap role pengguna
2. Menjelaskan proses bisnis utama sistem
3. Menetapkan business rules dan validasi data
4. Mendokumentasikan state transition aset
5. Menjelaskan strategi error handling

### 1.2 Ruang Lingkup

Dokumen ini mencakup:

- Alur kerja untuk 3 role: Admin Sekolah, Guru, Kepala Sekolah
- 5 proses bisnis utama: CRUD Aset, Laporan KIB, Mutasi, Pencarian, Ekspor
- Business rules untuk semua field data aset
- State transition diagram untuk siklus hidup aset
- Error handling dan validasi rules

---

## 2. Glossary

| Istilah | Definisi |
|---------|----------|
| Aset | Barang Milik Daerah (BMD) yang tercatat dalam sistem |
| KIB | Kartu Inventaris Barang (A-F) sesuai Permendagri 19/2016 |
| KIR | Kartu Inventaris Ruangan |
| Mutasi | Perpindahan aset dari satu ruangan ke ruangan lain |
| Soft Delete | Penghapusan aset dengan status "Dihapus", data tidak benar-benar dihapus |
| Nomor Register | Nomor urut unik per kategori KIB |
| Kode Barang | Kode identifikasi unik aset sesuai standar BMD |

---

## 3. Role dan Hak Akses

### 3.1 Admin Sekolah

**Tanggung Jawab:**

- Mengelola data aset (Create, Read, Update, Delete)
- Membuat dan mengekspor laporan KIB
- Mencatat mutasi aset antarruangan
- Mengelola data ruangan
- Mengelola user Viewer (Guru)

**Hak Akses:**

- ✅ CRUD data aset (semua kategori KIB)
- ✅ Generate laporan KIB A-F
- ✅ Generate laporan KIR
- ✅ Ekspor ke Excel
- ✅ Mutasi aset
- ✅ Soft delete aset
- ✅ Pencarian aset
- ✅ Cetak laporan
- ✅ Manajemen user Viewer

### 3.2 Guru (Viewer)

**Tanggung Jawab:**

- Melihat aset di ruangan tertentu
- Melaporkan kondisi aset (melalui Admin)
- Melihat riwayat mutasi aset

**Hak Akses:**

- ✅ Read data aset (view only)
- ✅ Pencarian aset
- ✅ Lihat laporan KIR per ruangan
- ❌ CRUD data aset
- ❌ Generate laporan KIB
- ❌ Ekspor ke Excel
- ❌ Mutasi aset
- ❌ Delete aset

### 3.3 Kepala Sekolah

**Tanggung Jawab:**

- Mengawasi pengelolaan aset
- Menandatangani laporan KIB
- Mereview laporan sebelum dikirim ke Dinas

**Hak Akses:**

- ✅ Read data aset (view only)
- ✅ Lihat semua laporan KIB dan KIR
- ✅ Ekspor ke Excel (untuk review)
- ✅ Cetak laporan
- ❌ CRUD data aset
- ❌ Mutasi aset
- ❌ Delete aset

**Catatan Implementasi (v2.0):**
Sistem menggunakan **2 technical roles** (Admin, Viewer) untuk mendukung **3 business roles** (Admin, Guru, Kepala Sekolah). Kepala Sekolah diimplementasikan sebagai Viewer dengan flag `dapat_ekspor=true` di tabel users. Ini menyederhanakan authorization logic sambil tetap memenuhi semua kebutuhan bisnis.

**Technical Implementation:**
- Database: `users.role = "Viewer"` AND `users.dapat_ekspor = true`
- API Middleware: Check `dapat_ekspor` flag untuk endpoint export
- UI: Show export buttons jika `dapat_ekspor = true`

**Future Enhancement:**
Jika diperlukan, role terpisah "Kepala Sekolah" dapat ditambahkan tanpa breaking changes dengan menambahkan enum value baru di `UserRole`.

---

## 4. Siklus Hidup Aset (State Transition)

### 4.1 Status Aset

Sistem mendukung 5 status aset:

| Status | Deskripsi | Warna Indikator |
|--------|-----------|-----------------|
| **Baru** | Aset baru tercatat, belum diverifikasi | Kuning |
| **Aktif** | Aset telah diverifikasi dan digunakan | Hijau |
| **Mutasi** | Aset dalam proses perpindahan ruangan | Biru |
| **Rusak** | Aset memiliki kondisi Rusak Ringan atau Rusak Berat | Oranye |
| **Dihapus** | Aset tidak lagi tercatat sebagai inventaris aktif (soft delete) | Abu-abu |

### 4.2 Diagram State Transition

```text
┌─────────┐
│  BARU   │ (Status awal saat input data)
└────┬────┘
     │ Verifikasi Admin
     ▼
┌─────────┐
│  AKTIF  │ ◄──────────────┐
└────┬────┘                │
     │                     │ Selesai Mutasi
     ├─────────────────────┤
     │ Mutasi Aset         │
     ▼                     │
┌─────────┐                │
│ MUTASI  │────────────────┘
└─────────┘

┌─────────┐
│  AKTIF  │
└────┬────┘
     │ Update Kondisi
     ▼
┌─────────┐
│  RUSAK  │ (Kondisi: Rusak Ringan/Berat)
└────┬────┘
     │ Perbaikan/Update
     ▼
┌─────────┐
│  AKTIF  │
└─────────┘

┌─────────┐     ┌─────────┐
│  AKTIF  │ ──► │ DIHAPUS │ (Soft Delete)
└─────────┘     └─────────┘
     ▲               │
     │               │ Restore (opsional)
     └───────────────┘
```

### 4.3 Aturan Transisi Status

| Dari Status | Ke Status | Kondisi | Aksi Sistem |
|-------------|-----------|---------|-------------|
| Baru | Aktif | Admin verifikasi data lengkap | Update status, catat timestamp |
| Aktif | Mutasi | Admin memulai proses mutasi | Update status, catat ruangan asal |
| Mutasi | Aktif | Admin konfirmasi mutasi selesai | Update status, update ruangan, catat riwayat |
| Aktif | Rusak | Admin update kondisi menjadi Rusak Ringan/Berat | Update status dan kondisi |
| Rusak | Aktif | Admin update kondisi menjadi Baik | Update status dan kondisi |
| Aktif | Dihapus | Admin soft delete aset | Update status, catat timestamp penghapusan |
| Rusak | Dihapus | Admin soft delete aset rusak | Update status, catat timestamp penghapusan |
| Dihapus | Aktif | Admin restore aset (opsional) | Update status, catat timestamp restore |

**Catatan Penting:**

- Status "Baru" hanya untuk aset yang baru diinput dan belum diverifikasi
- Status "Mutasi" bersifat temporary selama proses perpindahan
- Status "Rusak" otomatis terdeteksi dari field "Kondisi"
- Status "Dihapus" adalah soft delete, data tetap ada di database

---

## 5. Business Rules dan Validasi Data

### 5.1 Aturan Umum (Berlaku untuk Semua KIB)

| Field | Aturan | Validasi | Pesan Error |
|-------|--------|----------|-------------|
| **Kode Barang** | Wajib, unik, format standar BMD | Regex: `^\d{2}\.\d{2}\.\d{2}\.\d{4}$` | "Kode barang harus unik dan mengikuti format XX.XX.XX.XXXX" |
| **Nama Barang** | Wajib, min 3 karakter, max 200 karakter | Length: 3-200 | "Nama barang harus diisi (3-200 karakter)" |
| **Nomor Register** | Wajib, auto-generated, sequential per KIB | Auto-increment per kategori | "Nomor register dihasilkan otomatis oleh sistem" |
| **Tahun Perolehan** | Wajib, 4 digit, tidak boleh > tahun berjalan | Range: 1900 - tahun_sekarang | "Tahun perolehan tidak valid (1900 - {tahun_sekarang})" |
| **Asal Usul** | Wajib, pilihan: Pembelian/Hibah/Bantuan | Enum: ['Pembelian', 'Hibah', 'Bantuan'] | "Pilih asal usul aset" |
| **Harga (Rp)** | Wajib, angka positif, tidak boleh nol | Min: 1, Max: 999,999,999,999 | "Harga harus berupa angka positif" |
| **Kondisi** | Wajib, 3 pilihan | Enum: ['Baik', 'Rusak Ringan', 'Rusak Berat'] | "Pilih kondisi aset" |
| **Keterangan** | Opsional, max 500 karakter | Length: 0-500 | "Keterangan maksimal 500 karakter" |

### 5.2 Aturan Khusus per Kategori KIB

#### 5.2.1 KIB A (Tanah)

| Field | Aturan | Validasi | Pesan Error |
|-------|--------|----------|-------------|
| **Luas (m²)** | Wajib, angka positif | Min: 1, Max: 999,999 | "Luas tanah harus berupa angka positif" |
| **Alamat/Lokasi** | Wajib, min 10 karakter | Length: 10-500 | "Alamat lokasi tanah harus diisi lengkap" |
| **Sertifikat** | Opsional, nomor sertifikat | Length: 0-100 | "Nomor sertifikat maksimal 100 karakter" |

#### 5.2.2 KIB B (Peralatan dan Mesin)

| Field | Aturan | Validasi | Pesan Error |
|-------|--------|----------|-------------|
| **Merk/Type** | Wajib, min 2 karakter | Length: 2-100 | "Merk/Type harus diisi" |
| **Ukuran/CC** | Opsional | Length: 0-50 | "Ukuran/CC maksimal 50 karakter" |
| **Bahan** | Opsional | Length: 0-50 | "Bahan maksimal 50 karakter" |

#### 5.2.3 KIB C (Gedung dan Bangunan)

| Field | Aturan | Validasi | Pesan Error |
|-------|--------|----------|-------------|
| **Luas (m²)** | Wajib, angka positif | Min: 1, Max: 999,999 | "Luas bangunan harus berupa angka positif" |
| **Alamat/Lokasi** | Wajib, min 10 karakter | Length: 10-500 | "Alamat lokasi bangunan harus diisi lengkap" |
| **Bertingkat** | Opsional, jumlah lantai | Range: 1-10 | "Jumlah lantai antara 1-10" |

#### 5.2.4 KIB D (Jalan, Irigasi, dan Jaringan)

| Field | Aturan | Validasi | Pesan Error |
|-------|--------|----------|-------------|
| **Panjang (m)** | Wajib, angka positif | Min: 1, Max: 999,999 | "Panjang harus berupa angka positif" |
| **Lebar (m)** | Wajib, angka positif | Min: 0.1, Max: 999 | "Lebar harus berupa angka positif" |
| **Alamat/Lokasi** | Wajib, min 10 karakter | Length: 10-500 | "Alamat lokasi harus diisi lengkap" |

#### 5.2.5 KIB E (Aset Tetap Lainnya)

| Field | Aturan | Validasi | Pesan Error |
|-------|--------|----------|-------------|
| **Judul/Nama** | Wajib (untuk buku) | Length: 3-200 | "Judul/Nama harus diisi" |
| **Penerbit** | Opsional (untuk buku) | Length: 0-100 | "Penerbit maksimal 100 karakter" |

#### 5.2.6 KIB F (Konstruksi dalam Pengerjaan)

| Field | Aturan | Validasi | Pesan Error |
|-------|--------|----------|-------------|
| **Alamat/Lokasi** | Wajib, min 10 karakter | Length: 10-500 | "Alamat lokasi konstruksi harus diisi lengkap" |
| **Persentase Selesai** | Wajib, 0-100% | Range: 0-100 | "Persentase harus antara 0-100" |
| **Kondisi** | Tidak wajib untuk KIB F | N/A | N/A |

### 5.3 Aturan Kode Barang

**Format Standar:** `XX.XX.XX.XXXX`

**Struktur:**

- **2 digit pertama:** Kode wilayah/provinsi
- **2 digit kedua:** Kode sekolah
- **2 digit ketiga:** Kode kategori KIB (01=A, 02=B, 03=C, 04=D, 05=E, 06=F)
- **4 digit terakhir:** Nomor urut aset

**Contoh:**

- `32.01.02.0001` = Provinsi 32, Sekolah 01, KIB B, Aset ke-1
- `32.01.03.0125` = Provinsi 32, Sekolah 01, KIB C, Aset ke-125

**Aturan:**

- Kode barang harus unik dalam sistem
- Sistem akan memvalidasi format saat input
- Nomor urut auto-increment per kategori KIB

### 5.4 Aturan Nomor Register

**Format:** Sequential number per kategori KIB

**Aturan:**

- Auto-generated oleh sistem
- Dimulai dari 1 untuk setiap kategori KIB
- Tidak dapat diubah setelah dibuat
- Tidak dapat di-reset (permanent)

**Contoh:**

- KIB A: 1, 2, 3, 4, ...
- KIB B: 1, 2, 3, 4, ...
- KIB C: 1, 2, 3, 4, ...

---

## 6. Alur Kerja Proses Bisnis Utama

### 6.1 Proses 1: Pencatatan Aset Baru (Create)

**Actor:** Admin Sekolah

**Prasyarat:**

- User sudah login sebagai Admin
- Data ruangan sudah tersedia

**Alur Normal:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Admin memilih menu "Tambah Aset"                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Sistem menampilkan form input data aset                 │
│    - Pilih kategori KIB (A-F)                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Admin mengisi field wajib sesuai kategori KIB:          │
│    - Kode Barang (validasi format)                          │
│    - Nama Barang                                             │
│    - Tahun Perolehan                                         │
│    - Asal Usul                                               │
│    - Harga                                                   │
│    - Kondisi                                                 │
│    - Field khusus per KIB (Luas, Merk, Alamat, dll)        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Admin klik tombol "Simpan"                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Sistem melakukan validasi:                               │
│    ✓ Semua field wajib terisi                               │
│    ✓ Format data sesuai aturan                              │
│    ✓ Kode barang unik                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Sistem menyimpan data:                                   │
│    - Generate Nomor Register otomatis                        │
│    - Set status aset = "Baru"                                │
│    - Catat timestamp created_at                              │
│    - Catat user yang input (created_by)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Sistem menampilkan pesan sukses:                         │
│    "Aset berhasil ditambahkan dengan Nomor Register: XXX"   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Admin dapat:                                              │
│    - Tambah aset baru lagi                                   │
│    - Kembali ke daftar aset                                  │
│    - Verifikasi aset (ubah status ke "Aktif")               │
└─────────────────────────────────────────────────────────────┘
```

## Alur Alternatif 1: Validasi Gagal

```text
5a. Jika validasi gagal:

    - Sistem menampilkan pesan error spesifik per field
    - Form tetap terbuka dengan data yang sudah diisi
    - Admin memperbaiki data yang error
    - Kembali ke step 4

```

## Alur Alternatif 2: Kode Barang Duplikat

```text
5b. Jika kode barang sudah ada:

    - Sistem menampilkan error: "Kode barang sudah digunakan"
    - Sistem menampilkan data aset yang menggunakan kode tersebut
    - Admin mengubah kode barang
    - Kembali ke step 4

```

## Alur Alternatif 3: Admin Batal

```text
4a. Admin klik tombol "Batal":

    - Sistem menampilkan konfirmasi: "Data belum disimpan. Yakin batal?"
    - Jika Ya: Kembali ke daftar aset
    - Jika Tidak: Tetap di form input

```

**Output:**

- Data aset tersimpan di database dengan status "Baru"
- Nomor Register ter-generate otomatis
- Timestamp dan user tercatat

---

### 6.2 Proses 2: Pembuatan Laporan KIB

**Actor:** Admin Sekolah

**Prasyarat:**

- User sudah login sebagai Admin
- Minimal ada 1 aset dengan status "Aktif"

**Alur Normal:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Admin memilih menu "Laporan KIB"                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Sistem menampilkan pilihan:                              │
│    - Kategori KIB (A/B/C/D/E/F atau Semua)                  │
│    - Tahun Perolehan (filter opsional)                      │
│    - Ruangan (filter opsional)                               │
│    - Status (Aktif/Rusak/Semua)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Admin memilih filter dan klik "Generate Laporan"         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Sistem memproses:                                         │
│    - Query data aset sesuai filter                           │
│    - Urutkan berdasarkan Nomor Register                      │
│    - Hitung total nilai per kategori                         │
│    - Format sesuai standar Permendagri 19/2016              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Sistem menampilkan preview laporan:                      │
│    - Tabel data aset dengan kolom sesuai KIB                │
│    - Total jumlah aset                                       │
│    - Total nilai aset (Rp)                                   │
│    - Tanggal generate laporan                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Admin dapat memilih:                                      │
│    - Ekspor ke Excel                                         │
│    - Cetak (Print)                                           │
│    - Kembali (ubah filter)                                   │
└─────────────────────────────────────────────────────────────┘
```

## Alur Alternatif 1: Ekspor ke Excel

```text
6a. Admin klik "Ekspor ke Excel":

    - Sistem generate file Excel (.xlsx)
    - Format sesuai template KIB standar
    - Nama file: KIB_{kategori}_{tanggal}.xlsx
    - Sistem download file ke komputer Admin
    - Tampilkan notifikasi: "File berhasil diunduh"

```

## Alur Alternatif 2: Cetak Laporan

```text
6b. Admin klik "Cetak":

    - Sistem buka dialog print browser
    - Format landscape untuk KIB dengan banyak kolom
    - Admin pilih printer dan klik Print
    - Sistem cetak laporan

```

## Alur Alternatif 3: Tidak Ada Data

```text
4a. Jika tidak ada data sesuai filter:

    - Sistem tampilkan pesan: "Tidak ada data aset untuk filter yang dipilih"
    - Admin dapat mengubah filter
    - Kembali ke step 2

```

**Output:**

- File Excel laporan KIB sesuai format standar
- Atau dokumen cetak laporan KIB

**Format Laporan KIB (Contoh KIB B):**

| No Reg | Kode Barang | Nama Barang | Merk/Type | Ukuran | Bahan | Tahun | Asal Usul | Harga (Rp) | Kondisi | Ket |
|--------|-------------|-------------|-----------|--------|-------|-------|-----------|------------|---------|-----|
| 1 | 32.01.02.0001 | Laptop | HP Pavilion | 14" | Plastik | 2023 | Pembelian | 8,500,000 | Baik | - |
| 2 | 32.01.02.0002 | Printer | Canon G2010 | A4 | Plastik | 2023 | Hibah | 2,300,000 | Baik | - |

## Total: 2 unit | Total Nilai: Rp 10,800,000

---

### 6.3 Proses 3: Mutasi Aset Antarruangan

**Actor:** Admin Sekolah

**Prasyarat:**

- User sudah login sebagai Admin
- Aset yang akan dimutasi berstatus "Aktif"
- Ruangan tujuan sudah tersedia

**Alur Normal:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Admin memilih menu "Mutasi Aset"                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Admin mencari aset yang akan dimutasi:                   │
│    - Input Kode Barang atau Nama Barang                     │
│    - Sistem menampilkan hasil pencarian                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Admin memilih aset dan klik "Mutasi"                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Sistem menampilkan form mutasi:                          │
│    - Ruangan Asal: [Otomatis terisi dari data aset]        │
│    - Ruangan Tujuan: [Dropdown pilihan ruangan]             │
│    - Tanggal Mutasi: [Default: hari ini]                    │
│    - Alasan Mutasi: [Text area]                             │
│    - Kondisi Saat Mutasi: [Dropdown: Baik/Rusak]           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Admin mengisi form dan klik "Proses Mutasi"              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Sistem melakukan validasi:                               │
│    ✓ Ruangan tujuan berbeda dari ruangan asal               │
│    ✓ Alasan mutasi terisi (min 10 karakter)                 │
│    ✓ Tanggal mutasi tidak di masa depan                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Sistem menampilkan konfirmasi:                           │
│    "Mutasi aset [Nama] dari [Ruangan Asal] ke               │
│     [Ruangan Tujuan]. Lanjutkan?"                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Admin klik "Ya, Lanjutkan"                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Sistem memproses mutasi:                                 │
│    - Update status aset = "Mutasi"                           │
│    - Simpan data mutasi ke tabel riwayat_mutasi:            │
│      * aset_id                                               │
│      * ruangan_asal_id                                       │
│      * ruangan_tujuan_id                                     │
│      * tanggal_mutasi                                        │
│      * alasan                                                │
│      * kondisi_saat_mutasi                                   │
│      * user_id (Admin yang proses)                           │
│      * status_mutasi = "Dalam Proses"                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. Sistem menampilkan pesan:                               │
│     "Mutasi berhasil diproses. Konfirmasi setelah aset      │
│      tiba di ruangan tujuan."                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 11. Admin konfirmasi mutasi selesai (setelah aset tiba):   │
│     - Buka menu "Mutasi Pending"                            │
│     - Pilih mutasi yang akan dikonfirmasi                   │
│     - Klik "Konfirmasi Selesai"                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 12. Sistem finalisasi mutasi:                               │
│     - Update ruangan aset = ruangan_tujuan                  │
│     - Update status aset = "Aktif"                          │
│     - Update status_mutasi = "Selesai"                      │
│     - Catat timestamp selesai_mutasi                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 13. Sistem menampilkan pesan sukses:                        │
│     "Mutasi selesai. Aset sekarang berada di [Ruangan]"    │
└─────────────────────────────────────────────────────────────┘
```

## Alur Alternatif 1: Ruangan Tujuan Sama dengan Asal

```text
6a. Jika ruangan tujuan = ruangan asal:

    - Sistem tampilkan error: "Ruangan tujuan harus berbeda dari ruangan asal"
    - Admin memilih ruangan tujuan yang berbeda
    - Kembali ke step 5

```

## Alur Alternatif 2: Admin Batal Mutasi

```text
8a. Admin klik "Tidak, Batal":

    - Sistem kembali ke form mutasi
    - Data form tetap tersimpan
    - Admin dapat mengubah data atau benar-benar batal

```

## Alur Alternatif 3: Mutasi Dibatalkan (Sebelum Konfirmasi)

```text
11a. Admin membatalkan mutasi yang sedang proses:

     - Buka menu "Mutasi Pending"
     - Pilih mutasi yang akan dibatalkan
     - Klik "Batalkan Mutasi"
     - Sistem konfirmasi: "Yakin batalkan mutasi?"
     - Jika Ya:
       - Update status aset = "Aktif"
       - Update status_mutasi = "Dibatalkan"
       - Ruangan aset tetap di ruangan asal
       - Catat alasan pembatalan

```

**Output:**

- Data mutasi tersimpan di tabel riwayat_mutasi
- Aset berpindah ruangan
- Riwayat mutasi dapat diaudit kapan saja

**Aturan Bisnis Mutasi:**

1. Aset hanya bisa dimutasi jika status "Aktif"
2. Satu aset hanya bisa memiliki 1 mutasi pending
3. Mutasi harus dikonfirmasi dalam 7 hari, jika tidak otomatis dibatalkan
4. Riwayat mutasi tidak dapat dihapus (audit trail)

---

### 6.4 Proses 4: Pencarian Aset

**Actor:** Admin Sekolah, Guru (Viewer), Kepala Sekolah

**Prasyarat:**

- User sudah login
- Minimal ada 1 aset di database

**Alur Normal:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. User memilih menu "Pencarian Aset"                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Sistem menampilkan form pencarian dengan filter:         │
│    - Kata Kunci (Kode/Nama Barang)                          │
│    - Kategori KIB (A/B/C/D/E/F/Semua)                       │
│    - Ruangan (Dropdown/Semua)                               │
│    - Kondisi (Baik/Rusak/Semua)                             │
│    - Status (Aktif/Rusak/Dihapus/Semua)                     │
│    - Tahun Perolehan (Range)                                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. User mengisi minimal 1 filter dan klik "Cari"            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Sistem melakukan pencarian:                              │
│    - Query database dengan filter yang dipilih              │
│    - Pencarian kata kunci di: Kode Barang, Nama Barang      │
│    - Urutkan hasil berdasarkan relevansi                    │
│    - Batasi hasil maksimal 100 item per halaman             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Sistem menampilkan hasil pencarian:                      │
│    - Tabel dengan kolom: Kode, Nama, KIB, Ruangan,         │
│      Kondisi, Status, Harga                                  │
│    - Jumlah hasil ditemukan                                  │
│    - Pagination jika > 100 item                              │
│    - Waktu pencarian (< 5 detik)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. User dapat:                                               │
│    - Klik aset untuk melihat detail                         │
│    - Ekspor hasil pencarian ke Excel                        │
│    - Ubah filter dan cari lagi                              │
│    - [Admin only] Edit/Hapus aset dari hasil               │
└─────────────────────────────────────────────────────────────┘
```

## Alur Alternatif 1: Tidak Ada Hasil

```text
5a. Jika tidak ada hasil ditemukan:

    - Sistem tampilkan pesan: "Tidak ada aset yang sesuai dengan pencarian"
    - Sistem tampilkan saran:
      - "Coba gunakan kata kunci yang lebih umum"
      - "Periksa ejaan kata kunci"
      - "Kurangi jumlah filter"
    - User dapat mengubah filter
    - Kembali ke step 3

```

## Alur Alternatif 2: Pencarian Cepat (Quick Search)

```text
2a. User langsung ketik di search box (tanpa buka form filter):

    - Sistem melakukan pencarian real-time (debounce 500ms)
    - Pencarian di Kode Barang dan Nama Barang
    - Tampilkan hasil maksimal 10 item
    - User dapat klik "Lihat Semua Hasil" untuk full search

```

## Alur Alternatif 3: Lihat Detail Aset

```text
6a. User klik salah satu aset dari hasil:

    - Sistem tampilkan detail lengkap aset:
      - Semua field data aset
      - Foto aset (jika ada)
      - Riwayat mutasi
      - Riwayat perubahan kondisi
    - [Admin only] Tombol Edit dan Hapus
    - Tombol Kembali ke hasil pencarian

```

**Output:**

- Daftar aset yang sesuai dengan kriteria pencarian
- Waktu pencarian < 5 detik (sesuai indikator keberhasilan)

**Aturan Pencarian:**

1. Pencarian case-insensitive
2. Pencarian kata kunci menggunakan LIKE %keyword%
3. Multiple filter menggunakan operator AND
4. Hasil diurutkan berdasarkan: exact match > partial match > relevance
5. Viewer hanya bisa melihat aset dengan status "Aktif" dan "Rusak"
6. Admin bisa melihat semua status termasuk "Dihapus"

---

### 6.5 Proses 5: Penghapusan Aset (Soft Delete)

**Actor:** Admin Sekolah

**Prasyarat:**

- User sudah login sebagai Admin
- Aset yang akan dihapus berstatus "Aktif" atau "Rusak"

**Alur Normal:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Admin mencari aset yang akan dihapus                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Admin klik tombol "Hapus" pada detail aset               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Sistem menampilkan form konfirmasi penghapusan:          │
│    - Informasi aset yang akan dihapus                       │
│    - Alasan Penghapusan: [Text area, wajib]                 │
│    - Tanggal Penghapusan: [Default: hari ini]               │
│    - Checkbox: "Saya yakin ingin menghapus aset ini"        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Admin mengisi alasan dan centang checkbox                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Admin klik "Hapus Aset"                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Sistem melakukan validasi:                               │
│    ✓ Alasan penghapusan terisi (min 20 karakter)            │
│    ✓ Checkbox konfirmasi sudah dicentang                    │
│    ✓ Aset tidak sedang dalam status "Mutasi"                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Sistem menampilkan konfirmasi final:                     │
│    "PERHATIAN: Aset akan dihapus dari inventaris aktif.     │
│     Data tetap tersimpan untuk audit. Lanjutkan?"           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Admin klik "Ya, Hapus"                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Sistem melakukan soft delete:                            │
│    - Update status aset = "Dihapus"                         │
│    - Simpan data penghapusan:                               │
│      * deleted_at (timestamp)                               │
│      * deleted_by (user_id Admin)                           │
│      * delete_reason (alasan)                               │
│    - Data aset TIDAK dihapus dari database                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. Sistem menampilkan pesan sukses:                        │
│     "Aset berhasil dihapus dari inventaris aktif"           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 11. Aset tidak muncul lagi di:                              │
│     - Daftar aset aktif                                     │
│     - Laporan KIB                                           │
│     - Laporan KIR                                           │
│     - Pencarian (kecuali filter "Dihapus")                  │
└─────────────────────────────────────────────────────────────┘
```

## Alur Alternatif 1: Aset Sedang Mutasi

```text
6a. Jika aset sedang dalam status "Mutasi":

    - Sistem tampilkan error: "Aset tidak dapat dihapus karena sedang dalam proses mutasi"
    - Sistem tampilkan info mutasi yang sedang berjalan
    - Admin harus menyelesaikan atau membatalkan mutasi terlebih dahulu
    - Kembali ke daftar aset

```

## Alur Alternatif 2: Alasan Tidak Cukup Panjang

```text
6b. Jika alasan < 20 karakter:

    - Sistem tampilkan error: "Alasan penghapusan harus minimal 20 karakter"
    - Form tetap terbuka
    - Admin melengkapi alasan
    - Kembali ke step 5

```

## Alur Alternatif 3: Admin Batal Hapus

```text
8a. Admin klik "Tidak, Batal":

    - Sistem kembali ke detail aset
    - Data aset tidak berubah

```

## Alur Alternatif 4: Restore Aset (Opsional)

```text
11a. Admin ingin mengembalikan aset yang sudah dihapus:

     - Buka menu "Aset Dihapus"
     - Cari aset yang akan di-restore
     - Klik "Restore Aset"
     - Sistem konfirmasi: "Kembalikan aset ke inventaris aktif?"
     - Jika Ya:
       - Update status aset = "Aktif"
       - Catat restored_at dan restored_by
       - Aset muncul kembali di daftar aktif

```

**Output:**

- Aset berstatus "Dihapus" (soft delete)
- Data tetap tersimpan untuk audit
- Riwayat penghapusan tercatat

**Aturan Bisnis Penghapusan:**

1. Hanya Admin yang dapat menghapus aset
2. Aset dengan status "Mutasi" tidak dapat dihapus
3. Alasan penghapusan wajib diisi (min 20 karakter)
4. Data aset tidak benar-benar dihapus dari database (soft delete)
5. Aset yang dihapus tidak muncul di laporan KIB
6. Riwayat penghapusan tidak dapat dihapus (audit trail)
7. Restore aset adalah fitur opsional (dapat ditambahkan kemudian)

---

## 7. Strategi Error Handling dan Validasi

### 7.1 Prinsip Error Handling

Sistem Simanis62 V2 menerapkan prinsip error handling yang user-friendly:

1. **Pesan Error Jelas dan Spesifik**
   - Hindari pesan teknis (contoh: "Database connection failed")
   - Gunakan bahasa yang mudah dipahami pengguna
   - Berikan solusi atau saran perbaikan

2. **Validasi di Dua Layer**
   - **Client-side:** Validasi real-time saat user input (JavaScript/WPF)
   - **Server-side:** Validasi final sebelum simpan ke database (FastAPI)

3. **Feedback Visual yang Konsisten**
   - Error: Warna merah, icon ❌
   - Warning: Warna kuning, icon ⚠️
   - Success: Warna hijau, icon ✅
   - Info: Warna biru, icon ℹ️

### 7.2 Kategori Error dan Handling

#### 7.2.1 Validation Error (Input Tidak Valid)

**Contoh Kasus:**

- Field wajib tidak diisi
- Format data salah (email, tanggal, angka)
- Nilai di luar range yang diizinkan

**Handling:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Sistem deteksi input tidak valid (client-side)           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Tampilkan pesan error di bawah field yang error:         │
│    ❌ "Tahun perolehan tidak valid (1900 - 2026)"           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Highlight field dengan border merah                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Disable tombol "Simpan" sampai error diperbaiki          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. User memperbaiki input                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Sistem validasi ulang real-time                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Jika valid: Hilangkan error, enable tombol "Simpan"      │
└─────────────────────────────────────────────────────────────┘
```

**Contoh Pesan Error yang Baik:**

| ❌ Buruk | ✅ Baik |
|---------|--------|
| "Invalid input" | "Tahun perolehan harus antara 1900 - 2026" |
| "Field required" | "Nama barang harus diisi (minimal 3 karakter)" |
| "Duplicate entry" | "Kode barang 32.01.02.0001 sudah digunakan" |
| "Error 500" | "Terjadi kesalahan saat menyimpan data. Coba lagi." |

#### 7.2.2 Business Rule Violation

**Contoh Kasus:**

- Kode barang duplikat
- Mutasi aset yang sedang mutasi
- Hapus aset yang sedang mutasi

**Handling:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. User submit data yang melanggar business rule            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Server-side validasi mendeteksi pelanggaran              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Sistem tampilkan modal error dengan:                     │
│    - Judul: "Operasi Tidak Dapat Dilakukan"                 │
│    - Pesan: Penjelasan pelanggaran business rule            │
│    - Saran: Langkah yang harus dilakukan                    │
│    - Tombol: "Mengerti"                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. User klik "Mengerti"                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Sistem kembali ke form/halaman sebelumnya                │
└─────────────────────────────────────────────────────────────┘
```

**Contoh Pesan:**

```text
❌ Operasi Tidak Dapat Dilakukan

Aset tidak dapat dihapus karena sedang dalam proses mutasi.

Saran:

- Selesaikan proses mutasi terlebih dahulu, atau
- Batalkan mutasi yang sedang berjalan

[Mengerti]
```

#### 7.2.3 Database Error

**Contoh Kasus:**

- Koneksi database terputus
- Query timeout
- Constraint violation

**Handling:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Sistem deteksi database error                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Log error detail ke file log (untuk debugging)           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Tampilkan pesan error user-friendly:                     │
│    "Terjadi kesalahan saat menyimpan data.                  │
│     Silakan coba lagi dalam beberapa saat."                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Berikan opsi:                                             │
│    - [Coba Lagi] - Retry operasi                            │
│    - [Batal] - Kembali ke halaman sebelumnya                │
└─────────────────────────────────────────────────────────────┘
```

**Catatan:** Jangan tampilkan detail teknis error ke user (SQL query, stack trace, dll). Simpan di log file untuk debugging.

#### 7.2.4 Network Error (API Timeout)

**Contoh Kasus:**

- Request ke backend timeout
- Backend tidak merespons

**Handling:**

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Client mengirim request ke backend                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Tampilkan loading indicator                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Timeout setelah 30 detik                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Tampilkan error:                                          │
│    "Koneksi ke server terputus. Periksa koneksi jaringan    │
│     dan coba lagi."                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Berikan opsi:                                             │
│    - [Coba Lagi] - Retry request                            │
│    - [Batal] - Kembali ke halaman sebelumnya                │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 Success Feedback

**Prinsip:**

- Berikan feedback sukses yang jelas setelah operasi berhasil
- Gunakan toast notification (auto-dismiss setelah 3 detik)
- Jangan ganggu workflow user

**Contoh:**

```text
✅ Aset berhasil ditambahkan dengan Nomor Register: 123
✅ Laporan KIB B berhasil diekspor
✅ Mutasi aset berhasil diproses
✅ Aset berhasil dihapus dari inventaris aktif
```

### 7.4 Confirmation Dialog

**Kapan Menggunakan:**

- Operasi yang tidak dapat di-undo (delete, mutasi)
- Operasi yang berdampak besar (ekspor semua data)

**Format:**

```text
⚠️ Konfirmasi

[Pesan konfirmasi yang jelas]

[Tidak, Batal]  [Ya, Lanjutkan]
```

**Contoh:**

```text
⚠️ Konfirmasi Penghapusan

Aset "Laptop HP Pavilion" akan dihapus dari inventaris aktif.
Data tetap tersimpan untuk audit.

Yakin ingin melanjutkan?

[Tidak, Batal]  [Ya, Hapus]
```

---

## 8. Aturan Operasional Tambahan

### 8.1 Aturan Backup dan Recovery

**Backup Otomatis:**

- Sistem melakukan backup database setiap hari pada pukul 23:00
- Backup disimpan di folder `backup/` dengan format: `simanis62_YYYYMMDD.sql`
- Backup disimpan selama 30 hari, setelah itu otomatis dihapus
- Admin dapat melakukan backup manual kapan saja

**Manual Backup:**

```text

1. Admin buka menu "Pengaturan" > "Backup Database"
2. Klik "Backup Sekarang"
3. Sistem generate file backup
4. Sistem download file ke komputer Admin
5. Tampilkan notifikasi: "Backup berhasil dibuat"

```

**Recovery:**

```text

1. Admin buka menu "Pengaturan" > "Restore Database"
2. Pilih file backup (.sql)
3. Sistem tampilkan konfirmasi:

   "PERHATIAN: Data saat ini akan diganti dengan data backup.
    Yakin ingin melanjutkan?"

4. Jika Ya:
   - Sistem restore database dari file backup
   - Sistem restart aplikasi
   - Tampilkan notifikasi: "Database berhasil di-restore"

```

### 8.2 Aturan Ekspor Data

**Format Ekspor:**

- Excel (.xlsx) - Format utama untuk laporan KIB
- CSV (.csv) - Format alternatif untuk import ke sistem lain

**Aturan Ekspor:**

1. Ekspor hanya mencakup aset dengan status "Aktif" dan "Rusak" (kecuali filter khusus)
2. Aset dengan status "Dihapus" tidak diikutkan dalam ekspor (kecuali Admin memilih filter "Dihapus")
3. Format Excel mengikuti template standar Permendagri 19/2016
4. Nama file: `{jenis_laporan}_{tanggal}.xlsx`
5. Maksimal 10,000 baris per file (untuk performa)

**Contoh Nama File:**

- `KIB_B_20260105.xlsx`
- `KIR_Lab_Komputer_20260105.xlsx`
- `Buku_Inventaris_20260105.xlsx`

### 8.3 Aturan Cetak Laporan

**Format Cetak:**

- Orientasi: Landscape (untuk KIB dengan banyak kolom)
- Ukuran Kertas: A4
- Margin: 1 cm (semua sisi)
- Header: Logo sekolah, nama sekolah, judul laporan
- Footer: Halaman X dari Y, tanggal cetak

**Aturan Cetak:**

1. Laporan KIB dicetak per kategori (tidak bisa gabungan)
2. Setiap halaman memiliki header tabel
3. Total nilai dan jumlah aset di halaman terakhir
4. Tempat tanda tangan Kepala Sekolah di halaman terakhir

**Template Tanda Tangan:**

```text
Mengetahui,
Kepala Sekolah


(___________________)
NIP.
```

### 8.4 Aturan Performa dan Optimasi

**Target Performa:**

- Waktu loading halaman: < 2 detik
- Waktu pencarian aset: < 5 detik
- Waktu generate laporan KIB: < 10 detik (untuk 1000 aset)
- Waktu ekspor Excel: < 15 detik (untuk 1000 aset)

**Strategi Optimasi:**

1. **Pagination:** Maksimal 100 item per halaman
2. **Lazy Loading:** Load data saat dibutuhkan
3. **Caching:** Cache data yang sering diakses (daftar ruangan, kategori KIB)
4. **Indexing:** Index pada kolom yang sering di-query (kode_barang, nama_barang, ruangan_id)
5. **Query Optimization:** Gunakan JOIN yang efisien, hindari N+1 query

**Monitoring Performa:**

- Log waktu eksekusi query yang > 1 detik
- Alert jika database size > 1 GB
- Alert jika backup gagal

### 8.5 Aturan Keamanan Data

**Hak Akses:**

- Admin: Full access (CRUD semua data)
- Viewer: Read-only access (tidak bisa edit/delete)

**Password Policy:**

- Minimal 8 karakter
- Harus mengandung huruf dan angka
- Password di-hash menggunakan bcrypt
- Password tidak boleh sama dengan username

**Session Management:**

- Session timeout: 2 jam (tidak ada aktivitas)
- Auto-logout setelah timeout
- User harus login ulang setelah logout

**Audit Trail:**

- Semua operasi CRUD dicatat dengan:
  - User yang melakukan
  - Timestamp
  - Operasi yang dilakukan (Create/Update/Delete)
  - Data sebelum dan sesudah (untuk Update)
- Audit trail tidak dapat dihapus
- Audit trail dapat diakses oleh Admin

### 8.6 Aturan Data Integrity

**Referential Integrity:**

- Aset harus memiliki ruangan (foreign key ke tabel ruangan)
- Mutasi harus memiliki aset yang valid (foreign key ke tabel aset)
- User yang tercatat harus valid (foreign key ke tabel user)

**Constraint Database:**

- Kode barang: UNIQUE
- Nomor register: UNIQUE per kategori KIB
- Harga: CHECK (harga > 0)
- Tahun perolehan: CHECK (tahun >= 1900 AND tahun <= YEAR(CURRENT_DATE))

**Cascade Rules:**

- Jika ruangan dihapus: Aset di ruangan tersebut dipindahkan ke "Ruangan Tidak Diketahui"
- Jika user dihapus: Data created_by/updated_by tetap tersimpan (soft reference)

---

## 9. Diagram Alur Kerja (Activity Diagram)

### 9.1 Activity Diagram: Pencatatan Aset Baru

```text
@startuml
|Admin|
start
:Pilih menu "Tambah Aset";
:Pilih kategori KIB;
:Isi form data aset;

|Sistem|
:Validasi input;

if (Data valid?) then (tidak)
  |Sistem|
  :Tampilkan pesan error;
  |Admin|
  :Perbaiki data;
  stop
else (ya)
  |Sistem|
  :Generate Nomor Register;
  :Simpan data aset;
  :Set status = "Baru";
  :Catat timestamp & user;
  :Tampilkan pesan sukses;
  |Admin|
  :Verifikasi aset;
  |Sistem|
  :Update status = "Aktif";
endif

stop
@enduml
```

### 9.2 Activity Diagram: Pembuatan Laporan KIB

```text
@startuml
|Admin|
start
:Pilih menu "Laporan KIB";
:Pilih kategori KIB;
:Pilih filter (opsional);
:Klik "Generate Laporan";

|Sistem|
:Query data aset;
:Format sesuai KIB;
:Hitung total;
:Tampilkan preview;

|Admin|
if (Ekspor atau Cetak?) then (ekspor)
  |Sistem|
  :Generate file Excel;
  :Download file;
else (cetak)
  |Sistem|
  :Buka dialog print;
  |Admin|
  :Cetak laporan;
endif

stop
@enduml
```

### 9.3 Activity Diagram: Mutasi Aset

```text
@startuml
|Admin|
start
:Cari aset yang akan dimutasi;
:Klik "Mutasi";
:Pilih ruangan tujuan;
:Isi alasan mutasi;
:Klik "Proses Mutasi";

|Sistem|
:Validasi data;

if (Valid?) then (tidak)
  :Tampilkan error;
  stop
else (ya)
  :Update status = "Mutasi";
  :Simpan data mutasi;
  :Tampilkan konfirmasi;
endif

note right
  Aset dalam status "Mutasi"
  sampai dikonfirmasi selesai
end note

|Admin|
:Konfirmasi mutasi selesai;

|Sistem|
:Update ruangan aset;
:Update status = "Aktif";
:Catat riwayat mutasi;
:Tampilkan pesan sukses;

stop
@enduml
```

---

## 10. Matriks Traceability

Matriks ini menghubungkan fitur sistem dengan dokumen arsitektur lainnya.

| Fitur | Dok 1: Tujuan Bisnis | Dok 2: Masalah Inti | Alur Kerja |
|-------|---------------------|---------------------|------------|
| CRUD Data Aset | Bagian 3.1 (Fitur Wajib #1) | Bagian 4.1.1 (Masalah 1) | Bagian 6.1 |
| Pencarian Aset | Bagian 3.1 (Fitur Wajib #2) | Bagian 4.1.1 (Masalah 1) | Bagian 6.4 |
| Laporan KIB A-F | Bagian 3.1 (Fitur Wajib #3) | Bagian 4.1.2 (Masalah 2) | Bagian 6.2 |
| Laporan KIR | Bagian 3.1 (Fitur Wajib #4) | Bagian 4.1.1 (Masalah 1) | Bagian 6.2 |
| Mutasi Aset | Bagian 3.1 (Fitur Wajib #5) | Bagian 4.1.3 (Masalah 3) | Bagian 6.3 |
| Ekspor Excel | Bagian 3.1 (Fitur Wajib #6) | Bagian 4.1.2 (Masalah 2) | Bagian 8.2 |
| Kode Barang Unik | Bagian 3.1 (Fitur Wajib #7) | Bagian 4.1.1 (Masalah 1) | Bagian 5.3 |
| Multi User | Bagian 3.1 (Fitur Wajib #8) | Bagian 4.1.1 (Masalah 1) | Bagian 3 |
| Soft Delete | Bagian 3.2 (Fitur Penting #5) | Bagian 4.2 (Masalah Sekunder #2) | Bagian 6.5 |

---

## 11. Checklist Implementasi

Checklist ini membantu developer memastikan semua aturan telah diimplementasikan.

### 11.1 Business Rules

- [ ] Validasi kode barang (format dan uniqueness)
- [ ] Validasi nomor register (auto-generated, sequential)
- [ ] Validasi tahun perolehan (1900 - tahun sekarang)
- [ ] Validasi harga (positif, tidak nol)
- [ ] Validasi kondisi (3 pilihan: Baik, Rusak Ringan, Rusak Berat)
- [ ] Validasi field wajib per kategori KIB
- [ ] Aturan transisi status aset
- [ ] Aturan mutasi (tidak bisa mutasi aset yang sedang mutasi)
- [ ] Aturan penghapusan (soft delete, alasan wajib)

### 11.2 Workflow

- [ ] Alur pencatatan aset baru (Create)
- [ ] Alur pembuatan laporan KIB
- [ ] Alur mutasi aset antarruangan
- [ ] Alur pencarian aset
- [ ] Alur penghapusan aset (soft delete)
- [ ] Alur ekspor ke Excel
- [ ] Alur cetak laporan

### 11.3 Error Handling

- [ ] Validasi client-side (real-time)
- [ ] Validasi server-side (final check)
- [ ] Pesan error yang jelas dan spesifik
- [ ] Feedback visual (warna, icon)
- [ ] Confirmation dialog untuk operasi kritis
- [ ] Success notification (toast)
- [ ] Error logging untuk debugging

### 11.4 Performa

- [ ] Pagination (maksimal 100 item per halaman)
- [ ] Lazy loading
- [ ] Caching data yang sering diakses
- [ ] Database indexing
- [ ] Query optimization
- [ ] Target performa tercapai (< 5 detik untuk pencarian)

### 11.5 Keamanan

- [ ] Hak akses per role (Admin, Viewer)
- [ ] Password hashing (bcrypt)
- [ ] Session management (timeout 2 jam)
- [ ] Audit trail untuk semua operasi CRUD
- [ ] Referential integrity (foreign key constraints)
- [ ] Database constraints (unique, check)

### 11.6 Backup & Recovery

- [ ] Backup otomatis harian
- [ ] Manual backup
- [ ] Restore database dari backup
- [ ] Backup retention (30 hari)

---

## 12. Referensi Silang Dokumen

### 12.1 Hubungan dengan Dokumen Lain

Dokumen ini melengkapi dua dokumen arsitektur sebelumnya:

## Dokumen 1: Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala dan Asumsi

- Bagian 2 (Pemangku Kepentingan) → Bagian 3 dokumen ini (Role dan Hak Akses)
- Bagian 3 (Seleksi Fitur) → Bagian 6 dokumen ini (Alur Kerja Proses Bisnis)
- Bagian 4 (Kategori KIB) → Bagian 5 dokumen ini (Business Rules per KIB)
- Bagian 5 (Kendala) → Bagian 8.4 dokumen ini (Aturan Performa)

## Dokumen 2: Pemilik Kebenaran, Masalah Inti yang Diselesaikan, Konteks dan Batasan

- Bagian 4.1 (Masalah Primer) → Bagian 6 dokumen ini (Alur Kerja yang menyelesaikan masalah)
- Bagian 5.1 (Konteks Regulasi) → Bagian 5 dokumen ini (Business Rules sesuai Permendagri)
- Bagian 6 (Batasan Lingkup) → Bagian 8 dokumen ini (Aturan Operasional)
- Bagian 7 (Risiko) → Bagian 7 dokumen ini (Error Handling untuk mitigasi risiko)

### 12.2 Pemetaan Masalah ke Solusi

| Masalah (Dok 2) | Solusi (Alur Kerja) | Bagian |
|-----------------|---------------------|--------|
| Pencatatan aset manual tidak efisien | Alur CRUD Aset dengan validasi otomatis | 6.1 |
| Pencarian aset membutuhkan waktu lama | Alur Pencarian dengan target < 5 detik | 6.4 |
| Pembuatan laporan KIB memakan waktu | Alur Generate Laporan otomatis | 6.2 |
| Tidak ada jejak audit perpindahan aset | Alur Mutasi dengan riwayat permanen | 6.3 |
| Kondisi aset tidak terpantau | Business Rules kondisi aset | 5.1 |
| Penghapusan aset tidak tercatat | Alur Soft Delete dengan audit trail | 6.5 |

### 12.3 Pemetaan Fitur ke Workflow

| Fitur (Dok 1) | Workflow (Alur Kerja) | Bagian |
|---------------|----------------------|--------|
| CRUD Data Barang | Proses Pencatatan Aset Baru | 6.1 |
| Pencarian Aset | Proses Pencarian Aset | 6.4 |
| KIB A-F | Proses Pembuatan Laporan KIB | 6.2 |
| KIR | Proses Pembuatan Laporan KIR | 6.2 |
| Mutasi Barang | Proses Mutasi Aset Antarruangan | 6.3 |
| Ekspor Excel | Aturan Ekspor Data | 8.2 |
| Kode Barang Unik | Aturan Kode Barang | 5.3 |
| Multi User | Role dan Hak Akses | 3 |

---

## 13. Ringkasan Eksekutif

### 13.1 Esensi Dokumen

Dokumen Alur Kerja dan Aturan Main ini menjelaskan **bagaimana** sistem Simanis62 V2 beroperasi secara detail, melengkapi dokumen arsitektur sebelumnya yang menjelaskan **apa** (tujuan, fitur) dan **mengapa** (masalah, konteks).

### 13.2 Komponen Utama

Dokumen ini mencakup:

1. **Role dan Hak Akses** (3 role: Admin, Guru, Kepala Sekolah)
2. **Siklus Hidup Aset** (5 status: Baru, Aktif, Mutasi, Rusak, Dihapus)
3. **Business Rules** (Validasi data untuk semua field dan kategori KIB)
4. **5 Proses Bisnis Utama:**
   - Pencatatan Aset Baru (Create)
   - Pembuatan Laporan KIB
   - Mutasi Aset Antarruangan
   - Pencarian Aset
   - Penghapusan Aset (Soft Delete)
5. **Error Handling** (4 kategori error dengan strategi handling)
6. **Aturan Operasional** (Backup, Ekspor, Cetak, Performa, Keamanan)

### 13.3 Prinsip Desain

Alur kerja dirancang dengan prinsip:

- **User-Friendly:** Pesan error jelas, feedback visual konsisten
- **Audit Trail:** Semua operasi tercatat untuk akuntabilitas
- **Data Integrity:** Validasi di client dan server, constraint database
- **Performa:** Target < 5 detik untuk pencarian, < 10 detik untuk laporan
- **Keamanan:** Hak akses per role, password hashing, session management

### 13.4 Kesesuaian dengan Regulasi

Semua business rules dan format laporan mengikuti **Permendagri Nomor 19 Tahun 2016** tentang Pengelolaan Barang Milik Daerah, khususnya:

- Format KIB A-F dengan field wajib sesuai standar
- Nomor Register sequential per kategori
- Kode Barang sesuai klasifikasi BMD
- Kondisi aset: Baik, Rusak Ringan, Rusak Berat

### 13.5 Kesiapan Implementasi

Dokumen ini siap digunakan sebagai panduan implementasi dengan:

- ✅ Alur kerja detail untuk setiap proses bisnis
- ✅ Business rules lengkap dengan validasi
- ✅ Error handling strategy yang jelas
- ✅ Checklist implementasi untuk developer
- ✅ Activity diagram untuk visualisasi
- ✅ Matriks traceability ke dokumen lain

---

## 14. Catatan Perubahan

| Versi | Tanggal | Perubahan | Penulis |
|-------|---------|-----------|---------|
| 1.0 | 5 Januari 2026 | Dokumen awal | Architecture Engineer |

---

## 15. Lampiran

### 15.1 Contoh Kode Barang

| Kategori | Kode | Contoh |
|----------|------|--------|
| KIB A (Tanah) | 32.01.01.XXXX | 32.01.01.0001 |
| KIB B (Peralatan dan Mesin) | 32.01.02.XXXX | 32.01.02.0125 |
| KIB C (Gedung dan Bangunan) | 32.01.03.XXXX | 32.01.03.0015 |
| KIB D (Jalan, Irigasi, Jaringan) | 32.01.04.XXXX | 32.01.04.0003 |
| KIB E (Aset Tetap Lainnya) | 32.01.05.XXXX | 32.01.05.0450 |
| KIB F (Konstruksi dalam Pengerjaan) | 32.01.06.XXXX | 32.01.06.0001 |

### 15.2 Contoh Pesan Error

| Situasi | Pesan Error |
|---------|-------------|
| Field wajib kosong | "Nama barang harus diisi (minimal 3 karakter)" |
| Format salah | "Tahun perolehan harus antara 1900 - 2026" |
| Kode duplikat | "Kode barang 32.01.02.0001 sudah digunakan" |
| Business rule violation | "Aset tidak dapat dihapus karena sedang dalam proses mutasi" |
| Database error | "Terjadi kesalahan saat menyimpan data. Silakan coba lagi." |
| Network timeout | "Koneksi ke server terputus. Periksa koneksi jaringan dan coba lagi." |

### 15.3 Contoh Success Message

| Operasi | Pesan Sukses |
|---------|--------------|
| Tambah aset | "Aset berhasil ditambahkan dengan Nomor Register: 123" |
| Update aset | "Data aset berhasil diperbarui" |
| Mutasi aset | "Mutasi aset berhasil diproses" |
| Hapus aset | "Aset berhasil dihapus dari inventaris aktif" |
| Ekspor laporan | "Laporan KIB B berhasil diekspor" |
| Backup database | "Backup database berhasil dibuat" |

---

*Dokumen ini merupakan bagian dari dokumentasi arsitektur Simanis62 V2.*
### Referensi: Permendagri Nomor 19 Tahun 2016 tentang Pedoman Pengelolaan Barang Milik Daerah
