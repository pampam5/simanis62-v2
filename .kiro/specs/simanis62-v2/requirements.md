# Requirements Document: SIMANIS62 V2

## Introduction

SIMANIS62 V2 adalah sistem manajemen aset sekolah berbasis desktop yang dirancang untuk membantu sekolah di Indonesia dalam mengelola inventaris aset sesuai dengan regulasi Permendagri 19/2016 (dengan update 47/2021 dan 7/2024). Sistem ini menyediakan fitur CRUD aset, pembuatan laporan KIB A-F, pencatatan mutasi aset, dan ekspor data ke Excel.

## Glossary

### Entitas & Aktor
- **System**: SIMANIS62 V2 application (WPF Client + FastAPI Server)
- **Admin**: Admin Sekolah dengan hak akses penuh (CRUD, reports, export, user management)
- **Viewer**: Guru dengan hak akses read-only
- **Kepala_Sekolah**: Kepala Sekolah dengan hak akses read-only + export (implemented as Viewer with dapat_ekspor flag)
- **Aset**: Barang Milik Daerah (BMD) yang tercatat dalam sistem
- **KIB**: Kartu Inventaris Barang (A-F) sesuai Permendagri 19/2016
- **KIR**: Kartu Inventaris Ruangan
- **Mutasi**: Perpindahan aset dari satu ruangan ke ruangan lain

### Field Database (snake_case, Bahasa Indonesia)

#### Field Umum (Semua KIB)
- **nomor_register**: Nomor urut unik per kategori KIB, auto-generated oleh sistem
- **kode_barang**: Kode identifikasi unik aset format XX.XX.XX.XXXX
- **nama_barang**: Nama/deskripsi barang
- **kategori_kib**: Kategori KIB (A/B/C/D/E/F)
- **tahun_perolehan**: Tahun aset diperoleh
- **tanggal_perolehan**: Tanggal lengkap perolehan (format DD/MM/YYYY)
- **harga**: Nilai perolehan aset dalam Rupiah penuh (bukan ribuan)
- **kondisi**: Kondisi fisik aset (Baik/Rusak Ringan/Rusak Berat)
- **status**: Status aset (Baru/Aktif/Mutasi/Rusak/Dihapus)
- **asal_usul**: Sumber perolehan (Pembelian/Hibah/Bantuan/APBD)
- **keterangan**: Catatan tambahan

#### Field KIB A (Tanah) - Format BPAD DKI Jakarta (14 Kolom)
- **luas_m2**: Luas tanah dalam meter persegi
- **alamat_lokasi**: Alamat/lokasi tanah
- **status_hak_tanah**: Status hak tanah (Hak Milik/Hak Pakai/Hak Guna Bangunan)
- **tanggal_sertifikat**: Tanggal sertifikat (format DD/MM/YYYY)
- **nomor_sertifikat**: Nomor sertifikat tanah
- **penggunaan**: Penggunaan tanah (Sekolah/Lapangan/dll)

#### Field KIB B (Peralatan dan Mesin) - Format BPAD DKI Jakarta (18 Kolom)
- **ukuran_cc**: Ukuran atau CC (untuk kendaraan)
- **satuan**: Satuan barang (BH/Unit/Set/Buah)
- **tanggal_dokumen**: Tanggal BPKB/dokumen (format DD/MM/YYYY)
- **bahan**: Material/bahan barang
- **merk**: Merk barang
- **tipe**: Tipe/model barang
- **nomor_rangka**: Nomor rangka/chasis (untuk kendaraan)
- **nomor_mesin**: Nomor mesin/pabrik
- **nomor_polisi**: Nomor polisi (untuk kendaraan)
- **kapitalisasi**: Nilai kapitalisasi (Rupiah penuh)
- **total_harga**: Total harga (Rupiah penuh)

#### Field KIB C (Gedung dan Bangunan) - Format BPAD DKI Jakarta (17 Kolom)
- **kondisi**: Kondisi bangunan (B=Baik, KB=Kurang Baik, RB=Rusak Berat)
- **bertingkat**: Apakah bangunan bertingkat (Ya/Tidak)
- **beton**: Apakah konstruksi beton (Ya/Tidak)
- **luas_lantai_m2**: Luas lantai dalam meter persegi
- **alamat_lokasi**: Alamat/lokasi bangunan
- **tanggal_dokumen**: Tanggal dokumen (format DD/MM/YYYY)
- **nomor_dokumen**: Nomor dokumen
- **luas_tanah_m2**: Luas tanah dalam meter persegi
- **status_tanah**: Status tanah
- **kode_tanah**: Nomor kode tanah

