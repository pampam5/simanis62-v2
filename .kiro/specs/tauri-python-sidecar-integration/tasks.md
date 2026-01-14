# Rencana Implementasi: Integrasi Tauri Python Sidecar SIMANIS62 V2

## Gambaran Umum

Dokumen ini berisi checklist implementasi untuk mengintegrasikan backend FastAPI Python sebagai sidecar dalam aplikasi desktop Tauri SIMANIS62. Implementasi mencakup schema database 11 tabel, KIB B export 18 kolom BPAD DKI Jakarta, dan fitur mutasi aset.

**Referensi:**
- #[[file:.kiro/specs/tauri-python-sidecar-integration/requirements.md]]
- #[[file:.kiro/specs/tauri-python-sidecar-integration/design.md]]
- #[[file:docs/data_schema.md]]
- #[[file:docs/format_kib_spesifikasi.md]]

## Tasks

- [x] 1. Setup Infrastruktur Proyek
  - Persiapan folder dan konfigurasi dasar
  - _Requirements: 2.1, 5.1_

  - [x] 1.1 Buat folder struktur untuk sidecar
    - Buat folder `frontend-tauri/src-tauri/bin/api/`
    - Tambahkan `.gitkeep` untuk memastikan folder ter-track
    - _Requirements: 2.1_

  - [x] 1.2 Update .gitignore untuk sidecar executables
    - Tambahkan pattern untuk ignore compiled sidecar (`*.exe` di bin/api)
    - Pastikan source code tetap ter-track
    - _Requirements: 2.1_

- [x] 2. Backend Database Schema (11 Tabel)
  - Implementasi schema database lengkap sesuai docs/data_schema.md
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_
  - **STATUS: SUDAH ADA** - Semua model sudah diimplementasi sebelumnya

  - [x] 2.1 Implementasi model User dengan dapat_ekspor
    - `backend/app/models/user.py` dengan 9 kolom ✅
    - Field `dapat_ekspor` untuk implementasi Kepala Sekolah ✅
    - _Requirements: 8.5_

  - [x] 2.2 Implementasi model Ruangan
    - `backend/app/models/ruangan.py` dengan 6 kolom ✅
    - _Requirements: 8.1_

  - [x] 2.3 Implementasi model Aset (main table)
    - `backend/app/models/aset.py` dengan 19 kolom ✅
    - Soft-delete fields (deleted_at, delete_reason) ✅
    - _Requirements: 8.1, 8.3_

  - [x] 2.4 Implementasi model AsetKibB (extension table)
    - `backend/app/models/aset_kib.py` dengan semua 6 KIB tables (A-F) ✅
    - One-to-one relationship dengan Aset ✅
    - _Requirements: 8.1, 8.4_

  - [x] 2.5 Implementasi model RiwayatMutasi
    - `backend/app/models/mutasi.py` dengan 12 kolom ✅
    - _Requirements: 8.1_

  - [x] 2.6 Implementasi model AuditTrail
    - `backend/app/models/audit.py` dengan 9 kolom ✅
    - Operation enum (CREATE/UPDATE/DELETE) ✅
    - _Requirements: 8.1, 8.6_

  - [ ]* 2.7 Write property test untuk KIB B data integrity
    - **Property 8: KIB B Data Integrity**
    - **Validates: Requirements 8.2, 8.4**

- [-] 3. Backend PyInstaller Compatibility
  - Modifikasi backend agar kompatibel dengan PyInstaller
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 3.1 Modifikasi config.py untuk frozen path handling
    - Tambahkan fungsi `is_frozen()` ✅
    - Tambahkan fungsi `get_base_path()` ✅
    - Tambahkan fungsi `get_data_directory()` ✅
    - Update `DATABASE_PATH` property untuk handle frozen mode ✅
    - Update `LOG_DIR` property untuk handle frozen mode ✅
    - _Requirements: 1.2, 1.3, 1.4_

  - [x] 3.2 Modifikasi main.py dengan lifespan context manager
    - Lifespan context manager sudah ada ✅
    - Tambahkan `multiprocessing.freeze_support()` ✅
    - Tambahkan `uvicorn.run()` dengan konfigurasi production ✅
    - _Requirements: 1.5, 1.6_

  - [x] 3.3 Buat build script PyInstaller
    - Buat file `backend/build_sidecar.py` ✅
    - Implementasi fungsi `get_target_triple()` ✅
    - Implementasi fungsi `build_sidecar()` ✅
    - _Requirements: 1.1_

