---
inclusion: always
---

# Struktur Proyek: SIMANIS62 V2

## Direktori Utama

```
simanis62-v2/
├── AGENTS.md                    # Instruksi utama untuk agent
├── .kiro/                       # Kiro configuration
│   ├── steering/                # Steering files (persistent context)
│   │   ├── product.md
│   │   ├── tech.md
│   │   ├── structure.md
│   │   ├── api-standards.md
│   │   ├── wpf-standards.md
│   │   ├── security-policies.md
│   │   ├── deployment-guide.md
│   │   ├── maintenance-guide.md
│   │   └── agents-md-integration.md
│   ├── specs/                   # Feature specifications
│   └── hooks/                   # Agent hooks
│
├── docs/                        # Dokumentasi (BACA SAJA!)
│   ├── AGENTS.md                # Nested: "folder ini read-only"
│   ├── api_contract.md
│   ├── data_schema.md
│   ├── format_kib_spesifikasi.md
│   ├── tech_stack.md
│   ├── user_stories.md
│   ├── STAKEHOLDERS.md
│   ├── Alur Kerja_Aturan Main.md
│   ├── diagrams/                # UML diagrams (.drawio)
│   └── wireframes/              # UI wireframes (.drawio)
│
├── backend/                     # FastAPI Python (BACA & TULIS)
│   ├── AGENTS.md                # Nested: Python-specific rules
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Entry point FastAPI
│   │   ├── api/                 # Endpoint routes (1 file per resource)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # /api/v1/auth/*
│   │   │   ├── aset.py          # /api/v1/aset/*
│   │   │   ├── kib.py           # /api/v1/kib/*
│   │   │   ├── mutasi.py        # /api/v1/mutasi/*
│   │   │   └── ruangan.py       # /api/v1/ruangan/*
│   │   ├── models/              # SQLModel entities
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── aset.py
│   │   │   ├── ruangan.py
│   │   │   └── mutasi.py
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── aset.py
│   │   │   └── response.py
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── aset_service.py
│   │   │   └── kib_service.py
│   │   └── core/                # Config, security, logging
│   │       ├── __init__.py
│   │       ├── config.py
│   │       ├── database.py
│   │       ├── security.py
│   │       └── logging.py
│   ├── tests/                   # Pytest tests
│   │   ├── __init__.py
│   │   ├── conftest.py          # Fixtures
│   │   ├── test_auth.py
│   │   └── test_aset.py
│   ├── requirements.txt         # Dependencies
│   ├── pyproject.toml           # Project config
│   └── .env.example             # Environment template
│
├── frontend/                    # WPF .NET 8 (BACA & TULIS)
│   ├── AGENTS.md                # Nested: C#/XAML-specific rules
│   ├── Simanis62.WPF/
│   │   ├── Simanis62.WPF.csproj
│   │   ├── App.xaml
│   │   ├── MainWindow.xaml
│   │   ├── Views/               # XAML views
│   │   │   ├── LoginView.xaml
│   │   │   ├── DashboardView.xaml
│   │   │   ├── AsetListView.xaml
│   │   │   └── KibReportView.xaml
│   │   ├── ViewModels/          # MVVM ViewModels
│   │   │   ├── LoginViewModel.cs
│   │   │   ├── DashboardViewModel.cs
│   │   │   └── AsetListViewModel.cs
│   │   ├── Models/              # Data models
│   │   │   ├── User.cs
│   │   │   ├── Aset.cs
│   │   │   └── ApiResponse.cs
│   │   └── Services/            # API clients, logging
│   │       ├── IApiService.cs
│   │       ├── ApiService.cs
│   │       └── SentryService.cs
│   └── Simanis62.WPF.Tests/
│       └── Simanis62.WPF.Tests.csproj
│
├── installer/                   # Inno Setup scripts (BACA & TULIS)
│   ├── AGENTS.md                # Nested: Installer-specific rules
│   ├── simanis62.iss
│   └── distribution/            # Paket untuk flashdisk
│       ├── README.txt
│       └── LISENSI.txt
│
├── configs/                     # Configuration files (BACA & TULIS)
│   ├── development.json         # Dev environment config
│   ├── production.json          # Prod environment config
│   └── testing.json             # Test environment config
│
├── scripts/                     # Automation scripts (BACA & TULIS)
│   ├── setup_dev.ps1            # Setup development environment
│   ├── build_installer.ps1      # Build installer
│   └── run_tests.ps1            # Run all tests
│
├── logs/                        # Log files (JANGAN commit!)
│   └── .gitkeep
│
├── .gitignore
├── LICENSE
└── README.md
```

## Aturan Akses

| Folder | Akses | Keterangan |
|--------|-------|------------|
| `backend/` | BACA & TULIS | Kode Python FastAPI |
| `frontend/` | BACA & TULIS | Kode C# WPF |
| `docs/` | BACA SAJA | Dokumentasi referensi |
| `installer/` | BACA & TULIS | Script installer |
| `configs/` | BACA & TULIS | File konfigurasi |
| `scripts/` | BACA & TULIS | Script automation |
| `logs/` | JANGAN COMMIT | Log files runtime |
| `.kiro/` | BACA & TULIS | Konfigurasi Kiro |

## Nested AGENTS.md

Proyek ini menggunakan **nested AGENTS.md** untuk memberikan context spesifik per folder:

| Lokasi | Konten |
|--------|--------|
| Root `AGENTS.md` | Instruksi master |
| `docs/AGENTS.md` | "Folder ini READ-ONLY" |
| `backend/AGENTS.md` | Aturan khusus Python |
| `frontend/AGENTS.md` | Aturan khusus C#/XAML |
| `installer/AGENTS.md` | Aturan packaging |

## File Penting

| File | Fungsi |
|------|--------|
| `AGENTS.md` | Instruksi utama |
| `backend/app/main.py` | Entry point FastAPI |
| `backend/app/core/logging.py` | Konfigurasi logging backend |
| `frontend/Simanis62.WPF/App.xaml` | Entry point WPF |
| `frontend/Simanis62.WPF/Services/SentryService.cs` | GlitchTip integration |
| `docs/api_contract.md` | Spesifikasi API |
| `docs/data_schema.md` | Schema database |
| `configs/*.json` | Konfigurasi environment |
| `scripts/*.ps1` | Automation scripts |
| `dbhub.toml` | DBHub multi-database configuration |
| `.kiro/steering/DBHUB_GUIDE.md` | DBHub setup & usage guide |
