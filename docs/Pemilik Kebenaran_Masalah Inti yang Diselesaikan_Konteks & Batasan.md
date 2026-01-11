# Dokumentasi Proyek Simanis62 V2
## Pemilik Kebenaran, Masalah Inti yang Diselesaikan, Konteks dan Batasan

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 5 Januari 2026 | Architecture Engineer | Dokumen awal |
| 1.1 | 5 Januari 2026 | Architecture Engineer | Perbaikan: Unifikasi terminologi, tambah risiko |
| 1.2 | 8 Januari 2026 | Architecture Engineer | Perbaikan: Konsistensi database SQLite, perbaiki risiko R4 |

---

## 1. Pendahuluan

Dokumen ini melengkapi dokumen **Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala dan Asumsi** dengan menjelaskan:
- **Mengapa** sistem Simanis62 V2 perlu dibangun
- **Masalah inti** yang diselesaikan oleh sistem
- **Konteks bisnis dan regulasi** yang melatarbelakangi sistem
- **Batasan lingkup** yang jelas dan tegas

Dokumen ini menjadi referensi untuk memahami **alasan keberadaan** sistem dan **masalah fundamental** yang menjadi fokus penyelesaian.

---

## 2. Pemilik Kebenaran (Source of Truth)

### 2.1 Definisi

Pemilik Kebenaran adalah sumber data dan aturan yang menjadi acuan utama dalam pengembangan dan operasional sistem Simanis62 V2.

### 2.2 Hierarki Kebenaran

| Tingkat | Sumber | Keterangan |
|---------|--------|------------|
| 1 | Permendagri Nomor 19 Tahun 2016 | Regulasi pemerintah tentang Pengelolaan Barang Milik Daerah |
| 2 | Basis Data SQLite Simanis62 V2 | Data aset sekolah yang tercatat dalam sistem |
| 3 | Dokumen Fisik Sekolah | Buku inventaris manual, bukti pembelian, dokumen kepemilikan |

### 2.3 Prinsip Kebenaran

| No | Prinsip | Penjelasan |
|----|---------|------------|
| 1 | Format KIB mengikuti Permendagri 19/2016 | Struktur laporan tidak boleh menyimpang dari standar |
| 2 | Data dalam sistem adalah data operasional | Basis data adalah sumber kebenaran untuk operasional harian |
| 3 | Dokumen fisik adalah bukti legal | Jika terjadi sengketa, dokumen fisik menjadi rujukan akhir |

### 2.4 Penyelesaian Konflik Data

Jika terjadi perbedaan data:
1. **Permendagri 19/2016** > Sistem (format dan struktur)
2. **Dokumen Fisik** > Sistem (nilai dan kepemilikan)
3. **Basis Data** > Laporan Excel (data operasional)

---

## 3. Latar Belakang dan Urgensi

### 3.1 Mengapa Sistem Ini Perlu Ada

Sekolah-sekolah di Indonesia menghadapi tantangan dalam pengelolaan aset karena:

| No | Kondisi Saat Ini | Dampak Negatif |
|----|------------------|----------------|
| 1 | Pencatatan aset masih manual menggunakan buku fisik | Rentan hilang, rusak, dan sulit dicari |
| 2 | Pembuatan laporan KIB memakan waktu berhari-hari | Keterlambatan pelaporan ke Dinas Pendidikan |
| 3 | Tidak ada jejak audit perpindahan aset | Aset hilang tanpa dapat dilacak |
| 4 | Data aset tersebar di berbagai dokumen | Inkonsistensi dan duplikasi data |
| 5 | Sulit mengetahui kondisi aset secara real-time | Keputusan pengadaan tidak berbasis data |

### 3.2 Urgensi Pembangunan Sistem

| No | Alasan Urgensi | Justifikasi |
|----|----------------|-------------|
| 1 | Kewajiban pelaporan KIB ke pemerintah | Permendagri 19/2016 mewajibkan pelaporan berkala |
| 2 | Akuntabilitas pengelolaan aset negara | Aset sekolah adalah Barang Milik Daerah (BMD) |
| 3 | Efisiensi operasional sekolah | Waktu admin dapat dialokasikan untuk tugas lain |
| 4 | Transparansi pengelolaan aset | Kepala sekolah dan Dinas dapat mengawasi dengan mudah |

---

## 4. Masalah Inti yang Diselesaikan

### 4.1 Masalah Primer

Sistem Simanis62 V2 menyelesaikan **tiga masalah inti**:

#### 4.1.1 Masalah 1: Pencatatan Aset Manual yang Tidak Efisien