- [x] 3.4 Test build sidecar executable ✅
    - Build berhasil: 20.8 MB
    - Executable berjalan standalone
    - Database auto-create di C:\ProgramData\Simanis62\
    - _Requirements: 1.1, 1.5_

  - [ ]* 3.5 Write property test untuk frozen detection
    - **Property 1: Deteksi Mode Frozen**
    - **Validates: Requirements 1.2**

  - [ ]* 3.6 Write property test untuk database path
    - **Property 2: Database Path Writable**
    - **Validates: Requirements 1.4**

- [x] 4. Checkpoint - Verifikasi Backend Sidecar ✅ PASSED
  - **Build**: 20.8 MB executable berhasil dibuat
  - **Runtime**: Sidecar berjalan dengan benar
  - **Frozen Detection**: ✅ Paths ke C:\ProgramData\Simanis62\
  - **Database**: ✅ Auto-create 11 tabel dengan WAL mode
  - **Lifespan**: ✅ Startup/shutdown events bekerja
  - **Port Conflict**: Normal (proses lain masih running)

- [x] 5. Tauri Sidecar Configuration
  - Konfigurasi Tauri untuk spawn dan manage sidecar
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x] 5.1 Update tauri.conf.json dengan externalBin
    - Tambahkan `bundle.externalBin` configuration ✅
    - Tambahkan `plugins.shell` configuration ✅
    - _Requirements: 2.1_

  - [x] 5.2 Update Cargo.toml dengan dependencies
    - Tambahkan `tauri-plugin-shell` ✅
    - Tambahkan `tokio` untuk async runtime ✅
    - Tambahkan `reqwest` untuk health check ✅
    - Tambahkan `thiserror` untuk error handling ✅
    - _Requirements: 2.2_

  - [x] 5.3 Implementasi sidecar manager di lib.rs
    - Buat `src/sidecar.rs` dengan spawn, health check, shutdown ✅
    - Implementasi spawn sidecar on startup ✅
    - Implementasi logging untuk sidecar output ✅
    - Implementasi graceful shutdown ✅
    - _Requirements: 2.2, 2.3, 2.4_

  - [x] 5.4 Implementasi health check command
    - Buat Tauri command `check_backend_ready` ✅
    - Implementasi polling untuk wait backend ready ✅
    - _Requirements: 2.3_

  - [x] 5.5 Implementasi error handling untuk sidecar
    - Buat error types di `src/error.rs` ✅
    - Implementasi user-friendly error messages dalam Bahasa Indonesia ✅
    - _Requirements: 2.5_

  - [ ]* 5.6 Write property test untuk sidecar lifecycle
    - **Property 3: Sidecar Lifecycle Management**
    - **Validates: Requirements 2.2, 2.3, 2.4**

- [ ] 6. Checkpoint - Verifikasi Tauri Sidecar (MANUAL)
  - Jalankan `bun tauri dev` dan verifikasi sidecar auto-start
  - Verifikasi sidecar shutdown saat app close
  - Tanyakan user jika ada pertanyaan

- [x] 7. Frontend API Service Layer ✅
  - Buat abstraksi untuk komunikasi dengan backend
  - _Requirements: 3.1, 3.2, 3.3, 3.7_

  - [x] 7.1 Buat base API client ✅
    - Buat file `frontend-tauri/src/services/api.ts`
    - Implementasi class `ApiClient` dengan methods GET, POST, PUT, DELETE
    - Implementasi timeout dan error handling
    - _Requirements: 3.1, 3.2_

  - [x] 7.2 Buat TypeScript types (11 tabel) ✅
    - Buat file `frontend-tauri/src/services/types.ts`
    - Definisikan interfaces untuk semua 11 tabel database
    - Tambahkan KibBExportRow untuk 18 kolom BPAD
    - _Requirements: 3.3_

  - [x] 7.3 Buat Aset service ✅
    - Buat file `frontend-tauri/src/services/aset-service.ts`
    - Implementasi methods: getAll, getById, create, update, delete, search, getStats
    - _Requirements: 3.7_

  - [x] 7.4 Buat KIB B service ✅
    - Buat file `frontend-tauri/src/services/kib-service.ts`
    - Implementasi methods: getKibBData, exportKibB, downloadKibB
    - _Requirements: 3.7, 9.1_

  - [x] 7.5 Buat Mutasi service ✅
    - Buat file `frontend-tauri/src/services/mutasi-service.ts`
    - Implementasi methods: getAll, create, selesaikan, batalkan
    - _Requirements: 3.7, 10.1_

  - [x] 7.6 Buat Ruangan service ✅
    - Buat file `frontend-tauri/src/services/ruangan-service.ts`
    - Implementasi methods: getAll, getById, create, update, delete
    - _Requirements: 3.7_

  - [x] 7.7 Buat Auth service ✅
    - Buat file `frontend-tauri/src/services/auth-service.ts`
    - Implementasi methods: login, logout, getCurrentUser
    - _Requirements: 3.7_

  - [x] 7.8 Buat error handler utility ✅
    - Buat file `frontend-tauri/src/services/error-handler.ts`
    - Implementasi fungsi `handleApiError` dengan pesan Bahasa Indonesia
    - _Requirements: 3.2, 3.6_

  - [ ]* 7.9 Write property test untuk API error handling
    - **Property 4: API Error Handling Consistency**
    - **Validates: Requirements 3.2**

