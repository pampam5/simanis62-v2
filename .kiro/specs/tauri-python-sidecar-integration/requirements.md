# Dokumen Kebutuhan - Integrasi Tauri Python Sidecar SIMANIS62 V2

## Pendahuluan

Dokumen ini mendefinisikan kebutuhan untuk mengintegrasikan backend FastAPI Python sebagai sidecar dalam aplikasi desktop Tauri SIMANIS62. Tujuan utama adalah membuat aplikasi yang dapat didistribusikan via flashdisk dan dijalankan dengan double-click tanpa perlu instalasi dependencies tambahan.

**Referensi Dokumentasi:**
- `docs/data_schema.md` - Schema database 11 tabel
- `docs/format_kib_spesifikasi.md` - Format KIB B 18 kolom BPAD DKI Jakarta
- `docs/api_contract.md` - API endpoints lengkap
- `docs/Alur Kerja_Aturan Main.md` - Business rules

## Glosarium

- **Sidecar**: Proses eksternal (executable) yang di-bundle dan dijalankan oleh Tauri secara otomatis
- **PyInstaller**: Tool Python untuk mengompilasi aplikasi Python menjadi single executable
- **Frozen_App**: Aplikasi Python yang sudah di-bundle ke format .exe oleh PyInstaller
- **sys._MEIPASS**: Path ke folder temporary dimana PyInstaller mengekstrak file saat runtime
- **Target_Triple**: Identifier platform untuk executable (contoh: x86_64-pc-windows-msvc)
- **API_Service_Layer**: Abstraksi TypeScript untuk komunikasi frontend dengan backend API
- **Lifespan_Manager**: Komponen yang mengelola startup dan shutdown backend
- **KIB_B**: Kartu Inventaris Barang kategori B (Peralatan dan Mesin) dengan 18 kolom format BPAD DKI Jakarta
- **BPAD_DKI_Jakarta**: Badan Pengelolaan Aset Daerah DKI Jakarta - otoritas format KIB
- **Audit_Trail**: Log lengkap semua operasi CRUD untuk keperluan audit

## Kebutuhan

### Kebutuhan 1: Kompatibilitas Backend dengan PyInstaller

**User Story:** Sebagai developer, saya ingin backend FastAPI dapat dikompilasi menjadi single executable, sehingga dapat di-bundle sebagai sidecar Tauri.

#### Kriteria Penerimaan

1. WHEN backend di-compile dengan PyInstaller, THEN Frozen_App SHALL menghasilkan single file executable yang dapat dijalankan standalone
2. WHEN Frozen_App dijalankan, THEN Frozen_App SHALL mendeteksi apakah berjalan dalam mode frozen atau development
3. WHEN Frozen_App berjalan dalam mode frozen, THEN Frozen_App SHALL menggunakan sys._MEIPASS untuk mengakses file bundled
4. WHEN Frozen_App membutuhkan database, THEN Frozen_App SHALL menyimpan database di lokasi writable (C:\ProgramData\Simanis62\)
5. WHEN Frozen_App dijalankan, THEN Frozen_App SHALL menjalankan uvicorn server secara embedded menggunakan lifespan context manager
6. WHEN Frozen_App dijalankan di Windows, THEN Frozen_App SHALL mendukung multiprocessing.freeze_support()

### Kebutuhan 2: Konfigurasi Tauri Sidecar

**User Story:** Sebagai developer, saya ingin Tauri dapat menjalankan backend Python sebagai sidecar, sehingga backend otomatis start saat aplikasi dibuka.

#### Kriteria Penerimaan

1. WHEN aplikasi Tauri di-build, THEN Tauri_Builder SHALL menyertakan sidecar executable dalam bundle via externalBin configuration
2. WHEN aplikasi Tauri dijalankan, THEN Tauri_App SHALL spawn sidecar process menggunakan tauri-plugin-shell
3. WHEN sidecar berhasil start, THEN Tauri_App SHALL menunggu hingga backend ready (health check) sebelum menampilkan UI
4. WHEN aplikasi Tauri ditutup, THEN Tauri_App SHALL menghentikan sidecar process dengan graceful shutdown
5. IF sidecar gagal start, THEN Tauri_App SHALL menampilkan pesan error yang informatif kepada user
6. WHEN sidecar berjalan, THEN Sidecar SHALL listen pada port yang dikonfigurasi (default: 8000)

### Kebutuhan 3: API Service Layer Frontend

**User Story:** Sebagai developer, saya ingin frontend React memiliki service layer yang type-safe untuk berkomunikasi dengan backend, sehingga semua halaman dapat terhubung ke data nyata.

#### Kriteria Penerimaan

