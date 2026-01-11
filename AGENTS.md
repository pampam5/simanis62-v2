# AGENTS.md - SIMANIS62 V2
# Sistem Manajemen Aset Sekolah - Instruksi Pengembangan

## Identitas Proyek

- **Nama**: SIMANIS62 V2 (Sistem Manajemen Aset Sekolah)
- **Tujuan**: Aplikasi desktop untuk pengelolaan aset sekolah sesuai Permendagri 19/2016
- **Target Pengguna**: Sekolah di Indonesia (Admin, Guru, Kepala Sekolah)
- **Arsitektur**: Dual-process (WPF Client + FastAPI Server + SQLite)

---

## Tech Stack (WAJIB DIIKUTI)

### Backend
- **Python 3.12** - Runtime utama
- **FastAPI** - REST API framework
- **SQLModel** - ORM dengan type hints
- **SQLite 3 + WAL mode** - Database (BUKAN PostgreSQL)
- **Pydantic** - Validasi data

### Frontend
- **WPF .NET 8** - Desktop UI framework
- **MVVM CommunityToolkit** - Pattern implementation
- **Refit** - HTTP client untuk API
- **Polly** - Resilience dan retry
- **MaterialDesignInXaml** - UI components

### Reporting
- **ClosedXML** - Generate Excel (.xlsx)
- **QuestPDF** - Generate PDF

### Packaging
- **PyInstaller** - Bundle FastAPI ke executable
- **.NET Single-File** - Bundle WPF ke single EXE
- **Inno Setup** - MSI installer
- **Velopack** - Auto-update system

### Monitoring & Support
- **GlitchTip** - Error monitoring (self-hosted, Sentry SDK compatible)
- **RustDesk** - Remote support (self-hosted, gratis untuk komersial)
- **DBHub** - Database management & debugging (visual explorer, MCP integration)
- **Python logging** - Structured logging untuk backend
- **Serilog** - Structured logging untuk WPF frontend

---

## Struktur Proyek

```
simanis62-v2/
├── AGENTS.md                    # Instruksi master
├── .kiro/                       # Kiro configuration
│   ├── steering/                # Steering files (persistent context)
│   ├── specs/                   # Feature specifications
│   └── hooks/                   # Agent hooks
├── docs/                        # Dokumentasi (BACA SAJA!)
│   ├── AGENTS.md                # Nested: "folder ini read-only"
│   ├── api_contract.md
│   ├── data_schema.md
│   ├── diagrams/
│   └── wireframes/
├── backend/                     # FastAPI Python (BACA & TULIS)
│   ├── AGENTS.md                # Nested: Python-specific rules
│   ├── app/
│   │   ├── api/                 # Endpoint routes (1 file per resource)
│   │   ├── models/              # SQLModel entities
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── core/                # Config, security, logging
│   ├── tests/                   # Pytest tests
│   ├── requirements.txt
│   └── .env.example
├── frontend/                    # WPF .NET 8 (BACA & TULIS)
│   ├── AGENTS.md                # Nested: C#/XAML-specific rules
│   ├── Simanis62.WPF/
│   │   ├── Views/               # XAML views
│   │   ├── ViewModels/          # MVVM ViewModels
│   │   ├── Models/              # Data models
│   │   └── Services/            # API clients, logging
│   └── Simanis62.WPF.Tests/
├── installer/                   # Inno Setup scripts (BACA & TULIS)
│   ├── AGENTS.md                # Nested: Installer rules
│   ├── simanis62.iss
│   └── distribution/            # Paket untuk flashdisk
├── configs/                     # Configuration files (BACA & TULIS)
│   ├── development.json         # Dev environment
│   ├── production.json          # Prod environment
│   └── testing.json             # Test environment
├── scripts/                     # Automation scripts (BACA & TULIS)
│   ├── setup_dev.ps1            # Setup development environment
│   ├── build_installer.ps1      # Build installer
│   └── run_tests.ps1            # Run all tests
├── logs/                        # Log files (JANGAN commit!)
├── .gitignore
└── README.md
```

### Nested AGENTS.md

Proyek ini menggunakan **nested AGENTS.md** untuk context spesifik:

| Lokasi | Konten |
|--------|--------|
| Root `AGENTS.md` | Instruksi master |
| `docs/AGENTS.md` | "Folder ini READ-ONLY" |
| `backend/AGENTS.md` | Aturan khusus Python |
| `frontend/AGENTS.md` | Aturan khusus C#/XAML |
| `installer/AGENTS.md` | Aturan packaging |

**Prioritas**: Nested AGENTS.md → Root AGENTS.md → Steering files → User prompt

---

## Code Quality (WAJIB)

### Tools & Perintah

```bash
# Format dan lint (auto-fix) - GUNAKAN RUFF
cd backend && ruff check --fix . && ruff format .

# Type checking
cd backend && mypy app/

# Run tests dengan coverage
cd backend && pytest --cov=app --cov-report=html

# Run semua checks sekaligus (pre-commit)
cd backend && pre-commit run --all-files
```

### Prinsip Code Quality

1. **Type Hints Wajib** - Semua function harus punya type hints
2. **Ruff untuk Linting** - Pengganti flake8, isort, black (lebih cepat)
3. **MyPy Strict Mode** - Static type checking
4. **Pre-commit Hooks** - Otomatis check sebelum commit
5. **Google Style Docstrings** - Dokumentasi function yang konsisten

### Konfigurasi Lengkap

Lihat `.kiro/steering/code-quality.md` untuk:
- Konfigurasi `pyproject.toml` lengkap
- Pre-commit hooks setup
- CI/CD GitHub Actions workflow

---

## Perintah Build & Test

### Backend (Python)
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Jalankan development server
cd backend && uvicorn app.main:app --reload --port 8000

# Jalankan tests
cd backend && pytest -v

# Type checking
cd backend && mypy app/

# Format & lint (GUNAKAN RUFF)
cd backend && ruff check --fix . && ruff format .
```

### Frontend (.NET)
```bash
# Restore packages
cd frontend && dotnet restore

# Build project
cd frontend && dotnet build

# Jalankan tests
cd frontend && dotnet test

# Publish single-file
cd frontend && dotnet publish -c Release -r win-x64 --self-contained
```

### Packaging
```bash
# Bundle backend
cd backend && pyinstaller --onefile app/main.py -n Simanis62.API

# Build installer
iscc installer/simanis62.iss
```

### Automation Scripts
```powershell
# Setup development environment
./scripts/setup_dev.ps1

# Build installer (all-in-one)
./scripts/build_installer.ps1

# Run all tests
./scripts/run_tests.ps1

# Start DBHub for database management
./scripts/start_dbhub.ps1
```

---

## Database Management (DBHub)

### Overview
DBHub adalah MCP server untuk database management yang menyediakan:
- Visual interface untuk explore database
- Query testing dan optimization
- Multi-database support (dev/test/prod)
- MCP tools untuk database operations

### Quick Start
```powershell
# Start DBHub server
.\scripts\start_dbhub.ps1

# Access workbench
# Browser: http://localhost:8080
```

### Configuration
File `dbhub.toml` dengan 3 database sources:
- **development** - Daily development (D:/simanis62-v2/backend/simanis62-dev.db)
- **testing** - Unit testing (:memory:)
- **production** - Read-only production (C:/ProgramData/Simanis62/simanis62.db)

### MCP Integration
DBHub tersedia sebagai MCP server di Kiro untuk:
- Search database objects (tables, columns, indexes)
- Execute SQL queries
- Verify data integrity
- Debug database issues

### Use Cases
- **Phase 2 Development**: Test queries sebelum implement di code
- **Debugging**: Verify data integrity dan relationships
- **Performance**: Use EXPLAIN QUERY PLAN untuk optimization
- **Maintenance**: Check database health di production (read-only)

**Detail Lengkap**: Lihat `.kiro/steering/DBHUB_GUIDE.md`

---

## Gaya Kode

### Konvensi Penamaan (WAJIB DIIKUTI)

| Konteks | Konvensi | Bahasa | Contoh |
|---------|----------|--------|--------|
| Database fields | snake_case | Bahasa Indonesia | `nomor_register`, `tahun_perolehan`, `dapat_ekspor` |
| Class names | PascalCase | English | `AssetService`, `MutationRepository` |
| Function names (Python) | snake_case | English | `get_asset_by_id()`, `create_mutation()` |
| Function names (C#) | PascalCase | English | `GetAssetById()`, `CreateMutation()` |
| API endpoints | kebab-case | English | `/api/v1/aset`, `/api/v1/mutasi` |
| Enum values | TitleCase | Bahasa Indonesia | `"Aktif"`, `"Rusak"`, `"Dihapus"` |
| UI messages | - | Bahasa Indonesia | `"Aset berhasil disimpan"` |
| File output | - | Bahasa Indonesia | `KIB_B_2026-01-10.xlsx` |

### Python (Backend)
- Gunakan **type hints** di semua function
- Ikuti **PEP 8** dengan line length 88 (Black default)
- Docstring format: **Google style**
- Nama variabel: **snake_case**
- Nama class: **PascalCase**

```python
# Contoh yang BENAR
async def get_aset_by_id(aset_id: UUID) -> Aset:
    """Mengambil data aset berdasarkan ID.

    Args:
        aset_id: UUID dari aset yang dicari.

    Returns:
        Objek Aset jika ditemukan.

    Raises:
        HTTPException: Jika aset tidak ditemukan.
    """
    aset = await db.get(Aset, aset_id)
    if not aset:
        raise HTTPException(status_code=404, detail="Aset tidak ditemukan")
    return aset