#### Field KIB D (Jalan, Irigasi, Jaringan) - Format BPAD DKI Jakarta (16 Kolom)
- **jenis_konstruksi**: Jenis konstruksi
- **panjang_km**: Panjang dalam kilometer
- **lebar_m**: Lebar dalam meter
- **luas_m2**: Luas dalam meter persegi
- **alamat_lokasi**: Alamat/lokasi
- **tanggal_dokumen**: Tanggal dokumen (format DD/MM/YYYY)
- **nomor_dokumen**: Nomor dokumen
- **status_tanah**: Status tanah
- **kode_tanah**: Nomor kode tanah

#### Field KIB E (Aset Tetap Lainnya) - Format BPAD DKI Jakarta (16 Kolom)
- **judul_pencipta**: Judul/pencipta (untuk buku)
- **spesifikasi_buku**: Spesifikasi buku
- **asal_daerah**: Asal daerah (untuk barang bercorak)
- **pencipta**: Pencipta (untuk barang bercorak)
- **bahan**: Bahan (untuk barang bercorak)
- **jenis_hewan**: Jenis hewan/ternak
- **ukuran_hewan**: Ukuran hewan/ternak
- **jumlah**: Jumlah barang

#### Field KIB F (Konstruksi dalam Pengerjaan) - Format BPAD DKI Jakarta (12 Kolom)
- **jenis_bangunan**: Jenis bangunan
- **bertingkat**: Apakah bangunan bertingkat (Ya/Tidak)
- **beton**: Apakah konstruksi beton (Ya/Tidak)
- **luas_m2**: Luas dalam meter persegi
- **alamat_lokasi**: Alamat/lokasi konstruksi
- **info_dokumen**: Informasi dokumen (tanggal/nomor)

#### Field Lokasi dan Mutasi
- **ruangan_id**: Foreign key ke tabel ruangan (lokasi aset saat ini)
- **ruangan_asal_id**: FK ke ruangan asal mutasi
- **ruangan_tujuan_id**: FK ke ruangan tujuan mutasi
- **alasan**: Alasan perpindahan aset (min 10 karakter)
- **kondisi_saat_mutasi**: Kondisi aset saat mutasi
- **status_mutasi**: Status mutasi (Dalam Proses/Selesai/Dibatalkan)
- **mulai_mutasi**: Timestamp mulai mutasi
- **selesai_mutasi**: Timestamp selesai mutasi
- **alasan_pembatalan**: Alasan pembatalan mutasi (jika dibatalkan)

#### Field Ruangan
- **kode_ruangan**: Kode unik ruangan (contoh: LAB-01, RG-02)
- **nama_ruangan**: Nama ruangan (contoh: Lab Komputer, Ruang Guru)
- **keterangan**: Deskripsi/catatan ruangan (opsional)

> **CATATAN**: Model Ruangan TIDAK memiliki field `gedung` atau `lantai`. Jika diperlukan, informasi ini dapat disimpan di field `keterangan`.

#### Field Audit Trail
- **created_by**: User ID yang membuat record (FK ke users.id)
- **created_at**: Timestamp pembuatan record
- **updated_by**: User ID yang mengupdate record (FK ke users.id)
- **updated_at**: Timestamp update terakhir
- **deleted_by**: User ID yang menghapus record (FK ke users.id)
- **deleted_at**: Timestamp penghapusan (soft delete)
- **delete_reason**: Alasan penghapusan aset (min 20 karakter)

> **CATATAN PENTING**: Field audit menggunakan bahasa Inggris (`created_by`, `created_at`, dll) untuk konsistensi dengan SQLModel/SQLAlchemy conventions. Ini berbeda dengan field bisnis yang menggunakan Bahasa Indonesia.

#### Field User
- **dapat_ekspor**: Flag untuk izin export (boolean)

### Konsep Bisnis
- **Soft_Delete**: Penghapusan aset dengan status "Dihapus", data tidak benar-benar dihapus
- **Valid_Aset**: Aset dengan status "Aktif" atau "Rusak"
- **Session**: User authentication session dengan timeout 2 jam

