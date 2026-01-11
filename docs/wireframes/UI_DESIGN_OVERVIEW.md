# Rancangan Layar UI SIMANIS62 V2

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 9 Januari 2026 | UI/UX Designer | Rancangan UI berdasarkan 7 diagram UML |

---

## 1. Prinsip Desain UI

### 1.1 Prinsip Utama

| Prinsip | Implementasi | Alasan |
|---------|--------------|--------|
| **Jelas & Tepat** | Setiap elemen UI memiliki label deskriptif dan tujuan yang spesifik | User tahu apa yang harus dilakukan |
| **Sederhana** | Hanya tampilkan fitur yang relevan per role, hindari clutter | Tidak mengurangi fungsi inti sistem |
| **Mudah Dipahami** | Layout familiar (F-pattern), icons universal, Bahasa Indonesia | User dengan literasi teknis dasar-menengah dapat menggunakan |
| **Logis** | Alur kerja natural: Input → Proses → Output | Sesuai dengan mental model user |

### 1.2 Target User

- **Admin Sekolah:** Literasi teknis menengah, familiar dengan Excel
- **Guru (Viewer):** Literasi teknis dasar, perlu UI yang sangat intuitif
- **Kepala Sekolah:** Literasi teknis dasar-menengah, fokus pada laporan

---

## 2. Struktur Navigasi

### 2.1 Hierarki UI (3 Level)

```
Level 1: Login Screen (Entry Point)
    ↓
Level 2: Main Window (Persistent)
    ├── Header Bar (Fixed)
    ├── Sidebar Navigation (Fixed, Collapsible)
    └── Content Area (Dynamic)
        ↓
Level 3: Content Pages (Per Menu)
```

### 2.2 Sidebar Menu Structure

**Admin Sekolah:**
```
📊 Dashboard
📦 Aset
   ├── Daftar Aset
   └── Tambah Aset
📄 Laporan
   ├── KIB A (Tanah)
   ├── KIB B (Peralatan & Mesin)
   ├── KIB C (Gedung & Bangunan)
   ├── KIB D (Jalan, Irigasi, Jaringan)
   ├── KIB E (Aset Tetap Lainnya)
   ├── KIB F (Konstruksi dalam Pengerjaan)
   └── KIR (Per Ruangan)
🔄 Mutasi Aset
⚙️ Pengaturan
   ├── Manajemen User
   ├── Manajemen Ruangan
   └── Profil Saya
```

**Guru (Viewer):**
```
📊 Dashboard
📦 Aset (Read-only)
   └── Daftar Aset
📄 Laporan
   └── KIR (Per Ruangan)
⚙️ Pengaturan
   └── Profil Saya
```

**Kepala Sekolah:**
```
📊 Dashboard
📦 Aset (Read-only)
   └── Daftar Aset
📄 Laporan
   ├── KIB A-F (View & Export)
   └── KIR (Per Ruangan)
⚙️ Pengaturan
   └── Profil Saya
```

---

## 3. Layout Pattern Konsisten

