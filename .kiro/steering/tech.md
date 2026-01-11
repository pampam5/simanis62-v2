---
inclusion: always
---

# Tech Stack: SIMANIS62 V2

## Arsitektur

```
┌─────────────────┐     HTTP/REST     ┌─────────────────┐     SQLModel     ┌─────────────┐
│   WPF Client    │ ◄──────────────► │  FastAPI Server │ ◄──────────────► │   SQLite    │
│   (.NET 8)      │     Port 8000     │   (Python 3.12) │       ORM        │  (WAL Mode) │
└─────────────────┘                   └─────────────────┘                  └─────────────┘
```

## Backend Stack

| Komponen | Teknologi | Versi | Keterangan |
|----------|-----------|-------|------------|
| Runtime | Python | 3.12 | Runtime utama |
| Framework | FastAPI | Latest | REST API |
| ORM | SQLModel | Latest | Type hints + SQLAlchemy |
| Database | SQLite | 3.x | WAL mode untuk concurrency |
| Validasi | Pydantic | v2 | Data validation |
| Auth | bcrypt | Latest | Password hashing |

## Frontend Stack

| Komponen | Teknologi | Versi | Keterangan |
|----------|-----------|-------|------------|
| Framework | WPF | .NET 8 | Desktop UI |
| Pattern | MVVM | CommunityToolkit | MVVM implementation |
| HTTP Client | Refit | Latest | Type-safe REST client |
| Resilience | Polly | Latest | Retry policies |
| UI Kit | MaterialDesignInXaml | Latest | Material Design |

## Reporting Stack

| Komponen | Teknologi | Keterangan |
|----------|-----------|------------|
| Excel | ClosedXML | Generate .xlsx |
| PDF | QuestPDF | Generate PDF reports |

## Packaging & Deployment

| Komponen | Teknologi | Keterangan |
|----------|-----------|------------|
| Backend Bundle | PyInstaller | Bundle ke single EXE |
| Frontend Bundle | .NET Single-File | Self-contained EXE |
| Installer | Inno Setup | MSI/EXE installer |
| Auto-Update | Velopack | Delta updates, rollback |

## Monitoring & Support Stack

| Komponen | Teknologi | Keterangan |
|----------|-----------|------------|
| Error Monitoring | GlitchTip | Self-hosted, Sentry SDK compatible |
| Remote Support | RustDesk | Self-hosted, gratis komersial |
| Backend Logging | Python logging | RotatingFileHandler |
| Frontend Logging | Serilog | Structured logging + Sentry sink |

### Kenapa GlitchTip?
- **Gratis** - Open-source, self-hosted
- **Sentry Compatible** - Pakai Sentry SDK yang mature
- **Privacy** - Data error di server sendiri
- **Biaya** - Hanya VPS Rp 50-100k/bulan

### Kenapa RustDesk?
- **Gratis Komersial** - Tidak ada biaya lisensi
- **Self-hosted** - Relay server sendiri
- **Aman** - End-to-end encryption
- **Mudah** - User tinggal share ID

## PENTING: Aturan Tech Stack

### ✅ GUNAKAN
- SQLite dengan WAL mode (BUKAN PostgreSQL)
- SQLModel untuk ORM (BUKAN raw SQL)
- Pydantic v2 untuk validasi
- MVVM pattern untuk WPF
- Refit untuk HTTP client

### 🚫 JANGAN GUNAKAN
- PostgreSQL, MySQL, atau database server lain
- Entity Framework (gunakan SQLModel di Python)
- Raw SQL queries (gunakan ORM)
- JWT tokens (gunakan session-based auth)
- Sentry Cloud (gunakan GlitchTip self-hosted)
- TeamViewer/AnyDesk (gunakan RustDesk)

## Distribusi

### Metode Utama: Flashdisk
- Sekolah Indonesia sering internet tidak stabil
- Installer ~120-150MB (termasuk runtime)
- Sertakan RustDesk installer untuk support

### Isi Paket Flashdisk
```
SIMANIS62_Installer/
├── Simanis62_Setup_v2.0.0.exe
├── README.txt
├── LISENSI.txt
└── RustDesk_Setup.exe
```

## Configuration & Automation

### Config-Driven Design

Semua parameter environment disimpan di folder `configs/`:

```
configs/
├── development.json   # Port: 8000, Debug: true
├── production.json    # Port: 80, Debug: false
└── testing.json       # In-memory database
```

**Contoh `development.json`:**
```json
{
  "api": {
    "host": "127.0.0.1",
    "port": 8000,
    "debug": true
  },
  "database": {
    "path": "C:\\ProgramData\\Simanis62\\simanis62.db"
  },
  "logging": {
    "level": "DEBUG"
  }
}
```

### Automation Scripts

Script PowerShell untuk otomatisasi:

| Script | Fungsi |
|--------|--------|
| `scripts/setup_dev.ps1` | Setup environment (venv, dependencies) |
| `scripts/build_installer.ps1` | Build installer (pyinstaller, dotnet publish, iscc) |
| `scripts/run_tests.ps1` | Run semua tests (pytest, dotnet test) |

## Referensi Lengkap

#[[file:docs/tech_stack.md]]