- [x] 8. Checkpoint - Verifikasi API Service Layer ✅ PASSED
  - ✅ TypeScript check passed (bun run check)
  - ✅ Semua 9 service files tidak ada diagnostic errors
  - ✅ Semua exports bisa di-import dengan benar
  - ✅ Type definitions lengkap (11 tabel + API types + KibBExportRow 18 kolom)


- [x] 9. Backend KIB B Export Service ✅
  - Implementasi export KIB B dengan 18 kolom BPAD DKI Jakarta
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_

  - [x] 9.1 Buat KIB B repository ✅
    - File: `backend/app/repositories/kib_repository.py`
    - Query join aset + aset_kib_b dengan filter status "Aktif"
    - Methods: get_kib_b_data, get_kib_b_export_data, count_kib_b, get_total_nilai_kib_b
    - _Requirements: 9.5_

  - [x] 9.2 Buat KIB B service ✅
    - Transformasi data ke format 18 kolom di repository._to_export_row()
    - Format harga dalam Rupiah penuh
    - Format tanggal dalam DD/MM/YYYY
    - _Requirements: 9.2, 9.3, 9.4_

  - [x] 9.3 Buat KIB B export endpoint ✅
    - File: `backend/app/api/v1/reports.py`
    - GET /api/v1/reports/kib/b - Data dengan pagination
    - GET /api/v1/reports/kib/b/metadata - Preview metadata
    - GET /api/v1/reports/export/kib-b - Download Excel
    - GET /api/v1/reports/can-export - Check permission
    - _Requirements: 9.1_

  - [x] 9.4 Implementasi authorization untuk export ✅
    - ExportUser dependency: Admin atau Viewer dengan dapat_ekspor=true
    - Return 403 jika tidak diizinkan
    - _Requirements: 9.7_

  - [x] 9.5 Implementasi Excel export dengan openpyxl ✅
    - Generate file Excel dengan header BPAD DKI Jakarta
    - Include metadata (PROVINSI, UNIT ORGANISASI, dll)
    - 18 kolom dengan styling dan footer totals
    - _Requirements: 9.1, 9.2_

  - [ ]* 9.6 Write property test untuk KIB B export format
    - **Property 9: KIB B Export Format Compliance**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

  - [ ]* 9.7 Write property test untuk export authorization
    - **Property 12: Export Authorization**
    - **Validates: Requirements 9.7**

- [x] 10. Checkpoint - Verifikasi KIB B Export ✅
  - ✅ Export endpoint: GET /api/v1/reports/export/kib-b
  - ✅ Format 18 kolom sesuai BPAD DKI Jakarta
  - ✅ Authorization dengan ExportUser (Admin atau Viewer dengan dapat_ekspor=true)
  - ✅ Harga dalam Rupiah penuh, tanggal DD/MM/YYYY
  - ✅ Footer dengan total nilai

