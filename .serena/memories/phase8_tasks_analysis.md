# Phase 8 Tasks Analysis (8.4-8.7)

## Research Date: 12 Januari 2026

## Summary

Analisis mendalam untuk Tasks 8.4-8.7 dengan best practices terbaru.

---

## Task 8.4: Database Backup Script

### Requirements
- PowerShell script untuk SQLite WAL mode backup
- Timestamp naming: `simanis62_backup_YYYYMMDD_HHmmss.db`
- Retention: Keep last 7 backups
- Compression: zip format
- Location: `C:\ProgramData\Simanis62\backups\`

### Best Practices (SQLite WAL Mode)
1. **CRITICAL**: Run `PRAGMA wal_checkpoint(TRUNCATE)` BEFORE backup
2. This flushes WAL file content to main database
3. Then copy the .db file (ignore -wal and -shm files)
4. Alternative: Use SQLite `.backup` command

### Implementation Notes
- No additional installation needed (PowerShell built-in)
- Use `Compress-Archive` for zip compression
- Use `Get-ChildItem | Sort-Object | Select-Object -Skip 7 | Remove-Item` for retention

### Status: ✅ Ready to implement

---

## Task 8.5: Build Scripts

### Backend (PyInstaller)

#### CRITICAL ISSUE DISCOVERED
- **PyInstaller `--onefile` BREAKS uvicorn!** (GitHub Issue #8817)
- Uvicorn uses multiprocessing which doesn't work with onefile extraction
- **SOLUTION**: Use `--onedir` mode instead

#### Hidden Imports Required
```python
hiddenimports = [
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'fastapi',
    'pydantic',
    'sqlmodel',
    'email_validator',
    'passlib',
    'bcrypt',
    'passlib.handlers.bcrypt',
]
```

#### Command
```bash
pyinstaller --onedir --name Simanis62.API --clean backend/app/main.py
```

#### Output
- `dist/Simanis62.API/` folder with EXE and dependencies
- NOT a single file (due to uvicorn limitation)

### Frontend (.NET 8 WPF)

#### Command
```bash
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
```

#### Notes
- Self-contained + single file = ~150MB
- DO NOT use trimming for WPF (causes runtime errors)
- Some native DLLs may still be separate

### Dependencies to Install
1. **PyInstaller**: `pip install pyinstaller` (in backend venv)

### Status: ⚠️ Needs PyInstaller installation

---

## Task 8.6: Installer Creation (Inno Setup)

### Tool Selection
- **Inno Setup 6.7** (latest, released 2026-01-06)
- **InnoDependencyInstaller** for .NET 8 runtime detection

### Download Links
- Inno Setup: https://jrsoftware.org/isdl.php
- InnoDependencyInstaller: https://github.com/DomGries/InnoDependencyInstaller

### .NET 8 Detection
```pascal
// Using InnoDependencyInstaller
Dependency_AddDotNet80Desktop;

// Or manual check
function Dependency_IsNetCoreInstalled(const Version: String): Boolean;
```

### Installer Features
- Bundle backend folder (`Simanis62.API/`)
- Bundle frontend EXE (`Simanis62.WPF.exe`)
- Create desktop & Start Menu shortcuts
- Register uninstaller
- Auto-start backend on app launch
- Check/install .NET 8 Desktop Runtime

### Dependencies to Install
1. **Inno Setup 6.7**: Download from jrsoftware.org
2. **InnoDependencyInstaller**: Clone from GitHub

### Status: ⚠️ Needs Inno Setup installation

---

## Task 8.7: Documentation

### Requirements
1. Update `docs/api_contract.md` with setup endpoints
2. Create `installer/distribution/README.txt`
3. Verify KIB format compliance

### Setup Endpoints to Document
- `GET /api/v1/setup/status` - Check if setup needed
- `POST /api/v1/setup/admin` - Create first admin

### Status: ✅ Ready to implement

---

## Recommended Implementation Order

1. **Task 8.4** (Backup Script) - No dependencies, can start immediately
2. **Task 8.7** (Documentation) - No dependencies, can start immediately
3. **Task 8.5** (Build Scripts) - After PyInstaller installed
4. **Task 8.6** (Installer) - After Inno Setup installed + Task 8.5 complete

---

## User Actions Required

### 1. Install PyInstaller (Backend venv)
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install pyinstaller
```

### 2. Download & Install Inno Setup 6.7
- URL: https://jrsoftware.org/isdl.php
- File: `innosetup-6.7.0.exe`
- Install to default location

### 3. Download InnoDependencyInstaller
```powershell
cd installer
git clone https://github.com/DomGries/InnoDependencyInstaller.git deps
```

---

## Potential Issues & Solutions

| Issue | Solution |
|-------|----------|
| PyInstaller + uvicorn onefile = BROKEN | Use `--onedir` mode |
| .NET 8 WPF trimming = Runtime errors | Don't use trimming |
| SQLite backup during active connections | Use checkpoint first |
| Inno Setup .NET version mismatch | Use InnoDependencyInstaller |
| Large installer size (~300MB) | Use LZMA2 compression |

---

*Last Updated: 12 Januari 2026*