### 3.1 Main Window Layout (1366x768 minimum)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER BAR (Height: 60px, Background: #2196F3)                 │
│ Logo | SIMANIS62 - [Nama Sekolah]    [User: Admin] [Logout]   │
└─────────────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────────────────────┐
│ SIDEBAR  │ CONTENT AREA                                         │
│ (250px)  │ ┌──────────────────────────────────────────────────┐ │
│          │ │ TITLE BAR (Height: 50px)                         │ │
│ [Menu 1] │ │ Breadcrumb: Home > Aset > Daftar                 │ │
│ [Menu 2] │ │                          [Action Buttons]        │ │
│ [Menu 3] │ └──────────────────────────────────────────────────┘ │
│ [Menu 4] │ ┌──────────────────────────────────────────────────┐ │
│ [Menu 5] │ │ MAIN CONTENT (Scrollable)                        │ │
│          │ │                                                  │ │
│          │ │ [Content varies per page]                        │ │
│          │ │                                                  │ │
│          │ │                                                  │ │
│          │ └──────────────────────────────────────────────────┘ │
│          │ ┌──────────────────────────────────────────────────┐ │
│          │ │ FOOTER (Height: 40px)                            │ │
│          │ │ Pagination / Info                                │ │
│          │ └──────────────────────────────────────────────────┘ │
└──────────┴──────────────────────────────────────────────────────┘
```

### 3.2 Color Scheme

| Warna | Hex Code | Penggunaan |
|-------|----------|------------|
| **Primary Blue** | #2196F3 | Header, Sidebar, Primary buttons |
| **Success Green** | #4CAF50 | Status Aktif, Success messages, Save buttons |
| **Warning Orange** | #FF9800 | Status Rusak, Warnings |
| **Danger Red** | #F44336 | Delete actions, Errors, Status Dihapus |
| **Neutral Gray** | #757575 | Text, Borders, Disabled elements |
| **Background White** | #FFFFFF | Content area, Cards |
| **Background Light** | #F5F5F5 | Alternating rows, Hover states |

### 3.3 Typography

| Element | Font Size | Weight | Color |
|---------|-----------|--------|-------|
| Page Title | 24px | Bold | #212121 |
| Section Header | 18px | Semibold | #424242 |
| Body Text | 14px | Regular | #757575 |
| Button Text | 14px | Medium | #FFFFFF |
| Caption/Helper | 12px | Regular | #9E9E9E |

---

## 4. Wireframe Layar Utama

### 4.1 Login Screen

**Tujuan:** Autentikasi user dengan username dan password
**Role Detection:** Otomatis berdasarkan data user di database

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    [Logo SIMANIS62]                         │
│                                                             │
│            Sistem Manajemen Aset Sekolah                    │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                                                       │  │
│  │  Username:  [_____________________________]          │  │
│  │                                                       │  │
│  │  Password:  [_____________________________]          │  │
│  │                                                       │  │
│  │  Role akan terdeteksi otomatis setelah login         │  │
│  │                                                       │  │
│  │              [      LOGIN      ]                     │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│                © 2026 SIMANIS62 V2                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Validasi:**
- Username: Required, min 3 karakter
- Password: Required, min 6 karakter
- Error message: "Username atau password salah" (tidak spesifik untuk keamanan)

**Alur:**
1. User input username & password
2. Klik LOGIN
3. Sistem validasi credentials
4. Jika valid → Redirect ke Dashboard
5. Jika invalid → Tampilkan error message

---

### 4.2 Dashboard (Admin Sekolah)

**Tujuan:** Overview cepat kondisi aset sekolah
**Prinsip:** Informasi penting di atas (F-pattern), visual cards untuk metrics

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: SIMANIS62 - SDN 01 Jakarta    [Admin: Budi] [Logout]   │
└─────────────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────────────────────┐
│ SIDEBAR  │ Dashboard                                            │
│          │ Home > Dashboard                                     │
│ Dashboard│ ─────────────────────────────────────────────────    │
│ Aset     │                                                      │
│ Laporan  │ RINGKASAN ASET                                       │
│ Mutasi   │ ┌──────────┬──────────┬──────────┬──────────┐       │
│ Pengatur │ │ Total    │ Aktif    │ Rusak    │ Mutasi   │       │
│          │ │ 1,234    │ 1,150    │ 75       │ 9        │       │
│          │ │ aset     │ aset     │ aset     │ proses   │       │
│          │ └──────────┴──────────┴──────────┴──────────┘       │
│          │                                                      │
│          │ DISTRIBUSI PER KIB                                   │
│          │ ┌────────────────────────────────────────────┐       │
│          │ │ KIB A (Tanah)              : 15 aset       │       │
│          │ │ KIB B (Peralatan & Mesin)  : 850 aset      │       │
│          │ │ KIB C (Gedung & Bangunan)  : 25 aset       │       │
│          │ │ KIB D (Jalan, Irigasi)     : 10 aset       │       │
│          │ │ KIB E (Aset Tetap Lainnya) : 300 aset      │       │
│          │ │ KIB F (Konstruksi)         : 34 aset       │       │
│          │ └────────────────────────────────────────────┘       │
│          │                                                      │
│          │ TOTAL NILAI ASET                                     │
│          │ ┌────────────────────────────────────────────┐       │
│          │ │ Rp 15,750,000,000                          │       │
│          │ └────────────────────────────────────────────┘       │
│          │                                                      │
│          │ MUTASI TERBARU (5 terakhir)                         │
│          │ ┌────────────────────────────────────────────┐       │
│          │ │ Laptop HP → Lab Komputer (05/01/2026)      │       │
│          │ │ Proyektor → Ruang Kelas 1A (04/01/2026)    │       │
│          │ │ Meja Guru → Ruang Guru (03/01/2026)        │       │
│          │ └────────────────────────────────────────────┘       │
└──────────┴──────────────────────────────────────────────────────┘
```