- [x] 11. Backend Mutasi Service ✅
  - Implementasi workflow mutasi aset
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_
  - **STATUS: SUDAH ADA** - Service dan endpoints sudah diimplementasi sebelumnya

  - [x] 11.1 Buat Mutasi repository ✅
    - File: `backend/app/repositories/mutasi_repository.py` (sudah ada)
    - CRUD untuk riwayat_mutasi
    - _Requirements: 10.2_

  - [x] 11.2 Buat Mutasi service dengan state machine ✅
    - File: `backend/app/services/mutasi_service.py` (sudah ada)
    - create_mutasi (status aset -> "Mutasi")
    - selesaikan_mutasi (status aset -> "Aktif", update ruangan)
    - batalkan_mutasi (status aset -> "Aktif")
    - _Requirements: 10.1, 10.3, 10.4_

  - [x] 11.3 Implementasi validasi mutasi ✅
    - Cek status aset harus "Aktif" sebelum mutasi
    - Cek tidak ada mutasi pending untuk aset yang sama
    - _Requirements: 10.5, 10.6_

  - [x] 11.4 Buat Mutasi endpoints ✅
    - File: `backend/app/api/v1/mutasi.py`
    - GET /api/v1/mutasi - list all mutasi (added)
    - POST /api/v1/mutasi - create mutasi
    - GET /api/v1/mutasi/{id} - get by ID
    - PUT /api/v1/mutasi/{id}/complete - selesaikan mutasi
    - PUT /api/v1/mutasi/{id}/cancel - batalkan mutasi (with MutasiCancelRequest body)
    - _Requirements: 10.1, 10.3, 10.4_

  - [ ]* 11.5 Write property test untuk mutasi state machine
    - **Property 10: Mutasi State Machine**
    - **Validates: Requirements 10.1, 10.3, 10.4, 10.5**

- [x] 12. Backend Audit Trail Service
  - Implementasi logging semua operasi CRUD
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [x] 12.1 Buat Audit Trail repository ✅
    - File `backend/app/repositories/audit_repository.py` sudah ada
    - Implementasi create_audit_log via `log_operation` method
    - _Requirements: 11.4_

  - [x] 12.2 Implementasi audit middleware/decorator ✅
    - File `backend/app/services/audit_service.py` sudah ada
    - Decorator `audit_operation` tersedia untuk auto-log
    - _Requirements: 11.1, 11.2, 11.3_

  - [x] 12.3 Integrasi audit ke semua service ✅
    - AsetService: audit logging di create_asset, update_asset, delete_asset
    - MutasiService: audit logging di initiate_mutation, complete_mutation, cancel_mutation
    - _Requirements: 11.1, 11.2, 11.3_

  - [ ]* 12.4 Write property test untuk audit trail
    - **Property 11: Audit Trail Completeness**
    - **Validates: Requirements 11.1, 11.2, 11.3, 11.4**

- [x] 13. Checkpoint - Verifikasi Backend Services ✅
  - ✅ Backend berjalan di http://127.0.0.1:8000
  - ✅ Swagger UI tersedia di /docs
  - ✅ Mutasi workflow: initiate → complete/cancel
  - ✅ Audit trail terintegrasi di AsetService dan MutasiService
  - ✅ State machine: Aktif → Mutasi → Aktif (complete) atau Aktif (cancel)

- [ ] 14. Integrasi Halaman dengan Backend
  - Connect semua halaman ke data nyata dari backend
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [x] 14.1 Integrasi DashboardPage ✅
    - Fetch statistik dari backend (total, kondisi, nilai)
    - Fetch aset terbaru dari backend
    - Implementasi loading state dan error handling
    - Backend endpoints: GET /aset/stats, GET /aset/recent
    - _Requirements: 4.1, 3.5_

  - [x] 14.2 Integrasi AssetsPage dengan pagination ✅
    - Fetch daftar aset dengan pagination (20 per page)
    - Implementasi pagination controls (prev/next)
    - Loading state dan error handling
    - _Requirements: 4.2, 3.5_

  - [x] 14.3 Integrasi search functionality ✅
    - Connect search input ke backend search endpoint
    - Search on Enter key atau button click
    - _Requirements: 4.3_

  - [x] 14.4 Integrasi form tambah aset KIB B ✅
    - ✅ Komponen AsetForm di frontend-tauri/src/components/forms/aset-form.tsx
    - ✅ Form dengan field: kode_barang, nama_barang, kategori_kib, tahun, ruangan, harga, kondisi
    - ✅ Validasi client-side
    - _Requirements: 4.4_

  - [x] 14.5 Integrasi form edit aset ✅
    - ✅ AsetForm mendukung mode edit (prop aset)
    - ✅ Field yang tidak bisa diubah: kode_barang, kategori_kib, tahun_perolehan
    - ✅ Field yang bisa diubah: nama_barang, kondisi, ruangan, harga, keterangan
    - _Requirements: 4.5_

  - [x] 14.6 Integrasi delete aset dengan validasi ✅
    - ✅ Komponen DeleteConfirmDialog di frontend-tauri/src/components/forms/delete-confirm-dialog.tsx
    - ✅ Validasi alasan minimal 20 karakter
    - ✅ Soft-delete via asetService.delete()
    - _Requirements: 4.6_

  - [x] 14.7 Integrasi halaman mutasi ✅
    - ✅ MutationPage dengan list mutasi dan status badges
    - ✅ Form create mutasi dengan validasi alasan min 10 char
    - ✅ Buttons selesaikan/batalkan dengan konfirmasi
    - ✅ Status: DALAM_PROSES, SELESAI, DIBATALKAN
    - _Requirements: 10.1, 10.3, 10.4_

  - [x] 14.8 Integrasi halaman export KIB B ✅
    - ✅ KIBPage dengan filter ruangan, tahun, kondisi
    - ✅ Preview data (10 baris pertama)
    - ✅ Summary: total aset, total nilai
    - ✅ Download button dengan authorization check
    - _Requirements: 9.1, 9.7_

  - [ ]* 14.9 Write property test untuk pagination
    - **Property 5: Pagination Consistency**
    - **Validates: Requirements 4.2**

  - [ ]* 14.10 Write property test untuk search
    - **Property 6: Search Performance**
    - **Validates: Requirements 4.3**

  - [ ]* 14.11 Write property test untuk soft delete
    - **Property 7: Soft Delete Validation**
    - **Validates: Requirements 4.6**