### Konvensi Penamaan Kode
- **Database fields**: snake_case Bahasa Indonesia (contoh: `nomor_register`, `tahun_perolehan`)
- **Class names**: PascalCase English (contoh: `AssetService`, `MutationRepository`)
- **Function names**: snake_case English untuk Python, PascalCase untuk C# (contoh: `get_asset_by_id()`, `GetAssetById()`)
- **API endpoints**: kebab-case English (contoh: `/api/v1/aset`, `/api/v1/mutasi`)
- **Enum values**: Bahasa Indonesia (contoh: "Aktif", "Rusak", "Dihapus")
- **UI messages**: Bahasa Indonesia (contoh: "Aset berhasil disimpan")
- **File output**: Bahasa Indonesia (contoh: `KIB_B_2026-01-10.xlsx`)

## Requirements

### Requirement 1: User Authentication

**User Story:** As a user, I want to login to the system with username and password, so that I can access features based on my role.

#### Acceptance Criteria

1. WHEN a user submits valid credentials, THE System SHALL create a session and grant access based on user role
2. WHEN a user submits invalid credentials, THE System SHALL reject login and display error message
3. WHEN a session exceeds 2 hours of inactivity, THE System SHALL terminate the session automatically
4. WHEN a user logs out, THE System SHALL destroy the session immediately

### Requirement 2: Asset Data Entry

**User Story:** As an Admin, I want to record new assets by selecting KIB category and filling required fields, so that asset data is stored digitally with automatic validation.

#### Acceptance Criteria

1. WHEN Admin selects a KIB category, THE System SHALL display category-specific required fields
2. WHEN Admin submits asset data with valid inputs, THE System SHALL generate unique nomor_register automatically
3. WHEN Admin submits asset data with valid inputs, THE System SHALL save asset with status "Baru"
4. WHEN Admin submits duplicate kode_barang, THE System SHALL reject submission and display existing asset information
5. WHEN Admin submits invalid field values, THE System SHALL display field-specific error messages
6. WHEN Admin submits tahun_perolehan greater than current year, THE System SHALL reject submission with error message
7. WHEN Admin submits harga less than or equal to zero, THE System SHALL reject submission with error message
8. WHEN Admin submits kode_barang not matching format XX.XX.XX.XXXX, THE System SHALL reject submission with error message

### Requirement 3: Asset Data Viewing

**User Story:** As a user (Admin/Viewer/Kepala_Sekolah), I want to view complete asset details including mutation history, so that I can verify asset information and track changes.

#### Acceptance Criteria

1. WHEN a user selects an asset, THE System SHALL display all asset fields and mutation history
2. WHEN Admin views asset details, THE System SHALL display Edit and Delete buttons
3. WHEN Viewer or Kepala_Sekolah views asset details, THE System SHALL hide Edit and Delete buttons
4. WHEN a user views asset with status "Mutasi", THE System SHALL display current mutation information
5. WHEN a user views asset with mutation history, THE System SHALL display history sorted by date descending

### Requirement 4: Asset Data Modification

**User Story:** As an Admin, I want to modify recorded asset data, so that asset information remains accurate and up-to-date.

#### Acceptance Criteria

1. WHEN Admin updates asset fields with valid values, THE System SHALL save changes and update timestamp
2. WHEN Admin updates kondisi to "Rusak Ringan" or "Rusak Berat", THE System SHALL automatically set status to "Rusak"
3. WHEN Admin updates kondisi to "Baik", THE System SHALL automatically set status to "Aktif"
4. WHEN Admin attempts to update asset with status "Mutasi", THE System SHALL prevent ruangan_id field modification
5. WHEN Admin updates kode_barang to existing value, THE System SHALL reject update with error message
6. THE System SHALL NOT allow modification of nomor_register field
7. THE System SHALL NOT allow modification of kategori_kib field

### Requirement 5: Asset Search

**User Story:** As a user (Admin/Viewer/Kepala_Sekolah), I want to search assets with various filters, so that I can find assets quickly (< 5 seconds).

#### Acceptance Criteria

1. WHEN a user submits search with keyword, THE System SHALL search in kode_barang and nama_barang fields case-insensitively
2. WHEN a user submits search with multiple filters, THE System SHALL apply AND logic between filters
3. WHEN a user submits search, THE System SHALL return results within 5 seconds
4. WHEN search returns more than 100 items, THE System SHALL paginate results with 100 items per page
5. WHEN Viewer submits search, THE System SHALL exclude assets with status "Dihapus" from results
6. WHEN Admin submits search, THE System SHALL include all statuses in results
7. WHEN search returns no results, THE System SHALL display helpful suggestions including: alternative keywords based on partial matches, suggestion to check spelling, suggestion to broaden filters, and link to browse all assets in selected category

