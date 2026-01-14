# Semantic Analysis - Dokumentasi SIMANIS62 V2

**Tanggal Analisis:** 13 Januari 2026
**Total File Markdown:** 14 file utama + 2 wireframe files
**Total Lines:** ~15,000+ lines

---

## 1. Ringkasan Dokumen

### 1.1 Dokumen Arsitektur & Bisnis (5 files)

| File | Lines | Fokus Utama |
|------|-------|-------------|
| `Tujuan Bisnis_Peta Pemangku Kepentingan_Kendala & Asumsi.md` | 212 | Tujuan bisnis, stakeholders, kendala teknis |
| `Pemilik Kebenaran_Masalah Inti yang Diselesaikan_Konteks & Batasan.md` | 346 | SSOT, masalah inti, batasan lingkup, risiko |
| `STAKEHOLDERS.md` | 401 | Detail 3 role utama + stakeholder sekunder |
| `tech_stack.md` | 822 | Tech stack lengkap, deployment, tools |
| `SSOT_Report.md` | 91 | Verifikasi konsistensi dokumentasi |

### 1.2 Dokumen Teknis (5 files)

| File | Lines | Fokus Utama |
|------|-------|-------------|
| `api_contract.md` | 2542 | REST API endpoints, request/response schemas |
| `data_schema.md` | 2293 | 11 tabel database, SQLModel definitions |
| `format_kib_spesifikasi.md` | 450 | Format KIB A-F BPAD DKI Jakarta (18 kolom) |
| `UML_Diagram_Guidelines.md` | 471 | Panduan pembuatan 7 UML diagram |
| `RESEARCH_REPORT_KIB_FORMAT.md` | 216 | Riset format KIB B terverifikasi |

### 1.3 Dokumen Fungsional (2 files)

| File | Lines | Fokus Utama |
|------|-------|-------------|
| `Alur Kerja_Aturan Main.md` | 1741 | Business rules, state transitions, workflows |
| `user_stories.md` | 1854 | 19 user stories dengan acceptance criteria |

### 1.4 Dokumen UI/UX (2 files)

| File | Lines | Fokus Utama |
|------|-------|-------------|
| `wireframes/UI_DESIGN_OVERVIEW.md` | 463 | Wireframes, layout, navigation |
| `wireframes/UI_DESIGN_SPECIFICATION.md` | 1 | (Placeholder) |

---

## 2. Konsistensi Antar Dokumen

### 2.1 Konsistensi TERKONFIRMASI ✅

| Aspek | Nilai Konsisten | Dokumen Referensi |
|-------|-----------------|-------------------|
| **Database** | SQLite 3 + WAL mode | tech_stack.md, data_schema.md |
| **Backend** | Python 3.12 + FastAPI | tech_stack.md, api_contract.md |
| **Frontend** | WPF .NET 8 | tech_stack.md |
| **Format KIB B** | 18 kolom BPAD DKI Jakarta | format_kib_spesifikasi.md, RESEARCH_REPORT.md |
| **Jumlah Tabel** | 11 tabel | data_schema.md |
| **Role Sistem** | 2 technical (Admin, Viewer) + 3 business | STAKEHOLDERS.md, api_contract.md |
| **Harga** | Rupiah penuh (bukan ribuan) | format_kib_spesifikasi.md |

### 2.2 Naming Convention TERKONFIRMASI ✅

| Konteks | Konvensi | Contoh |
|---------|----------|--------|
| Database fields | snake_case Indonesia | `nomor_register`, `dapat_ekspor` |
| Class names | PascalCase English | `AssetService`, `UserRole` |
| API endpoints | kebab-case English | `/api/v1/aset`, `/api/v1/mutasi` |
| Enum values | TitleCase Indonesia | `"Aktif"`, `"Rusak Ringan"` |

---

## 3. Entitas Utama

### 3.1 Database Schema (11 Tabel)

1. **users** - Authentication & authorization (9 kolom)
2. **ruangan** - Room/location management (6 kolom)
3. **aset** - Main asset table (19 kolom)
4. **aset_kib_a** - KIB A Tanah (4 kolom)
5. **aset_kib_b** - KIB B Peralatan & Mesin (12 kolom) ⭐ MVP
6. **aset_kib_c** - KIB C Gedung & Bangunan (4 kolom)
7. **aset_kib_d** - KIB D Jalan, Irigasi, Jaringan (4 kolom)
8. **aset_kib_e** - KIB E Aset Tetap Lainnya (3 kolom)
9. **aset_kib_f** - KIB F Konstruksi dalam Pengerjaan (3 kolom)
10. **riwayat_mutasi** - Asset movement history (12 kolom)
11. **audit_trail** - Complete audit log (9 kolom)

### 3.2 Status Aset (State Machine)

```
Baru → Aktif → Mutasi → Aktif
         ↓         ↓
       Rusak ← ← ←
         ↓
      Dihapus (soft delete)
```