1. THE API_Service_Layer SHALL menyediakan base client dengan konfigurasi default (baseURL, headers, timeout)
2. WHEN API_Service_Layer melakukan request, THEN API_Service_Layer SHALL menangani error secara konsisten dengan format {message, code, details}
3. THE API_Service_Layer SHALL menyediakan TypeScript types yang sesuai dengan schema backend (11 tabel)
4. WHEN halaman membutuhkan data, THEN Halaman SHALL menggunakan API_Service_Layer (bukan fetch langsung)
5. WHEN API request sedang berjalan, THEN UI SHALL menampilkan loading state
6. IF API request gagal, THEN UI SHALL menampilkan error message yang user-friendly dalam Bahasa Indonesia
7. THE API_Service_Layer SHALL menyediakan service untuk setiap resource (Aset, Ruangan, Mutasi, User, Auth, KIB, Report)

### Kebutuhan 4: Integrasi Halaman dengan Backend

**User Story:** Sebagai user, saya ingin semua halaman menampilkan data nyata dari database, sehingga saya dapat mengelola aset sekolah.

#### Kriteria Penerimaan

1. WHEN DashboardPage dimuat, THEN DashboardPage SHALL menampilkan statistik aset dari backend (total, kondisi, nilai)
2. WHEN AssetsPage dimuat, THEN AssetsPage SHALL menampilkan daftar aset dari backend dengan pagination (default 20 per page)
3. WHEN user mencari aset, THEN SearchComponent SHALL mengirim query ke backend dan menampilkan hasil dalam < 5 detik
4. WHEN user menambah aset baru, THEN FormComponent SHALL mengirim data ke backend dan menampilkan konfirmasi
5. WHEN user mengedit aset, THEN FormComponent SHALL mengupdate data di backend dan menampilkan konfirmasi
6. WHEN user menghapus aset, THEN UI SHALL meminta konfirmasi dengan alasan (min 20 karakter) dan soft-delete di backend
7. WHEN data berubah di backend, THEN UI SHALL memperbarui tampilan secara otomatis

### Kebutuhan 5: Build dan Packaging

**User Story:** Sebagai developer, saya ingin proses build menghasilkan installer yang siap distribusi, sehingga user dapat menginstall aplikasi dengan mudah.

#### Kriteria Penerimaan

1. WHEN developer menjalankan build command, THEN Build_System SHALL mengompilasi sidecar terlebih dahulu dengan PyInstaller
2. WHEN developer menjalankan build command, THEN Build_System SHALL mengompilasi frontend Tauri dengan NSIS installer
3. WHEN build selesai, THEN Build_System SHALL menghasilkan installer (.exe) di folder dist dengan ukuran < 200MB
4. WHEN user menjalankan installer, THEN Installer SHALL menginstall aplikasi tanpa memerlukan dependencies tambahan
5. WHEN aplikasi terinstall, THEN Aplikasi SHALL dapat dijalankan dengan double-click
6. THE Installer SHALL menyertakan WebView2 runtime jika belum terinstall di sistem user
7. WHEN aplikasi dijalankan pertama kali, THEN Aplikasi SHALL membuat database baru dengan schema 11 tabel jika belum ada

### Kebutuhan 6: Distribusi via Flashdisk

**User Story:** Sebagai user, saya ingin dapat mengcopy aplikasi ke flashdisk dan menjalankannya di komputer lain, sehingga mudah untuk distribusi offline.

#### Kriteria Penerimaan

1. THE Installer SHALL berukuran maksimal 200MB untuk kemudahan distribusi via flashdisk
2. WHEN installer di-copy ke flashdisk, THEN Installer SHALL tetap dapat dijalankan dari flashdisk
3. WHEN aplikasi diinstall dari flashdisk, THEN Aplikasi SHALL berfungsi normal
4. THE Aplikasi SHALL tidak memerlukan koneksi internet untuk berfungsi (offline-first)
5. WHEN database perlu di-backup, THEN User SHALL dapat mengcopy file database ke lokasi lain

### Kebutuhan 7: Testing dengan Playwright

**User Story:** Sebagai developer, saya ingin dapat menguji UI aplikasi dengan Playwright, sehingga dapat memastikan semua fitur berfungsi dengan benar.

#### Kriteria Penerimaan

1. WHEN frontend berjalan di mode development (localhost:1420), THEN Playwright SHALL dapat mengakses aplikasi
2. WHEN backend berjalan di mode development, THEN Playwright SHALL dapat menguji flow lengkap dengan data nyata
3. THE Test_Suite SHALL mencakup test untuk setiap halaman utama (Dashboard, Assets, Rooms, Mutations)
4. THE Test_Suite SHALL mencakup test untuk CRUD operations
5. WHEN test dijalankan, THEN Test_Suite SHALL menghasilkan report yang jelas