**Deskripsi Masalah:**
- Admin sekolah mencatat aset dalam buku fisik atau Excel terpisah
- Pencarian aset membutuhkan waktu lama (membuka banyak halaman/file)
- Risiko kehilangan data tinggi (buku hilang, file corrupt)

**Solusi yang Diberikan:**
- Basis data terpusat dengan pencarian cepat (< 5 detik)
- Backup otomatis dan keamanan data
- Akses multi-user dengan hak akses berbeda

**Kriteria Keberhasilan:**
- Waktu pencarian aset berkurang dari menit menjadi detik
- Data aset tidak hilang selama sistem beroperasi
- Admin dapat mengakses data dari mana saja dalam jaringan lokal

#### 4.1.2 Masalah 2: Pembuatan Laporan KIB yang Memakan Waktu

**Deskripsi Masalah:**
- Pembuatan laporan KIB A-F secara manual membutuhkan 3-5 hari kerja
- Rentan kesalahan pengetikan dan perhitungan
- Format laporan sering tidak sesuai standar Permendagri

**Solusi yang Diberikan:**
- Generasi laporan KIB otomatis dalam format Excel
- Validasi data sesuai struktur Permendagri 19/2016
- Ekspor laporan dalam hitungan detik

**Kriteria Keberhasilan:**
- Waktu pembuatan laporan KIB berkurang dari hari menjadi menit
- Laporan sesuai format standar pemerintah
- Kesalahan perhitungan dan pengetikan minimal

#### 4.1.3 Masalah 3: Tidak Ada Jejak Audit Perpindahan Aset

**Deskripsi Masalah:**
- Aset berpindah ruangan tanpa pencatatan yang jelas
- Sulit melacak siapa yang bertanggung jawab atas aset
- Aset hilang tanpa dapat diidentifikasi kapan dan di mana

**Solusi yang Diberikan:**
- Fitur mutasi aset dengan pencatatan otomatis
- Riwayat perpindahan aset tersimpan permanen
- Kartu Inventaris Ruangan (KIR) untuk pelacakan lokasi

**Kriteria Keberhasilan:**
- Setiap perpindahan aset tercatat dengan timestamp dan user
- Lokasi aset dapat diketahui secara akurat
- Riwayat mutasi dapat diaudit kapan saja

### 4.2 Masalah Sekunder (Diselesaikan Sebagian)

| No | Masalah | Solusi Parsial | Alasan Parsial |
|----|---------|----------------|----------------|
| 1 | Kondisi aset tidak terpantau | Pencatatan kondisi (Baik, Rusak Ringan, Rusak Berat) | Tidak ada notifikasi otomatis atau jadwal pemeliharaan |
| 2 | Penghapusan aset tidak tercatat | Soft delete dengan status "Dihapus" | Tidak ada workflow persetujuan formal |
| 3 | Aset sulit diidentifikasi fisik | Kode barang unik | Tidak ada QR Code atau label fisik |

**Catatan:** Masalah sekunder ini diselesaikan sebagian karena solusi lengkap memerlukan fitur yang sengaja tidak dikerjakan (lihat Bagian 6.1 Batasan Fungsional).

---

## 5. Konteks Bisnis dan Regulasi

### 5.1 Konteks Regulasi

#### 5.1.1 Permendagri Nomor 19 Tahun 2016

Regulasi ini mengatur:
- **Definisi Barang Milik Daerah (BMD)**: Semua barang yang dibeli atau diperoleh atas beban APBD atau berasal dari perolehan lainnya yang sah
- **Kewajiban Pencatatan**: Setiap BMD harus dicatat dalam Kartu Inventaris Barang (KIB)
- **Klasifikasi KIB**: Enam kategori (A-F) dengan struktur field yang berbeda
- **Pelaporan Berkala**: Laporan inventaris harus disampaikan secara berkala

#### 5.1.2 Implikasi untuk Simanis62 V2

| Aspek Regulasi | Implikasi Sistem |
|----------------|------------------|
| Format KIB A-F | Struktur tabel basis data harus mengakomodasi field wajib per kategori |
| Nomor Register | Sistem harus menghasilkan nomor register unik dan berurutan |
| Kode Barang | Sistem harus mendukung format kode barang standar BMD |
| Kondisi Aset | Sistem harus mencatat kondisi: Baik, Rusak Ringan, Rusak Berat |

### 5.2 Konteks Bisnis Sekolah

#### 5.2.1 Karakteristik Pengguna

| Karakteristik | Deskripsi | Implikasi Desain |
|---------------|-----------|------------------|
| Literasi Teknis | Bervariasi (rendah hingga sedang) | Antarmuka harus sangat intuitif |
| Waktu Pelatihan | Maksimal 2 jam | Kurva pembelajaran harus minimal |
| Beban Kerja | Admin sekolah memiliki banyak tugas lain | Proses harus cepat dan efisien |

