---
inclusion: manual
---

# Panduan Maintenance & Support - SIMANIS62 V2

## Overview

Dokumen ini berisi panduan untuk developer dalam melakukan maintenance dan support untuk user SIMANIS62.

## Tools yang Digunakan

| Tool | Fungsi | Biaya |
|------|--------|-------|
| GlitchTip | Error monitoring | Rp 50-100k/bulan (VPS) |
| RustDesk | Remote support | Gratis (self-hosted) |
| DBHub | Database management & debugging | Gratis (development tool) |

### GlitchTip
- Self-hosted error monitoring
- Sentry SDK compatible
- Dashboard: https://glitchtip.yourdomain.com

### RustDesk
- Self-hosted remote desktop
- End-to-end encryption
- User harus approve setiap koneksi

### DBHub
- Visual database explorer
- Query testing dan debugging
- MCP integration untuk Kiro
- **Use Case**: Debug database issues, verify data integrity
- **Setup**: See `.kiro/steering/DBHUB_GUIDE.md`
| WhatsApp | Komunikasi dengan user | Gratis |
| Velopack | Auto-update | Gratis |

## Error Monitoring (GlitchTip)

### Setup GlitchTip Server
1. Sewa VPS (DigitalOcean, Vultr, atau lokal)
2. Install Docker
3. Deploy GlitchTip dengan docker-compose
4. Buat project untuk SIMANIS62
5. Copy DSN untuk backend dan frontend

### Dashboard GlitchTip
- **Issues**: Daftar error yang terjadi
- **Frequency**: Seberapa sering error terjadi
- **Users Affected**: Berapa user yang terkena
- **First Seen / Last Seen**: Kapan error pertama/terakhir

### Workflow Harian
1. Buka dashboard GlitchTip setiap pagi
2. Cek error baru (sort by "First Seen")
3. Prioritaskan error dengan frequency tinggi
4. Investigasi dan buat fix
5. Deploy update via Velopack

### Prioritas Error
| Severity | Contoh | Response Time |
|----------|--------|---------------|
| Critical | App crash, data loss | < 4 jam |
| High | Fitur utama tidak jalan | < 24 jam |
| Medium | Fitur minor error | < 1 minggu |
| Low | UI glitch, typo | Next release |

## Remote Support (RustDesk)

### Setup RustDesk Server (Opsional)
Jika ingin self-hosted relay:
1. Sewa VPS dengan IP public
2. Install RustDesk server
3. Konfigurasi client untuk pakai server sendiri

### Workflow Support
```
1. User lapor masalah via WhatsApp
   "Pak, aplikasi error pas export Excel"

2. Minta informasi awal
   - Screenshot error
   - Kode error dari GlitchTip (jika ada)
   - Langkah yang dilakukan sebelum error

3. Jika perlu remote:
   - Minta user install RustDesk (dari paket distribusi)
   - Minta ID RustDesk
   - Request koneksi
   - User approve koneksi

4. Selesaikan masalah
   - Cek log di C:\ProgramData\Simanis62\logs\
   - Cek database integrity
   - Fix atau workaround

5. Dokumentasi
   - Catat masalah dan solusi
   - Jika bug, buat issue di GitHub
   - Jika perlu update, deploy via Velopack
```

### Etika Remote Support
- ✅ Minta izin sebelum akses
- ✅ Jelaskan apa yang sedang dilakukan
- ✅ Disconnect setelah selesai
- ❌ Jangan akses file pribadi user
- ❌ Jangan install software tanpa izin
- ❌ Jangan remote tanpa user di depan PC

## Update Distribution (Velopack)

### Cara Kerja Velopack
1. Build versi baru
2. Generate delta update (hanya perubahan)
3. Upload ke update server
4. Aplikasi user auto-detect update
5. User konfirmasi → download → install → restart

### Proses Release Update
```bash
# 1. Update version di project
# 2. Build release
cd frontend/Simanis62.WPF
dotnet publish -c Release -r win-x64 --self-contained

# 3. Generate Velopack update
vpk pack --packId Simanis62 --packVersion 2.0.1 --packDir publish/

# 4. Upload ke update server
vpk upload --channel stable
```

