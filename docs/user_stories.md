# Dokumentasi Proyek Simanis62 V2


## User Stories

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 5 Januari 2026 | Architecture Engineer | Dokumen awal |

---

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

Dokumen ini mendefinisikan user stories untuk sistem Simanis62 V2 yang menjelaskan kebutuhan pengguna dalam format yang:

- **Spesifik:** Setiap story memiliki scope yang jelas dan terukur
- **Jelas:** Menggunakan bahasa yang mudah dipahami tanpa ambiguitas
- **Logis:** Mengikuti alur kerja yang masuk akal dan natural
- **Realistis:** Fokus pada fitur inti tanpa over-engineering
- **Tidak Ambisius:** Menghindari fitur kompleks yang tidak esensial
- **Tidak Ambigu:** Setiap story memiliki acceptance criteria yang tegas

### 1.2 Format User Story

Setiap user story mengikuti format standar:

**Format Dasar:**

```text
As a [role]
I want [feature]
So that [benefit]
```

**Acceptance Criteria (Given-When-Then):**

```text
Given [initial context/precondition]
When [action/event]
Then [expected outcome]
```

### 1.3 INVEST Criteria

Semua user stories dalam dokumen ini memenuhi kriteria INVEST:

| Kriteria | Penjelasan | Implementasi |
|----------|------------|--------------|
| **Independent** | Story dapat dikerjakan secara independen | Setiap story memiliki scope terpisah |
| **Negotiable** | Detail implementasi dapat didiskusikan | Story fokus pada "apa" bukan "bagaimana" |
| **Valuable** | Memberikan nilai bisnis yang jelas | Setiap story menyelesaikan masalah spesifik |
| **Estimable** | Dapat diestimasi effort-nya | Story memiliki scope yang jelas |
| **Small** | Dapat diselesaikan dalam 1-3 hari | Story tidak terlalu besar atau kompleks |
| **Testable** | Memiliki kriteria penerimaan yang jelas | Acceptance criteria dalam format Given-When-Then |

---

## 2. Glossary

| Istilah | Definisi |
|---------|----------|
| **Aset** | Barang Milik Daerah (BMD) yang tercatat dalam sistem |
| **KIB** | Kartu Inventaris Barang (A-F) sesuai Permendagri 19/2016 |
| **KIR** | Kartu Inventaris Ruangan |
| **Mutasi** | Perpindahan aset dari satu ruangan ke ruangan lain |
| **Soft Delete** | Penghapusan aset dengan status "Dihapus", data tidak benar-benar dihapus |
| **Nomor Register** | Nomor urut unik per kategori KIB, auto-generated oleh sistem |
| **Kode Barang** | Kode identifikasi unik aset sesuai standar BMD (format: XX.XX.XX.XXXX) |
| **Status Aset** | Kondisi operasional aset: Baru, Aktif, Mutasi, Rusak, Dihapus |
| **Kondisi Aset** | Kondisi fisik aset: Baik, Rusak Ringan, Rusak Berat |
| **Admin Sekolah** | Pengguna dengan hak akses penuh (CRUD semua data) |
| **Viewer** | Pengguna dengan hak akses read-only (Guru) |
| **Kepala Sekolah** | Pengguna dengan hak akses view dan export laporan |

---

## 3. User Roles Summary

### 3.1 Admin Sekolah

**Tanggung Jawab:**

- Mengelola data aset (Create, Read, Update, Delete)
- Membuat dan mengekspor laporan KIB dan KIR
- Mencatat mutasi aset antarruangan
- Mengelola user Viewer

**Hak Akses:**

- ✅ Full CRUD data aset
- ✅ Generate dan ekspor semua laporan
- ✅ Mutasi dan soft delete aset
- ✅ Manajemen user

### 3.2 Guru (Viewer)

**Tanggung Jawab:**

- Melihat aset di ruangan tertentu
- Melaporkan kondisi aset (melalui Admin)

**Hak Akses:**

- ✅ Read-only data aset
- ✅ Pencarian aset
- ✅ Lihat KIR per ruangan
- ❌ Tidak bisa CRUD, mutasi, atau delete

### 3.3 Kepala Sekolah

**Tanggung Jawab:**

- Mengawasi pengelolaan aset
- Mereview dan menandatangani laporan KIB

**Hak Akses:**

- ✅ Read-only data aset
- ✅ Lihat semua laporan KIB dan KIR
- ✅ Ekspor laporan untuk review
- ❌ Tidak bisa CRUD, mutasi, atau delete

---

## 4. Epic Overview

### EPIC 1: Asset Data Management

**Tujuan:** Mendigitalisasi pencatatan aset sekolah dengan validasi otomatis
**Masalah yang Diselesaikan:** Pencatatan aset manual yang tidak efisien
**User Stories:** US-001, US-002, US-003, US-004, US-005
**Prioritas:** CRITICAL

### EPIC 2: KIB Reporting

**Tujuan:** Menghasilkan laporan KIB A-F sesuai Permendagri 19/2016
**Masalah yang Diselesaikan:** Pembuatan laporan KIB yang memakan waktu
**User Stories:** US-006, US-007, US-008, US-009, US-010, US-011, US-012
**Prioritas:** CRITICAL

### EPIC 3: Asset Movement Tracking

**Tujuan:** Mencatat perpindahan aset dengan jejak audit
**Masalah yang Diselesaikan:** Tidak ada jejak audit perpindahan aset
**User Stories:** US-013, US-014, US-015
**Prioritas:** CRITICAL

### EPIC 4: Room Inventory Management

**Tujuan:** Menyediakan laporan inventaris per ruangan
**Masalah yang Diselesaikan:** Sulit melacak aset berdasarkan lokasi fisik
**User Stories:** US-016, US-017
**Prioritas:** HIGH

### EPIC 5: User Access Management

**Tujuan:** Mengatur hak akses pengguna berdasarkan role
**Masalah yang Diselesaikan:** Keamanan data dan pembagian tanggung jawab
**User Stories:** US-018, US-019
**Prioritas:** HIGH

---

## 5. User Stories

### EPIC 1: Asset Data Management

---

#### US-001: Pencatatan Aset Baru

**As a** Admin Sekolah
**I want** mencatat aset baru dengan memilih kategori KIB dan mengisi field wajib
**So that** data aset tersimpan secara digital dengan validasi otomatis dan nomor register unik

**Prioritas:** CRITICAL
**Estimasi:** 2-3 hari
**Epic:** Asset Data Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** Admin login dan membuka menu "Tambah Aset"
2. **Proses:** Admin memilih kategori KIB (A-F), mengisi field wajib sesuai kategori, sistem validasi real-time
3. **Output:** Aset tersimpan dengan status "Baru", nomor register ter-generate otomatis, notifikasi sukses

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di halaman "Tambah Aset"
When Admin memilih kategori KIB B (Peralatan dan Mesin)
And mengisi field wajib:

  - Kode Barang: "32.01.02.0001" (format XX.XX.XX.XXXX)
  - Nama Barang: "Laptop HP Pavilion" (3-200 karakter)
  - Merk/Type: "HP Pavilion 14" (wajib untuk KIB B)
  - Tahun Perolehan: "2024" (1900 - tahun sekarang)
  - Asal Usul: "Pembelian"
  - Harga: "8500000" (angka positif, tidak nol)
  - Kondisi: "Baik"
  - Ruangan: "Lab Komputer"