### Requirement 6: Asset Deletion

**User Story:** As an Admin, I want to delete assets from active inventory with deletion reason, so that assets don't appear in KIB reports but data remains for audit.

#### Acceptance Criteria

1. WHEN Admin submits deletion with valid reason (min 20 characters), THE System SHALL set asset status to "Dihapus"
2. WHEN Admin attempts to delete asset with status "Mutasi", THE System SHALL reject deletion with error message
3. WHEN Admin submits deletion reason with less than 20 characters, THE System SHALL reject deletion with error message
4. WHEN asset status is "Dihapus", THE System SHALL exclude asset from KIB reports
5. WHEN asset status is "Dihapus", THE System SHALL exclude asset from active asset lists
6. WHEN asset status is "Dihapus", THE System SHALL preserve all asset data in database

### Requirement 7: KIB A Report Generation

**User Story:** As an Admin or Kepala_Sekolah, I want to generate KIB A (Tanah) report according to BPAD DKI Jakarta 14-column format, so that report can be used for submission to Education Department.

#### Acceptance Criteria

1. WHEN user generates KIB A report, THE System SHALL query assets with kategori_kib "A" and status "Aktif" or "Rusak"
2. WHEN user generates KIB A report, THE System SHALL complete generation within 10 seconds for 1000 assets
3. WHEN user generates KIB A report, THE System SHALL display 14 columns according to BPAD DKI Jakarta format:
   - Kolom 1: NO. URUT (no_urut, auto-increment)
   - Kolom 2: NAMA BARANG/JENIS BARANG (nama_barang)
   - Kolom 3: KODE BARANG (kode_barang)
   - Kolom 4: REGISTER (nomor_register)
   - Kolom 5: LUAS M² (luas_m2)
   - Kolom 6: TAHUN PENGADAAN (tahun_perolehan)
   - Kolom 7: LETAK/ALAMAT (alamat_lokasi)
   - Kolom 8: STATUS TANAH - HAK (status_hak_tanah)
   - Kolom 9: SERTIFIKAT - TANGGAL (tanggal_sertifikat, format DD/MM/YYYY)
   - Kolom 10: SERTIFIKAT - NOMOR (nomor_sertifikat)
   - Kolom 11: PENGGUNAAN (penggunaan)
   - Kolom 12: ASAL USUL (asal_usul)
   - Kolom 13: HARGA (harga, Rupiah penuh)
   - Kolom 14: KETERANGAN (keterangan)
4. WHEN user generates KIB A report, THE System SHALL display total count and total value at footer
5. WHEN user generates KIB A report with no matching data, THE System SHALL display "Tidak ada data" message

### Requirement 8: KIB B Report Generation

**User Story:** As an Admin or Kepala_Sekolah, I want to generate KIB B (Peralatan dan Mesin) report according to BPAD DKI Jakarta 18-column format, so that report can be used for submission to Education Department.

#### Acceptance Criteria

1. WHEN user generates KIB B report, THE System SHALL query assets with kategori_kib "B" and status "Aktif" or "Rusak"
2. WHEN user generates KIB B report, THE System SHALL complete generation within 10 seconds for 1000 assets
3. WHEN user generates KIB B report, THE System SHALL display 18 columns according to BPAD DKI Jakarta format:
   - Kolom 1: NO. (no_urut, auto-increment)
   - Kolom 2: KODE BARANG (kode_barang)
   - Kolom 3: REG. (nomor_register)
   - Kolom 4: JENIS BARANG (nama_barang)
   - Kolom 5: UKU-RAN (ukuran_cc)
   - Kolom 6: SATU-AN (satuan)
   - Kolom 7: TGL. OLEH (tanggal_perolehan, format DD/MM/YYYY)
   - Kolom 8: BA-HAN (bahan)
   - Kolom 9: MEREK (merk)
   - Kolom 10: TYPE (tipe)
   - Kolom 11: TGL. BPKB/DOK. (tanggal_dokumen, format DD/MM/YYYY)
   - Kolom 12: NO. CHASIS/RANGKA (nomor_rangka)
   - Kolom 13: NO. MESIN/PABRIK (nomor_mesin)
   - Kolom 14: NOMOR POLISI (nomor_polisi)
   - Kolom 15: ASAL OLEH (asal_usul)
   - Kolom 16: HARGA (Rp.) (harga, Rupiah penuh)
   - Kolom 17: KAPITALISASI (Rp.) (kapitalisasi)
   - Kolom 18: TOTAL (Rp.) (total_harga)
