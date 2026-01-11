# WARP.md - SIMANIS62 V2 (Master Context)
# Identitas & Instruksi Pengembangan Komprehensif

File ini adalah representasi tunggal dan komprehensif dari seluruh aturan pengembangan proyek SIMANIS62 V2, menggabungkan instruksi dari `AGENTS.md` dan file `WARP.md` di sub-folder.

---

## 🚀 Identitas Proyek
- **Nama**: SIMANIS62 V2 (Sistem Manajemen Aset Sekolah)
- **Tujuan**: Aplikasi desktop pengelolaan aset sesuai Permendagri 19/2016.
- **Arsitektur**: Dual-process (WPF Client + FastAPI Server + SQLite).
- **Bahasa Utama UI/Respon**: Bahasa Indonesia.

---

## 🛠️ Tech Stack (WAJIB DIIKUTI)

### Backend (Python)
- **Runtime**: Python 3.12 (`py -3.12`)
- **Framework**: FastAPI + Uvicorn
- **ORM**: SQLModel + SQLite 3 (WAL mode)
- **Validation**: Pydantic v2
- **Tools**: Ruff (Lint/Format), MyPy (Type Check), Pytest

### Frontend (C#/.NET)
- **Framework**: WPF .NET 8
- **Pattern**: MVVM (CommunityToolkit.Mvvm)
- **API Client**: Refit (Interface-based REST)
- **UI/UX**: MaterialDesignInXaml + Vanilla XAML
- **Logging**: Serilog + Serilog.Sinks.GlitchTip

### Reporting & DevOps
- **Excel**: ClosedXML (.xlsx)
- **PDF**: QuestPDF
- **Bundling**: PyInstaller (Backend Context), .NET Single-File (Frontend)
- **Installer**: Inno Setup + Velopack (Auto-update)

---

## 📂 Struktur Proyek Terpadu

```
simanis62-v2/
├── backend/                # Python FastAPI Server
│   ├── app/
│   │   ├── api/            # Controller/Routes
│   │   ├── core/           # Security & Config
│   │   ├── models/         # SQLModel Entities
│   │   ├── schemas/        # Pydantic DTOs
│   │   └── services/       # Business Logic
│   └── tests/              # Pytest Suite
├── frontend/               # WPF Client Application
│   ├── Simanis62.WPF/
│   │   ├── Models/         # Mirror API Models
│   │   ├── ViewModels/     # Observable Objects & Commands
│   │   ├── Views/          # XAML Files
│   │   ├── Services/       # Refit Clients & Loggers
│   │   └── Converters/     # UI Value Converters
├── configs/                # Shared configurations
├── docs/                   # Business & System Documentation
└── scripts/                # Build & Automation scripts
```

---

## 💻 Perintah Utama (Terminal)

### Backend Operations
```bash
# Jalankan Server (Dev)
cd backend && uvicorn app.main:app --reload --port 8000

# Audit Kode
ruff check --fix . && mypy app/

# Testing
pytest -v --cov=app
```

### Frontend Operations
```bash
# Build & Restore
dotnet restore
dotnet build

# Publish (Production)
dotnet publish -c Release -r win-x64 --self-contained
```

---

## 📊 Reporting & Maintenance

### Workflow Reporting
- **Excel**: Generate via `ClosedXML` di Frontend atau library Python di Backend.
- **PDF**: Standar menggunakan `QuestPDF` untuk layout yang presisi.

### Support & Monitoring
- **Error Tracking**: Gunakan GlitchTip (Self-hosted).
- **Remote Support**: RustDesk untuk bantuan teknis jarak jauh.
- **Log Correlation**: Gunakan ID unik untuk melacak error dari Frontend ke Backend.

---

## 📏 Konvensi Kode & Standar

### Standar Global
- **Bahasa**: Gunakan Bahasa Indonesia untuk User Messages (Messagebox, Validation error).
- **Logging**: Semua error fatal WAJIB dikirim ke GlitchTip.
- **Kemananan**: JANGAN PERNAH hardcode password atau API Key. Gunakan `.env` atau `appsettings.json`.

### Python (Backend) Pattern
- **Type Hints**: WAJIB di semua function params dan return values.
- **Naming**: `snake_case` untuk function/variabel, `PascalCase` untuk Class.
- **Async**: Gunakan `async def` untuk operasi I/O.

```python
# Contoh Pattern FastAPI + SQLModel
async def get_aset_by_id(aset_id: UUID) -> Aset:
    """Mengambil aset berdasarkan ID.
    Args: aset_id: UUID dari aset.
    Returns: Objek Aset jika ditemukan.
    Raises: NotFoundError: Jika tidak ditemukan.
    """
    aset = await db.get(Aset, aset_id)
    if not aset:
        raise NotFoundError("Aset", aset_id)
    return aset
```

### C# (Frontend) Pattern
- **MVVM**: Gunakan `[ObservableProperty]` dan `[RelayCommand]`.
- **Async I/O**: Jangan pernah blok UI Thread, gunakan `await`.
- **Naming**: `_camelCase` untuk private fields, `PascalCase` untuk sisanya.

```csharp
// Contoh Pattern MVVM (CommunityToolkit)
public partial class AsetViewModel : ObservableObject
{
    private readonly IApiService _apiService;
    [ObservableProperty] private string _namaBarang = string.Empty;

    [RelayCommand]
    private async Task LoadAsetAsync() {
        try {
            var result = await _apiService.GetAsetAsync();
            // Upate UI logic
        } catch (Exception ex) {
            // Log to GlitchTip via Serilog
        }
    }
}
```

---

## 🚫 JANGAN (Anti-Patterns)

1. **Database**: JANGAN gunakan PostgreSQL/MySQL. Gunakan SQLite.
2. **Logic**: JANGAN letakkan business logic di Middleware atau Views. Gunakan Folder `Services`.
3. **Frontend**: JANGAN gunakan Entity Framework di WPF Client (Gunakan Refit API Client).
4. **UI**: JANGAN gunakan bahasa Inggris untuk pesan sukses/gagal yang muncul ke user.
5. **Secrets**: JANGAN commit file `.env` yang berisi kredensial asli.

---

## 🤖 IDE & Agent Steering

File ini (`WARP.md`) bertindak sebagai instruksi primer untuk **Warp IDE**. AI Agent harus selalu merujuk ke file ini sebelum melakukan perubahan besar pada arsitektur.

*Terakhir Diupdate: 11 Januari 2026*
*Versi: 2.0 (Unified Master)*