#### 5.2.2 Infrastruktur Sekolah

| Aspek | Kondisi Umum | Implikasi Sistem |
|-------|--------------|------------------|
| Perangkat Keras | Laptop spesifikasi rendah (RAM 2-4GB) | Sistem harus ringan dan responsif |
| Jaringan | LAN lokal, tidak selalu terhubung internet | Sistem desktop, bukan web |
| Dukungan TI | Minimal atau tidak ada | Instalasi dan pemeliharaan harus mudah |

---

## 6. Batasan Lingkup Sistem

**Definisi:** Batasan Lingkup adalah keputusan desain untuk **SENGAJA TIDAK** mengerjakan fitur tertentu (scope boundaries), bukan karena ketidakmampuan teknis.

Berbeda dengan "Kendala" yang merupakan kondisi eksternal yang tidak dapat diubah (lihat Dokumen "Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala dan Asumsi" Bagian 5).

### 6.1 Batasan Fungsional

Sistem Simanis62 V2 **TIDAK** mencakup:

| No | Fungsi yang Tidak Didukung | Alasan |
|----|----------------------------|--------|
| 1 | Integrasi dengan SIMBADA | Memerlukan API pemerintah yang tidak tersedia |
| 2 | Perhitungan depresiasi dan penyusutan | Kompleksitas tinggi, bukan kebutuhan inti sekolah |
| 3 | Workflow persetujuan penghapusan aset | Proses formal melibatkan banyak pihak di luar sistem |
| 4 | Pemeliharaan dan perbaikan aset | Fitur tambahan yang dapat ditambahkan kemudian |
| 5 | Peminjaman aset | Tidak semua sekolah memerlukan fitur ini |
| 6 | Notifikasi otomatis | Memerlukan infrastruktur email/SMS yang tidak selalu tersedia |
| 7 | Dashboard dan visualisasi data | Fitur tambahan yang dapat ditambahkan kemudian |

### 6.2 Batasan Teknis

| No | Batasan | Penjelasan |
|----|---------|------------|
| 1 | Sistem desktop, bukan web | Keputusan arsitektur untuk performa optimal di laptop kentang |
| 2 | Akses hanya dalam jaringan lokal | Tidak ada akses remote atau cloud |
| 3 | Basis data SQLite lokal | Tidak ada replikasi atau sinkronisasi multi-site |
| 4 | Ekspor hanya ke Excel | Tidak ada ekspor ke PDF atau format lain |

### 6.3 Batasan Data

| No | Batasan | Penjelasan |
|----|---------|------------|
| 1 | Data aset hanya untuk satu sekolah | Tidak ada fitur multi-tenant atau multi-sekolah |
| 2 | Riwayat mutasi tidak dapat dihapus | Audit trail bersifat permanen |
| 3 | Soft delete untuk penghapusan aset | Data tidak benar-benar dihapus dari basis data |

### 6.4 Batasan Pengguna

| No | Batasan | Penjelasan |
|----|---------|------------|
| 1 | Maksimal 10 user concurrent | Sistem dirancang untuk sekolah kecil hingga menengah |
| 2 | Dua role: Admin dan Viewer | Tidak ada role kompleks seperti Approver atau Auditor |
| 3 | Tidak ada fitur kolaborasi real-time | Tidak ada notifikasi atau chat antar user |

---

## 7. Risiko dan Mitigasi

### 7.1 Definisi Risiko

Risiko adalah kejadian yang **MUNGKIN** terjadi di masa depan dan dapat berdampak negatif terhadap keberhasilan sistem. Berbeda dengan Kendala (pasti ada) dan Batasan (keputusan desain), risiko bersifat probabilistik.

### 7.2 Kategori Risiko

#### 7.2.1 Risiko Regulasi

| No | Risiko | Probabilitas | Dampak | Mitigasi |
|----|--------|--------------|--------|----------|
| 1 | Perubahan format KIB oleh pemerintah (Permendagri baru) | Rendah | Tinggi | Desain modular untuk modul laporan; isolasi logika format KIB |
| 2 | Perubahan klasifikasi kode barang BMD | Rendah | Sedang | Tabel kode barang terpisah dari data aset; mudah diupdate |
| 3 | Penambahan field wajib baru di KIB | Sedang | Sedang | Skema database fleksibel dengan kolom cadangan |

#### 7.2.2 Risiko Teknis