4. WHEN user generates KIB B report, THE System SHALL display total count and total value at footer
5. WHEN user generates KIB B report, THE System SHALL format all currency fields in Rupiah penuh (not ribuan)
6. WHEN user generates KIB B report for non-vehicle assets, THE System SHALL allow empty values for kolom 12-14 (nomor_rangka, nomor_mesin, nomor_polisi)

### Requirement 9: KIB C Report Generation

**User Story:** As an Admin or Kepala_Sekolah, I want to generate KIB C (Gedung dan Bangunan) report according to BPAD DKI Jakarta 17-column format, so that report can be used for submission to Education Department.

#### Acceptance Criteria

1. WHEN user generates KIB C report, THE System SHALL query assets with kategori_kib "C" and status "Aktif" or "Rusak"
2. WHEN user generates KIB C report, THE System SHALL complete generation within 10 seconds for 1000 assets
3. WHEN user generates KIB C report, THE System SHALL display 17 columns according to BPAD DKI Jakarta format:
   - Kolom 1: NO. URUT (no_urut, auto-increment)
   - Kolom 2: NAMA BARANG/JENIS BARANG (nama_barang)
   - Kolom 3: KODE BARANG (kode_barang)
   - Kolom 4: NOMOR REGISTER (nomor_register)
   - Kolom 5: KONDISI BANGUNAN (kondisi: B/KB/RB)
   - Kolom 6: KONSTRUKSI - BERTINGKAT (bertingkat: Ya/Tidak)
   - Kolom 7: KONSTRUKSI - BETON (beton: Ya/Tidak)
   - Kolom 8: LUAS LANTAI M² (luas_lantai_m2)
   - Kolom 9: LETAK/LOKASI ALAMAT (alamat_lokasi)
   - Kolom 10: DOKUMEN - TANGGAL (tanggal_dokumen, format DD/MM/YYYY)
   - Kolom 11: DOKUMEN - NOMOR (nomor_dokumen)
   - Kolom 12: LUAS TANAH M² (luas_tanah_m2)
   - Kolom 13: STATUS TANAH (status_tanah)
   - Kolom 14: NOMOR KODE TANAH (kode_tanah)
   - Kolom 15: ASAL USUL (asal_usul)
   - Kolom 16: HARGA (harga, Rupiah penuh)
   - Kolom 17: KETERANGAN (keterangan)
4. WHEN user generates KIB C report, THE System SHALL display total count and total value at footer

### Requirement 10: KIB D Report Generation

**User Story:** As an Admin or Kepala_Sekolah, I want to generate KIB D (Jalan, Irigasi, dan Jaringan) report according to BPAD DKI Jakarta 16-column format, so that report can be used for submission to Education Department.

#### Acceptance Criteria

1. WHEN user generates KIB D report, THE System SHALL query assets with kategori_kib "D" and status "Aktif" or "Rusak"
2. WHEN user generates KIB D report, THE System SHALL complete generation within 10 seconds for 1000 assets
3. WHEN user generates KIB D report, THE System SHALL display 16 columns according to BPAD DKI Jakarta format:
   - Kolom 1: NO. URUT (no_urut, auto-increment)
   - Kolom 2: NAMA BARANG/JENIS BARANG (nama_barang)
   - Kolom 3: KODE BARANG (kode_barang)
   - Kolom 4: NOMOR REGISTER (nomor_register)
   - Kolom 5: KONSTRUKSI (jenis_konstruksi)
   - Kolom 6: PANJANG KM (panjang_km)
   - Kolom 7: LEBAR M (lebar_m)
   - Kolom 8: LUAS M² (luas_m2)
   - Kolom 9: LETAK/ALAMAT (alamat_lokasi)
   - Kolom 10: DOKUMEN - TANGGAL (tanggal_dokumen, format DD/MM/YYYY)
   - Kolom 11: DOKUMEN - NOMOR (nomor_dokumen)
   - Kolom 12: STATUS TANAH (status_tanah)
   - Kolom 13: NOMOR KODE TANAH (kode_tanah)
   - Kolom 14: ASAL USUL (asal_usul)
   - Kolom 15: HARGA (harga, Rupiah penuh)
   - Kolom 16: KETERANGAN (keterangan)
4. WHEN user generates KIB D report, THE System SHALL display total count and total value at footer

