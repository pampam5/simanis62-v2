# AGENTS.md - Installer

**Stack**: Inno Setup, Velopack, PyInstaller

---

## Aturan Khusus

### Versioning
- Versioning harus **sinkron** antara backend, frontend, dan installer
- Format: `MAJOR.MINOR.PATCH` (contoh: `2.0.0`)
- Update version di:
  - `backend/app/__init__.py`
  - `frontend/Simanis62.WPF/Simanis62.WPF.csproj`
  - `installer/simanis62.iss`

### Checklist Sebelum Build

- [ ] Semua tests passing (`pytest` dan `dotnet test`)
- [ ] Version number sudah diupdate
- [ ] Dependencies sudah di-bundle
- [ ] Database migration sudah siap (jika ada)
- [ ] GlitchTip DSN sudah dikonfigurasi

### Struktur Paket Distribusi

```
SIMANIS62_Installer/
├── Simanis62_Setup_v2.0.0.exe    # Installer utama (~120-150MB)
├── README.txt                     # Panduan instalasi (Bahasa Indonesia)
├── LISENSI.txt                    # Informasi lisensi
└── RustDesk_Setup.exe             # Installer RustDesk untuk support
```

### Lokasi Instalasi

```
C:\Program Files\Simanis62\
├── Simanis62.WPF.exe             # Frontend
├── Simanis62.API.exe             # Backend (bundled Python)
└── resources/                     # Assets

C:\ProgramData\Simanis62\
├── simanis62.db                  # Database SQLite
├── simanis62.db-wal              # WAL file
├── config.json                   # Konfigurasi
└── backups/                      # Backup otomatis (retain 7 hari)
```

### Build Commands

```powershell
# 1. Bundle backend dengan PyInstaller
cd backend
pyinstaller --onefile app/main.py -n Simanis62.API

# 2. Publish frontend
cd frontend
dotnet publish -c Release -r win-x64 --self-contained

# 3. Build installer
iscc installer/simanis62.iss

# Atau gunakan script all-in-one:
./scripts/build_installer.ps1
```

### Velopack Auto-Update

- Delta updates untuk ukuran download lebih kecil
- Auto-rollback jika update gagal
- Update channel: `stable`, `beta`

---

*Sinkronisasi dengan: Root AGENTS.md v1.6*