| No | Risiko | Probabilitas | Dampak | Mitigasi |
|----|--------|--------------|--------|----------|
| 4 | Performa SQLite menurun pada data besar | Sedang | Sedang | Optimasi query; indexing agresif; limit data per query |
| 5 | WPF tidak kompatibel dengan Windows versi lama | Rendah | Sedang | Target minimum Windows 10; dokumentasi requirement jelas |
| 6 | Performa lambat saat data aset > 10,000 item | Sedang | Sedang | Pagination; lazy loading; caching; indexing database |

#### 7.2.3 Risiko Adopsi Pengguna

| No | Risiko | Probabilitas | Dampak | Mitigasi |
|----|--------|--------------|--------|----------|
| 7 | User tidak mengadopsi sistem (tetap manual) | Sedang | Tinggi | Pelatihan intensif; UI sangat intuitif; dukungan on-site |
| 8 | Data awal tidak akurat (migrasi dari manual) | Tinggi | Sedang | Validasi data saat import; wizard import dengan preview |
| 9 | Resistensi perubahan dari admin lama | Sedang | Sedang | Demonstrasi manfaat; involve user dalam testing |

#### 7.2.4 Risiko Data

| No | Risiko | Probabilitas | Dampak | Mitigasi |
|----|--------|--------------|--------|----------|
| 10 | Kehilangan data karena hardware failure | Sedang | Tinggi | Backup otomatis harian; export Excel berkala |
| 11 | Data tidak konsisten antar ruangan | Sedang | Sedang | Validasi referential integrity; constraint database |
| 12 | Duplikasi kode barang | Rendah | Sedang | Unique constraint pada kode barang; validasi input |

### 7.3 Matriks Risiko

| Dampak / Probabilitas | Rendah | Sedang | Tinggi |
|------------------------|--------|--------|--------|
| **Tinggi** | R1, R2 | - | R7, R10 |
| **Sedang** | R5 | R3, R4, R6, R8, R9, R11 | - |
| **Rendah** | - | R12 | - |

**Prioritas Mitigasi:**
1. **CRITICAL** (Dampak Tinggi + Probabilitas Tinggi): R7, R10
2. **HIGH** (Dampak Tinggi + Probabilitas Sedang/Rendah): R1, R2
3. **MEDIUM** (Dampak Sedang): R3, R4, R6, R8, R9, R11
4. **LOW** (Dampak Rendah): R5, R12

### 7.4 Rencana Kontingensi

| Risiko | Rencana Kontingensi (Jika Mitigasi Gagal) |
|--------|-------------------------------------------|
| R1 (Perubahan format KIB) | Alokasi 2 minggu untuk refactoring modul laporan |
| R4 (Performa SQLite menurun) | Rekomendasi upgrade RAM ke 8GB; optimasi schema database |
| R7 (User tidak mengadopsi) | Hybrid system: tetap support manual + digital paralel |
| R10 (Kehilangan data) | Restore dari backup terakhir; maksimal kehilangan 1 hari data |

---

## 8. Ringkasan Eksekutif

### 8.1 Esensi Sistem

Simanis62 V2 adalah sistem pengelolaan aset sekolah yang menyelesaikan **tiga masalah inti**:
1. Pencatatan aset manual yang tidak efisien
2. Pembuatan laporan KIB yang memakan waktu
3. Tidak ada jejak audit perpindahan aset

### 8.2 Konteks Keberadaan

Sistem ini ada karena:
- **Kewajiban regulasi**: Permendagri 19/2016 mewajibkan pelaporan KIB
- **Kebutuhan operasional**: Sekolah memerlukan efisiensi dalam pengelolaan aset
- **Akuntabilitas**: Aset sekolah adalah Barang Milik Daerah yang harus dipertanggungjawabkan

### 8.3 Batasan yang Jelas

Sistem ini **TIDAK** dirancang untuk:
- Integrasi dengan sistem pemerintah (SIMBADA)
- Perhitungan depresiasi dan penyusutan
- Workflow persetujuan formal
- Akses remote atau cloud

### 8.4 Pemilik Kebenaran

Hierarki kebenaran:
1. **Permendagri 19/2016** (format dan struktur)
2. **Basis Data Simanis62 V2** (data operasional)
3. **Dokumen Fisik Sekolah** (bukti legal)

### 8.5 Risiko Utama

Risiko dengan prioritas CRITICAL yang memerlukan perhatian khusus:
1. **Performa SQLite menurun pada data besar** (R4)
2. **User tidak mengadopsi sistem** (R7)
3. **Kehilangan data karena hardware failure** (R10)

Mitigasi untuk ketiga risiko ini harus diimplementasikan sejak awal development.

---

*Dokumen ini melengkapi dokumen "Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala dan Asumsi".*
*Referensi: Permendagri Nomor 19 Tahun 2016 tentang Pedoman Pengelolaan Barang Milik Daerah*