### 3.3 Kondisi Aset

- Baik (🟢)
- Rusak Ringan (🟡)
- Rusak Berat (🔴)

---

## 4. API Endpoints Summary

### 4.1 Authentication
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### 4.2 Users
- `GET /api/v1/users`
- `POST /api/v1/users`
- `GET /api/v1/users/{id}`
- `PUT /api/v1/users/{id}`
- `DELETE /api/v1/users/{id}`

### 4.3 Ruangan
- `GET /api/v1/ruangan`
- `POST /api/v1/ruangan`
- `GET /api/v1/ruangan/{id}`
- `PUT /api/v1/ruangan/{id}`
- `DELETE /api/v1/ruangan/{id}`

### 4.4 Aset
- `GET /api/v1/aset`
- `POST /api/v1/aset`
- `GET /api/v1/aset/{id}`
- `PUT /api/v1/aset/{id}`
- `DELETE /api/v1/aset/{id}`
- `GET /api/v1/aset/search`

### 4.5 Mutasi
- `GET /api/v1/mutasi`
- `POST /api/v1/mutasi`
- `PUT /api/v1/mutasi/{id}/selesai`
- `PUT /api/v1/mutasi/{id}/batal`

### 4.6 Reports
- `GET /api/v1/reports/kib/{kategori}`
- `GET /api/v1/reports/kir/{ruangan_id}`
- `GET /api/v1/reports/export/{type}`

---

## 5. Business Rules Kunci

### 5.1 Validasi Aset
- Kode Barang: Format XX.XX.XX.XXXX (13 char), unique
- Nama Barang: 3-200 karakter
- Tahun Perolehan: 1900 - tahun sekarang
- Harga: Positif, max 999,999,999,999 (Rupiah penuh)
- Nomor Register: Auto-generated per kategori KIB

### 5.2 Mutasi Rules
- Aset hanya bisa dimutasi jika status "Aktif"
- Satu aset hanya bisa memiliki 1 mutasi pending
- Mutasi harus dikonfirmasi dalam 7 hari
- Riwayat mutasi tidak dapat dihapus (audit trail)

### 5.3 Soft Delete Rules
- Aset dengan status "Mutasi" tidak dapat dihapus
- Alasan penghapusan wajib (min 20 karakter)
- Data tidak benar-benar dihapus dari database

### 5.4 Authorization
- Admin: Full CRUD, Reports, Export, User Management
- Viewer: Read-only, Search
- Kepala Sekolah: Viewer + `dapat_ekspor=true`

---

## 6. Performance Targets

| Operasi | Target |
|---------|--------|
| Search aset | < 5 detik |
| Generate KIB | < 10 detik |
| Export Excel | < 15 detik |
| Login | < 2 detik |
| Detail view | < 2 detik |

---

## 7. Fitur yang TIDAK Diimplementasi (Batasan Lingkup)

1. Integrasi SIMBADA
2. Perhitungan depresiasi/penyusutan
3. Workflow persetujuan penghapusan
4. Pemeliharaan dan perbaikan aset
5. Peminjaman aset
6. Notifikasi otomatis
7. Dashboard visualisasi data (post-MVP)

---

## 8. Regulasi Acuan

### 8.1 Nasional
- Permendagri No. 19/2016 (Pedoman Pengelolaan BMD)
- Permendagri No. 47/2021 (Perubahan)
- Permendagri No. 7/2024 (Perubahan Kedua)

### 8.2 DKI Jakarta (PRIORITAS)
- Pergub DKI No. 67/2022
- Kepgub DKI No. 52/2023
- Insekda DKI No. 11/2024 (KIB B)
- Insekda DKI No. 20/2025 (KIB E & ATB)

---

## 9. Kesimpulan Semantic Analysis

### 9.1 Kekuatan Dokumentasi
- ✅ Konsistensi tinggi antar dokumen
- ✅ Detail teknis lengkap (API, schema, validasi)
- ✅ Business rules terdefinisi jelas
- ✅ Format KIB terverifikasi dari sumber resmi
- ✅ User stories dengan acceptance criteria

### 9.2 Area yang Perlu Perhatian
- ⚠️ UI_DESIGN_SPECIFICATION.md masih placeholder
- ⚠️ Beberapa diagram UML belum dibuat (hanya guidelines)
- ⚠️ Test cases belum terdokumentasi

### 9.3 Rekomendasi untuk Implementasi
1. Prioritaskan KIB B (18 kolom) untuk MVP
2. Implementasi backend API terlebih dahulu
3. Gunakan SQLite WAL mode untuk concurrency
4. Ikuti naming convention yang sudah ditetapkan
5. Validasi format kode barang (13 karakter)

---

*Analisis ini dapat digunakan sebagai referensi untuk implementasi specs.*
