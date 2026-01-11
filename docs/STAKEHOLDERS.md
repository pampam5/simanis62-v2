# Dokumentasi Pemangku Kepentingan (Stakeholders)
## Simanis62 V2 - Sistem Manajemen Aset Sekolah

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 5 Januari 2026 | Architecture Engineer | Dokumen awal stakeholder |

---

## 1. Pendahuluan

Dokumen ini mendefinisikan semua pemangku kepentingan (stakeholders) dalam sistem Simanis62 V2, termasuk peran, tanggung jawab, kebutuhan, dan tingkat keterlibatan masing-masing.

---

## 2. Klasifikasi Stakeholder

### 2.1 Stakeholder Primer (Primary)

Stakeholder yang **langsung menggunakan** sistem dan memiliki interaksi harian dengan aplikasi.

### 2.2 Stakeholder Sekunder (Secondary)

Stakeholder yang **tidak langsung menggunakan** sistem namun terpengaruh oleh output atau memiliki kepentingan terhadap sistem.

### 2.3 Stakeholder Tersier (Tertiary)

Stakeholder yang **mendukung** implementasi dan pemeliharaan sistem.

---

## 3. Stakeholder Primer (Primary)

### 3.1 Admin Sekolah

**Deskripsi:**
Pengguna utama sistem yang bertanggung jawab mengelola seluruh data aset sekolah.

**Peran:**
- Operator utama sistem
- Data entry dan maintenance
- Pembuat laporan KIB

**Tanggung Jawab:**
- Mencatat aset baru yang masuk ke sekolah
- Mengupdate kondisi dan status aset
- Mencatat mutasi aset antarruangan
- Membuat dan mengekspor laporan KIB A-F
- Mengelola user Viewer (Guru)
- Melakukan soft delete aset yang sudah tidak digunakan

**Kebutuhan Utama:**
- Antarmuka yang sederhana dan intuitif
- Proses input data yang cepat (< 2 menit per aset)
- Validasi otomatis untuk mencegah kesalahan input
- Ekspor laporan ke Excel dengan 1 klik
- Pencarian aset yang cepat (< 5 detik)

**Hak Akses:**
- ✅ Full CRUD (Create, Read, Update, Delete) data aset
- ✅ Generate dan ekspor semua laporan KIB dan KIR
- ✅ Mutasi dan soft delete aset
- ✅ Manajemen user Viewer

**Frekuensi Penggunaan:** Harian (2-4 jam per hari)

**Tingkat Literasi Teknis:** Menengah (familiar dengan Excel dan aplikasi desktop)

**Pain Points Saat Ini:**
- Pencatatan manual di Excel memakan waktu
- Sering terjadi duplikasi data
- Sulit melacak riwayat perpindahan aset
- Pembuatan laporan KIB memakan waktu 2-3 hari

---

### 3.2 Guru (Viewer)

**Deskripsi:**
Pengguna dengan hak akses read-only yang perlu melihat aset di ruangan tertentu.

**Peran:**
- Pengawas aset di ruangan
- Pelapor kondisi aset

**Tanggung Jawab:**
- Melihat daftar aset di ruangan yang dikelola
- Melaporkan kondisi aset yang rusak kepada Admin
- Memverifikasi keberadaan aset saat inventarisasi

**Kebutuhan Utama:**
- Akses informasi aset yang mudah dan cepat
- Tampilan KIR (Kartu Inventaris Ruangan) per ruangan
- Pencarian aset berdasarkan nama atau kode

**Hak Akses:**
- ✅ Read-only data aset
- ✅ Pencarian aset
- ✅ Lihat KIR per ruangan
- ❌ Tidak bisa CRUD, mutasi, atau delete

**Frekuensi Penggunaan:** Mingguan (15-30 menit per minggu)

**Tingkat Literasi Teknis:** Dasar (familiar dengan aplikasi sederhana)

**Pain Points Saat Ini:**
- Tidak tahu aset apa saja yang ada di ruangan
- Sulit melaporkan aset rusak karena tidak tahu kode barang

---

### 3.3 Kepala Sekolah

**Deskripsi:**
Pengguna dengan hak akses view dan export yang perlu mengawasi pengelolaan aset dan menandatangani laporan.

**Peran:**
- Pengawas pengelolaan aset
- Penandatangan laporan KIB

**Tanggung Jawab:**
- Mengawasi pengelolaan aset sekolah
- Mereview laporan KIB sebelum dikirim ke Dinas
- Menandatangani laporan KIB
- Memastikan akurasi data aset

**Kebutuhan Utama:**
- Laporan yang akurat dan lengkap
- Ekspor laporan untuk review offline
- Dashboard ringkasan (opsional, future feature)

**Hak Akses:**
- ✅ Read-only data aset
- ✅ Lihat semua laporan KIB dan KIR
- ✅ Ekspor laporan untuk review
- ❌ Tidak bisa CRUD, mutasi, atau delete