**Komponen:**
- 4 Metric Cards (Total, Aktif, Rusak, Mutasi) dengan warna berbeda
- Bar chart atau list untuk distribusi per KIB
- Total nilai aset (highlight dengan font besar)
- List mutasi terbaru (5 item, link ke detail)

**Interaksi:**
- Klik metric card → Filter daftar aset sesuai status
- Klik KIB category → Lihat daftar aset KIB tersebut
- Klik mutasi item → Lihat detail mutasi

---

### 4.3 Daftar Aset (dengan Filter & Search)

**Tujuan:** Menampilkan semua aset dengan kemampuan filter dan search
**Prinsip:** Filter di atas, table di tengah, pagination di bawah

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: SIMANIS62 - SDN 01 Jakarta    [Admin: Budi] [Logout]   │
└─────────────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────────────────────┐
│ SIDEBAR  │ Daftar Aset                    [+ Tambah Aset]       │
│          │ Home > Aset > Daftar Aset                            │
│ Dashboard│ ─────────────────────────────────────────────────    │
│ Aset     │                                                      │
│ Laporan  │ FILTER & PENCARIAN                                   │
│ Mutasi   │ ┌────────────────────────────────────────────┐       │
│ Pengatur │ │ Kata Kunci: [____________] [Cari]          │       │
│          │ │                                            │       │
│          │ │ KIB: [Semua ▼] Ruangan: [Semua ▼]         │       │
│          │ │ Kondisi: [Semua ▼] Status: [Semua ▼]      │       │
│          │ │                                            │       │
│          │ │ [Reset Filter]                             │       │
│          │ └────────────────────────────────────────────┘       │
│          │                                                      │
│          │ HASIL: 125 aset ditemukan                            │
│          │ ┌────────────────────────────────────────────┐       │
│          │ │Kode    │Nama      │KIB│Ruangan │Kondisi│  │       │
│          │ ├────────┼──────────┼───┼────────┼───────┤  │       │
│          │ │32.01.02│Laptop HP │ B │Lab Komp│Baik   │👁│       │
│          │ │32.01.03│Proyektor │ B │Kelas 1A│Baik   │👁│       │
│          │ │11.02.01│Tanah     │ A │-       │Baik   │👁│       │
│          │ │...     │...       │...│...     │...    │  │       │
│          │ └────────────────────────────────────────────┘       │
│          │                                                      │
│          │ [< Prev] Halaman 1 dari 5 [Next >]                  │
└──────────┴──────────────────────────────────────────────────────┘
```

**Komponen:**
- Search box (kata kunci)
- 4 Dropdown filters (KIB, Ruangan, Kondisi, Status)
- Reset filter button
- Result count
- Data table dengan columns: Kode, Nama, KIB, Ruangan, Kondisi, Actions
- Pagination (100 items per page)
- Action button: 👁 (View detail)

**Interaksi:**
- Ketik kata kunci → Auto-search setelah 500ms
- Pilih filter → Auto-refresh table
- Klik Reset → Clear semua filter
- Klik row atau 👁 → Lihat detail aset
- Klik [+ Tambah Aset] → Form tambah aset

**Validasi:**
- Minimal 1 filter atau kata kunci untuk search
- Jika tidak ada hasil → Tampilkan "Tidak ada aset yang sesuai"

---

### 4.4 Form Tambah Aset (Dinamis per KIB)

**Tujuan:** Input data aset baru dengan validasi real-time
**Prinsip:** Form wizard 2-step (Pilih KIB → Isi Detail), validasi inline

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: SIMANIS62 - SDN 01 Jakarta    [Admin: Budi] [Logout]   │
└─────────────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────────────────────┐
│ SIDEBAR  │ Tambah Aset Baru                                     │
│          │ Home > Aset > Tambah Aset                            │
│ Dashboard│ ─────────────────────────────────────────────────    │
│ Aset     │                                                      │
│ Laporan  │ STEP 1: PILIH KATEGORI KIB                           │
│ Mutasi   │ ┌────────────────────────────────────────────┐       │
│ Pengatur │ │ ○ KIB A - Tanah                            │       │
│          │ │ ● KIB B - Peralatan dan Mesin              │       │
│          │ │ ○ KIB C - Gedung dan Bangunan              │       │
│          │ │ ○ KIB D - Jalan, Irigasi, dan Jaringan     │       │
│          │ │ ○ KIB E - Aset Tetap Lainnya               │       │
│          │ │ ○ KIB F - Konstruksi dalam Pengerjaan      │       │
│          │ └────────────────────────────────────────────┘       │
│          │                                                      │
│          │ STEP 2: ISI DATA ASET (KIB B)                        │
│          │ ┌────────────────────────────────────────────┐       │
│          │ │ DATA UMUM (Semua KIB)                      │       │
│          │ │ Kode Barang*: [__________] (XX.XX.XX.XXXX) │       │
│          │ │ Nama Barang*: [__________________________] │       │
│          │ │ Tahun Perolehan*: [____] (1900-2026)       │       │
│          │ │ Asal Usul*: [Pembelian ▼]                  │       │
│          │ │ Harga*: [Rp __________]                    │       │
│          │ │ Kondisi*: [Baik ▼]                         │       │
│          │ │ Ruangan*: [Lab Komputer ▼]                 │       │
│          │ │ Keterangan: [_________________________]    │       │
│          │ │                                            │       │
│          │ │ DATA KHUSUS KIB B                          │       │
│          │ │ Merk/Type*: [__________________________]   │       │
│          │ │ Ukuran/CC: [__________________________]    │       │
│          │ │ Bahan: [__________________________]        │       │
│          │ │                                            │       │
│          │ │ * = Field wajib                            │       │
│          │ │                                            │       │
│          │ │ [Batal]              [Simpan]              │       │
│          │ └────────────────────────────────────────────┘       │
└──────────┴──────────────────────────────────────────────────────┘
```