- [ ] 15. Checkpoint - Verifikasi Integrasi Halaman
  - Test semua halaman dengan data nyata
  - Verifikasi CRUD operations berfungsi
  - Verifikasi export KIB B berfungsi
  - Tanyakan user jika ada pertanyaan

- [ ] 16. Build dan Packaging
  - Setup build pipeline untuk production
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [ ] 16.1 Update package.json dengan build scripts
    - Tambahkan script `build:sidecar`
    - Tambahkan script `build:all`
    - _Requirements: 5.1, 5.2_

  - [ ] 16.2 Konfigurasi Tauri bundler
    - Setup NSIS installer configuration
    - Konfigurasi WebView2 bootstrapper
    - Setup icon dan metadata
    - _Requirements: 5.3, 5.6_

  - [ ] 16.3 Build production installer
    - Jalankan `bun tauri build`
    - Verifikasi installer dibuat di folder dist
    - Verifikasi ukuran < 200MB
    - _Requirements: 5.3, 6.1_

  - [ ] 16.4 Test instalasi di clean Windows
    - Install di VM atau komputer lain
    - Verifikasi aplikasi berjalan tanpa dependencies tambahan
    - Verifikasi database dibuat otomatis dengan 11 tabel
    - _Requirements: 5.4, 5.5, 5.7_

- [ ] 17. Checkpoint - Verifikasi Build
  - Test installer di berbagai kondisi
  - Verifikasi ukuran installer < 200MB
  - Tanyakan user jika ada pertanyaan

- [ ] 18. Testing dengan Playwright
  - Setup dan jalankan E2E tests
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ] 18.1 Setup Playwright configuration
    - Install Playwright dependencies
    - Buat `playwright.config.ts`
    - _Requirements: 7.1_

  - [ ] 18.2 Buat test untuk Dashboard
    - Test loading statistics
    - Test loading recent assets
    - _Requirements: 7.3_

  - [ ] 18.3 Buat test untuk Assets page
    - Test list assets dengan pagination
    - Test search
    - Test CRUD operations
    - _Requirements: 7.3, 7.4_

  - [ ] 18.4 Buat test untuk KIB B export
    - Test export dengan Admin
    - Test export ditolak untuk Viewer tanpa dapat_ekspor
    - _Requirements: 7.4_

  - [ ] 18.5 Buat test untuk Mutasi
    - Test create mutasi
    - Test selesaikan mutasi
    - Test batalkan mutasi
    - _Requirements: 7.4_

  - [ ] 18.6 Jalankan test suite dan generate report
    - Jalankan semua tests
    - Generate HTML report
    - _Requirements: 7.5_

- [ ] 19. Final Checkpoint
  - Verifikasi semua tests passing
  - Verifikasi aplikasi siap distribusi via flashdisk
  - Dokumentasi untuk user

## Catatan

- Tasks dengan `*` adalah property-based tests (opsional untuk MVP cepat)
- Setiap checkpoint adalah kesempatan untuk review dan feedback
- Estimasi waktu: 16-20 hari kerja (dengan semua tests)
- Prioritas: Phase 1-3 (Backend + Sidecar + Services) harus selesai sebelum Phase 4-5
- Property-based tests memastikan kualitas dan kebenaran implementasi
- Semua pesan error dan UI dalam Bahasa Indonesia