### Kebutuhan 8: Database Schema Lengkap (11 Tabel)

**User Story:** Sebagai developer, saya ingin database memiliki schema lengkap sesuai dokumentasi, sehingga semua fitur dapat diimplementasikan dengan benar.

#### Kriteria Penerimaan

1. THE Database SHALL memiliki 11 tabel sesuai docs/data_schema.md: users, ruangan, aset, aset_kib_a, aset_kib_b, aset_kib_c, aset_kib_d, aset_kib_e, aset_kib_f, riwayat_mutasi, audit_trail
2. WHEN aset dibuat dengan kategori_kib="B", THEN System SHALL membuat record di tabel aset DAN aset_kib_b
3. THE tabel aset SHALL memiliki 19 kolom sesuai dokumentasi termasuk soft-delete fields (deleted_at, delete_reason)
4. THE tabel aset_kib_b SHALL memiliki 12 kolom untuk menyimpan data spesifik KIB B (satuan, ukuran_cc, merk, tipe, dll)
5. THE tabel users SHALL memiliki field dapat_ekspor untuk implementasi role Kepala Sekolah
6. WHEN operasi CRUD dilakukan, THEN System SHALL mencatat di tabel audit_trail

### Kebutuhan 9: Export KIB B Format BPAD DKI Jakarta (18 Kolom)

**User Story:** Sebagai Admin, saya ingin dapat mengexport data aset ke format KIB B BPAD DKI Jakarta dengan 18 kolom, sehingga dapat digunakan untuk pelaporan resmi.

#### Kriteria Penerimaan

1. WHEN Admin memilih export KIB B, THEN System SHALL menghasilkan file Excel dengan 18 kolom sesuai format BPAD DKI Jakarta
2. THE Export SHALL menggunakan header resmi: NO, KODE BARANG, REG, JENIS BARANG, UKURAN, SATUAN, TGL OLEH, BAHAN, MEREK, TYPE, TGL BPKB/DOK, NO CHASIS, NO MESIN, NOMOR POLISI, ASAL OLEH, HARGA, KAPITALISASI, TOTAL
3. WHEN export dilakukan, THEN System SHALL memformat harga dalam Rupiah penuh (bukan ribuan)
4. WHEN export dilakukan, THEN System SHALL memformat tanggal dalam format DD/MM/YYYY
5. THE Export SHALL hanya menyertakan aset dengan status "Aktif"
6. WHEN export selesai, THEN System SHALL menghasilkan file dalam < 15 detik untuk 1000 aset
7. IF user memiliki role Viewer tanpa dapat_ekspor=true, THEN System SHALL menolak akses export

### Kebutuhan 10: Mutasi Aset

**User Story:** Sebagai Admin, saya ingin dapat memindahkan aset antar ruangan dengan workflow yang jelas, sehingga perpindahan aset tercatat dengan baik.

#### Kriteria Penerimaan

1. WHEN Admin membuat mutasi, THEN System SHALL mengubah status aset menjadi "Mutasi"
2. WHEN mutasi dibuat, THEN System SHALL mencatat ruangan_asal, ruangan_tujuan, tanggal_mutasi, dan alasan (min 10 karakter)
3. WHEN mutasi diselesaikan, THEN System SHALL mengubah ruangan_id aset ke ruangan_tujuan dan status kembali ke "Aktif"
4. WHEN mutasi dibatalkan, THEN System SHALL mengembalikan status aset ke "Aktif" tanpa mengubah ruangan
5. THE System SHALL mencegah mutasi untuk aset dengan status selain "Aktif"
6. THE System SHALL mencegah aset memiliki lebih dari 1 mutasi pending

### Kebutuhan 11: Audit Trail

**User Story:** Sebagai Admin, saya ingin semua perubahan data tercatat dalam audit trail, sehingga dapat dilacak siapa melakukan apa dan kapan.

#### Kriteria Penerimaan

1. WHEN operasi CREATE dilakukan, THEN System SHALL mencatat di audit_trail dengan operation="CREATE" dan new_value berisi data baru
2. WHEN operasi UPDATE dilakukan, THEN System SHALL mencatat di audit_trail dengan operation="UPDATE", old_value dan new_value
3. WHEN operasi DELETE dilakukan, THEN System SHALL mencatat di audit_trail dengan operation="DELETE" dan old_value berisi data sebelum dihapus
4. THE audit_trail SHALL mencatat user_id, timestamp, table_name, dan record_id untuk setiap operasi
5. THE audit_trail SHALL tidak dapat dihapus atau dimodifikasi (append-only)