### Requirement 11: KIB E Report Generation

**User Story:** As an Admin or Kepala_Sekolah, I want to generate KIB E (Aset Tetap Lainnya) report according to BPAD DKI Jakarta 16-column format, so that report can be used for submission to Education Department.

#### Acceptance Criteria

1. WHEN user generates KIB E report, THE System SHALL query assets with kategori_kib "E" and status "Aktif" or "Rusak"
2. WHEN user generates KIB E report, THE System SHALL complete generation within 10 seconds for 1000 assets
3. WHEN user generates KIB E report, THE System SHALL display 16 columns according to BPAD DKI Jakarta format:
   - Kolom 1: NO. URUT (no_urut, auto-increment)
   - Kolom 2: NAMA BARANG/JENIS BARANG (nama_barang)
   - Kolom 3: KODE BARANG (kode_barang)
   - Kolom 4: NOMOR REGISTER (nomor_register)
   - Kolom 5: BUKU - JUDUL/PENCIPTA (judul_pencipta)
   - Kolom 6: BUKU - SPESIFIKASI (spesifikasi_buku)
   - Kolom 7: BARANG BERCORAK - ASAL DAERAH (asal_daerah)
   - Kolom 8: BARANG BERCORAK - PENCIPTA (pencipta)
   - Kolom 9: BARANG BERCORAK - BAHAN (bahan)
   - Kolom 10: HEWAN/TERNAK - JENIS (jenis_hewan)
   - Kolom 11: HEWAN/TERNAK - UKURAN (ukuran_hewan)
   - Kolom 12: JUMLAH (jumlah)
   - Kolom 13: TAHUN CETAK/PEMBELIAN (tahun_perolehan)
   - Kolom 14: ASAL USUL (asal_usul)
   - Kolom 15: HARGA (harga, Rupiah penuh)
   - Kolom 16: KETERANGAN (keterangan)
4. WHEN user generates KIB E report, THE System SHALL display total count and total value at footer

### Requirement 12: KIB F Report Generation

**User Story:** As an Admin or Kepala_Sekolah, I want to generate KIB F (Konstruksi dalam Pengerjaan) report according to BPAD DKI Jakarta 12-column format, so that report can be used for submission to Education Department.

#### Acceptance Criteria

1. WHEN user generates KIB F report, THE System SHALL query assets with kategori_kib "F" and status "Aktif" or "Rusak"
2. WHEN user generates KIB F report, THE System SHALL complete generation within 10 seconds for 1000 assets
3. WHEN user generates KIB F report, THE System SHALL display 12 columns according to BPAD DKI Jakarta format:
   - Kolom 1: NO. URUT (no_urut, auto-increment)
   - Kolom 2: NAMA BARANG/JENIS BARANG (nama_barang)
   - Kolom 3: KODE BARANG (kode_barang)
   - Kolom 4: NOMOR REGISTER (nomor_register)
   - Kolom 5: BANGUNAN (jenis_bangunan)
   - Kolom 6: KONSTRUKSI - BERTINGKAT (bertingkat: Ya/Tidak)
   - Kolom 7: KONSTRUKSI - BETON (beton: Ya/Tidak)
   - Kolom 8: LUAS M² (luas_m2)
   - Kolom 9: LETAK/ALAMAT (alamat_lokasi)
   - Kolom 10: DOKUMEN - TANGGAL/NOMOR (info_dokumen)
   - Kolom 11: ASAL USUL (asal_usul)
   - Kolom 12: HARGA (harga, Rupiah penuh)
4. WHEN user generates KIB F report, THE System SHALL display total count and total value at footer
5. WHEN user generates KIB F report, THE System SHALL NOT display kondisi column (KIB F tidak memiliki kolom kondisi)

### Requirement 13: Excel Export

**User Story:** As an Admin or Kepala_Sekolah, I want to export KIB reports to Excel format, so that reports can be edited, printed, or submitted to Education Department.

#### Acceptance Criteria

1. WHEN user exports KIB report to Excel, THE System SHALL generate .xlsx file within 15 seconds for 1000 assets
2. WHEN user exports KIB report to Excel, THE System SHALL format file according to Permendagri 19/2016 template
3. WHEN user exports KIB report to Excel, THE System SHALL name file as "KIB_{kategori}_{tanggal}.xlsx"
4. WHEN user exports KIB report to Excel, THE System SHALL include header with school name and report title
5. WHEN user exports KIB report to Excel, THE System SHALL include footer with total count and value
6. WHEN user exports report with more than 10000 assets, THE System SHALL display warning message and recommend using date range filter to reduce data size