And klik tombol "Simpan"
Then sistem melakukan validasi semua field
And sistem generate Nomor Register otomatis (sequential per KIB B)
And sistem simpan data dengan status "Baru"
And sistem catat timestamp created_at dan user created_by
And sistem tampilkan notifikasi: "Aset berhasil ditambahkan dengan Nomor Register: 1"
```

```gherkin
Given Admin mengisi form aset baru
When Admin mengisi Kode Barang yang sudah digunakan: "32.01.02.0001"
And klik "Simpan"
Then sistem tampilkan error: "Kode barang 32.01.02.0001 sudah digunakan"
And sistem tampilkan data aset yang menggunakan kode tersebut
And form tetap terbuka dengan data yang sudah diisi
And tombol "Simpan" tetap enabled untuk perbaikan
```

```gherkin
Given Admin mengisi form aset baru KIB A (Tanah)
When Admin tidak mengisi field wajib "Luas (m²)"
And klik "Simpan"
Then sistem tampilkan error di bawah field: "Luas tanah harus berupa angka positif"
And highlight field dengan border merah
And disable tombol "Simpan" sampai error diperbaiki
```

```gherkin
Given Admin mengisi form aset baru
When Admin mengisi Tahun Perolehan: "2030" (di masa depan)
And klik "Simpan"
Then sistem tampilkan error: "Tahun perolehan tidak valid (1900 - 2026)"
And form tetap terbuka untuk perbaikan
```

**Business Rules:**

- Kode Barang: Format XX.XX.XX.XXXX, unique, regex validation
- Nama Barang: 3-200 karakter, wajib
- Nomor Register: Auto-generated, sequential per kategori KIB, tidak dapat diubah
- Tahun Perolehan: 1900 - tahun sekarang
- Harga: Angka positif, tidak boleh nol, max 999,999,999,999
- Kondisi: Enum ['Baik', 'Rusak Ringan', 'Rusak Berat']
- Field khusus per KIB:
  - KIB A: Luas (m²), Alamat/Lokasi wajib
  - KIB B: Merk/Type wajib
  - KIB C: Luas (m²), Alamat/Lokasi wajib
  - KIB D: Panjang (m), Lebar (m), Alamat/Lokasi wajib
  - KIB E: Judul/Nama wajib
  - KIB F: Alamat/Lokasi, Persentase Selesai (0-100%) wajib

**Dependencies:** None (first story)

---

#### US-002: Melihat Detail Aset

**As a** Admin Sekolah / Guru (Viewer) / Kepala Sekolah
**I want** melihat detail lengkap aset termasuk riwayat mutasi
**So that** saya dapat memverifikasi informasi aset dan melacak perubahan

**Prioritas:** CRITICAL
**Estimasi:** 1 hari
**Epic:** Asset Data Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan mencari aset melalui pencarian atau daftar aset
2. **Proses:** User klik aset untuk melihat detail, sistem load data lengkap termasuk riwayat
3. **Output:** Tampilan detail aset dengan semua field, riwayat mutasi, dan opsi aksi sesuai role

**Acceptance Criteria:**

```gherkin
Given User sudah login (Admin/Viewer/Kepala Sekolah)
When User klik aset dengan Kode Barang "32.01.02.0001" dari daftar aset
Then sistem tampilkan detail lengkap aset:

  - Semua field data aset (Kode, Nama, Nomor Register, dll)
  - Status aset (Baru/Aktif/Mutasi/Rusak/Dihapus)
  - Kondisi aset (Baik/Rusak Ringan/Rusak Berat)
  - Ruangan saat ini
  - Riwayat mutasi (jika ada)
  - Timestamp created_at dan updated_at
  - User created_by dan updated_by

And jika role Admin: tampilkan tombol "Edit" dan "Hapus"
And jika role Viewer/Kepala Sekolah: tidak tampilkan tombol aksi
```

```gherkin
Given Admin melihat detail aset dengan status "Mutasi"
When sistem tampilkan detail aset
Then sistem tampilkan informasi mutasi yang sedang berjalan:

  - Ruangan asal
  - Ruangan tujuan
  - Tanggal mutasi
  - Alasan mutasi
  - Status mutasi: "Dalam Proses"

And tampilkan tombol "Konfirmasi Selesai" atau "Batalkan Mutasi"
```

```gherkin
Given User melihat detail aset yang memiliki riwayat mutasi
When sistem tampilkan riwayat mutasi
Then sistem tampilkan tabel riwayat dengan kolom:

  - Tanggal mutasi
  - Ruangan asal
  - Ruangan tujuan
  - Alasan
  - User yang memproses
  - Status (Selesai/Dibatalkan)

And urutkan berdasarkan tanggal terbaru
```

**Business Rules:**

- Semua role dapat melihat detail aset dengan status "Aktif" dan "Rusak"
- Hanya Admin yang dapat melihat aset dengan status "Dihapus"
- Riwayat mutasi tidak dapat dihapus (audit trail permanen)
- Waktu loading detail aset: < 2 detik

**Dependencies:** US-001 (Create asset)

---

#### US-003: Mengubah Data Aset

**As a** Admin Sekolah
**I want** mengubah data aset yang sudah tercatat
**So that** informasi aset tetap akurat dan up-to-date

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** Asset Data Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** Admin melihat detail aset dan klik tombol "Edit"
2. **Proses:** Admin mengubah field yang perlu diupdate, sistem validasi real-time
3. **Output:** Data aset terupdate, timestamp updated_at tercatat, notifikasi sukses

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan melihat detail aset
When Admin klik tombol "Edit"
And sistem tampilkan form edit dengan data aset saat ini
And Admin mengubah field "Kondisi" dari "Baik" menjadi "Rusak Ringan"
And Admin mengubah field "Keterangan" menjadi "Layar retak"
And klik "Simpan Perubahan"
Then sistem validasi perubahan
And sistem update data aset
And sistem update status aset menjadi "Rusak" (karena kondisi Rusak Ringan)
And sistem catat timestamp updated_at dan user updated_by
And sistem tampilkan notifikasi: "Data aset berhasil diperbarui"
```

```gherkin
Given Admin mengedit aset
When Admin mengubah "Kode Barang" menjadi kode yang sudah digunakan aset lain
And klik "Simpan Perubahan"
Then sistem tampilkan error: "Kode barang sudah digunakan"
And form tetap terbuka dengan perubahan yang belum disimpan
And Admin dapat memperbaiki kode barang
```

```gherkin
Given Admin mengedit aset dengan status "Mutasi"
When Admin klik tombol "Edit"
Then sistem tampilkan warning: "Aset sedang dalam proses mutasi. Beberapa field tidak dapat diubah."
And sistem disable field: Ruangan, Status
And sistem enable field lain untuk edit (Kondisi, Keterangan, dll)
```

```gherkin
Given Admin mengedit aset
When Admin mengubah "Kondisi" dari "Rusak Berat" menjadi "Baik"
And klik "Simpan Perubahan"
Then sistem update kondisi aset
And sistem update status aset dari "Rusak" menjadi "Aktif"
And sistem catat perubahan di audit trail
```

**Business Rules:**

- Hanya Admin yang dapat mengubah data aset
- Field yang tidak dapat diubah: Nomor Register, Kategori KIB
- Aset dengan status "Mutasi": field Ruangan tidak dapat diubah
- Perubahan kondisi aset otomatis update status aset:
  - Kondisi "Baik" → Status "Aktif"
  - Kondisi "Rusak Ringan/Berat" → Status "Rusak"
- Semua perubahan tercatat di audit trail
- Validasi sama dengan create (format, range, dll)

**Dependencies:** US-001 (Create asset), US-002 (View asset)

---

#### US-004: Mencari Aset dengan Filter

**As a** Admin Sekolah / Guru (Viewer) / Kepala Sekolah
**I want** mencari aset dengan berbagai filter (kata kunci, kategori KIB, ruangan, kondisi, status)
**So that** saya dapat menemukan aset dengan cepat (< 5 detik)

**Prioritas:** CRITICAL
**Estimasi:** 2 hari
**Epic:** Asset Data Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Pencarian Aset"
2. **Proses:** User mengisi filter (minimal 1), klik "Cari", sistem query database
3. **Output:** Daftar aset yang sesuai filter, pagination jika > 100 item, waktu pencarian < 5 detik

**Acceptance Criteria:**

```gherkin
Given User sudah login dan berada di halaman "Pencarian Aset"
When User mengisi filter:

  - Kata Kunci: "Laptop"
  - Kategori KIB: "B (Peralatan dan Mesin)"
  - Ruangan: "Lab Komputer"
  - Kondisi: "Baik"
  - Status: "Aktif"

And klik tombol "Cari"
Then sistem melakukan pencarian dalam waktu < 5 detik
And sistem tampilkan hasil pencarian dalam tabel dengan kolom:

  - Kode Barang, Nama Barang, KIB, Ruangan, Kondisi, Status, Harga

And sistem tampilkan jumlah hasil: "Ditemukan 5 aset"
And jika hasil > 100 item: tampilkan pagination
```

```gherkin
Given User melakukan pencarian dengan kata kunci "laptop"
When sistem melakukan pencarian (case-insensitive)
Then sistem cari di field: Kode Barang dan Nama Barang
And sistem tampilkan hasil yang mengandung "laptop", "Laptop", "LAPTOP"
And urutkan hasil berdasarkan relevansi:

  1. Exact match di Nama Barang
  2. Partial match di Nama Barang
  3. Match di Kode Barang

```

```gherkin
Given User melakukan pencarian
When tidak ada aset yang sesuai dengan filter
Then sistem tampilkan pesan: "Tidak ada aset yang sesuai dengan pencarian"
And sistem tampilkan saran:

  - "Coba gunakan kata kunci yang lebih umum"
  - "Periksa ejaan kata kunci"
  - "Kurangi jumlah filter"

And User dapat mengubah filter dan cari lagi
```

```gherkin
Given Viewer (Guru) melakukan pencarian
When Viewer mengisi filter dan klik "Cari"
Then sistem hanya tampilkan aset dengan status "Aktif" dan "Rusak"
And sistem tidak tampilkan aset dengan status "Dihapus"
And Viewer tidak dapat melihat tombol "Edit" atau "Hapus" di hasil
```

```gherkin
Given User melihat hasil pencarian dengan 250 aset
When sistem tampilkan hasil
Then sistem tampilkan maksimal 100 item per halaman
And sistem tampilkan pagination: "Halaman 1 dari 3"
And User dapat navigasi ke halaman berikutnya
And waktu loading setiap halaman < 2 detik
```

**Business Rules:**

