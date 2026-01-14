# Tauri Python Sidecar Pattern - Reference

## Arsitektur dari Template

```
SIMANIS62.exe (Tauri)
├── Frontend (React + Vite) → WebView
├── Rust Core (src-tauri/src/main.rs)
│   └── Spawn & manage sidecar process
├── Python Sidecar (PyInstaller .exe)
│   └── FastAPI server on localhost:8000
└── SQLite Database (C:\ProgramData\Simanis62\)
```

## Key Files Structure

```
/frontend-tauri
  /src              # React frontend code
  /src-tauri
    /bin/api        # Compiled Python sidecar goes here
    /src/main.rs    # Tauri main app logic (spawn sidecar)
    tauri.conf.json # Sidecar config, permissions
/backend
  /app              # FastAPI code
  build_sidecar.py  # PyInstaller build script
```

## Build Process

1. **Compile Python sidecar** (PyInstaller)
   ```bash
   pyinstaller --onefile --name simanis62-api-x86_64-pc-windows-msvc backend/app/main.py
   # Output: frontend-tauri/src-tauri/bin/api/simanis62-api-x86_64-pc-windows-msvc.exe
   ```

2. **Build Frontend** (Vite)
   ```bash
   cd frontend-tauri && bun run build
   ```

3. **Build Tauri App**
   ```bash
   cd frontend-tauri && bun tauri build
   # Output: src-tauri/target/release/bundle/nsis/SIMANIS62_x.x.x_x64-setup.exe
   ```

## tauri.conf.json Key Config

```json
{
  "bundle": {
    "externalBin": ["bin/api/simanis62-api"]
  },
  "plugins": {
    "shell": {
      "sidecar": true,
      "scope": [{ "name": "simanis62-api", "sidecar": true }]
    }
  }
}
```

## main.rs Sidecar Management

- Spawn sidecar on app startup
- Wait for backend ready (health check)
- Graceful shutdown on app close
- Log sidecar stdout/stderr

## Communication

- Frontend ↔ Backend: HTTP (localhost:8000)
- Frontend ↔ Tauri: IPC (invoke commands)
- Tauri ↔ Sidecar: stdin/stdout for lifecycle

## PyInstaller Considerations

- Use `sys._MEIPASS` for bundled files
- Use `multiprocessing.freeze_support()` for Windows
- Database path: `C:\ProgramData\Simanis62\simanis62.db`
