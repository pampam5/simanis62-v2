# WARP.md - SIMANIS62 V2
# Project Rules untuk Warp IDE

> **Catatan**: File ini adalah versi lean dari `AGENTS.md` untuk Warp IDE.
> Untuk dokumentasi lengkap, lihat `AGENTS.md` dan `.kiro/steering/`.

## Identitas Proyek

- **Nama**: SIMANIS62 V2 (Sistem Manajemen Aset Sekolah)
- **Arsitektur**: WPF Client (.NET 8) + FastAPI Server (Python 3.12) + SQLite
- **Target**: Sekolah di Indonesia (offline-capable desktop app)

## Tech Stack (WAJIB)

### Backend
- Python 3.12, FastAPI, SQLModel, SQLite (WAL mode), Pydantic v2
- **BUKAN** PostgreSQL/MySQL

### Frontend  
- WPF .NET 8, MVVM CommunityToolkit, Refit, MaterialDesignInXaml
- **BUKAN** Entity Framework

### Tools
- Ruff (linting), MyPy (type check), Pytest, Pre-commit
- ClosedXML (Excel), QuestPDF (PDF)

## Konvensi Penamaan

| Konteks | Konvensi | Bahasa | Contoh |
|---------|----------|--------|--------|
| Database fields | snake_case | Indonesia | `nomor_register`, `dapat_ekspor` |
| Class names | PascalCase | English | `AssetService` |
| Python functions | snake_case | English | `get_asset_by_id()` |
| C# methods | PascalCase | English | `GetAssetById()` |
| API endpoints | kebab-case | English | `/api/v1/aset` |
| Enum values | TitleCase | Indonesia | `"Aktif"`, `"Rusak"` |

## Perintah Utama

```bash
# Backend
cd backend && ruff check --fix . && ruff format .
cd backend && mypy app/
cd backend && pytest -v
cd backend && uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && dotnet build
cd frontend && dotnet test

# Scripts
./scripts/setup_dev.ps1
./scripts/run_tests.ps1
./scripts/build_installer.ps1
```

## Aturan Kritis

### ✅ SELALU
- Type hints di semua Python functions
- Validasi input dengan Pydantic
- Ikuti format KIB dari `docs/format_kib_spesifikasi.md`
- Gunakan SQLModel untuk database operations

### 🚫 JANGAN
- Hardcode credentials atau secrets
- Gunakan PostgreSQL (pakai SQLite)
- Ubah format 18 kolom KIB B tanpa referensi docs
- Commit file `*.db` ke repository
- Log data sensitif (password, session token)

## Format KIB B (BPAD DKI Jakarta)

- **18 kolom** (BUKAN 20)
- Harga dalam **Rupiah penuh** (bukan ribuan)
- `kode_barang` format: XX.XX.XX.XXXX (13 karakter)
- Referensi: `docs/format_kib_spesifikasi.md`

## Struktur Folder

```
backend/app/     → FastAPI (api/, models/, schemas/, services/, core/)
frontend/        → WPF .NET 8 (Views/, ViewModels/, Models/, Services/)
docs/            → READ-ONLY dokumentasi
configs/         → Environment configs (development.json, production.json)
scripts/         → PowerShell automation
```

## Dokumentasi Referensi

| File | Keterangan |
|------|------------|
| `AGENTS.md` | Instruksi lengkap (master) |
| `docs/api_contract.md` | API endpoints |
| `docs/data_schema.md` | Database schema (11 tabel) |
| `docs/format_kib_spesifikasi.md` | Format KIB A-F |
| `.kiro/steering/` | Detail implementasi |

## Git Workflow

- Branch: `feature/`, `bugfix/`, `hotfix/`
- Commit: `[FEAT]`, `[FIX]`, `[DOCS]`, `[TEST]` (Bahasa Indonesia)
- PR: Semua tests passing, code formatted, no hardcoded secrets

---

*Sinkronisasi dengan: `AGENTS.md` v1.6*
*Terakhir diupdate: 11 Januari 2026*