- Pencarian case-insensitive
- Kata kunci dicari di: Kode Barang dan Nama Barang (LIKE %keyword%)
- Multiple filter menggunakan operator AND
- Hasil maksimal 100 item per halaman (pagination)
- Viewer hanya bisa melihat aset dengan status "Aktif" dan "Rusak"
- Admin bisa melihat semua status termasuk "Dihapus"
- Target performa: < 5 detik untuk pencarian
- Hasil diurutkan: exact match > partial match > relevance

**Dependencies:** US-001 (Create asset)

---

#### US-005: Menghapus Aset (Soft Delete)

**As a** Admin Sekolah
**I want** menghapus aset dari inventaris aktif dengan mencatat alasan penghapusan
**So that** aset tidak muncul di laporan KIB namun data tetap tersimpan untuk audit

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** Asset Data Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** Admin melihat detail aset dan klik tombol "Hapus"
2. **Proses:** Admin mengisi alasan penghapusan (min 20 karakter), centang konfirmasi, sistem validasi
3. **Output:** Aset berstatus "Dihapus", tidak muncul di laporan, data tersimpan untuk audit

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan melihat detail aset dengan status "Aktif"
When Admin klik tombol "Hapus"
And sistem tampilkan form konfirmasi penghapusan:

  - Informasi aset yang akan dihapus
  - Field "Alasan Penghapusan" (text area, wajib)
  - Tanggal Penghapusan (default: hari ini)
  - Checkbox: "Saya yakin ingin menghapus aset ini"

And Admin mengisi alasan: "Aset rusak total dan tidak dapat diperbaiki"
And Admin centang checkbox konfirmasi
And Admin klik "Hapus Aset"
Then sistem validasi alasan (min 20 karakter) dan checkbox
And sistem tampilkan konfirmasi final: "PERHATIAN: Aset akan dihapus dari inventaris aktif. Data tetap tersimpan untuk audit. Lanjutkan?"
And Admin klik "Ya, Hapus"
Then sistem update status aset = "Dihapus"
And sistem simpan data penghapusan: deleted_at, deleted_by, delete_reason
And sistem tampilkan notifikasi: "Aset berhasil dihapus dari inventaris aktif"
```

```gherkin
Given Admin mencoba menghapus aset dengan status "Mutasi"
When Admin klik tombol "Hapus"
Then sistem tampilkan error: "Aset tidak dapat dihapus karena sedang dalam proses mutasi"
And sistem tampilkan info mutasi yang sedang berjalan
And Admin harus menyelesaikan atau membatalkan mutasi terlebih dahulu
```

```gherkin
Given Admin mengisi form penghapusan
When Admin mengisi alasan dengan < 20 karakter: "Rusak"
And klik "Hapus Aset"
Then sistem tampilkan error: "Alasan penghapusan harus minimal 20 karakter"
And form tetap terbuka untuk perbaikan
```

```gherkin
Given Aset sudah dihapus (status "Dihapus")
When sistem generate laporan KIB
Then aset dengan status "Dihapus" tidak diikutkan dalam laporan
And aset tidak muncul di daftar aset aktif
And aset tidak muncul di pencarian (kecuali Admin pilih filter "Dihapus")
And data aset tetap tersimpan di database (soft delete)
```

**Business Rules:**

- Hanya Admin yang dapat menghapus aset
- Aset dengan status "Mutasi" tidak dapat dihapus
- Alasan penghapusan wajib diisi (min 20 karakter)
- Data aset tidak benar-benar dihapus dari database (soft delete)
- Aset yang dihapus tidak muncul di laporan KIB dan KIR
- Riwayat penghapusan tidak dapat dihapus (audit trail)
- Restore aset adalah fitur opsional (dapat ditambahkan kemudian)

**Dependencies:** US-001 (Create asset), US-002 (View asset)

---

### EPIC 2: KIB Reporting

---

#### US-006: Generate Laporan KIB A (Tanah)

**As a** Admin Sekolah / Kepala Sekolah
**I want** generate laporan KIB A (Tanah) sesuai format Permendagri 19/2016
**So that** laporan dapat digunakan untuk pelaporan ke Dinas Pendidikan

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** KIB Reporting

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Laporan KIB" → pilih "KIB A (Tanah)"
2. **Proses:** User pilih filter (opsional), klik "Generate Laporan", sistem query dan format data
3. **Output:** Preview laporan KIB A dengan kolom sesuai standar, total nilai dan jumlah aset

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Laporan KIB"
When Admin pilih kategori "KIB A (Tanah)"
And Admin pilih filter (opsional):

  - Tahun Perolehan: "2024"
  - Status: "Aktif"

And Admin klik "Generate Laporan"
Then sistem query data aset KIB A sesuai filter dalam waktu < 10 detik
And sistem format data sesuai standar Permendagri 19/2016
And sistem tampilkan preview laporan dengan kolom:

  - No Register, Kode Barang, Nama Barang, Luas (m²), Tahun Perolehan, Alamat/Lokasi, Asal Usul, Harga (Rp), Kondisi, Keterangan

And sistem tampilkan total: "Total: 5 bidang tanah | Total Nilai: Rp 500,000,000"
And sistem tampilkan tanggal generate laporan
```

```gherkin
Given Admin generate laporan KIB A
When tidak ada data aset KIB A yang sesuai filter
Then sistem tampilkan pesan: "Tidak ada data aset KIB A untuk filter yang dipilih"
And Admin dapat mengubah filter atau kembali
```

```gherkin
Given Admin melihat preview laporan KIB A
When Admin klik tombol "Ekspor ke Excel"
Then sistem generate file Excel (.xlsx) dalam waktu < 15 detik
And format Excel sesuai template KIB A standar
And nama file: "KIB_A_20260105.xlsx"
And sistem download file ke komputer Admin
And sistem tampilkan notifikasi: "File berhasil diunduh"
```

**Business Rules:**

- Hanya aset dengan status "Aktif" dan "Rusak" yang diikutkan (kecuali filter khusus)
- Aset dengan status "Dihapus" tidak diikutkan
- Urutkan berdasarkan Nomor Register (ascending)
- Format Excel mengikuti template standar Permendagri 19/2016
- Kolom wajib KIB A: No Register, Kode Barang, Nama Barang, Luas (m²), Tahun, Alamat/Lokasi, Asal Usul, Harga, Kondisi, Keterangan
- Target performa: < 10 detik untuk generate (1000 aset)

**Dependencies:** US-001 (Create asset with KIB A)

---

#### US-007: Generate Laporan KIB B (Peralatan dan Mesin)

**As a** Admin Sekolah / Kepala Sekolah
**I want** generate laporan KIB B (Peralatan dan Mesin) sesuai format Permendagri 19/2016
**So that** laporan dapat digunakan untuk pelaporan ke Dinas Pendidikan

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** KIB Reporting

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Laporan KIB" → pilih "KIB B (Peralatan dan Mesin)"
2. **Proses:** User pilih filter (opsional), klik "Generate Laporan", sistem query dan format data
3. **Output:** Preview laporan KIB B dengan kolom sesuai standar, total nilai dan jumlah aset

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Laporan KIB"
When Admin pilih kategori "KIB B (Peralatan dan Mesin)"
And Admin klik "Generate Laporan" (tanpa filter)
Then sistem query semua data aset KIB B dengan status "Aktif" dan "Rusak"
And sistem tampilkan preview laporan dengan kolom:

  - No Register, Kode Barang, Nama Barang, Merk/Type, Ukuran/CC, Bahan, Tahun Perolehan, Asal Usul, Harga (Rp), Kondisi, Keterangan

And sistem tampilkan total: "Total: 125 unit | Total Nilai: Rp 850,000,000"
And waktu generate < 10 detik untuk 1000 aset
```

```gherkin
Given Admin generate laporan KIB B dengan filter Ruangan "Lab Komputer"
When sistem query data
Then sistem hanya tampilkan aset KIB B yang berada di ruangan "Lab Komputer"
And sistem tampilkan total khusus untuk ruangan tersebut
```

**Business Rules:**

- Sama dengan US-006, dengan kolom khusus KIB B
- Kolom wajib KIB B: No Register, Kode Barang, Nama Barang, Merk/Type, Ukuran/CC, Bahan, Tahun, Asal Usul, Harga, Kondisi, Keterangan
- Merk/Type adalah field wajib untuk KIB B

**Dependencies:** US-001 (Create asset with KIB B)

---

#### US-008: Generate Laporan KIB C (Gedung dan Bangunan)

**As a** Admin Sekolah / Kepala Sekolah
**I want** generate laporan KIB C (Gedung dan Bangunan) sesuai format Permendagri 19/2016
**So that** laporan dapat digunakan untuk pelaporan ke Dinas Pendidikan

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** KIB Reporting

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Laporan KIB" → pilih "KIB C (Gedung dan Bangunan)"
2. **Proses:** User pilih filter (opsional), klik "Generate Laporan", sistem query dan format data
3. **Output:** Preview laporan KIB C dengan kolom sesuai standar, total nilai dan jumlah aset

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Laporan KIB"
When Admin pilih kategori "KIB C (Gedung dan Bangunan)"
And Admin klik "Generate Laporan"
Then sistem tampilkan preview laporan dengan kolom:

  - No Register, Kode Barang, Nama Barang, Luas (m²), Alamat/Lokasi, Bertingkat, Tahun Perolehan, Asal Usul, Harga (Rp), Kondisi, Keterangan

And sistem tampilkan total nilai dan jumlah bangunan
```