### Rollback Jika Update Bermasalah
Velopack support rollback otomatis:
1. User buka aplikasi
2. Jika crash, Velopack auto-rollback ke versi sebelumnya
3. User bisa pakai versi lama sambil menunggu fix

## Komunikasi dengan User

### Template WhatsApp

**Konfirmasi Masalah**
```
Terima kasih sudah menghubungi support SIMANIS62.

Untuk membantu menyelesaikan masalah, mohon kirimkan:
1. Screenshot error
2. Langkah yang dilakukan sebelum error
3. Versi aplikasi (lihat di menu About)

Terima kasih 🙏
```

**Request Remote Support**
```
Untuk menyelesaikan masalah ini, saya perlu remote ke komputer Bapak/Ibu.

Langkah-langkah:
1. Buka aplikasi RustDesk (sudah terinstall bersama SIMANIS62)
2. Kirimkan ID yang muncul di RustDesk
3. Saya akan request koneksi
4. Klik "Accept" untuk mengizinkan

Apakah sekarang waktu yang tepat untuk remote?
```

**Konfirmasi Selesai**
```
Masalah sudah selesai diperbaiki ✅

Ringkasan:
- Masalah: [deskripsi masalah]
- Solusi: [apa yang dilakukan]

Jika ada masalah lain, silakan hubungi kembali.
Terima kasih 🙏
```

## Log Files

### Lokasi Log
```
C:\ProgramData\Simanis62\logs\
├── simanis62.log           # Backend log
├── simanis62-wpf.log       # Frontend log
└── simanis62-wpf-20260109.log  # Rotated log
```

### Cara Baca Log
```
2026-01-09 10:30:45 - simanis62 - INFO - Login success: admin
2026-01-09 10:31:02 - simanis62 - INFO - Created aset: 550e8400-e29b-41d4-a716-446655440000
2026-01-09 10:32:15 - simanis62 - ERROR - Failed to export: Database locked
```

### Minta Log dari User
```
Mohon kirimkan file log untuk investigasi:

1. Buka File Explorer
2. Ketik di address bar: C:\ProgramData\Simanis62\logs
3. Kirimkan file simanis62.log dan simanis62-wpf.log

Terima kasih 🙏
```

## Database Maintenance

### Backup Otomatis
- Aplikasi backup database setiap hari
- Disimpan di `C:\ProgramData\Simanis62\backups\`
- Retain 7 hari terakhir

### Cek Integrity Database

**Via DBHub (Recommended)**:
```
1. Start DBHub: .\scripts\start_dbhub.ps1
2. Open workbench: http://localhost:8080
3. Select production database (read-only)
4. Run query: PRAGMA integrity_check;
5. Verify results
```

**Via Kiro MCP**:
```
User: "Check database integrity for production"
Kiro: [calls mcp_dbhub_execute_sql_production with sql="PRAGMA integrity_check;"]
```

**Via SQLite CLI**:
```sql
-- Jalankan di SQLite CLI atau DB Browser
PRAGMA integrity_check;
```

### Debug Database Issues dengan DBHub

DBHub sangat berguna untuk:
- **Explore schema**: List tables, columns, indexes
- **Test queries**: Verify query results sebelum implement di code
- **Check data**: Verify data integrity dan relationships
- **Performance**: Use EXPLAIN QUERY PLAN untuk optimization

**Setup DBHub**: Lihat `.kiro/steering/DBHUB_GUIDE.md`

### Vacuum Database (Jika Lambat)
```sql
VACUUM;
```

### Recovery dari Backup
1. Tutup aplikasi
2. Rename database lama
3. Copy backup ke lokasi database
4. Buka aplikasi

## Checklist Maintenance Bulanan

- [ ] Cek dashboard GlitchTip, resolve old issues
- [ ] Review log files, hapus yang > 30 hari
- [ ] Cek disk space di VPS GlitchTip
- [ ] Test backup & recovery
- [ ] Update dependencies jika ada security patch
- [ ] Backup konfigurasi GlitchTip dan RustDesk server

## Referensi

#[[file:AGENTS.md]]
#[[file:.kiro/steering/deployment-guide.md]]
#[[file:.kiro/steering/security-policies.md]]
#[[file:.kiro/steering/DBHUB_GUIDE.md]]
