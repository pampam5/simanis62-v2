---
inclusion: manual
---

# Panduan Deployment & Distribusi - SIMANIS62 V2

## Metode Distribusi

### Prioritas Metode
1. **Flashdisk** - Metode utama untuk instalasi pertama
2. **Google Drive** - Backup jika flashdisk tidak tersedia
3. **Velopack** - Auto-update setelah instalasi pertama

### Kenapa Flashdisk?
- Internet sekolah di Indonesia sering tidak stabil
- Download 150MB bisa gagal berkali-kali
- Flashdisk lebih reliable untuk first install
- Guru/admin tidak perlu skill teknis tinggi

## Persiapan Paket Distribusi

### Struktur Folder Flashdisk
```
SIMANIS62_Installer/
├── Simanis62_Setup_v2.0.0.exe    # Installer utama (~120-150MB)
├── README.txt                     # Panduan instalasi singkat
├── LISENSI.txt                    # Informasi lisensi
├── RustDesk_Setup.exe             # Installer RustDesk
└── CHANGELOG.txt                  # Daftar perubahan versi
```

### Isi README.txt
```
PANDUAN INSTALASI SIMANIS62 V2
==============================

1. Klik 2x pada file "Simanis62_Setup_v2.0.0.exe"
2. Klik "Next" sampai selesai
3. Aplikasi akan muncul di Desktop

BUTUH BANTUAN?
- WhatsApp: [nomor support]
- Install RustDesk_Setup.exe untuk remote support

Terima kasih telah menggunakan SIMANIS62!
```

## Checklist Sebelum Distribusi

### Testing Matrix
| OS | Status | Catatan |
|----|--------|---------|
| Windows 7 SP1 | ⬜ Test | Butuh .NET 8 runtime |
| Windows 10 | ⬜ Test | Target utama |
| Windows 11 | ⬜ Test | Target utama |

### Checklist Wajib
- [ ] Build Release berhasil tanpa error
- [ ] Test instalasi fresh (PC tanpa .NET runtime)
- [ ] Test login dengan semua role (Admin, Viewer, Kepala Sekolah)
- [ ] Test CRUD aset (tambah, edit, hapus)
- [ ] Test export Excel dan PDF
- [ ] Test backup database
- [ ] Test auto-update via Velopack
- [ ] GlitchTip menerima test error
- [ ] RustDesk bisa connect

### Checklist Opsional
- [ ] Test di PC dengan RAM 4GB (minimum spec)
- [ ] Test di PC dengan HDD (bukan SSD)
- [ ] Test dengan antivirus aktif
- [ ] Test offline mode (tanpa internet)

## Proses Build Installer

### 1. Build Backend (Python)
```bash
cd backend
pip install pyinstaller
pyinstaller --onefile --name Simanis62.API app/main.py
# Output: dist/Simanis62.API.exe
```

### 2. Build Frontend (.NET)
```bash
cd frontend/Simanis62.WPF
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true
# Output: bin/Release/net8.0-windows/win-x64/publish/Simanis62.WPF.exe
```

### 3. Build Installer (Inno Setup)
```bash
iscc installer/simanis62.iss
# Output: installer/Output/Simanis62_Setup_v2.0.0.exe
```

### 4. Siapkan Paket Flashdisk
```bash
mkdir SIMANIS62_Installer
copy installer/Output/Simanis62_Setup_v2.0.0.exe SIMANIS62_Installer/
copy installer/distribution/README.txt SIMANIS62_Installer/
copy installer/distribution/LISENSI.txt SIMANIS62_Installer/
# Download RustDesk dari https://rustdesk.com/
copy RustDesk_Setup.exe SIMANIS62_Installer/
```

## Troubleshooting Instalasi

### Error: "This app requires .NET 8"
**Penyebab**: .NET runtime tidak terinstall
**Solusi**: Installer seharusnya include runtime. Jika tidak, download dari https://dotnet.microsoft.com/download/dotnet/8.0

### Error: "Windows protected your PC"
**Penyebab**: SmartScreen karena installer belum di-sign
**Solusi**: Klik "More info" → "Run anyway"

### Error: "Port 8000 already in use"
**Penyebab**: Ada aplikasi lain pakai port 8000
**Solusi**: Tutup aplikasi lain atau restart PC

### Error: "Database is locked"
**Penyebab**: Multiple instance aplikasi
**Solusi**: Tutup semua SIMANIS62, restart aplikasi

### Error: "Cannot connect to API"
**Penyebab**: Firewall blokir atau API tidak running
**Solusi**:
1. Cek apakah Simanis62.API.exe running di Task Manager
2. Tambahkan exception di Windows Firewall
3. Restart aplikasi

## Update via Velopack

### Cara Kerja
1. Aplikasi cek update saat startup
2. Jika ada update, download delta (hanya perubahan)
3. User konfirmasi install update
4. Aplikasi restart dengan versi baru

### Jika Update Gagal
1. Download installer terbaru dari Google Drive
2. Uninstall versi lama
3. Install ulang dengan installer baru

## Backup & Recovery

### Lokasi Data
```
C:\ProgramData\Simanis62\
├── simanis62.db          # Database utama
├── simanis62.db-wal      # Write-ahead log
├── config.json           # Konfigurasi
└── backups/              # Backup otomatis
    └── simanis62_2026-01-09.db
```

### Backup Manual
1. Tutup aplikasi SIMANIS62
2. Copy folder `C:\ProgramData\Simanis62\` ke flashdisk
3. Simpan di tempat aman

### Recovery dari Backup
1. Tutup aplikasi SIMANIS62
2. Rename `simanis62.db` menjadi `simanis62.db.old`
3. Copy file backup ke `C:\ProgramData\Simanis62\simanis62.db`
4. Buka aplikasi SIMANIS62

## Referensi

#[[file:AGENTS.md]]
#[[file:docs/tech_stack.md]]