**Business Rules:**

- Sama dengan US-006, dengan kolom khusus KIB C
- Kolom wajib KIB C: No Register, Kode Barang, Nama Barang, Luas (m²), Alamat/Lokasi, Tahun, Asal Usul, Harga, Kondisi, Keterangan
- Bertingkat (jumlah lantai) adalah field opsional

**Dependencies:** US-001 (Create asset with KIB C)

---

#### US-009: Generate Laporan KIB D (Jalan, Irigasi, dan Jaringan)

**As a** Admin Sekolah / Kepala Sekolah
**I want** generate laporan KIB D (Jalan, Irigasi, dan Jaringan) sesuai format Permendagri 19/2016
**So that** laporan dapat digunakan untuk pelaporan ke Dinas Pendidikan

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** KIB Reporting

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Laporan KIB" → pilih "KIB D (Jalan, Irigasi, dan Jaringan)"
2. **Proses:** User pilih filter (opsional), klik "Generate Laporan", sistem query dan format data
3. **Output:** Preview laporan KIB D dengan kolom sesuai standar, total nilai dan jumlah aset

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Laporan KIB"
When Admin pilih kategori "KIB D (Jalan, Irigasi, dan Jaringan)"
And Admin klik "Generate Laporan"
Then sistem tampilkan preview laporan dengan kolom:

  - No Register, Kode Barang, Nama Barang, Panjang (m), Lebar (m), Alamat/Lokasi, Tahun Perolehan, Asal Usul, Harga (Rp), Kondisi, Keterangan

And sistem tampilkan total nilai dan jumlah aset
```

**Business Rules:**

- Sama dengan US-006, dengan kolom khusus KIB D
- Kolom wajib KIB D: No Register, Kode Barang, Nama Barang, Panjang (m), Lebar (m), Alamat/Lokasi, Tahun, Asal Usul, Harga, Kondisi, Keterangan

**Dependencies:** US-001 (Create asset with KIB D)

---

#### US-010: Generate Laporan KIB E (Aset Tetap Lainnya)

**As a** Admin Sekolah / Kepala Sekolah
**I want** generate laporan KIB E (Aset Tetap Lainnya) sesuai format Permendagri 19/2016
**So that** laporan dapat digunakan untuk pelaporan ke Dinas Pendidikan

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** KIB Reporting

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Laporan KIB" → pilih "KIB E (Aset Tetap Lainnya)"
2. **Proses:** User pilih filter (opsional), klik "Generate Laporan", sistem query dan format data
3. **Output:** Preview laporan KIB E dengan kolom sesuai standar, total nilai dan jumlah aset

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Laporan KIB"
When Admin pilih kategori "KIB E (Aset Tetap Lainnya)"
And Admin klik "Generate Laporan"
Then sistem tampilkan preview laporan dengan kolom:

  - No Register, Kode Barang, Judul/Nama, Penerbit, Tahun Perolehan, Asal Usul, Harga (Rp), Kondisi, Keterangan

And sistem tampilkan total nilai dan jumlah aset
```

**Business Rules:**

- Sama dengan US-006, dengan kolom khusus KIB E
- Kolom wajib KIB E: No Register, Kode Barang, Judul/Nama, Tahun, Asal Usul, Harga, Kondisi, Keterangan
- Penerbit adalah field opsional (untuk buku perpustakaan)

**Dependencies:** US-001 (Create asset with KIB E)

---

#### US-011: Generate Laporan KIB F (Konstruksi dalam Pengerjaan)

**As a** Admin Sekolah / Kepala Sekolah
**I want** generate laporan KIB F (Konstruksi dalam Pengerjaan) sesuai format Permendagri 19/2016
**So that** laporan dapat digunakan untuk pelaporan ke Dinas Pendidikan

**Prioritas:** CRITICAL
**Estimasi:** 1-2 hari
**Epic:** KIB Reporting

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Laporan KIB" → pilih "KIB F (Konstruksi dalam Pengerjaan)"
2. **Proses:** User pilih filter (opsional), klik "Generate Laporan", sistem query dan format data
3. **Output:** Preview laporan KIB F dengan kolom sesuai standar, total nilai dan jumlah aset

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Laporan KIB"
When Admin pilih kategori "KIB F (Konstruksi dalam Pengerjaan)"
And Admin klik "Generate Laporan"
Then sistem tampilkan preview laporan dengan kolom:

  - No Register, Kode Barang, Nama Barang, Alamat/Lokasi, Persentase Selesai (%), Tahun Perolehan, Asal Usul, Harga (Rp), Keterangan

And sistem tampilkan total nilai dan jumlah konstruksi
And kolom "Kondisi" tidak ditampilkan (tidak wajib untuk KIB F)
```

**Business Rules:**

- Sama dengan US-006, dengan kolom khusus KIB F
- Kolom wajib KIB F: No Register, Kode Barang, Nama Barang, Alamat/Lokasi, Persentase Selesai (0-100%), Tahun, Asal Usul, Harga, Keterangan
- Kondisi TIDAK wajib untuk KIB F (konstruksi belum selesai)

**Dependencies:** US-001 (Create asset with KIB F)

---

#### US-012: Ekspor Laporan KIB ke Excel

**As a** Admin Sekolah / Kepala Sekolah
**I want** ekspor laporan KIB ke format Excel (.xlsx)
**So that** laporan dapat diedit, dicetak, atau dikirim ke Dinas Pendidikan

**Prioritas:** CRITICAL
**Estimasi:** 1 hari
**Epic:** KIB Reporting

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User sudah generate laporan KIB (A-F) dan melihat preview
2. **Proses:** User klik "Ekspor ke Excel", sistem generate file Excel dengan format standar
3. **Output:** File Excel terdownload dengan nama sesuai format, notifikasi sukses

**Acceptance Criteria:**

```gherkin
Given Admin sudah generate laporan KIB B dan melihat preview
When Admin klik tombol "Ekspor ke Excel"
Then sistem generate file Excel (.xlsx) dalam waktu < 15 detik untuk 1000 aset
And format Excel sesuai template KIB B standar Permendagri 19/2016
And nama file: "KIB_B_20260105.xlsx" (format: KIB_{kategori}_{tanggal})
And file include:

  - Header: Logo sekolah, nama sekolah, judul laporan
  - Tabel data dengan semua kolom KIB B
  - Footer: Total jumlah dan nilai aset
  - Tempat tanda tangan Kepala Sekolah

And sistem download file ke komputer User
And sistem tampilkan notifikasi: "File berhasil diunduh"
```

```gherkin
Given Admin ekspor laporan KIB dengan 5000 aset
When sistem generate file Excel
Then sistem batasi maksimal 10,000 baris per file (untuk performa)
And jika > 10,000 aset: sistem buat multiple file atau tampilkan warning
```

```gherkin
Given Kepala Sekolah (bukan Admin) ekspor laporan KIB
When Kepala Sekolah klik "Ekspor ke Excel"
Then sistem allow ekspor (Kepala Sekolah punya hak ekspor)
And proses ekspor sama dengan Admin
```

**Business Rules:**

- Format Excel mengikuti template standar Permendagri 19/2016
- Nama file: KIB_{kategori}_{YYYYMMDD}.xlsx
- Maksimal 10,000 baris per file (untuk performa)
- Header include: Logo sekolah, nama sekolah, judul laporan, tanggal
- Footer include: Total jumlah dan nilai, tempat tanda tangan
- Target performa: < 15 detik untuk 1000 aset
- Admin dan Kepala Sekolah dapat ekspor, Viewer tidak bisa

**Dependencies:** US-006 to US-011 (Generate KIB reports)

---

### EPIC 3: Asset Movement Tracking

---

#### US-013: Memulai Mutasi Aset Antarruangan

**As a** Admin Sekolah
**I want** memulai proses mutasi aset dari satu ruangan ke ruangan lain dengan mencatat alasan
**So that** perpindahan aset tercatat dengan jejak audit yang jelas

**Prioritas:** CRITICAL
**Estimasi:** 2-3 hari
**Epic:** Asset Movement Tracking

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** Admin mencari aset yang akan dimutasi dan klik "Mutasi"
2. **Proses:** Admin pilih ruangan tujuan, isi alasan mutasi, sistem validasi dan simpan
3. **Output:** Aset berstatus "Mutasi", data mutasi tersimpan, menunggu konfirmasi selesai

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan mencari aset dengan Kode "32.01.02.0001"
And aset berstatus "Aktif" dan berada di ruangan "Lab Komputer"
When Admin klik tombol "Mutasi" pada detail aset
And sistem tampilkan form mutasi:

  - Ruangan Asal: "Lab Komputer" (auto-fill, read-only)
  - Ruangan Tujuan: [Dropdown pilihan ruangan]
  - Tanggal Mutasi: "05/01/2026" (default: hari ini)
  - Alasan Mutasi: [Text area]
  - Kondisi Saat Mutasi: [Dropdown: Baik/Rusak]

And Admin pilih Ruangan Tujuan: "Ruang Guru"
And Admin isi Alasan: "Dipindahkan untuk kebutuhan administrasi guru"
And Admin pilih Kondisi: "Baik"
And Admin klik "Proses Mutasi"
Then sistem validasi:

  - Ruangan tujuan berbeda dari ruangan asal ✓
  - Alasan mutasi terisi (min 10 karakter) ✓
  - Tanggal mutasi tidak di masa depan ✓

And sistem tampilkan konfirmasi: "Mutasi aset Laptop HP Pavilion dari Lab Komputer ke Ruang Guru. Lanjutkan?"
And Admin klik "Ya, Lanjutkan"
Then sistem update status aset = "Mutasi"
And sistem simpan data mutasi ke tabel riwayat_mutasi:

  - aset_id, ruangan_asal_id, ruangan_tujuan_id, tanggal_mutasi, alasan, kondisi_saat_mutasi, user_id, status_mutasi = "Dalam Proses"

And sistem tampilkan notifikasi: "Mutasi berhasil diproses. Konfirmasi setelah aset tiba di ruangan tujuan."
```

