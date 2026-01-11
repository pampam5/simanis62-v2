---
inclusion: always
---

# Produk: SIMANIS62 V2

## Identitas

- **Nama**: SIMANIS62 V2 (Sistem Manajemen Aset Sekolah)
- **Versi**: 2.0
- **Tanggal Mulai**: Januari 2026

## Tujuan

SIMANIS62 V2 adalah aplikasi desktop untuk pengelolaan aset sekolah yang sesuai dengan regulasi Permendagri 19/2016 (dengan update 47/2021 dan 7/2024). Aplikasi ini dirancang untuk membantu sekolah di Indonesia dalam:

1. Mengelola inventaris aset (CRUD)
2. Menghasilkan laporan KIB A-F sesuai format BPAD DKI Jakarta
3. Mencatat mutasi aset antar ruangan
4. Mengekspor data ke Excel dengan format standar

## Target Pengguna

### 3 Aktor Utama

| Aktor | Role | Akses |
|-------|------|-------|
| Admin Sekolah | Admin | Full CRUD, Reports, Export, User Management |
| Guru | Viewer | Read-only, Search |
| Kepala Sekolah | Viewer + Export | Read-only, Reports, Export |

## Fitur Utama

1. **CRUD Aset** - Tambah, Edit, Hapus, Lihat data aset
2. **Laporan KIB A-F** - Generate laporan sesuai format BPAD DKI Jakarta
3. **Mutasi Aset** - Perpindahan aset antar ruangan dengan audit trail
4. **Ekspor Excel** - Export data dengan 18 kolom standar BPAD DKI Jakarta
5. **Audit Trail** - Log semua perubahan untuk akuntabilitas

## Regulasi yang Diikuti

- **Permendagri No. 19/2016** - Pedoman Pengelolaan BMD
- **Permendagri No. 47/2021** - Perubahan Permendagri 19/2016
- **Permendagri No. 7/2024** - Perubahan Kedua
- **Format BPAD DKI Jakarta** - 18 kolom KIB B

## Konteks Bisnis

- **Deployment**: Desktop application (offline-capable)
- **Target Market**: Sekolah di Indonesia
- **Model Bisnis**: Lisensi per instalasi
- **Support**: Remote via RustDesk, auto-update via Velopack
- **Error Monitoring**: GlitchTip (self-hosted)

## Distribusi & Delivery

### Metode Distribusi (Prioritas)
1. **Flashdisk** - Metode utama (internet sekolah tidak stabil)
2. **Google Drive** - Backup untuk download online
3. **Velopack** - Auto-update setelah instalasi pertama

### Isi Paket Distribusi
```
SIMANIS62_Installer/
├── Simanis62_Setup_v2.0.0.exe    # ~120-150MB
├── README.txt                     # Panduan instalasi
├── LISENSI.txt                    # Info lisensi
└── RustDesk_Setup.exe             # Untuk remote support
```

### Kenapa Flashdisk?
- Internet sekolah di Indonesia sering tidak stabil
- Download 150MB bisa gagal berkali-kali
- Flashdisk lebih reliable untuk first install
- Update selanjutnya via Velopack (delta update, lebih kecil)

## Remote Support (RustDesk)

### Setup untuk User
1. Install RustDesk dari paket distribusi
2. Catat ID yang muncul di RustDesk
3. Saat butuh support, share ID via WhatsApp
4. Approve koneksi saat developer request

### Kenapa RustDesk?
- Gratis untuk penggunaan komersial
- Self-hosted relay server (privacy)
- End-to-end encryption
- User harus approve setiap koneksi

## Success Metrics

1. Waktu search aset < 5 detik
2. Generate laporan KIB < 10 detik
3. Export Excel < 15 detik
4. Zero data loss (backup otomatis)
5. Compliance 100% dengan format BPAD
