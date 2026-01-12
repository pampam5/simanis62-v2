# Tasks: SIMANIS62 V2

## Overview

Dokumen ini berisi daftar task implementasi untuk SIMANIS62 V2 berdasarkan requirements dan design yang sudah disetujui. Tasks diorganisir dalam phases untuk memudahkan tracking progress.

**Referensi:**
- `requirements.md` - User stories dan acceptance criteria
- `design.md` - Arsitektur teknis dan design patterns

---

## Phase 1: Project Setup & Infrastructure

### Task 1.1: Backend Project Structure
- [x] Create backend directory structure sesuai design.md
- [x] Setup `pyproject.toml` dengan dependencies
- [x] Setup `requirements.txt`
- [x] Create `.env.example` template
- [x] Setup pre-commit hooks configuration

**Files:**
- `backend/app/__init__.py`
- `backend/app/main.py`
- `backend/pyproject.toml`
- `backend/requirements.txt`
- `backend/.env.example`
- `backend/.pre-commit-config.yaml`

**Acceptance Criteria:** REQ-23 (Data Persistence)


### Task 1.2: Core Infrastructure - Configuration
- [x] Implement `app/core/config.py` dengan Pydantic Settings
- [x] Setup environment-based configuration loading
- [x] Create config files di `configs/` folder

**Files:**
- `backend/app/core/__init__.py`
- `backend/app/core/config.py`
- `configs/development.json`
- `configs/production.json`
- `configs/testing.json`

**Acceptance Criteria:** REQ-23

---

### Task 1.3: Core Infrastructure - Database
- [x] Implement `app/core/database.py` dengan SQLite WAL mode
- [x] Setup async SQLAlchemy engine dengan optimal pragmas
- [x] Implement DatabaseManager class dengan health check
- [x] Create database session dependency untuk FastAPI

**Files:**
- `backend/app/core/database.py`

**Acceptance Criteria:** REQ-23 (SQLite WAL mode, concurrent access)

---

### Task 1.4: Core Infrastructure - Logging
- [x] Implement `app/core/logging.py` dengan structured logging
- [x] Setup StructuredFormatter (JSON) dan HumanReadableFormatter
- [x] Implement correlation ID context variable
- [x] Setup GlitchTip integration dengan sensitive data filter
- [x] Configure RotatingFileHandler

**Files:**
- `backend/app/core/logging.py`

**Acceptance Criteria:** REQ-21 (Audit Trail logging)

---

### Task 1.5: Core Infrastructure - Exceptions
- [x] Implement `app/core/exceptions.py` dengan exception hierarchy
- [x] Create SimanisException base class
- [x] Create Authentication exceptions (InvalidCredentialsError, SessionExpiredError)
- [x] Create Authorization exceptions (InsufficientPermissionError)
- [x] Create Validation exceptions (DuplicateKodeBarangError, InvalidKodeBarangFormatError, dll)
- [x] Create Business exceptions (AssetInMutationError, SameRoomMutationError)
- [x] Create Resource exceptions (AssetNotFoundError, UserNotFoundError, RuanganNotFoundError)
- [x] Create Database exceptions

**Files:**
- `backend/app/core/exceptions.py`

**Acceptance Criteria:** REQ-2, REQ-4, REQ-6, REQ-14, REQ-20 (validation errors)


### Task 1.6: Core Infrastructure - Security
- [x] Implement `app/core/security.py`
- [x] Setup password hashing dengan bcrypt
- [x] Implement session management (create, verify, destroy)
- [x] Configure session timeout (2 jam)

**Files:**
- `backend/app/core/security.py`

**Acceptance Criteria:** REQ-1, REQ-24 (Session Management)

---

### Task 1.7: API Middleware
- [x] Implement `app/api/middleware.py`
- [x] Create ErrorHandlingMiddleware dengan correlation ID
- [x] Setup global exception handler untuk SimanisException
- [x] Setup handler untuk unexpected exceptions
- [x] Add X-Correlation-ID header ke responses

**Files:**
- `backend/app/api/__init__.py`
- `backend/app/api/middleware.py`

**Acceptance Criteria:** REQ-20, REQ-21

---

### Task 1.8: API Response Schemas
- [x] Implement `app/schemas/response.py`
- [x] Create SuccessResponse generic schema
- [x] Create ErrorResponse schema
- [x] Create PaginatedResponse generic schema