**Komponen:**
- Radio buttons untuk pilih KIB (Step 1)
- Form fields dinamis berdasarkan KIB yang dipilih (Step 2)
- Field wajib ditandai dengan * (asterisk)
- Inline validation dengan icon ✓ atau ✗
- Helper text di bawah field (format, range)
- 2 Buttons: Batal (abu-abu), Simpan (hijau)

**Validasi Real-time:**
- Kode Barang: Format XX.XX.XX.XXXX, unique check
- Nama Barang: 3-200 karakter
- Tahun: 1900 - tahun sekarang
- Harga: Angka positif, tidak nol
- Merk/Type (KIB B): Wajib diisi

**Alur:**
1. Pilih kategori KIB (radio button)
2. Form fields muncul sesuai KIB
3. Isi field wajib (validasi inline)
4. Klik Simpan → Validasi semua field
5. Jika valid → Simpan ke database, generate Nomor Register
6. Jika invalid → Highlight field error, tampilkan pesan
7. Success → Redirect ke detail aset, tampilkan notifikasi

**Field Khusus per KIB:**
- **KIB A:** Luas (m²), Alamat/Lokasi
- **KIB B:** Merk/Type, Ukuran/CC, Bahan
- **KIB C:** Luas (m²), Alamat/Lokasi, Bertingkat
- **KIB D:** Panjang (m), Lebar (m), Alamat/Lokasi
- **KIB E:** Judul/Nama, Penerbit
- **KIB F:** Alamat/Lokasi, Persentase Selesai (%)