```

### C# (Frontend)
- Gunakan **nullable reference types**
- Ikuti **.NET naming conventions**
- Nama variabel: **camelCase** (private), **PascalCase** (public)
- XAML: Gunakan **MaterialDesign** components

```csharp
// Contoh yang BENAR
public partial class AsetViewModel : ObservableObject
{
    [ObservableProperty]
    private string _namaBarang = string.Empty;

    [RelayCommand]
    private async Task SimpanAsetAsync()
    {
        // Implementasi
    }
}
```

---

## Alur Kerja Git

### Branch Naming
- `feature/nama-fitur` - Fitur baru
- `bugfix/deskripsi-bug` - Perbaikan bug
- `hotfix/deskripsi` - Perbaikan urgent

### Commit Message (Bahasa Indonesia)
```
[TIPE] Deskripsi singkat

Contoh:
[FEAT] Tambah endpoint GET /api/v1/kib/b
[FIX] Perbaiki validasi harga aset
[DOCS] Update dokumentasi API
[TEST] Tambah unit test untuk mutasi
[REFACTOR] Refactor service layer
```

### PR Checklist
- ✅ Semua tests passing (`pytest` dan `dotnet test`)
- ✅ Code sudah di-format (`ruff check --fix . && ruff format .`)
- ✅ Type checking passed (`mypy app/`)
- ✅ Tidak ada hardcoded credentials
- ✅ Dokumentasi diupdate jika perlu

---

## Error Handling (Best Practices)

### Prinsip Utama

1. **Be Specific** - Tangkap hanya exception yang bisa ditangani
2. **Handle at Right Level** - Tangani di level dengan context cukup
3. **Don't Suppress** - Log dengan benar, berikan feedback bermakna
4. **Use Custom Exceptions** - Buat exception spesifik aplikasi
5. **Fail Fast** - Raise exception sedini mungkin

### Custom Exception Hierarchy

```python
# backend/app/core/exceptions.py
class AppException(Exception):
    """Base exception untuk SIMANIS62."""
    def __init__(self, message: str, error_code: str, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

class NotFoundError(AppException):
    """Resource tidak ditemukan."""
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} dengan ID {identifier} tidak ditemukan",
            error_code="NOT_FOUND",
            status_code=404
        )

class ValidationError(AppException):
    """Error validasi input."""
    pass

class AuthorizationError(AppException):
    """Tidak punya izin."""
    pass

class BusinessRuleError(AppException):
    """Pelanggaran aturan bisnis."""
    pass
```

### Correlation ID untuk Debugging

Setiap request memiliki `correlation_id` unik yang muncul di semua log entries:

```python
# Middleware menambahkan correlation_id ke setiap request
# Semua log dalam request yang sama punya ID yang sama
# Memudahkan tracing error di production