```gherkin
Given Admin memulai mutasi aset
When Admin pilih Ruangan Tujuan yang sama dengan Ruangan Asal
And klik "Proses Mutasi"
Then sistem tampilkan error: "Ruangan tujuan harus berbeda dari ruangan asal"
And form tetap terbuka untuk perbaikan
```

```gherkin
Given Admin memulai mutasi aset
When Admin isi Alasan dengan < 10 karakter: "Pindah"
And klik "Proses Mutasi"
Then sistem tampilkan error: "Alasan mutasi harus minimal 10 karakter"
And form tetap terbuka untuk perbaikan
```

```gherkin
Given Aset sudah memiliki mutasi pending (status "Mutasi")
When Admin mencoba memulai mutasi baru untuk aset yang sama
Then sistem tampilkan error: "Aset sedang dalam proses mutasi. Selesaikan mutasi yang ada terlebih dahulu."
And sistem tampilkan info mutasi yang sedang berjalan
```

**Business Rules:**

- Hanya Admin yang dapat memulai mutasi
- Aset hanya bisa dimutasi jika status "Aktif"
- Satu aset hanya bisa memiliki 1 mutasi pending
- Ruangan tujuan harus berbeda dari ruangan asal
- Alasan mutasi wajib diisi (min 10 karakter)
- Tanggal mutasi tidak boleh di masa depan
- Status aset berubah menjadi "Mutasi" sampai dikonfirmasi selesai
- Mutasi harus dikonfirmasi dalam 7 hari, jika tidak otomatis dibatalkan

**Dependencies:** US-001 (Create asset), US-002 (View asset)

---

#### US-014: Konfirmasi Mutasi Selesai

**As a** Admin Sekolah
**I want** konfirmasi bahwa mutasi aset sudah selesai setelah aset tiba di ruangan tujuan
**So that** lokasi aset terupdate dan status kembali "Aktif"

**Prioritas:** CRITICAL
**Estimasi:** 1 hari
**Epic:** Asset Movement Tracking

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** Admin membuka menu "Mutasi Pending" dan melihat daftar mutasi yang belum selesai
2. **Proses:** Admin pilih mutasi yang akan dikonfirmasi, klik "Konfirmasi Selesai"
3. **Output:** Ruangan aset terupdate, status kembali "Aktif", riwayat mutasi tercatat

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan membuka menu "Mutasi Pending"
And ada mutasi aset "Laptop HP Pavilion" dengan status "Dalam Proses"
When Admin klik mutasi tersebut untuk melihat detail
And sistem tampilkan info mutasi:

  - Nama Aset, Kode Barang
  - Ruangan Asal: "Lab Komputer"
  - Ruangan Tujuan: "Ruang Guru"
  - Tanggal Mutasi: "05/01/2026"
  - Alasan: "Dipindahkan untuk kebutuhan administrasi guru"
  - Status: "Dalam Proses"

And Admin klik tombol "Konfirmasi Selesai"
Then sistem tampilkan konfirmasi: "Konfirmasi bahwa aset sudah tiba di Ruang Guru?"
And Admin klik "Ya, Konfirmasi"
Then sistem finalisasi mutasi:

  - Update ruangan aset = "Ruang Guru"
  - Update status aset = "Aktif"
  - Update status_mutasi = "Selesai"
  - Catat timestamp selesai_mutasi

And sistem tampilkan notifikasi: "Mutasi selesai. Aset sekarang berada di Ruang Guru"
```

```gherkin
Given Admin melihat daftar mutasi pending
When mutasi sudah berjalan > 7 hari tanpa konfirmasi
Then sistem otomatis batalkan mutasi:

  - Update status aset = "Aktif"
  - Update status_mutasi = "Dibatalkan"
  - Ruangan aset tetap di ruangan asal
  - Catat alasan pembatalan: "Timeout - tidak dikonfirmasi dalam 7 hari"

And sistem tampilkan warning di daftar: "Mutasi dibatalkan otomatis (timeout)"
```

```gherkin
Given Admin ingin membatalkan mutasi sebelum konfirmasi selesai
When Admin klik tombol "Batalkan Mutasi" di detail mutasi
And sistem tampilkan konfirmasi: "Yakin batalkan mutasi?"
And Admin klik "Ya, Batalkan"
Then sistem batalkan mutasi:

  - Update status aset = "Aktif"
  - Update status_mutasi = "Dibatalkan"
  - Ruangan aset tetap di ruangan asal
  - Catat alasan pembatalan (input dari Admin)

And sistem tampilkan notifikasi: "Mutasi berhasil dibatalkan"
```

**Business Rules:**

- Hanya Admin yang dapat konfirmasi mutasi
- Mutasi harus dikonfirmasi dalam 7 hari, jika tidak otomatis dibatalkan
- Setelah konfirmasi: ruangan aset update, status kembali "Aktif"
- Riwayat mutasi tidak dapat dihapus (audit trail)
- Admin dapat membatalkan mutasi sebelum konfirmasi

**Dependencies:** US-013 (Initiate mutation)

---

#### US-015: Melihat Riwayat Mutasi Aset

**As a** Admin Sekolah / Guru (Viewer) / Kepala Sekolah
**I want** melihat riwayat mutasi aset untuk melacak perpindahan
**So that** saya dapat mengaudit pergerakan aset dan mengetahui lokasi historis

**Prioritas:** HIGH
**Estimasi:** 1 hari
**Epic:** Asset Movement Tracking

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User melihat detail aset dan scroll ke bagian "Riwayat Mutasi"
2. **Proses:** Sistem load riwayat mutasi dari database
3. **Output:** Tabel riwayat mutasi dengan semua perpindahan aset

**Acceptance Criteria:**

```gherkin
Given User sudah login dan melihat detail aset "Laptop HP Pavilion"
And aset memiliki riwayat mutasi
When User scroll ke bagian "Riwayat Mutasi"
Then sistem tampilkan tabel riwayat dengan kolom:

  - Tanggal Mutasi
  - Ruangan Asal
  - Ruangan Tujuan
  - Alasan
  - User yang Memproses
  - Status (Selesai/Dibatalkan)

And urutkan berdasarkan tanggal terbaru (descending)
And tampilkan maksimal 50 riwayat per halaman (pagination jika > 50)
```

```gherkin
Given User melihat riwayat mutasi aset
When aset belum pernah dimutasi
Then sistem tampilkan pesan: "Belum ada riwayat mutasi untuk aset ini"
```

```gherkin
Given Admin melihat riwayat mutasi
When Admin klik salah satu riwayat mutasi
Then sistem tampilkan detail lengkap mutasi:

  - Semua field mutasi (tanggal, ruangan, alasan, kondisi saat mutasi)
  - Timestamp mulai dan selesai mutasi
  - User yang memproses dan mengkonfirmasi
  - Alasan pembatalan (jika dibatalkan)