**Catatan Implementasi (v2.0):**
Dalam implementasi, Kepala Sekolah menggunakan role **"Viewer"** dengan flag tambahan `dapat_ekspor=true` di tabel `users`. Ini adalah keputusan desain untuk menyederhanakan sistem dengan hanya 2 technical roles (Admin, Viewer) yang mendukung 3 business roles. Jika diperlukan, role terpisah "Kepala Sekolah" dapat ditambahkan di versi mendatang tanpa breaking changes.

**Frekuensi Penggunaan:** Bulanan (1-2 jam per bulan, saat pelaporan)

**Tingkat Literasi Teknis:** Dasar-Menengah

**Pain Points Saat Ini:**
- Laporan KIB sering terlambat
- Sulit memverifikasi akurasi data
- Tidak ada ringkasan cepat kondisi aset

---

## 4. Stakeholder Sekunder (Secondary)

### 4.1 Dinas Pendidikan

**Deskripsi:**
Instansi pemerintah yang menerima laporan KIB dari sekolah.

**Peran:**
- Penerima laporan KIB
- Pengawas pengelolaan BMD sekolah

**Tanggung Jawab:**
- Menerima dan memverifikasi laporan KIB dari sekolah
- Mengkonsolidasi data aset dari semua sekolah
- Melaporkan ke tingkat provinsi/pusat

**Kebutuhan Utama:**
- Format laporan sesuai Permendagri 19/2016
- Laporan dalam format Excel yang dapat diolah
- Data akurat dan tepat waktu

**Hak Akses:** Tidak ada (menerima laporan eksternal)

**Frekuensi Interaksi:** Triwulanan/Tahunan (saat pelaporan)

**Ekspektasi:**
- Laporan KIB sesuai format standar
- Data lengkap dan akurat
- Tepat waktu (sesuai deadline pelaporan)

---

### 4.2 BPK/BPKP (Badan Pemeriksa Keuangan)

**Deskripsi:**
Auditor eksternal yang memeriksa pengelolaan Barang Milik Daerah (BMD).

**Peran:**
- Auditor pengelolaan BMD
- Pemeriksa kepatuhan regulasi

**Tanggung Jawab:**
- Audit pengelolaan aset sekolah
- Verifikasi keberadaan fisik aset
- Pemeriksaan kepatuhan terhadap Permendagri 19/2016

**Kebutuhan Utama:**
- Audit trail lengkap (siapa, kapan, apa yang diubah)
- Riwayat mutasi aset yang jelas
- Data penghapusan aset dengan alasan

**Hak Akses:** Tidak ada (akses saat audit dengan pendampingan)

**Frekuensi Interaksi:** Tahunan (saat audit)

**Ekspektasi:**
- Audit trail lengkap dan tidak dapat diubah
- Riwayat perubahan data tersimpan
- Kepatuhan terhadap regulasi

---

### 4.3 Pemerintah Daerah (Pemda)

**Deskripsi:**
Pemilik legal Barang Milik Daerah (BMD) yang dikelola sekolah.

**Peran:**
- Pemilik aset (BMD)
- Pembuat kebijakan pengelolaan aset

**Tanggung Jawab:**
- Menetapkan kebijakan pengelolaan BMD
- Menyediakan anggaran pengadaan aset
- Monitoring kondisi aset daerah

**Kebutuhan Utama:**
- Laporan kondisi aset daerah
- Data akurat untuk perencanaan anggaran
- Transparansi pengelolaan BMD

**Hak Akses:** Tidak ada (menerima laporan konsolidasi dari Dinas)

**Frekuensi Interaksi:** Tahunan (saat pelaporan dan perencanaan anggaran)

**Ekspektasi:**
- Data aset akurat dan terkini
- Transparansi pengelolaan
- Kepatuhan terhadap regulasi

---

## 5. Stakeholder Tersier (Tertiary)

### 5.1 Tim Pengembang

**Deskripsi:**
Tim yang membangun dan memelihara sistem Simanis62 V2.

**Peran:**
- Developer sistem
- Maintainer aplikasi

**Tanggung Jawab:**
- Membangun sistem sesuai spesifikasi
- Memperbaiki bug dan error
- Menambahkan fitur baru (jika diperlukan)
- Dokumentasi teknis

**Kebutuhan Utama:**
- Spesifikasi yang jelas dan tidak ambigu
- Dokumentasi arsitektur lengkap
- Feedback dari pengguna

**Hak Akses:** Full access (development environment)

**Frekuensi Interaksi:** Harian (selama development), Mingguan (maintenance)

**Ekspektasi:**
- Sistem sesuai spesifikasi
- Code quality tinggi
- Dokumentasi lengkap

---

### 5.2 Staf TI Sekolah

**Deskripsi:**
Staf yang menyediakan infrastruktur dan support teknis.

**Peran:**
- Penyedia infrastruktur
- Technical support

**Tanggung Jawab:**
- Menyediakan laptop/komputer untuk sistem
- Instalasi dan konfigurasi aplikasi
- Backup data berkala
- Troubleshooting masalah teknis