### Requirement 14: Asset Mutation Initiation

**User Story:** As an Admin, I want to initiate asset movement between rooms with reason, so that asset location changes are tracked with audit trail.

#### Acceptance Criteria

1. WHEN Admin submits mutation with valid data, THE System SHALL set asset status to "Mutasi"
2. WHEN Admin submits mutation with valid data, THE System SHALL create mutation record with status "Dalam Proses"
3. WHEN Admin attempts to mutate asset with status "Mutasi", THE System SHALL reject mutation with error message
4. WHEN Admin submits mutation with ruangan_tujuan same as current room, THE System SHALL reject mutation with error message
5. WHEN Admin submits mutation with alasan_mutasi less than 10 characters, THE System SHALL reject mutation with error message
6. WHEN Admin submits mutation with tanggal_mutasi in future, THE System SHALL reject mutation with error message

### Requirement 15: Asset Mutation Completion

**User Story:** As an Admin, I want to confirm mutation completion after asset arrives at destination, so that asset location is updated and mutation is finalized.

#### Acceptance Criteria

1. WHEN Admin confirms mutation completion, THE System SHALL update asset ruangan_id to ruangan_tujuan
2. WHEN Admin confirms mutation completion, THE System SHALL set asset status to "Aktif"
3. WHEN Admin confirms mutation completion, THE System SHALL set mutation status to "Selesai"
4. WHEN Admin confirms mutation completion, THE System SHALL record selesai_mutasi timestamp

### Requirement 16: Asset Mutation Cancellation

**User Story:** As an Admin, I want to cancel pending mutations with cancellation reason, so that asset remains in original location.

#### Acceptance Criteria

1. WHEN Admin cancels mutation with valid reason (min 10 characters), THE System SHALL set mutation status to "Dibatalkan"
2. WHEN Admin cancels mutation, THE System SHALL set asset status back to "Aktif"
3. WHEN Admin cancels mutation, THE System SHALL keep asset in ruangan_asal
4. WHEN Admin cancels mutation, THE System SHALL record alasan_pembatalan field

> **CATATAN**: Field pembatalan menggunakan `alasan_pembatalan` (bukan `alasan_batal` atau `dibatalkan_pada`). Timestamp pembatalan dapat dilihat dari `updated_at` pada record mutasi.

### Requirement 17: Room Inventory Report

**User Story:** As a user (Admin/Viewer/Kepala_Sekolah), I want to view inventory report per room (KIR), so that I can see all assets in specific location.

#### Acceptance Criteria

1. WHEN user generates KIR for a room, THE System SHALL display all Valid_Aset in that room
2. WHEN user generates KIR for a room, THE System SHALL display columns: kode_barang, nama_barang, kategori_kib, kondisi, harga
3. WHEN user generates KIR for a room, THE System SHALL display total count and total value for that room

### Requirement 18: User Management

**User Story:** As an Admin, I want to create and manage Viewer users, so that teachers can access the system with appropriate permissions.

#### Acceptance Criteria

1. WHEN Admin creates user with valid data, THE System SHALL save user with status "Aktif"
2. WHEN Admin creates user with duplicate username, THE System SHALL reject creation with error message
3. WHEN Admin creates user with password less than 8 characters, THE System SHALL reject creation with error message
4. WHEN Admin updates user data, THE System SHALL save changes and update updated_at timestamp
5. WHEN Admin deactivates user, THE System SHALL set user status to "Nonaktif"
6. THE System SHALL NOT allow Admin to delete themselves
7. THE System SHALL NOT allow Admin to change their own role
8. WHEN Admin creates Viewer user for Kepala_Sekolah, THE System SHALL allow setting dapat_ekspor flag to true
9. WHEN dapat_ekspor flag is true for Viewer user, THE System SHALL grant export permission equivalent to Kepala_Sekolah role

### Requirement 19: Role-Based Access Control

**User Story:** As the System, I want to enforce role-based permissions on all operations, so that users can only perform actions allowed by their role.

#### Acceptance Criteria