```

**Business Rules:**

- Semua role dapat melihat riwayat mutasi
- Riwayat mutasi tidak dapat dihapus (audit trail permanen)
- Riwayat diurutkan berdasarkan tanggal terbaru
- Maksimal 50 riwayat per halaman (pagination)

**Dependencies:** US-013 (Initiate mutation), US-014 (Confirm mutation)

---

### EPIC 4: Room Inventory Management

---

#### US-016: Generate Laporan KIR (Kartu Inventaris Ruangan)

**As a** Admin Sekolah / Kepala Sekolah
**I want** generate laporan KIR untuk ruangan tertentu
**So that** saya dapat melihat semua aset yang berada di ruangan tersebut

**Prioritas:** HIGH
**Estimasi:** 1-2 hari
**Epic:** Room Inventory Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User login dan membuka menu "Laporan KIR"
2. **Proses:** User pilih ruangan, klik "Generate Laporan", sistem query aset di ruangan tersebut
3. **Output:** Preview laporan KIR dengan daftar aset per ruangan, total nilai

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Laporan KIR"
When Admin pilih ruangan "Lab Komputer"
And Admin klik "Generate Laporan"
Then sistem query semua aset dengan ruangan = "Lab Komputer" dan status "Aktif" atau "Rusak"
And sistem tampilkan preview laporan KIR dengan kolom:

  - No, Kode Barang, Nama Barang, Kategori KIB, Merk/Type (jika ada), Kondisi, Harga (Rp)

And sistem tampilkan header: "Kartu Inventaris Ruangan: Lab Komputer"
And sistem tampilkan total: "Total: 25 unit | Total Nilai: Rp 125,000,000"
And sistem tampilkan tanggal generate laporan
And waktu generate < 5 detik
```

```gherkin
Given Admin generate laporan KIR untuk ruangan "Lab Komputer"
When Admin klik tombol "Ekspor ke Excel"
Then sistem generate file Excel dengan nama: "KIR_Lab_Komputer_20260105.xlsx"
And format Excel include header ruangan dan tabel aset
And sistem download file
```

```gherkin
Given Admin pilih ruangan yang tidak memiliki aset
When Admin klik "Generate Laporan"
Then sistem tampilkan pesan: "Tidak ada aset di ruangan ini"
And Admin dapat memilih ruangan lain
```

**Business Rules:**

- Hanya aset dengan status "Aktif" dan "Rusak" yang diikutkan
- Aset dengan status "Dihapus" tidak diikutkan
- Urutkan berdasarkan Kategori KIB, lalu Nama Barang
- Format Excel include header ruangan dan total nilai
- Target performa: < 5 detik untuk generate

**Dependencies:** US-001 (Create asset)

---

#### US-017: Melihat Aset per Ruangan (Viewer)

**As a** Guru (Viewer)
**I want** melihat daftar aset yang berada di ruangan tertentu
**So that** saya dapat mengetahui inventaris ruangan yang saya gunakan

**Prioritas:** HIGH
**Estimasi:** 1 hari
**Epic:** Room Inventory Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** Viewer login dan membuka menu "Aset per Ruangan"
2. **Proses:** Viewer pilih ruangan, sistem tampilkan daftar aset
3. **Output:** Daftar aset di ruangan tersebut (read-only)

**Acceptance Criteria:**

```gherkin
Given Viewer (Guru) sudah login
When Viewer membuka menu "Aset per Ruangan"
And Viewer pilih ruangan "Lab Komputer"
Then sistem tampilkan daftar aset di ruangan tersebut dengan kolom:

  - Kode Barang, Nama Barang, Kategori KIB, Kondisi

And Viewer dapat klik aset untuk melihat detail (read-only)
And Viewer tidak dapat edit atau hapus aset
```

```gherkin
Given Viewer melihat daftar aset per ruangan
When Viewer klik salah satu aset
Then sistem tampilkan detail aset (read-only)
And tidak tampilkan tombol "Edit" atau "Hapus"
```

**Business Rules:**

- Viewer hanya dapat melihat aset dengan status "Aktif" dan "Rusak"
- Viewer tidak dapat edit, hapus, atau mutasi aset
- Viewer tidak dapat ekspor laporan

**Dependencies:** US-001 (Create asset), US-002 (View asset)

---

### EPIC 5: User Access Management

---

#### US-018: Login dengan Role-Based Access

**As a** Admin Sekolah / Guru (Viewer) / Kepala Sekolah
**I want** login ke sistem dengan username dan password
**So that** saya dapat mengakses fitur sesuai dengan role saya

**Prioritas:** HIGH
**Estimasi:** 1-2 hari
**Epic:** User Access Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** User membuka aplikasi Simanis62 V2
2. **Proses:** User input username dan password, sistem validasi kredensial dan role
3. **Output:** User login sukses, redirect ke dashboard sesuai role

**Acceptance Criteria:**

```gherkin
Given User membuka aplikasi Simanis62 V2
When User berada di halaman login
And User input username: "admin_sekolah" dan password: "password123"
And User klik tombol "Login"
Then sistem validasi kredensial
And sistem load role user: "Admin"
And sistem create session dengan timeout 2 jam
And sistem redirect ke dashboard Admin dengan menu:

  - Tambah Aset, Daftar Aset, Pencarian Aset
  - Laporan KIB, Laporan KIR
  - Mutasi Aset, Mutasi Pending
  - Manajemen User, Pengaturan

And sistem tampilkan notifikasi: "Selamat datang, Admin Sekolah"
```

```gherkin
Given Viewer (Guru) login dengan username: "guru_matematika"
When sistem validasi kredensial dan load role: "Viewer"
Then sistem redirect ke dashboard Viewer dengan menu terbatas:

  - Daftar Aset (read-only)
  - Pencarian Aset
  - Aset per Ruangan

And tidak tampilkan menu: Tambah Aset, Mutasi, Manajemen User
```

```gherkin
Given User input username atau password yang salah
When User klik "Login"
Then sistem tampilkan error: "Username atau password salah"
And form login tetap terbuka untuk retry
And sistem log failed login attempt
```

```gherkin
Given User sudah login dan tidak ada aktivitas selama 2 jam
When session timeout tercapai
Then sistem otomatis logout user
And sistem tampilkan pesan: "Session telah berakhir. Silakan login kembali."
And redirect ke halaman login
```

**Business Rules:**

- Password minimal 8 karakter, harus mengandung huruf dan angka
- Password di-hash menggunakan bcrypt
- Session timeout: 2 jam (tidak ada aktivitas)
- Failed login attempts di-log untuk security audit
- 3 role: Admin (full access), Viewer (read-only), Kepala Sekolah (view + export)

**Dependencies:** None (first story for user management)

---

#### US-019: Manajemen User Viewer (Admin Only)

**As a** Admin Sekolah
**I want** menambah, mengubah, dan menghapus user Viewer (Guru)
**So that** saya dapat mengatur akses pengguna ke sistem

**Prioritas:** HIGH
**Estimasi:** 1-2 hari
**Epic:** User Access Management

**Alur Kerja (Awal - Proses - Output):**

1. **Awal:** Admin login dan membuka menu "Manajemen User"
2. **Proses:** Admin tambah/edit/hapus user Viewer, sistem validasi dan simpan
3. **Output:** User Viewer ter-create/update/delete, notifikasi sukses

**Acceptance Criteria:**

```gherkin
Given Admin sudah login dan berada di menu "Manajemen User"
When Admin klik tombol "Tambah User"
And Admin mengisi form:

  - Username: "guru_matematika" (unique, 5-50 karakter)
  - Password: "password123" (min 8 karakter, huruf + angka)
  - Nama Lengkap: "Budi Santoso"
  - Role: "Viewer" (fixed, tidak bisa pilih Admin)

And Admin klik "Simpan"
Then sistem validasi:

  - Username unique ✓
  - Password sesuai policy ✓

And sistem hash password menggunakan bcrypt
And sistem simpan user dengan role "Viewer"
And sistem tampilkan notifikasi: "User berhasil ditambahkan"
```

```gherkin
Given Admin melihat daftar user Viewer
When Admin klik tombol "Edit" pada user "guru_matematika"
And Admin mengubah Nama Lengkap menjadi "Budi Santoso, S.Pd"
And Admin klik "Simpan Perubahan"
Then sistem update data user
And sistem tampilkan notifikasi: "Data user berhasil diperbarui"
```

```gherkin
Given Admin ingin menghapus user Viewer
When Admin klik tombol "Hapus" pada user "guru_matematika"
And sistem tampilkan konfirmasi: "Yakin hapus user ini?"
And Admin klik "Ya, Hapus"
Then sistem soft delete user (set status = "Nonaktif")
And user tidak dapat login lagi
And sistem tampilkan notifikasi: "User berhasil dihapus"
```

```gherkin
Given Admin mencoba menambah user dengan username yang sudah ada
When Admin input username: "guru_matematika" (sudah ada)
And klik "Simpan"
Then sistem tampilkan error: "Username sudah digunakan"
And form tetap terbuka untuk perbaikan
```

**Business Rules:**

- Hanya Admin yang dapat manajemen user
- Admin tidak dapat menghapus dirinya sendiri
- Admin tidak dapat mengubah role user lain menjadi Admin
- Username harus unique (5-50 karakter)
- Password policy: min 8 karakter, huruf + angka
- Password di-hash menggunakan bcrypt
- User yang dihapus di-soft delete (status "Nonaktif")

**Dependencies:** US-018 (Login with role)

---

---

## 6. Story Mapping

### 6.1 User Journey: Admin Sekolah