---

### 4.5 Detail Aset (dengan Riwayat Mutasi)

**Tujuan:** Menampilkan informasi lengkap aset dan riwayat perubahan
**Prinsip:** Read-only view dengan action buttons di top-right

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: SIMANIS62 - SDN 01 Jakarta    [Admin: Budi] [Logout]   │
└─────────────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────────────────────┐
│ SIDEBAR  │ Detail Aset                [Edit] [Mutasi] [Hapus]   │
│          │ Home > Aset > Detail > 32.01.02.0001                 │
│ Dashboard│ ─────────────────────────────────────────────────    │
│ Aset     │                                                      │
│ Laporan  │ INFORMASI ASET                                       │
│ Mutasi   │ ┌────────────────────────────────────────────┐       │
│ Pengatur │ │ Nomor Register: 1                          │       │
│          │ │ Kode Barang: 32.01.02.0001                 │       │
│          │ │ Nama Barang: Laptop HP Pavilion 14         │       │
│          │ │ Kategori KIB: B (Peralatan dan Mesin)      │       │
│          │ │                                            │       │
│          │ │ Status: [Aktif] Kondisi: [Baik]            │       │
│          │ │                                            │       │
│          │ │ Tahun Perolehan: 2024                      │       │
│          │ │ Asal Usul: Pembelian                       │       │
│          │ │ Harga: Rp 8,500,000                        │       │
│          │ │ Ruangan: Lab Komputer                      │       │
│          │ │                                            │       │
│          │ │ DATA KHUSUS KIB B                          │       │
│          │ │ Merk/Type: HP Pavilion 14                  │       │
│          │ │ Ukuran/CC: 14 inch                         │       │
│          │ │ Bahan: Plastik/Metal                       │       │
│          │ │                                            │       │
│          │ │ Keterangan: Laptop untuk praktikum siswa   │       │
│          │ │                                            │       │
│          │ │ Dibuat: 05/01/2026 oleh Admin Budi         │       │
│          │ │ Diupdate: 05/01/2026 oleh Admin Budi       │       │
│          │ └────────────────────────────────────────────┘       │
│          │                                                      │
│          │ RIWAYAT MUTASI (2 kali)                              │
│          │ ┌────────────────────────────────────────────┐       │
│          │ │ 05/01/2026: Ruang Guru → Lab Komputer      │       │
│          │ │ Alasan: Untuk praktikum siswa              │       │
│          │ │ Kondisi: Baik | Oleh: Admin Budi           │       │
│          │ │                                            │       │
│          │ │ 01/01/2026: Gudang → Ruang Guru            │       │
│          │ │ Alasan: Distribusi awal                    │       │
│          │ │ Kondisi: Baik | Oleh: Admin Budi           │       │
│          │ └────────────────────────────────────────────┘       │
└──────────┴──────────────────────────────────────────────────────┘
```

**Komponen:**
- Info panel dengan semua field aset (read-only)
- Status badge dengan warna (Aktif=hijau, Rusak=oranye, Dihapus=abu)
- Kondisi badge dengan warna
- Data khusus per KIB (conditional)
- Metadata (created_at, updated_at, user)
- Riwayat mutasi (timeline format)
- 3 Action buttons (top-right): Edit, Mutasi, Hapus

**Interaksi:**
- Klik [Edit] → Form edit aset (pre-filled)
- Klik [Mutasi] → Form mutasi aset
- Klik [Hapus] → Konfirmasi dialog → Soft delete
- Klik riwayat mutasi item → Expand detail

**Conditional Display:**
- Jika status "Mutasi" → Tampilkan info mutasi yang sedang berjalan
- Jika status "Dihapus" → Disable Edit & Mutasi, tampilkan info penghapusan
- Jika role Viewer → Hide action buttons

---