1. WHEN Admin performs any operation, THE System SHALL allow the operation
2. WHEN Viewer attempts CRUD operation on assets, THE System SHALL reject operation with error message
3. WHEN Viewer attempts to export reports, THE System SHALL reject operation with error message
4. WHEN Kepala_Sekolah attempts CRUD operation on assets, THE System SHALL reject operation with error message
5. WHEN Kepala_Sekolah attempts to export reports, THE System SHALL allow the operation
6. WHEN unauthenticated user attempts any operation, THE System SHALL reject operation with error message

### Requirement 20: Data Validation

**User Story:** As the System, I want to validate all input data according to business rules, so that data integrity is maintained.

#### Acceptance Criteria

1. WHEN user submits kode_barang, THE System SHALL validate format matches XX.XX.XX.XXXX pattern
2. WHEN user submits nama_barang, THE System SHALL validate length is between 3 and 200 characters
3. WHEN user submits tahun_perolehan, THE System SHALL validate value is between 1900 and current year
4. WHEN user submits harga, THE System SHALL validate value is positive and less than 999999999999
5. WHEN user submits luas_m2 for KIB A, C, D, or F, THE System SHALL validate value is positive
6. WHEN user submits satuan for KIB B, THE System SHALL validate field is not empty and is one of: BH/Unit/Set/Buah/Paket/Rim/Dus
7. WHEN user submits kondisi for KIB C, THE System SHALL validate value is one of: B/KB/RB
8. WHEN user submits tanggal_perolehan, THE System SHALL validate format is DD/MM/YYYY
9. WHEN user submits panjang_km for KIB D, THE System SHALL validate value is positive
10. WHEN user submits jumlah for KIB E, THE System SHALL validate value is positive integer

### Requirement 21: Audit Trail

**User Story:** As the System, I want to log all CRUD operations with user and timestamp, so that all changes can be audited.

#### Acceptance Criteria

1. WHEN user creates asset, THE System SHALL record created_by user ID and created_at timestamp
2. WHEN user updates asset, THE System SHALL record updated_by user ID and updated_at timestamp
3. WHEN user deletes asset, THE System SHALL record deleted_by user ID, deleted_at timestamp, and delete_reason
4. WHEN user performs mutation, THE System SHALL record user_id and timestamps in riwayat_mutasi table
5. THE System SHALL NOT allow modification or deletion of audit_trail records

> **CATATAN**: Field audit menggunakan bahasa Inggris (`created_by`, `created_at`, `updated_by`, `updated_at`, `deleted_by`, `deleted_at`, `delete_reason`) untuk konsistensi dengan SQLModel/SQLAlchemy conventions.

### Requirement 22: Performance Requirements

**User Story:** As a user, I want the system to respond quickly, so that I can work efficiently.

#### Acceptance Criteria

1. WHEN user performs asset search, THE System SHALL return results within 5 seconds
2. WHEN user generates KIB report, THE System SHALL complete generation within 10 seconds for 1000 assets
3. WHEN user exports to Excel, THE System SHALL generate file within 15 seconds for 1000 assets
4. WHEN user logs in with valid credentials, THE System SHALL complete authentication within 2 seconds
5. WHEN user views asset details, THE System SHALL load data within 2 seconds

### Requirement 23: Data Persistence

**User Story:** As the System, I want to store all data in SQLite database with WAL mode, so that data is persisted reliably with concurrent access support.

#### Acceptance Criteria

1. THE System SHALL use SQLite database with WAL mode enabled
2. THE System SHALL store database file at C:\ProgramData\Simanis62\simanis62.db
3. WHEN multiple users access database concurrently, THE System SHALL handle concurrent reads without blocking
4. WHEN database operation fails, THE System SHALL rollback transaction and display error message
5. THE System SHALL create automatic backup daily and retain 7 days of backups

#### Development Tools

**DBHub Integration:**
- DBHub SHALL be used during development for database management and debugging
- DBHub provides visual interface for exploring database schema and testing queries
- DBHub configuration in `dbhub.toml` with 3 database sources: development, testing, production
- DBHub available as MCP server in Kiro for database operations
- See `.kiro/steering/DBHUB_GUIDE.md` for complete setup and usage guide

### Requirement 24: Session Management

**User Story:** As the System, I want to manage user sessions securely, so that unauthorized access is prevented.

#### Acceptance Criteria

1. WHEN user logs in successfully, THE System SHALL create session with 2-hour timeout
2. WHEN session exceeds timeout, THE System SHALL terminate session automatically
3. WHEN user logs out, THE System SHALL destroy session immediately
4. THE System SHALL use HttpOnly cookies for session management
5. THE System SHALL NOT expose session tokens in URLs or logs