```text
┌─────────────────────────────────────────────────────────────────────┐
│ SETUP & LOGIN                                                       │
├─────────────────────────────────────────────────────────────────────┤
│ US-018: Login dengan Role-Based Access                             │
│ US-019: Manajemen User Viewer                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ASSET DATA MANAGEMENT (Daily Operations)                           │
├─────────────────────────────────────────────────────────────────────┤
│ US-001: Pencatatan Aset Baru                                       │
│ US-002: Melihat Detail Aset                                        │
│ US-003: Mengubah Data Aset                                         │
│ US-004: Mencari Aset dengan Filter                                 │
│ US-005: Menghapus Aset (Soft Delete)                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ASSET MOVEMENT (As Needed)                                         │
├─────────────────────────────────────────────────────────────────────┤
│ US-013: Memulai Mutasi Aset Antarruangan                           │
│ US-014: Konfirmasi Mutasi Selesai                                  │
│ US-015: Melihat Riwayat Mutasi Aset                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ REPORTING (Monthly/Quarterly)                                      │
├─────────────────────────────────────────────────────────────────────┤
│ US-006: Generate Laporan KIB A (Tanah)                             │
│ US-007: Generate Laporan KIB B (Peralatan dan Mesin)               │
│ US-008: Generate Laporan KIB C (Gedung dan Bangunan)               │
│ US-009: Generate Laporan KIB D (Jalan, Irigasi, Jaringan)          │
│ US-010: Generate Laporan KIB E (Aset Tetap Lainnya)                │
│ US-011: Generate Laporan KIB F (Konstruksi dalam Pengerjaan)       │
│ US-012: Ekspor Laporan KIB ke Excel                                │
│ US-016: Generate Laporan KIR (Kartu Inventaris Ruangan)            │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 User Journey: Guru (Viewer)

```text
┌─────────────────────────────────────────────────────────────────────┐
│ LOGIN                                                               │
├─────────────────────────────────────────────────────────────────────┤
│ US-018: Login dengan Role-Based Access                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VIEW ASSETS (Read-Only)                                            │
├─────────────────────────────────────────────────────────────────────┤
│ US-002: Melihat Detail Aset                                        │
│ US-004: Mencari Aset dengan Filter                                 │
│ US-017: Melihat Aset per Ruangan                                   │
│ US-015: Melihat Riwayat Mutasi Aset                                │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.3 User Journey: Kepala Sekolah