**Kebutuhan Utama:**
- Sistem ringan (dapat berjalan di laptop spesifikasi rendah)
- Instalasi mudah (tidak perlu konfigurasi kompleks)
- Dokumentasi instalasi yang jelas

**Hak Akses:** System admin (instalasi dan maintenance)

**Frekuensi Interaksi:** Mingguan (support), Bulanan (maintenance)

**Ekspektasi:**
- Sistem stabil dan reliable
- Instalasi mudah
- Minimal downtime

---

## 6. Matriks Stakeholder

### 6.1 Power-Interest Grid

| Stakeholder | Power | Interest | Strategi Engagement |
|-------------|-------|----------|---------------------|
| Admin Sekolah | HIGH | HIGH | **Manage Closely** - Involve in all decisions |
| Kepala Sekolah | HIGH | HIGH | **Manage Closely** - Regular updates |
| Guru (Viewer) | LOW | MEDIUM | **Keep Informed** - Training and support |
| Dinas Pendidikan | HIGH | MEDIUM | **Keep Satisfied** - Ensure compliance |
| BPK/BPKP | HIGH | LOW | **Keep Satisfied** - Audit trail ready |
| Pemerintah Daerah | HIGH | LOW | **Keep Satisfied** - Compliance |
| Tim Pengembang | MEDIUM | HIGH | **Manage Closely** - Clear requirements |
| Staf TI Sekolah | MEDIUM | MEDIUM | **Keep Informed** - Technical docs |

### 6.2 Tingkat Keterlibatan

| Stakeholder | Unaware | Resistant | Neutral | Supportive | Leading |
|-------------|---------|-----------|---------|------------|---------|
| Admin Sekolah | | | | | ✅ |
| Kepala Sekolah | | | | ✅ | |
| Guru (Viewer) | | | ✅ | | |
| Dinas Pendidikan | | | ✅ | | |
| BPK/BPKP | | | ✅ | | |
| Pemerintah Daerah | | | ✅ | | |
| Tim Pengembang | | | | | ✅ |
| Staf TI Sekolah | | | | ✅ | |

---

## 7. Komunikasi Stakeholder

### 7.1 Frekuensi Komunikasi

| Stakeholder | Frekuensi | Channel | Konten |
|-------------|-----------|---------|--------|
| Admin Sekolah | Harian | In-app, Email | Updates, Support |
| Kepala Sekolah | Mingguan | Email, Meeting | Progress, Issues |
| Guru (Viewer) | Bulanan | Email | Training, Updates |
| Dinas Pendidikan | Triwulanan | Email, Laporan | Compliance, Reports |
| BPK/BPKP | Tahunan | Audit Meeting | Audit Trail |
| Tim Pengembang | Harian | Slack, Git | Development |
| Staf TI Sekolah | Mingguan | Email, Phone | Technical Support |

---

## 8. Risiko Stakeholder

### 8.1 Risiko dan Mitigasi

| Stakeholder | Risiko | Dampak | Mitigasi |
|-------------|--------|--------|----------|
| Admin Sekolah | Resistensi terhadap perubahan | HIGH | Training intensif, UI intuitif |
| Kepala Sekolah | Tidak menggunakan sistem | HIGH | Demo manfaat, ROI jelas |
| Guru (Viewer) | Tidak mengakses sistem | MEDIUM | Simplifikasi UI, training |
| Dinas Pendidikan | Menolak format laporan | HIGH | Pastikan compliance Permendagri |
| BPK/BPKP | Audit trail tidak memadai | HIGH | Implement audit trail lengkap |
| Staf TI Sekolah | Tidak bisa install/maintain | MEDIUM | Dokumentasi lengkap, support |

---

## 9. Kesimpulan

### 9.1 Stakeholder Kunci

**Paling Kritis:**
1. Admin Sekolah - Pengguna utama, kesuksesan sistem bergantung pada mereka
2. Kepala Sekolah - Decision maker, perlu buy-in untuk adopsi
3. Dinas Pendidikan - Compliance requirement, format laporan harus sesuai

**Perlu Perhatian:**
1. Guru (Viewer) - Perlu training dan support untuk adopsi
2. Staf TI Sekolah - Perlu dokumentasi teknis yang baik

### 9.2 Rekomendasi

1. **Prioritas Tinggi:**
   - Libatkan Admin Sekolah dalam UAT (User Acceptance Testing)
   - Demo sistem ke Kepala Sekolah untuk buy-in
   - Validasi format laporan dengan Dinas Pendidikan

2. **Prioritas Menengah:**
   - Training untuk Guru (Viewer)
   - Dokumentasi instalasi untuk Staf TI

3. **Prioritas Rendah:**
   - Komunikasi dengan BPK/BPKP (saat audit)
   - Koordinasi dengan Pemerintah Daerah (via Dinas)

---

*Dokumen ini merupakan bagian dari dokumentasi arsitektur Simanis62 V2.*
*Referensi: Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala dan Asumsi*
