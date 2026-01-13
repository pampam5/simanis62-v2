================================================================================
                         SIMANIS62 V2
              Sistem Manajemen Aset Sekolah
================================================================================

Terima kasih telah menggunakan SIMANIS62!

SIMANIS62 adalah aplikasi desktop untuk pengelolaan aset sekolah yang sesuai 
dengan regulasi Permendagri 19/2016 dan format BPAD DKI Jakarta.

================================================================================
                         PANDUAN INSTALASI
================================================================================

1. PERSYARATAN SISTEM
   - Windows 10/11 (64-bit)
   - RAM minimal 4 GB
   - Ruang disk minimal 500 MB
   - .NET 8 Desktop Runtime (akan diminta install jika belum ada)

2. LANGKAH INSTALASI
   a. Jalankan file Simanis62_Setup_vX.X.X.exe
   b. Ikuti petunjuk di layar
   c. Jika diminta install .NET 8, download dari:
      https://dotnet.microsoft.com/download/dotnet/8.0
      Pilih ".NET Desktop Runtime" untuk Windows x64
   d. Setelah instalasi selesai, jalankan SIMANIS62 dari desktop atau Start Menu

3. SETUP PERTAMA KALI
   - Saat pertama kali dijalankan, aplikasi akan menampilkan Setup Wizard
   - Buat akun Administrator dengan username dan password
   - Setelah selesai, login dengan akun yang baru dibuat

================================================================================
                         FITUR UTAMA
================================================================================

- Pengelolaan Aset (CRUD)
- Laporan KIB A-F sesuai format BPAD DKI Jakarta
- Mutasi Aset antar ruangan
- Export ke Excel
- Audit Trail untuk semua perubahan

================================================================================
                         LOKASI FILE
================================================================================

- Aplikasi    : C:\Program Files\SIMANIS62\
- Database    : C:\ProgramData\Simanis62\simanis62.db
- Backup      : C:\ProgramData\Simanis62\backups\
- Log         : C:\ProgramData\Simanis62\logs\

================================================================================
                         TROUBLESHOOTING
================================================================================

1. Aplikasi tidak bisa dibuka
   - Pastikan .NET 8 Desktop Runtime sudah terinstall
   - Coba jalankan sebagai Administrator

2. Tidak bisa connect ke server
   - Pastikan backend API sudah berjalan
   - Cek apakah port 8000 tidak diblokir firewall

3. Database error
   - Cek apakah folder C:\ProgramData\Simanis62\ bisa diakses
   - Pastikan tidak ada aplikasi lain yang mengunci database

================================================================================
                         DUKUNGAN TEKNIS
================================================================================

Jika memerlukan bantuan teknis:
1. Hubungi administrator IT sekolah Anda
2. Untuk remote support, install RustDesk dan share ID Anda

================================================================================
                         VERSI
================================================================================

Versi: 2.0.0
Tanggal Rilis: Januari 2026

================================================================================
