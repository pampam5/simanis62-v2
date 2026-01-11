# AGENTS.md - Dokumentasi

**Status**: READ-ONLY

---

## ⚠️ PERINGATAN

Folder `docs/` adalah **READ-ONLY**. Agent TIDAK BOLEH memodifikasi file di folder ini tanpa izin eksplisit dari user.

## Aturan Akses

| Aksi | Diizinkan? |
|------|------------|
| Membaca file | ✅ Ya |
| Memodifikasi file | ❌ Tidak |
| Menambah file baru | ❌ Tidak |
| Menghapus file | ❌ Tidak |

## Alasan

Folder `docs/` berisi dokumentasi yang sudah diverifikasi dan disetujui:
- Spesifikasi API (`api_contract.md`)
- Schema database (`data_schema.md`)
- Format KIB resmi (`format_kib_spesifikasi.md`)
- Regulasi dan aturan bisnis

Perubahan pada dokumentasi harus melalui proses review yang proper.

## Jika Perlu Update Dokumentasi

1. **Tanya user terlebih dahulu** - Jelaskan perubahan yang diperlukan
2. **Tunggu persetujuan** - User harus memberikan izin eksplisit
3. **Dokumentasikan perubahan** - Catat versi dan tanggal update

## File Penting di Folder Ini

| File | Keterangan |
|------|------------|
| `api_contract.md` | Spesifikasi endpoint REST API |
| `data_schema.md` | Schema database 11 tabel |
| `format_kib_spesifikasi.md` | Format KIB A-F BPAD DKI Jakarta (18 kolom untuk KIB B) |
| `tech_stack.md` | Arsitektur dan teknologi |
| `user_stories.md` | User stories dengan acceptance criteria |
| `STAKEHOLDERS.md` | Definisi role dan permissions |
| `Alur Kerja_Aturan Main.md` | Business rules dan validasi |

## Format KIB B (Referensi Cepat)

Format KIB B mengikuti standar **BPAD DKI Jakarta** dengan **18 kolom**:

| No | Kolom | Field Database |
|----|-------|----------------|
| 1 | NO. | auto-increment |
| 2 | KODE BARANG | kode_barang |
| 3 | REG. | nomor_register |
| 4 | JENIS BARANG | nama_barang |
| 5 | UKU-RAN | ukuran_cc |
| 6 | SATU-AN | satuan |
| 7 | TGL. OLEH | tanggal_perolehan |
| 8 | BA-HAN | bahan |
| 9 | MEREK | merk |
| 10 | TYPE | tipe |
| 11 | TGL. BPKB/DOK. | tanggal_dokumen |
| 12 | NO. CHASIS/RANGKA | nomor_rangka |
| 13 | NO. MESIN/PABRIK | nomor_mesin |
| 14 | NOMOR POLISI | nomor_polisi |
| 15 | ASAL OLEH | asal_usul |
| 16 | HARGA (Rp.) | harga |
| 17 | KAPITALISASI (Rp.) | kapitalisasi |
| 18 | TOTAL (Rp.) | total_harga |

> **PENTING**: Harga dalam **Rupiah penuh** (bukan ribuan)

---

*Sinkronisasi dengan: Root AGENTS.md v1.6*
