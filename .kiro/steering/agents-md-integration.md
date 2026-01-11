---
inclusion: always
---

# Integrasi AGENTS.md - SIMANIS62 V2

## Instruksi Utama

Agent WAJIB membaca dan mematuhi file `AGENTS.md` sebagai sumber kebenaran utama (Single Source of Truth) untuk semua instruksi pengembangan.

## Lokasi File (Nested Hierarchy)

Proyek ini menggunakan **nested AGENTS.md** untuk context spesifik per folder:

```
simanis62-v2/
├── AGENTS.md                    # Master instructions
├── docs/AGENTS.md               # "Folder ini READ-ONLY"
├── backend/AGENTS.md            # Aturan khusus Python
├── frontend/AGENTS.md           # Aturan khusus C#/XAML
└── installer/AGENTS.md          # Aturan packaging
```

## Cara Kerja Nested AGENTS.md

1. **SCAN**: Baca AGENTS.md terdekat dengan file yang sedang dikerjakan
2. **INHERIT**: Jika tidak ada aturan spesifik, naik ke parent folder
3. **OVERRIDE**: Aturan di nested file override aturan di root

### Contoh Prioritas
```
Mengerjakan backend/app/api/aset.py:
1. Cek backend/AGENTS.md (Python rules) ← Prioritas tertinggi
2. Cek root AGENTS.md (Master rules)
3. Cek steering files (Detail tambahan)
```

## Aturan Prioritas

1. **Nested AGENTS.md** - Aturan spesifik per folder
2. **Root AGENTS.md** - Aturan master proyek
3. **Steering files** - Pelengkap dan detail teknis
4. **User prompt** - Override untuk kasus spesifik

## Checklist Sebelum Coding

- [ ] Sudah membaca AGENTS.md (root dan nested)
- [ ] Memahami tech stack (Python 3.12 + FastAPI + WPF .NET 8 + SQLite)
- [ ] Mengetahui batasan (JANGAN hardcode credentials, JANGAN pakai PostgreSQL)
- [ ] Mengikuti gaya kode (PEP 8 untuk Python, .NET conventions untuk C#)
- [ ] Referensi dokumentasi di `docs/` jika diperlukan
- [ ] Memahami logging strategy (Python logging + Serilog)
- [ ] Memahami config-driven design (`configs/*.json`)

## Perintah Penting

### Setup Environment
```bash
# Gunakan automation script
./scripts/setup_dev.ps1
```

### Backend (Python)
```bash
pip install -r backend/requirements.txt
cd backend && uvicorn app.main:app --reload --port 8000
cd backend && pytest -v
cd backend && black app/ && isort app/
```

### Frontend (.NET)
```bash
cd frontend && dotnet restore
cd frontend && dotnet build
cd frontend && dotnet test
```

### Build Installer
```bash
./scripts/build_installer.ps1
```

## Batasan Kritis

🚫 **JANGAN PERNAH:**
- Hardcode credentials, API keys, atau secrets
- Menggunakan PostgreSQL (proyek ini pakai SQLite)
- Mengubah format 18 kolom KIB B tanpa referensi dokumentasi
- Commit file database (`*.db`) ke repository
- Mengabaikan regulasi Permendagri 19/2016
- Log data sensitif (password, session token, data pribadi)
- Kirim data aset ke GlitchTip (hanya error info)
- Modifikasi file di `docs/` (READ-ONLY)

## Dokumentasi Referensi

| File | Keterangan |
|------|------------|
| `docs/api_contract.md` | Endpoint, request/response |
| `docs/data_schema.md` | 11 tabel database |
| `docs/format_kib_spesifikasi.md` | KIB A-F BPAD DKI Jakarta |
| `docs/tech_stack.md` | Arsitektur & deployment |
| `configs/*.json` | Environment configuration |
| `.kiro/steering/deployment-guide.md` | Panduan distribusi & instalasi |
| `.kiro/steering/maintenance-guide.md` | Panduan maintenance & support |
| `.kiro/steering/DBHUB_GUIDE.md` | DBHub setup & database management |