logger.info("Creating aset", extra={"correlation_id": "abc-123"})
logger.info("Validating input", extra={"correlation_id": "abc-123"})
logger.error("Validation failed", extra={"correlation_id": "abc-123"})
```

### Detail Lengkap

Lihat `.kiro/steering/error-handling.md` untuk:
- Exception handlers FastAPI
- Structured logging dengan JSON format
- Middleware correlation ID
- Contoh penggunaan di service layer

---

## Batasan & Larangan

### ✅ SELALU LAKUKAN
- Baca dokumentasi di `docs/` sebelum implementasi
- Ikuti format KIB dari `docs/format_kib_spesifikasi.md`
- Gunakan SQLModel untuk semua database operations
- Validasi input dengan Pydantic
- Tulis unit tests untuk logic baru

### ⚠️ TANYA DULU SEBELUM
- Mengubah struktur database (migration)
- Menambah dependency baru
- Mengubah format laporan KIB
- Modifikasi file di `docs/`

### 🚫 JANGAN PERNAH
- Hardcode credentials, API keys, atau secrets
- Modifikasi file `.env` atau `config.json` langsung
- Mengabaikan regulasi Permendagri 19/2016
- Mengubah format 18 kolom KIB B tanpa referensi dokumentasi
- Commit file database (`*.db`) ke repository
- Menggunakan PostgreSQL (proyek ini pakai SQLite)

---

## Dokumentasi Referensi

| Topik | File | Keterangan |
|-------|------|------------|
| API Contract | `docs/api_contract.md` | Endpoint, request/response |
| Data Schema | `docs/data_schema.md` | 11 tabel database |
| Format KIB | `docs/format_kib_spesifikasi.md` | KIB A-F BPAD DKI Jakarta |
| Business Rules | `docs/Alur Kerja_Aturan Main.md` | Aturan bisnis & validasi |
| User Stories | `docs/user_stories.md` | Acceptance criteria |
| Tech Stack | `docs/tech_stack.md` | Arsitektur & deployment |
| Stakeholders | `docs/STAKEHOLDERS.md` | Role & permissions |

**PENTING**: Selalu baca dokumentasi yang relevan sebelum implementasi!

---

## Konteks Bisnis

### 3 Aktor Utama
1. **Admin Sekolah** - Full CRUD, Reports, Export, User Management
2. **Guru (Viewer)** - Read-only, Search
3. **Kepala Sekolah** - Viewer dengan `dapat_ekspor=true` (Read-only + Export)

> **Catatan Implementasi**: Kepala Sekolah BUKAN role terpisah, melainkan user dengan role Viewer yang memiliki flag `dapat_ekspor=true`. Ini memungkinkan fleksibilitas untuk memberikan izin export ke user Viewer lainnya jika diperlukan.

### Fitur Utama
- CRUD Aset (Tambah, Edit, Hapus, Lihat)
- Laporan KIB A-F (format BPAD DKI Jakarta)
- Mutasi Aset (perpindahan antar ruangan)
- Ekspor Excel (18 kolom sesuai standar BPAD DKI Jakarta)
- Audit Trail (log semua perubahan)

### Regulasi yang WAJIB Diikuti
- **Permendagri No. 19/2016** - Pedoman Pengelolaan BMD
- **Permendagri No. 47/2021** - Perubahan Permendagri 19/2016
- **Permendagri No. 7/2024** - Perubahan Kedua
- **Format BPAD DKI Jakarta** - 18 kolom KIB B (BUKAN format generic Permendagri)

### Format KIB (BPAD DKI Jakarta)

| KIB | Nama | Kolom | Prioritas |
|-----|------|-------|-----------|
| A | Tanah | 14 | Post-MVP |
| B | Peralatan dan Mesin | **18** | **MVP** ⭐ |
| C | Gedung dan Bangunan | 17 | Post-MVP |
| D | Jalan, Irigasi, Jaringan | 16 | Post-MVP |
| E | Aset Tetap Lainnya | 16 | Post-MVP |
| F | Konstruksi Dalam Pengerjaan | 12 | Post-MVP |

> **PENTING**: Harga dalam **Rupiah penuh** (bukan ribuan). Lihat `docs/format_kib_spesifikasi.md` untuk detail.

### Status Aset (State Machine)
```
Baru → Aktif → Mutasi → Rusak → Dihapus
```

---

## Keamanan

### Authentication
- Session-based dengan cookie HttpOnly
- Session timeout: 2 jam
- Cookie name: `simanis62_session`

### Authorization (RBAC)
```python
# Admin: Full access (CRUD, Reports, Export, User Management)
# Viewer: GET endpoints only (Read-only, Search)
# Viewer + dapat_ekspor=true: GET + Export (Kepala Sekolah)