```text
┌─────────────────────────────────────────────────────────────────────┐
│ LOGIN                                                               │
├─────────────────────────────────────────────────────────────────────┤
│ US-018: Login dengan Role-Based Access                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ VIEW & REVIEW                                                       │
├─────────────────────────────────────────────────────────────────────┤
│ US-002: Melihat Detail Aset                                        │
│ US-004: Mencari Aset dengan Filter                                 │
│ US-015: Melihat Riwayat Mutasi Aset                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ REPORTING & APPROVAL                                                │
├─────────────────────────────────────────────────────────────────────┤
│ US-006 to US-011: Generate Laporan KIB A-F                         │
│ US-012: Ekspor Laporan KIB ke Excel                                │
│ US-016: Generate Laporan KIR                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Traceability Matrix

### 7.1 User Stories → Architecture Documents

| User Story | Dok 1: Tujuan Bisnis | Dok 2: Masalah Inti | Dok 3: Alur Kerja |
|------------|---------------------|---------------------|-------------------|
| US-001 | Fitur Wajib #1 (CRUD) | Masalah 1 (Pencatatan manual) | Bagian 6.1 |
| US-002 | Fitur Wajib #1 (CRUD) | Masalah 1 (Pencatatan manual) | Bagian 6.1 |
| US-003 | Fitur Wajib #1 (CRUD) | Masalah 1 (Pencatatan manual) | Bagian 6.1 |
| US-004 | Fitur Wajib #2 (Pencarian) | Masalah 1 (Pencatatan manual) | Bagian 6.4 |
| US-005 | Fitur Penting #5 (Penghapusan) | Masalah Sekunder #2 | Bagian 6.5 |
| US-006 | Fitur Wajib #3 (KIB A-F) | Masalah 2 (Laporan KIB) | Bagian 6.2 |
| US-007 | Fitur Wajib #3 (KIB A-F) | Masalah 2 (Laporan KIB) | Bagian 6.2 |
| US-008 | Fitur Wajib #3 (KIB A-F) | Masalah 2 (Laporan KIB) | Bagian 6.2 |
| US-009 | Fitur Wajib #3 (KIB A-F) | Masalah 2 (Laporan KIB) | Bagian 6.2 |
| US-010 | Fitur Wajib #3 (KIB A-F) | Masalah 2 (Laporan KIB) | Bagian 6.2 |
| US-011 | Fitur Wajib #3 (KIB A-F) | Masalah 2 (Laporan KIB) | Bagian 6.2 |
| US-012 | Fitur Wajib #6 (Ekspor Excel) | Masalah 2 (Laporan KIB) | Bagian 8.2 |
| US-013 | Fitur Wajib #5 (Mutasi) | Masalah 3 (Jejak audit) | Bagian 6.3 |
| US-014 | Fitur Wajib #5 (Mutasi) | Masalah 3 (Jejak audit) | Bagian 6.3 |
| US-015 | Fitur Wajib #5 (Mutasi) | Masalah 3 (Jejak audit) | Bagian 6.3 |
| US-016 | Fitur Wajib #4 (KIR) | Masalah 1 (Pencatatan manual) | Bagian 6.2 |
| US-017 | Fitur Wajib #4 (KIR) | Masalah 1 (Pencatatan manual) | Bagian 6.2 |
| US-018 | Fitur Wajib #8 (Multi User) | Masalah 1 (Pencatatan manual) | Bagian 3 |
| US-019 | Fitur Wajib #8 (Multi User) | Masalah 1 (Pencatatan manual) | Bagian 3 |

### 7.2 User Stories → Core Problems

| Core Problem | User Stories yang Menyelesaikan |
|--------------|--------------------------------|
| **Problem 1:** Pencatatan aset manual yang tidak efisien | US-001, US-002, US-003, US-004, US-016, US-017, US-018, US-019 |
| **Problem 2:** Pembuatan laporan KIB yang memakan waktu | US-006, US-007, US-008, US-009, US-010, US-011, US-012 |
| **Problem 3:** Tidak ada jejak audit perpindahan aset | US-013, US-014, US-015 |

### 7.3 User Stories → Mandatory Features

| Mandatory Feature | User Stories |
|-------------------|--------------|
| 1. CRUD Data Barang | US-001, US-002, US-003 |
| 2. Pencarian Aset | US-004 |
| 3. KIB A-F | US-006, US-007, US-008, US-009, US-010, US-011 |
| 4. KIR | US-016, US-017 |
| 5. Mutasi Barang | US-013, US-014, US-015 |
| 6. Ekspor Excel | US-012 |
| 7. Kode Barang Unik | US-001 (included in create) |
| 8. Multi User | US-018, US-019 |

---

## 8. Implementation Priority

### 8.1 Sprint 1 (Week 1-2): Foundation & Core CRUD

**Goal:** Setup project, database, dan implement core CRUD functionality

| Priority | User Story | Estimasi | Rationale |
|----------|------------|----------|-----------|
| 1 | US-018 | 1-2 hari | Login required untuk semua fitur |
| 2 | US-001 | 2-3 hari | Create asset adalah fondasi sistem |
| 3 | US-002 | 1 hari | View asset untuk verifikasi create |
| 4 | US-003 | 1-2 hari | Update asset untuk koreksi data |
| 5 | US-004 | 2 hari | Search asset untuk efisiensi operasional |

**Deliverable:** User dapat login, create, view, update, dan search assets

### 8.2 Sprint 2 (Week 3-4): KIB Reporting

**Goal:** Implement KIB A-F reporting dan export Excel

| Priority | User Story | Estimasi | Rationale |
|----------|------------|----------|-----------|
| 1 | US-006 | 1-2 hari | KIB A (Tanah) - template untuk KIB lain |
| 2 | US-007 | 1-2 hari | KIB B (Peralatan) - kategori terbanyak |
| 3 | US-008 | 1-2 hari | KIB C (Gedung) |
| 4 | US-009 | 1-2 hari | KIB D (Jalan) |
| 5 | US-010 | 1-2 hari | KIB E (Aset Lainnya) |
| 6 | US-011 | 1-2 hari | KIB F (Konstruksi) |
| 7 | US-012 | 1 hari | Export Excel untuk semua KIB |

**Deliverable:** User dapat generate dan export laporan KIB A-F

### 8.3 Sprint 3 (Week 5-6): Asset Movement & Room Inventory

**Goal:** Implement mutasi aset dan laporan KIR

| Priority | User Story | Estimasi | Rationale |
|----------|------------|----------|-----------|
| 1 | US-013 | 2-3 hari | Initiate mutation dengan validasi |
| 2 | US-014 | 1 hari | Confirm mutation completion |
| 3 | US-015 | 1 hari | View mutation history untuk audit |
| 4 | US-016 | 1-2 hari | Generate KIR report |
| 5 | US-017 | 1 hari | View assets by room (Viewer) |

**Deliverable:** User dapat mutasi aset dan generate laporan KIR

### 8.4 Sprint 4 (Week 7-8): User Management & Soft Delete

**Goal:** Complete user management dan soft delete functionality

| Priority | User Story | Estimasi | Rationale |
|----------|------------|----------|-----------|
| 1 | US-019 | 1-2 hari | Manage Viewer users |
| 2 | US-005 | 1-2 hari | Soft delete assets dengan audit |

**Deliverable:** Admin dapat manage users dan soft delete assets

### 8.5 Sprint 5 (Week 9-10): Testing, Bug Fixes, Documentation

**Goal:** End-to-end testing, bug fixes, dan user documentation

- Integration testing semua fitur
- Performance testing (target < 5 detik search, < 10 detik report)
- User acceptance testing dengan Admin Sekolah
- Bug fixes berdasarkan testing
- User manual dan installation guide

**Deliverable:** Production-ready system dengan dokumentasi lengkap

---

## 9. Acceptance Testing Guidelines

### 9.1 Definition of Done (DoD)

Setiap user story dianggap selesai jika memenuhi kriteria berikut:

| Kriteria | Deskripsi |
|----------|-----------|
| **Code Complete** | Semua code untuk story sudah ditulis dan di-commit |
| **Unit Tests Pass** | Semua unit tests pass dengan coverage > 80% |
| **Integration Tests Pass** | Integration tests untuk story pass |
| **Acceptance Criteria Met** | Semua acceptance criteria dalam story terpenuhi |
| **Code Review Done** | Code sudah di-review oleh minimal 1 developer lain |
| **No Critical Bugs** | Tidak ada bug dengan severity Critical atau High |
| **Performance Criteria Met** | Performance target tercapai (search < 5s, report < 10s) |
| **Documentation Updated** | User manual dan technical docs updated |
| **Demo to Stakeholder** | Story sudah di-demo dan approved oleh Product Owner |

### 9.2 Testing Checklist per Story

#### Functional Testing

- [ ] Semua acceptance criteria terpenuhi
- [ ] Happy path scenario berjalan dengan baik
- [ ] Alternative path scenario berjalan dengan baik
- [ ] Error handling berfungsi dengan benar
- [ ] Validation rules diterapkan dengan benar

#### Non-Functional Testing

- [ ] Performance target tercapai
- [ ] UI responsive dan user-friendly
- [ ] Error messages jelas dan helpful
- [ ] Audit trail tercatat dengan benar
- [ ] Security: hak akses sesuai role

#### Integration Testing

- [ ] Integrasi dengan database berfungsi
- [ ] Integrasi dengan API backend berfungsi
- [ ] Integrasi dengan fitur lain tidak broken

#### Regression Testing

- [ ] Fitur existing tidak broken
- [ ] Data existing tidak corrupt
- [ ] Performance tidak degraded

### 9.3 Test Data Requirements

**Master Data:**

- Minimal 3 ruangan (Lab Komputer, Ruang Guru, Perpustakaan)
- Minimal 3 user (1 Admin, 1 Viewer, 1 Kepala Sekolah)

**Asset Data:**

- Minimal 10 aset per kategori KIB (A-F)
- Minimal 5 aset dengan kondisi "Rusak"
- Minimal 3 aset dengan riwayat mutasi
- Minimal 2 aset dengan status "Dihapus"

**Edge Cases:**

- Aset dengan nama sangat panjang (200 karakter)
- Aset dengan harga sangat besar (999,999,999,999)
- Aset dengan tahun perolehan sangat lama (1900)
- Ruangan dengan banyak aset (> 100 aset)

### 9.4 Performance Testing Criteria

| Operasi | Target | Measurement |
|---------|--------|-------------|
| Login | < 2 detik | Dari klik "Login" sampai dashboard muncul |
| Create Asset | < 3 detik | Dari klik "Simpan" sampai notifikasi sukses |
| Search Asset | < 5 detik | Dari klik "Cari" sampai hasil muncul |
| View Asset Detail | < 2 detik | Dari klik aset sampai detail muncul |
| Generate KIB Report | < 10 detik | Untuk 1000 aset, dari klik "Generate" sampai preview |
| Export Excel | < 15 detik | Untuk 1000 aset, dari klik "Ekspor" sampai download |
| Initiate Mutation | < 3 detik | Dari klik "Proses Mutasi" sampai notifikasi |

**Testing Environment:**

- Laptop kentang: RAM 2GB, Pentium 4
- Database: 1000 aset, 10 ruangan, 5 users
- Concurrent users: 5 users simultaneous

---

## 10. Risks dan Mitigasi

### 10.1 Risks Terkait User Stories

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **R1:** Perubahan format KIB oleh pemerintah | High | Low | Desain modular untuk modul laporan, isolasi logika format KIB |
| **R2:** Performance tidak mencapai target (< 5s search) | High | Medium | Optimasi query, indexing agresif, pagination, caching |
| **R3:** User tidak mengadopsi sistem | High | Medium | UI sangat intuitif, pelatihan intensif, dukungan on-site |
| **R4:** Data loss karena hardware failure | High | Medium | Backup otomatis harian, export Excel berkala |
| **R5:** Kompleksitas validasi per KIB category | Medium | Medium | Reusable validation components, comprehensive unit tests |
| **R6:** Excel export timeout untuk data besar | Medium | Low | Batasi maksimal 10,000 baris per file, streaming export |

### 10.2 Technical Debt Prevention

**Code Quality:**

- Code review mandatory untuk setiap PR
- Unit test coverage > 80%
- Follow coding standards (PEP 8 untuk Python, C# conventions untuk WPF)
- Refactoring sprint setiap 2 sprint

**Documentation:**

- Update user manual setiap sprint
- Update technical docs setiap major change
- Maintain API documentation (Swagger/OpenAPI)

**Testing:**

- Automated regression tests
- Performance testing setiap sprint
- User acceptance testing setiap 2 sprint

---

## 11. Ringkasan Eksekutif

### 11.1 Total User Stories

| Epic | Jumlah Stories | Estimasi Total |
|------|----------------|----------------|
| EPIC 1: Asset Data Management | 5 stories | 7-10 hari |
| EPIC 2: KIB Reporting | 7 stories | 8-14 hari |
| EPIC 3: Asset Movement Tracking | 3 stories | 4-5 hari |
| EPIC 4: Room Inventory Management | 2 stories | 2-3 hari |
| EPIC 5: User Access Management | 2 stories | 2-4 hari |
| **TOTAL** | **19 stories** | **23-36 hari** |

**Estimasi Total dengan Buffer (20%):** 28-43 hari kerja (6-9 minggu)

### 11.2 Coverage Validation

✅ **Semua 8 Mandatory Features Covered:**

1. CRUD Data Barang → US-001, US-002, US-003
2. Pencarian Aset → US-004
3. KIB A-F → US-006 to US-011
4. KIR → US-016, US-017
5. Mutasi Barang → US-013, US-014, US-015
6. Ekspor Excel → US-012
7. Kode Barang Unik → US-001 (included)
8. Multi User → US-018, US-019

✅ **Semua 3 Core Problems Addressed:**

1. Pencatatan manual tidak efisien → 8 stories
2. Laporan KIB memakan waktu → 7 stories
3. Tidak ada jejak audit → 3 stories

✅ **Semua 3 User Roles Supported:**

1. Admin Sekolah → 19 stories (full access)
2. Guru (Viewer) → 5 stories (read-only)
3. Kepala Sekolah → 10 stories (view + export)

### 11.3 Quality Assurance

- **INVEST Criteria:** ✅ All stories meet INVEST criteria
- **Acceptance Criteria:** ✅ 3-5 criteria per story in Given-When-Then format
- **Business Rules:** ✅ Documented per story with validation rules
- **Performance Targets:** ✅ Defined and measurable
- **Traceability:** ✅ Mapped to architecture documents
- **Realistic Scope:** ✅ No ambitious or idealistic features
- **Clear Flow:** ✅ Awal-Proses-Output documented per story

### 11.4 Ready for Implementation

✅ **Documentation Complete:**

- 19 user stories dengan acceptance criteria lengkap
- Story mapping untuk 3 user roles
- Traceability matrix ke 3 dokumen arsitektur
- Implementation priority dengan 5 sprint plan
- Testing guidelines dan DoD

✅ **Aligned with Architecture:**

- Konsisten dengan Tujuan Bisnis (Dok 1)
- Menyelesaikan Masalah Inti (Dok 2)
- Mengikuti Alur Kerja (Dok 3)
- Sesuai Tech Stack (SQLite, WPF, FastAPI)

✅ **Realistic and Achievable:**

- Estimasi total: 6-9 minggu
- Tidak ambisius, fokus pada core functionality
- Tidak ada fitur dari "deferred list"
- Performance targets realistis untuk laptop kentang

**Status:** ✅ **READY TO CODE**

---

*Dokumen ini merupakan bagian dari dokumentasi arsitektur Simanis62 V2.*
*Referensi: Permendagri Nomor 19 Tahun 2016 tentang Pedoman Pengelolaan Barang Milik Daerah*