**Files:**
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/response.py`

**Acceptance Criteria:** REQ-5 (pagination)

---

## Phase 2: Domain Models & Repositories

### Task 2.1: Base Models
- [x] Implement `app/models/base.py` dengan common fields
- [x] Create BaseModel dengan id, created_at, updated_at
- [x] Setup UUID primary key generation

**Files:**
- `backend/app/models/__init__.py`
- `backend/app/models/base.py`

**Acceptance Criteria:** REQ-21 (audit fields)


### Task 2.2: User Model
- [x] Implement `app/models/user.py`
- [x] Create User SQLModel dengan fields: username, password_hash, nama_lengkap, role, dapat_ekspor, status
- [x] Create UserRole enum (Admin, Viewer)
- [x] Add timestamps (created_at, updated_at)

> **CATATAN**: Model User menggunakan `created_at` dan `updated_at` (bukan `dibuat_oleh`, `dibuat_pada`, dll). User tidak memiliki field `created_by`/`updated_by` karena user adalah entitas yang membuat/mengupdate dirinya sendiri.

**Files:**
- `backend/app/models/user.py`

**Acceptance Criteria:** REQ-18, REQ-19 (RBAC)

---

### Task 2.3: Ruangan Model
- [x] Implement `app/models/ruangan.py`
- [x] Create Ruangan SQLModel dengan fields: kode_ruangan, nama_ruangan, keterangan
- [x] Add timestamps (created_at, updated_at)
- [x] Add relationship ke Aset dan RiwayatMutasi

> **CATATAN**: Model Ruangan TIDAK memiliki field `gedung` atau `lantai`. Informasi lokasi dapat disimpan di field `keterangan` jika diperlukan.

**Files:**
- `backend/app/models/ruangan.py`

**Acceptance Criteria:** REQ-17 (KIR)

---

### Task 2.4: Aset Model - Core Fields
- [x] Implement `app/models/aset.py`
- [x] Create Aset SQLModel dengan common fields untuk semua KIB
- [x] Create KategoriKIB enum (A, B, C, D, E, F)
- [x] Create StatusAset enum (Baru, Aktif, Mutasi, Rusak, Dihapus)
- [x] Create Kondisi enum (Baik, Rusak_Ringan, Rusak_Berat)
- [x] Add foreign key ke Ruangan
- [x] Add audit fields

**Files:**
- `backend/app/models/aset.py`

**Acceptance Criteria:** REQ-2, REQ-4, REQ-6, REQ-20

---

### Task 2.5: Aset Model - KIB-Specific Fields
- [x] Add KIB A fields (luas_m2, alamat_lokasi, status_hak_tanah, dll)
- [x] Add KIB B fields (ukuran_cc, satuan, merk, tipe, nomor_rangka, dll)
- [x] Add KIB C fields (bertingkat, beton, luas_lantai_m2, dll)
- [x] Add KIB D fields (jenis_konstruksi, panjang_km, lebar_m, dll)
- [x] Add KIB E fields (judul_pencipta, asal_daerah, jenis_hewan, dll)
- [x] Add KIB F fields (jenis_bangunan, info_dokumen, dll)

**Files:**
- `backend/app/models/aset_kib.py`

**Acceptance Criteria:** REQ-7 sampai REQ-12 (KIB A-F)


### Task 2.6: Mutasi Model
- [x] Implement `app/models/mutasi.py`
- [x] Create RiwayatMutasi SQLModel dengan fields: aset_id, ruangan_asal_id, ruangan_tujuan_id, user_id, alasan, tanggal_mutasi, kondisi_saat_mutasi, status_mutasi
- [x] Create StatusMutasi enum (Dalam_Proses, Selesai, Dibatalkan)
- [x] Add fields untuk timestamps (mulai_mutasi, selesai_mutasi)
- [x] Add field untuk cancellation (alasan_pembatalan)

> **CATATAN**: Field pembatalan menggunakan `alasan_pembatalan` (bukan `alasan_batal`).

**Files:**
- `backend/app/models/mutasi.py`

**Acceptance Criteria:** REQ-14, REQ-15, REQ-16

---

### Task 2.7: Audit Model
- [x] Implement `app/models/audit.py`
- [x] Create AuditTrail SQLModel untuk logging semua operasi
- [x] Fields: user_id, action, table_name, record_id, old_value, new_value, timestamp

**Files:**
- `backend/app/models/audit.py`

**Acceptance Criteria:** REQ-21 (Audit Trail)

---

### Task 2.8: Base Repository
- [x] Implement `app/repositories/base.py`
- [x] Create BaseRepository generic class dengan CRUD operations
- [x] Implement get_by_id, get_all, count, create, update, delete methods
- [x] Add pagination support

**Files:**
- `backend/app/repositories/__init__.py`
- `backend/app/repositories/base.py`

**Acceptance Criteria:** REQ-5 (pagination)

---

### Task 2.9: User Repository
- [x] Implement `app/repositories/user_repository.py`
- [x] Add get_by_username method
- [x] Add get_active_users method

**Files:**
- `backend/app/repositories/user_repository.py`

**Acceptance Criteria:** REQ-1, REQ-18


### Task 2.10: Aset Repository
- [x] Implement `app/repositories/aset_repository.py`
- [x] Add get_by_kode_barang method
- [x] Add search method dengan multiple filters (keyword, kategori_kib, status, ruangan_id)
- [x] Add get_next_nomor_register method
- [x] Add get_for_kib_report method (status Aktif/Rusak only)
- [x] Add soft_delete method

**Files:**
- `backend/app/repositories/aset_repository.py`

**Acceptance Criteria:** REQ-2, REQ-5, REQ-6, REQ-7 sampai REQ-12

---

### Task 2.11: Mutasi Repository
- [x] Implement `app/repositories/mutasi_repository.py`
- [x] Add get_by_aset_id method
- [x] Add get_pending_mutations method
- [x] Add get_mutation_history method

**Files:**
- `backend/app/repositories/mutasi_repository.py`

**Acceptance Criteria:** REQ-3, REQ-14, REQ-15, REQ-16

---

### Task 2.12: Ruangan Repository
- [x] Implement `app/repositories/ruangan_repository.py`
- [x] Add get_by_kode method
- [x] Add get_assets_in_room method untuk KIR

**Files:**
- `backend/app/repositories/ruangan_repository.py`

**Acceptance Criteria:** REQ-17

---

## Phase 3: Pydantic Schemas

### Task 3.1: Auth Schemas
- [x] Implement `app/schemas/auth.py`
- [x] Create LoginRequest schema
- [x] Create LoginResponse schema
- [x] Create UserResponse schema

**Files:**
- `backend/app/schemas/auth.py`

**Acceptance Criteria:** REQ-1


### Task 3.2: Aset Schemas - Core
- [x] Implement `app/schemas/aset.py`
- [x] Create AssetBase schema dengan common fields
- [x] Create AssetCreate schema dengan validators
- [x] Create AssetUpdate schema (partial update)
- [x] Create AssetResponse schema
- [x] Create AssetSearchParams schema

**Validators:**
- kode_barang: format XX.XX.XX.XXXX
- nama_barang: 3-200 characters
- tahun_perolehan: 1900 - current year
- harga: > 0 dan <= 999.999.999.999

**Files:**
- `backend/app/schemas/aset.py`

**Acceptance Criteria:** REQ-2, REQ-20

---

### Task 3.3: Aset Schemas - KIB Specific
- [x] Create KIB A specific schemas dengan validators (luas_m2 > 0)
- [x] Create KIB B specific schemas dengan validators (satuan enum)
- [x] Create KIB C specific schemas dengan validators (kondisi B/KB/RB)
- [x] Create KIB D specific schemas dengan validators (panjang_km > 0)
- [x] Create KIB E specific schemas dengan validators (jumlah > 0)
- [x] Create KIB F specific schemas

**Files:**
- `backend/app/schemas/aset.py` (update)

**Acceptance Criteria:** REQ-7 sampai REQ-12, REQ-20

---

### Task 3.4: Mutasi Schemas
- [x] Implement `app/schemas/mutasi.py`
- [x] Create MutationCreate schema dengan validators
- [x] Create MutationResponse schema
- [x] Create MutationCancelRequest schema

**Validators:**
- alasan: min 10 characters
- tanggal_mutasi: not in future
- alasan_pembatalan: min 10 characters (untuk pembatalan mutasi)

**Files:**
- `backend/app/schemas/mutasi.py`

**Acceptance Criteria:** REQ-14, REQ-16

---

### Task 3.5: KIB Report Schemas
- [x] Implement `app/schemas/kib.py`
- [x] Create KibReportResponse schema
- [x] Create KibExportRequest schema

**Files:**
- `backend/app/schemas/kib.py`

**Acceptance Criteria:** REQ-7 sampai REQ-13


### Task 3.6: User Management Schemas
- [x] Implement `app/schemas/user.py`
- [x] Create UserCreate schema dengan validators
- [x] Create UserUpdate schema
- [x] Create UserResponse schema

**Validators:**
- username: unique
- password: min 8 characters

**Files:**
- `backend/app/schemas/user.py`

**Acceptance Criteria:** REQ-18

---

## Phase 4: Service Layer

### Task 4.1: Base Service
- [x] Implement `app/services/base.py`
- [x] Create BaseService generic class
- [x] Setup logger per service

**Files:**
- `backend/app/services/__init__.py`
- `backend/app/services/base.py`

---

### Task 4.2: Auth Service
- [x] Implement `app/services/auth_service.py`
- [x] Implement login method dengan credential validation
- [x] Implement logout method
- [x] Implement session verification
- [x] Add logging untuk login/logout events

**Files:**
- `backend/app/services/auth_service.py`

**Acceptance Criteria:** REQ-1, REQ-24

---

### Task 4.3: Aset Service - CRUD
- [x] Implement `app/services/aset_service.py`
- [x] Implement validation methods (_validate_kode_barang_format, _validate_tahun_perolehan, _validate_harga, _validate_delete_reason)
- [x] Implement create_asset method dengan auto nomor_register
- [x] Implement update_asset method dengan status auto-update based on kondisi
- [x] Implement delete_asset method (soft delete)
- [x] Implement get_asset_by_id method
- [x] Add comprehensive logging

**Files:**
- `backend/app/services/aset_service.py`

**Acceptance Criteria:** REQ-2, REQ-4, REQ-6, REQ-20, REQ-21


### Task 4.4: Aset Service - Search
- [x] Implement search_assets method dengan multiple filters
- [x] Add pagination support
- [x] Implement exclude deleted for Viewer role
- [x] Ensure search performance < 5 seconds

**Files:**
- `backend/app/services/aset_service.py` (update)

**Acceptance Criteria:** REQ-5, REQ-22

---

### Task 4.5: Mutasi Service
- [x] Implement `app/services/mutasi_service.py`
- [x] Implement initiate_mutation method
- [x] Implement complete_mutation method
- [x] Implement cancel_mutation method
- [x] Add validation: same room rejection, asset in mutation check
- [x] Add logging untuk mutation events

**Files:**
- `backend/app/services/mutasi_service.py`

**Acceptance Criteria:** REQ-14, REQ-15, REQ-16

---

### Task 4.6: KIB Service - Report Generation
- [x] Implement `app/services/kib_service.py`
- [x] Implement get_kib_report method untuk semua kategori (A-F)
- [x] Filter hanya status Aktif dan Rusak
- [x] Ensure generation < 10 seconds untuk 1000 assets

**Files:**
- `backend/app/services/kib_service.py`

**Acceptance Criteria:** REQ-7 sampai REQ-12, REQ-22

---

### Task 4.7: KIB Service - Excel Export
- [x] Implement export_to_excel method menggunakan ClosedXML
- [x] Create template sesuai format BPAD DKI Jakarta
- [x] Add header dengan nama sekolah dan judul report
- [x] Add footer dengan total count dan value
- [x] Format currency dalam Rupiah penuh
- [x] Ensure export < 15 seconds untuk 1000 assets

**Files:**
- `backend/app/services/kib_service.py` (update)

**Acceptance Criteria:** REQ-13, REQ-22


---

### Task 4.8: User Service
- [x] Implement `app/services/user_service.py`
- [x] Implement create_user method dengan password hashing
- [x] Implement update_user method
- [x] Implement deactivate_user method
- [x] Add validation: cannot delete self, cannot change own role
- [x] Add logging untuk user management events

**Files:**
- `backend/app/services/user_service.py`

**Acceptance Criteria:** REQ-18

---

### Task 4.9: Ruangan Service
- [x] Implement `app/services/ruangan_service.py`
- [x] Implement CRUD methods untuk ruangan
- [x] Implement get_kir_report method (Kartu Inventaris Ruangan)
- [x] Add logging

**Files:**
- `backend/app/services/ruangan_service.py`

**Acceptance Criteria:** REQ-17

---

### Task 4.10: Mutation Expiration Service
- [x] Implement query untuk cari pending mutations > 7 hari
- [x] Implement logic update status ke CANCELLED
- [x] Integrate dengan FastAPI startup event

**Files:**
- `backend/app/services/mutation_service.py`
- `backend/app/main.py`

**Acceptance Criteria:** US-013 (Auto-cancel 7 days)

---

## Phase 5: API Endpoints

### Task 5.1: FastAPI Main Setup
- [x] Implement `app/main.py` dengan FastAPI app
- [x] Register all routers
- [x] Add middleware (ErrorHandling, CORS)
- [x] Add startup/shutdown events untuk database
- [x] Setup logging on startup

**Files:**
- `backend/app/main.py`

**Acceptance Criteria:** REQ-23

---

### Task 5.2: API Dependencies
- [x] Implement `app/api/deps.py`
- [x] Create get_db dependency
- [x] Create get_current_user dependency
- [x] Create require_admin dependency
- [x] Create require_export_permission dependency
- [x] Create service dependencies

**Files:**
- `backend/app/api/deps.py`

**Acceptance Criteria:** REQ-19 (RBAC)

---

### Task 5.3: Auth API Endpoints
- [x] Implement `app/api/v1/auth.py`
- [x] POST /api/v1/auth/login
- [x] POST /api/v1/auth/logout
- [x] GET /api/v1/auth/me (current user info)

**Files:**
- `backend/app/api/v1/__init__.py`
- `backend/app/api/v1/auth.py`

**Acceptance Criteria:** REQ-1, REQ-24

---

### Task 5.4: Aset API Endpoints
- [x] Implement `app/api/v1/aset.py`
- [x] GET /api/v1/aset (search with filters)
- [x] GET /api/v1/aset/{id} (get by ID)
- [x] POST /api/v1/aset (create - Admin only)
- [x] PUT /api/v1/aset/{id} (update - Admin only)
- [x] DELETE /api/v1/aset/{id} (soft delete - Admin only)

**Files:**
- `backend/app/api/v1/aset.py`

**Acceptance Criteria:** REQ-2, REQ-3, REQ-4, REQ-5, REQ-6

---

### Task 5.5: KIB API Endpoints
- [x] Implement `app/api/v1/kib.py`
- [x] GET /api/v1/kib/{kategori} (get KIB report)
- [x] GET /api/v1/kib/{kategori}/export (export to Excel)
- [x] Add Admin/Kepala_Sekolah authorization (require_export_permission)

**Files:**
- `backend/app/api/v1/kib.py`

**Acceptance Criteria:** REQ-7 sampai REQ-13

---

### Task 5.6: Mutasi API Endpoints
- [x] Implement `app/api/v1/mutasi.py`
- [x] POST /api/v1/mutasi (initiate mutation - Admin only)
- [x] GET /api/v1/mutasi (list mutations)
- [x] GET /api/v1/mutasi/{id} (get mutation detail)
- [x] PUT /api/v1/mutasi/{id}/complete (complete mutation - Admin only)
- [x] PUT /api/v1/mutasi/{id}/cancel (cancel mutation - Admin only)

**Files:**
- `backend/app/api/v1/mutasi.py`

**Acceptance Criteria:** REQ-14, REQ-15, REQ-16

---

### Task 5.7: Ruangan API Endpoints
- [x] Implement `app/api/v1/ruangan.py`
- [x] GET /api/v1/ruangan (list rooms)
- [x] GET /api/v1/ruangan/{id} (get room detail)
- [x] POST /api/v1/ruangan (create room - Admin only)
- [x] PUT /api/v1/ruangan/{id} (update room - Admin only)
- [x] DELETE /api/v1/ruangan/{id} (delete room - Admin only)
- [x] GET /api/v1/ruangan/{id}/kir (get KIR report for room)

**Files:**
- `backend/app/api/v1/ruangan.py`

**Acceptance Criteria:** REQ-17

---

### Task 5.8: User Management API Endpoints
- [x] Implement `app/api/v1/users.py`
- [x] GET /api/v1/users (list users - Admin only)
- [x] GET /api/v1/users/{id} (get user detail - Admin only)
- [x] POST /api/v1/users (create user - Admin only)
- [x] PUT /api/v1/users/{id} (update user - Admin only)
- [x] PUT /api/v1/users/{id}/deactivate (deactivate user - Admin only)
- [x] Add validation: cannot delete self, cannot change own role

**Files:**
- `backend/app/api/v1/users.py`

**Acceptance Criteria:** REQ-18, REQ-19

---

### Task 5.9: API Router Setup
- [x] Implement `app/api/v1/router.py`
- [x] Register all routers (auth, aset, kib, mutasi, ruangan, users)
- [x] Add API versioning prefix /api/v1
- [x] GET /api/v1/health (health check endpoint)

**Files:**
- `backend/app/api/v1/router.py`

**Acceptance Criteria:** REQ-23

---

## Phase 6: Frontend Implementation (WPF .NET 8)

### Task 6.1: Frontend Project Structure
- [x] Create WPF project dengan .NET 8
- [x] Setup directory structure sesuai design.md
- [x] Configure NuGet packages (CommunityToolkit.Mvvm, Refit, Polly, Serilog, MaterialDesignInXaml)
- [x] Setup App.xaml dengan DI container

**Files:**
- `frontend/Simanis62.WPF/Frontend.csproj`
- `frontend/Simanis62.WPF/App.xaml`
- `frontend/Simanis62.WPF/App.xaml.cs`

**Acceptance Criteria:** REQ-22 (Performance)

---

### Task 6.2: Frontend Core Infrastructure
- [x] Implement `Core/Configuration/AppSettings.cs`
- [x] Implement `Core/Exceptions/` (SimanisException, ApiException, etc.)
- [x] Implement `Core/Logging/LoggingService.cs` dengan Serilog
- [x] Setup global exception handlers

**Files:**
- `frontend/Simanis62.WPF/Core/Configuration/AppSettings.cs`
- `frontend/Simanis62.WPF/Core/Exceptions/SimanisException.cs`
- `frontend/Simanis62.WPF/Core/Logging/LoggingService.cs`

**Acceptance Criteria:** REQ-21 (Audit Trail logging)

---

### Task 6.3: Frontend API Service
- [x] Implement `Services/Interfaces/IApiService.cs` dengan Refit
- [x] Implement `Services/ApiService.cs` dengan error handling
- [x] Setup Polly retry policies
- [x] Configure HttpClient dengan base URL dari config

**Files:**
- `frontend/Simanis62.WPF/Services/Interfaces/IApiService.cs`
- `frontend/Simanis62.WPF/Services/ApiService.cs`

**Acceptance Criteria:** REQ-22 (Performance < 5 detik)

---

### Task 6.4: Frontend Models
- [x] Implement `Models/User.cs`
- [x] Implement `Models/Asset.cs`
- [x] Implement `Models/Mutation.cs`
- [x] Implement `Models/Room.cs`
- [x] Implement `Models/ApiResponse.cs`

**Files:**
- `frontend/Simanis62.WPF/Models/`

**Acceptance Criteria:** REQ-2, REQ-14, REQ-17

---

### Task 6.5: Frontend ViewModelBase
- [x] Implement `ViewModels/Base/ViewModelBase.cs` dengan ObservableObject
- [x] Add IsBusy, ErrorMessage, HasError properties
- [x] Implement ExecuteAsync helper dengan error handling

**Files:**
- `frontend/Simanis62.WPF/ViewModels/Base/ViewModelBase.cs`

**Acceptance Criteria:** REQ-20 (Error display)

---

### Task 6.6: Login View & ViewModel
- [x] Implement `ViewModels/LoginViewModel.cs`
- [x] Implement `Views/LoginView.xaml`
- [x] Add username/password validation
- [x] Handle login errors dengan user-friendly messages

**Files:**
- `frontend/Simanis62.WPF/ViewModels/LoginViewModel.cs`
- `frontend/Simanis62.WPF/Views/LoginView.xaml`
- `frontend/Simanis62.WPF/Views/LoginView.xaml.cs`

**Acceptance Criteria:** REQ-1 (Authentication < 2 detik)

---

### Task 6.7: Dashboard View & ViewModel
- [x] Implement `ViewModels/DashboardViewModel.cs`
- [x] Implement `Views/DashboardView.xaml`
- [x] Display summary statistics (total aset per kategori)
- [x] Add navigation to other views

**Files:**
- `frontend/Simanis62.WPF/ViewModels/DashboardViewModel.cs`
- `frontend/Simanis62.WPF/Views/DashboardView.xaml`
- `frontend/Simanis62.WPF/Views/DashboardView.xaml.cs`

**Acceptance Criteria:** REQ-3 (Asset viewing)

---

### Task 6.8: Asset List View & ViewModel
- [x] Implement `ViewModels/AssetListViewModel.cs`
- [x] Implement `Views/AssetListView.xaml`
- [x] Add search dengan filters (keyword, kategori_kib, status)
- [x] Add pagination (100 items per page)
- [x] Show/hide Edit/Delete buttons based on role

**Files:**
- `frontend/Simanis62.WPF/ViewModels/AssetListViewModel.cs`
- `frontend/Simanis62.WPF/Views/AssetListView.xaml`
- `frontend/Simanis62.WPF/Views/AssetListView.xaml.cs`

**Acceptance Criteria:** REQ-3, REQ-5 (Search < 5 detik)

---

### Task 6.9: Asset Form View & ViewModel
- [x] Implement `ViewModels/AssetFormViewModel.cs`
- [x] Implement `Views/AssetFormView.xaml`
- [x] Dynamic form fields based on kategori_kib
- [x] Client-side validation dengan error messages
- [x] Create and Update modes

**Files:**
- `frontend/Simanis62.WPF/ViewModels/AssetFormViewModel.cs`
- `frontend/Simanis62.WPF/Views/AssetFormView.xaml`
- `frontend/Simanis62.WPF/Views/AssetFormView.xaml.cs`

**Acceptance Criteria:** REQ-2, REQ-4, REQ-20

---

### Task 6.10: KIB Report View & ViewModel
- [x] Implement `ViewModels/KibReportViewModel.cs`
- [x] Implement `Views/KibReportView.xaml`
- [x] Display KIB report dengan correct columns per kategori
- [x] Add export to Excel button
- [x] Show total count dan total value

**Files:**
- `frontend/Simanis62.WPF/ViewModels/KibReportViewModel.cs`
- `frontend/Simanis62.WPF/Views/KibReportView.xaml`
- `frontend/Simanis62.WPF/Views/KibReportView.xaml.cs`

**Acceptance Criteria:** REQ-7 sampai REQ-13

---

### Task 6.11: Mutation View & ViewModel
- [x] Implement `ViewModels/MutationViewModel.cs`
- [x] Implement `Views/MutationView.xaml`
- [x] Form untuk initiate mutation
- [x] List pending mutations
- [x] Complete/Cancel mutation actions

**Files:**
- `frontend/Simanis62.WPF/ViewModels/MutationViewModel.cs`
- `frontend/Simanis62.WPF/Views/MutationView.xaml`
- `frontend/Simanis62.WPF/Views/MutationView.xaml.cs`

**Acceptance Criteria:** REQ-14, REQ-15, REQ-16

---

### Task 6.12: Navigation Service
- [x] Implement `Services/NavigationService.cs`
- [x] Setup navigation between views
- [x] Handle back navigation
- [x] Pass parameters between views

**Files:**
- `frontend/Simanis62.WPF/Services/Interfaces/INavigationService.cs`
- `frontend/Simanis62.WPF/Services/NavigationService.cs`

**Acceptance Criteria:** REQ-3 (View navigation)

---

### Task 6.13: MainWindow & Shell
- [x] Implement `MainWindow.xaml` dengan navigation frame
- [x] Add sidebar menu
- [x] Add user info display
- [x] Add logout button

**Files:**
- `frontend/Simanis62.WPF/MainWindow.xaml`
- `frontend/Simanis62.WPF/MainWindow.xaml.cs`
- `frontend/Simanis62.WPF/ViewModels/MainViewModel.cs`

**Acceptance Criteria:** REQ-1 (Logout)

---

## Phase 7: Testing

### Task 7.1: Backend Unit Tests Setup
- [ ] Setup pytest dengan fixtures di `tests/conftest.py`
- [ ] Create mock database session
- [ ] Create test data factories

**Files:**
- `backend/tests/__init__.py`
- `backend/tests/conftest.py`
- `backend/tests/factories.py`

**Acceptance Criteria:** REQ-20, REQ-21

---

### Task 7.2: Service Unit Tests
- [ ] Test `AssetService` validation methods
- [ ] Test `AssetService` CRUD operations
- [ ] Test `MutationService` business logic
- [ ] Test `AuthService` login/logout

**Files:**
- `backend/tests/unit/test_services/test_aset_service.py`
- `backend/tests/unit/test_services/test_mutasi_service.py`
- `backend/tests/unit/test_services/test_auth_service.py`

**Acceptance Criteria:** REQ-2, REQ-4, REQ-6, REQ-14-16, REQ-20

---

### Task 7.3: Repository Unit Tests
- [ ] Test `AssetRepository` queries
- [ ] Test `MutationRepository` queries
- [ ] Test pagination

**Files:**
- `backend/tests/unit/test_repositories/test_aset_repository.py`
- `backend/tests/unit/test_repositories/test_mutasi_repository.py`

**Acceptance Criteria:** REQ-5 (Search)

---

### Task 7.4: API Integration Tests
- [ ] Test auth endpoints (login, logout)
- [ ] Test asset CRUD endpoints
- [ ] Test KIB report endpoints
- [ ] Test mutation endpoints
- [ ] Test RBAC (Admin vs Viewer access)

**Files:**
- `backend/tests/integration/test_api/test_auth.py`
- `backend/tests/integration/test_api/test_aset.py`
- `backend/tests/integration/test_api/test_kib.py`
- `backend/tests/integration/test_api/test_mutasi.py`

**Acceptance Criteria:** REQ-1, REQ-2-6, REQ-7-13, REQ-14-16, REQ-19

---

### Task 7.5: Performance Tests
- [ ] Test search performance (< 5 detik untuk 1000 aset)
- [ ] Test KIB report generation (< 10 detik untuk 1000 aset)
- [ ] Test Excel export (< 15 detik untuk 1000 aset)
- [ ] Test login performance (< 2 detik)

**Files:**
- `backend/tests/performance/test_search_performance.py`
- `backend/tests/performance/test_report_performance.py`

**Acceptance Criteria:** REQ-22

---

### Task 7.6: Frontend Unit Tests
- [ ] Setup xUnit test project
- [ ] Test ViewModels dengan mock services
- [ ] Test validation logic

**Files:**
- `frontend/Simanis62.WPF.Tests/`

**Acceptance Criteria:** REQ-20

---

## Phase 8: Deployment & Installer

### Task 8.1: Database Migration Scripts
- [ ] Create initial migration script
- [ ] Create seed data script (default admin user, sample rooms)
- [ ] Create backup script

**Files:**
- `scripts/migrations/001_initial.sql`
- `scripts/seed_data.py`
- `scripts/backup_database.ps1`

**Acceptance Criteria:** REQ-23

---

### Task 8.2: Build Scripts
- [ ] Update `scripts/build_backend.ps1` untuk PyInstaller
- [ ] Update `scripts/build_frontend.ps1` untuk .NET publish
- [ ] Update `scripts/run_tests.ps1` untuk pytest dan dotnet test

**Files:**
- `scripts/build_backend.ps1`
- `scripts/build_frontend.ps1`
- `scripts/run_tests.ps1`

**Acceptance Criteria:** REQ-23

---

### Task 8.3: Installer Creation
- [ ] Setup Inno Setup script `installer/simanis62.iss`
- [ ] Bundle Python runtime (embedded)
- [ ] Bundle .NET 8 runtime
- [ ] Create desktop shortcut
- [ ] Setup auto-start backend service

**Files:**
- `installer/simanis62.iss`
- `installer/distribution/README.txt`
- `installer/distribution/LISENSI.txt`

**Acceptance Criteria:** REQ-23 (Flashdisk deployment)

---

### Task 8.4: Documentation
- [ ] Update `docs/api_contract.md` dengan semua endpoints
- [ ] Create `installer/distribution/README.txt` (Panduan instalasi)
- [ ] Verify all KIB column specifications match BPAD DKI Jakarta format

**Files:**
- `docs/api_contract.md`
- `installer/distribution/README.txt`

**Acceptance Criteria:** REQ-7 sampai REQ-13

---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Infrastructure | 8 tasks | ✅ Complete |
| Phase 2: Domain Models | 12 tasks | ✅ Complete |
| Phase 3: Schemas | 6 tasks | ✅ Complete |
| Phase 4: Services | 10 tasks | ✅ Complete |
| Phase 5: API Endpoints | 9 tasks | ✅ Complete |
| Phase 6: Frontend | 13 tasks | ✅ Complete |
| Phase 7: Testing | 6 tasks | ⬜ Not Started |
| Phase 8: Deployment | 4 tasks | ⬜ Not Started |

**Total: 68 tasks (58 completed)**

---

## Requirements Coverage Matrix

| Requirement | Tasks |
|-------------|-------|
| REQ-1 (Auth) | 1.6, 4.2, 5.3, 6.6, 7.4 |
| REQ-2 (Asset Entry) | 1.5, 2.4, 3.2, 4.3, 5.4, 6.9, 7.2 |
| REQ-3 (Asset View) | 2.11, 5.4, 6.7, 6.8 |
| REQ-4 (Asset Modify) | 1.5, 2.4, 4.3, 5.4, 6.9, 7.2 |
| REQ-5 (Search) | 1.8, 2.8, 2.10, 4.4, 5.4, 6.8, 7.3 |
| REQ-6 (Delete) | 1.5, 2.10, 4.3, 5.4, 7.2 |
| REQ-7-12 (KIB A-F) | 2.5, 3.3, 3.5, 4.6, 5.5, 6.10, 7.4 |
| REQ-13 (Excel Export) | 4.7, 5.5, 6.10 |
| REQ-14-16 (Mutasi) | 2.6, 2.11, 3.4, 4.5, 5.6, 6.11, 7.2, 7.4 |
| REQ-17 (KIR) | 2.3, 2.12, 4.9, 5.7 |
| REQ-18 (User Mgmt) | 2.2, 3.6, 4.8, 5.8 |
| REQ-19 (RBAC) | 2.2, 5.2, 5.8, 7.4 |
| REQ-20 (Validation) | 1.5, 1.7, 3.2, 3.3, 4.3, 6.5, 6.9, 7.1, 7.2, 7.6 |
| REQ-21 (Audit) | 1.4, 1.7, 2.1, 2.7, 6.2, 7.1 |
| REQ-22 (Performance) | 4.4, 4.6, 4.7, 6.1, 6.3, 7.5 |
| REQ-23 (Persistence) | 1.1, 1.2, 1.3, 5.1, 5.9, 8.1, 8.2, 8.3 |
| REQ-24 (Session) | 1.6, 4.2, 5.3 |

---

*Dokumen ini adalah bagian dari `.kiro/specs/simanis62-v2/` dan harus dibaca bersama dengan `requirements.md` dan `design.md`.*

*Terakhir diupdate: 11 Januari 2026*
*Versi: 1.3 - Phase 6 Frontend Complete*