# Implementasi di database:
# - Role: "Admin" atau "Viewer"
# - Field dapat_ekspor: boolean (default False)
# - Kepala Sekolah = Viewer dengan dapat_ekspor=True
```

### Data Protection
- Password di-hash dengan bcrypt
- Tidak simpan credentials di code
- SQLite database di `C:\ProgramData\Simanis62\`

### Error Monitoring (GlitchTip)
- Self-hosted di VPS (Rp 50-100k/bulan)
- Sentry SDK compatible (Python & .NET)
- Data error dikirim: stack trace, OS info, app version
- Data TIDAK dikirim: password, session token, data aset

#### Filter Data Sensitif (WAJIB)
```python
# Backend - app/core/logging.py
import sentry_sdk

def before_send(event, hint):
    """Filter data sensitif sebelum kirim ke GlitchTip."""
    if 'request' in event:
        if 'data' in event['request']:
            event['request']['data'] = '[FILTERED]'
        if 'cookies' in event['request']:
            event['request']['cookies'] = '[FILTERED]'
    return event

sentry_sdk.init(
    dsn=os.getenv("GLITCHTIP_DSN"),
    before_send=before_send,
    environment="production"
)
```

### Remote Support (RustDesk)
- Self-hosted relay server
- Gratis untuk penggunaan komersial
- Koneksi terenkripsi end-to-end
- User harus approve sebelum remote access
- **DILARANG**: Remote tanpa user di depan komputer

---

## Distribusi & Deployment

### Metode Distribusi
- **Flashdisk** - Metode utama untuk sekolah Indonesia (internet tidak stabil)
- **Google Drive** - Backup untuk download online
- **Velopack** - Auto-update setelah instalasi pertama

### Isi Paket Distribusi (Flashdisk)
```
SIMANIS62_Installer/
├── Simanis62_Setup_v2.0.0.exe    # Installer utama (~120-150MB)
├── README.txt                     # Panduan instalasi singkat
├── LISENSI.txt                    # Informasi lisensi
└── RustDesk_Setup.exe             # Installer RustDesk untuk support
```

### Checklist Sebelum Distribusi
- ✅ Test di Windows 7, 10, 11
- ✅ Test instalasi fresh (tanpa .NET runtime)
- ✅ Test auto-update via Velopack
- ✅ Backup database berfungsi
- ✅ GlitchTip menerima error reports

---

## Logging Strategy

### Backend (Python)
```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'logs/simanis62.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)
```

### Frontend (.NET dengan Serilog)
```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .WriteTo.File("logs/simanis62-wpf.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 7)
    .WriteTo.Sentry(o => o.Dsn = "YOUR_GLITCHTIP_DSN")
    .CreateLogger();
```

### Apa yang Di-log
- ✅ Login/logout events
- ✅ CRUD operations (tanpa data sensitif)
- ✅ Error dan exceptions
- ✅ Performance metrics (query time)
- ❌ Password atau credentials
- ❌ Session tokens
- ❌ Data pribadi pengguna

---

## Performance Targets

| Operasi | Target | Keterangan |
|---------|--------|------------|
| Search aset | < 5 detik | Dengan pagination |
| Generate KIB | < 10 detik | Query database |
| Export Excel | < 15 detik | Generate file |
| Login | < 2 detik | Validasi credentials |

---

## Catatan untuk AI Agent

1. **Baca dokumentasi dulu** - Semua spesifikasi ada di `docs/`
2. **Ikuti format yang ada** - Jangan buat format baru tanpa alasan
3. **Test sebelum commit** - Jalankan `pytest` dan `dotnet test`
4. **Tanya jika ragu** - Lebih baik tanya daripada asumsi salah
5. **Bahasa Indonesia** - Semua komentar dan dokumentasi dalam Bahasa Indonesia

---

## Troubleshooting Umum

| Masalah | Penyebab | Solusi |
|---------|----------|--------|
| API tidak bisa connect | Port 8000 diblokir | Cek firewall, pastikan Simanis62.API.exe running |
| Login gagal terus | Session expired | Restart aplikasi, cek waktu sistem |
| Export Excel lambat | Data terlalu banyak | Gunakan filter, batasi range tanggal |
| Database locked | Multiple process | Tutup semua instance, restart aplikasi |
| Update gagal | Internet putus | Download manual dari Google Drive |

---

## Database Maintenance

### Lokasi Database
```
C:\ProgramData\Simanis62\
├── simanis62.db          # Database utama
├── simanis62.db-wal      # Write-ahead log
├── config.json           # Konfigurasi
└── backups/              # Backup otomatis (retain 7 hari)
```

### Perintah Maintenance
```sql
-- Cek integritas database
PRAGMA integrity_check;

-- Optimalkan database jika lambat
VACUUM;

-- Cek mode WAL aktif
PRAGMA journal_mode;
```

### Maintenance dengan DBHub
DBHub sangat berguna untuk database maintenance:
```powershell
# Start DBHub
.\scripts\start_dbhub.ps1

# Via Workbench (http://localhost:8080):
# - Select production database (read-only)
# - Run: PRAGMA integrity_check;
# - Verify results

# Via Kiro MCP:
# User: "Check database integrity for production"
# Kiro: [calls mcp_dbhub_execute_sql_production]
```

### Recovery dari Backup
1. Tutup aplikasi SIMANIS62
2. Rename `simanis62.db` → `simanis62.db.old`
3. Copy file backup ke `C:\ProgramData\Simanis62\simanis62.db`
4. Buka aplikasi SIMANIS62

---

## Maintenance & Support

### Workflow Support via WhatsApp
1. User lapor masalah via WhatsApp
2. Minta screenshot error atau kode error dari GlitchTip
3. Jika perlu remote: kirim link RustDesk + ID
4. User approve koneksi RustDesk
5. Selesaikan masalah, dokumentasikan solusi

### Monitoring via GlitchTip
- Cek dashboard GlitchTip setiap hari
- Prioritaskan error dengan frequency tinggi
- Buat hotfix untuk critical errors
- Distribusikan update via Velopack
- Velopack support auto-rollback jika update bermasalah

---

## Referensi Steering Files

Untuk detail implementasi lebih lengkap, lihat file di `.kiro/steering/`:

| File | Keterangan |
|------|------------|
| `api-standards.md` | Standar kode Python & contoh endpoint |
| `wpf-standards.md` | Standar kode C# & XAML |
| `security-policies.md` | Kebijakan keamanan detail & RBAC |
| `error-handling.md` | Custom exceptions, structured logging, correlation ID |
| `code-quality.md` | Ruff, MyPy, pre-commit, testing standards |
| `deployment-guide.md` | Panduan deployment & troubleshooting |
| `maintenance-guide.md` | Panduan maintenance & template komunikasi |
| `DBHUB_GUIDE.md` | DBHub setup, usage, & MCP integration |

---

## Kompatibilitas Multi-IDE

Proyek ini mendukung multiple AI-powered IDEs:

| IDE | File Rules | Lokasi |
|-----|------------|--------|
| **Kiro** | `AGENTS.md` | Root + nested folders |
| **Warp** | `WARP.md` | Root + nested folders |
| **Cursor** | `.cursorrules` | (link ke AGENTS.md via Warp `/init`) |
| **Claude** | `CLAUDE.md` | (link ke AGENTS.md via Warp `/init`) |

### Warp IDE Setup

Warp IDE dapat menggunakan `WARP.md` yang sudah disediakan:
- `WARP.md` - Project-wide rules (lean version)
- `backend/WARP.md` - Python/FastAPI specific
- `frontend/WARP.md` - WPF/.NET specific

Atau gunakan `/init` di Warp untuk link ke `AGENTS.md` yang sudah ada.

---

*Terakhir diupdate: 11 Januari 2026*
*Versi: 1.7*
*Sinkronisasi dengan: `.kiro/specs/simanis62-v2/requirements.md`, `WARP.md`*
