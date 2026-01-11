# Dokumentasi Proyek Simanis62 V2
## Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala dan Asumsi

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 4 Januari 2026 | Architecture Engineer | Dokumen awal |
| 1.1 | 4 Januari 2026 | Architecture Engineer | Revisi: Penambahan dukungan KIB |
| 1.2 | 4 Januari 2026 | Architecture Engineer | Revisi: Seleksi fitur berdasarkan riset |
| 1.3 | 5 Januari 2026 | Architecture Engineer | Perbaikan: Hapus duplikasi, unifikasi terminologi |

---

## 1. Tujuan Bisnis

### 1.1 Tujuan Utama

Simanis62 V2 bertujuan menyediakan sistem pengelolaan aset sekolah yang mendukung pelaporan Kartu Inventaris Barang (KIB) sesuai Permendagri Nomor 19 Tahun 2016 tentang Pedoman Pengelolaan Barang Milik Daerah.

| No | Tujuan | Indikator Keberhasilan |
|----|--------|------------------------|
| 1 | Mendigitalisasi pencatatan aset sekolah | Data aset tersimpan dalam basis data terpusat |
| 2 | Menghasilkan laporan KIB A sampai F | Laporan sesuai format standar pemerintah |
| 3 | Mempermudah pencarian dan pelacakan aset | Waktu pencarian kurang dari 5 detik |
| 4 | Menyediakan laporan dalam format Excel | Ekspor data tanpa kehilangan informasi |
| 5 | Mendukung mutasi aset antarruangan | Riwayat perubahan tercatat akurat |

### 1.2 Referensi Batasan Fungsional

Untuk informasi lengkap mengenai batasan fungsional sistem (fitur yang sengaja tidak dikerjakan), silakan lihat:

**Dokumen:** *Pemilik Kebenaran, Masalah Inti yang Diselesaikan, Konteks dan Batasan*
**Bagian:** 6.1 Batasan Fungsional

Dokumen tersebut menjelaskan secara detail fungsi-fungsi yang **TIDAK** didukung oleh sistem beserta alasan dan justifikasinya.

---

## 2. Peta Pemangku Kepentingan

### 2.1 Pemangku Kepentingan Primer

| Peran | Tanggung Jawab | Kebutuhan Utama |
|-------|----------------|-----------------|
| Admin Sekolah | Mengelola data aset, membuat laporan KIB, mencatat mutasi | Antarmuka sederhana, proses cepat |
| Guru | Melihat aset di ruangan, melaporkan kondisi aset | Akses informasi yang mudah |
| Kepala Sekolah | Mengawasi pengelolaan aset, menandatangani laporan KIB | Laporan yang akurat dan lengkap |

### 2.2 Pemangku Kepentingan Sekunder

| Peran | Tanggung Jawab | Kebutuhan Utama |
|-------|----------------|-----------------|
| Tim Pengembang | Membangun dan memelihara sistem | Spesifikasi yang jelas |
| Staf TI Sekolah | Menyediakan infrastruktur perangkat keras | Sistem ringan dan mudah dipasang |
| Dinas Pendidikan | Menerima laporan KIB dari sekolah | Format laporan sesuai standar |

---

## 3. Seleksi Fitur

### 3.1 Fitur Wajib Mutlak (Core)

Fitur yang harus ada agar sistem dapat berfungsi dan memenuhi tujuan utama.

| No | Fitur | Justifikasi | Kompleksitas |
|----|-------|-------------|--------------|
| 1 | CRUD Data Barang | Fondasi sistem, semua laporan bergantung pada data ini | Rendah |
| 2 | Pencarian Aset | Efisiensi operasional, kebutuhan harian pengguna | Rendah |
| 3 | Kartu Inventaris Barang (KIB A-F) | Persyaratan pelaporan pemerintah | Sedang |
| 4 | Kartu Inventaris Ruangan (KIR) | Pelacakan aset berdasarkan lokasi fisik | Rendah |
| 5 | Mutasi Barang | Jejak audit perpindahan aset | Sedang |
| 6 | Ekspor Excel | Fleksibilitas pengolahan data | Rendah |
| 7 | Kode Barang Unik | Identifikasi dan pelacakan aset | Rendah |
| 8 | Multi User (Admin, Viewer) | Pembagian hak akses dasar | Rendah |

### 3.2 Fitur Penting (Disederhanakan)

Fitur yang penting namun implementasinya disederhanakan untuk menjaga performa.

| No | Fitur | Penyederhanaan | Kompleksitas |
|----|-------|----------------|--------------|
| 1 | Buku Inventaris | Ekspor Excel dari seluruh data aset | Rendah |
| 2 | Daftar Rekapitulasi | Ringkasan per kategori KIB | Rendah |
| 3 | Pencatatan Kondisi | Tiga status: Baik, Rusak Ringan, Rusak Berat | Rendah |
| 4 | Cetak Laporan | Print dari tampilan, bukan engine PDF kompleks | Rendah |
| 5 | Penghapusan Barang | Soft delete dengan status "Dihapus" | Rendah |

### 3.3 Fitur Opsional (Iterasi Selanjutnya)

Fitur yang ditunda untuk menjaga fokus dan kesederhanaan sistem.

| No | Fitur | Alasan Penundaan |
|----|-------|------------------|
| 1 | Pemeliharaan Aset | Menambah kompleksitas data model dan logika bisnis |
| 2 | Peminjaman Barang | Tidak semua sekolah memerlukan, bukan bagian KIB |
| 3 | QR Code/Label | Peningkatan usability, bukan kebutuhan inti |
| 4 | Riwayat Perubahan Detail | Audit trail lengkap dapat ditambahkan kemudian |
| 5 | Dashboard Statistik | Visualisasi data dapat ditambahkan kemudian |

---

## 4. Kategori KIB yang Didukung

Berdasarkan Permendagri 19/2016, sistem mendukung enam kategori KIB:

| Kode | Nama | Contoh Aset di Sekolah |
|------|------|------------------------|
| KIB A | Tanah | Tanah sekolah, lapangan olahraga |
| KIB B | Peralatan dan Mesin | Komputer, printer, AC, proyektor, meja, kursi |
| KIB C | Gedung dan Bangunan | Gedung kelas, laboratorium, perpustakaan, toilet |
| KIB D | Jalan, Irigasi, dan Jaringan | Jalan lingkungan, saluran air, jaringan listrik |
| KIB E | Aset Tetap Lainnya | Buku perpustakaan, alat kesenian, tanaman hias |
| KIB F | Konstruksi dalam Pengerjaan | Bangunan yang sedang dibangun/renovasi |

### 4.1 Field Wajib per KIB

| Field | KIB A | KIB B | KIB C | KIB D | KIB E | KIB F |
|-------|-------|-------|-------|-------|-------|-------|
| Kode Barang | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Nama Barang | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Nomor Register | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Luas/Ukuran | ✓ | - | ✓ | ✓ | - | - |
| Tahun Perolehan | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Asal Usul | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Harga (Rp) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Kondisi | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Merk/Type | - | ✓ | - | - | - | - |
| Alamat/Lokasi | ✓ | - | ✓ | ✓ | - | ✓ |
| Keterangan | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 5. Kendala

**Definisi:** Kendala adalah batasan yang **TIDAK DAPAT DIUBAH** karena merupakan kondisi eksternal yang harus diterima (hardware, regulasi, organisasi, waktu).

Berbeda dengan "Batasan Lingkup" yang merupakan keputusan desain untuk **SENGAJA TIDAK** mengerjakan fitur tertentu (lihat Dokumen "Pemilik Kebenaran, Masalah Inti yang Diselesaikan, Konteks dan Batasan" Bagian 6).

### 5.1 Kendala Teknis

| No | Kendala | Implikasi |
|----|---------|-----------|
| 1 | Sistem harus berjalan pada laptop spesifikasi rendah (RAM 2-4GB) | Tidak menggunakan WebView2 atau teknologi berat |
| 2 | Teknologi: Python FastAPI, WPF .NET 8, SQLite | Tidak ada substitusi teknologi |
| 3 | AI coding assistance 70-80% akurat untuk XAML | Butuh manual coding untuk UI kompleks |

### 5.2 Kendala Fungsional

| No | Kendala | Implikasi |
|----|---------|-----------|
| 1 | Format KIB harus sesuai standar Permendagri 19/2016 | Struktur data mengikuti format KIB A-F |
| 2 | Kondisi aset: Baik, Rusak Ringan, Rusak Berat | Tiga status kondisi sesuai standar |
| 3 | Kode barang mengikuti format standar | Struktur kode sesuai klasifikasi BMD |

### 5.3 Kendala Pengguna

| No | Kendala | Implikasi |
|----|---------|-----------|
| 1 | Tingkat literasi teknis pengguna bervariasi | Antarmuka harus sangat intuitif |
| 2 | Waktu pelatihan terbatas | Kurva pembelajaran harus minimal |

---

## 6. Asumsi

### 6.1 Asumsi Infrastruktur

| No | Asumsi | Risiko jika Tidak Terpenuhi |
|----|--------|----------------------------|
| 1 | Sekolah memiliki minimal satu laptop | Sistem tidak dapat digunakan |
| 2 | Tersedia jaringan lokal untuk akses basis data | Sistem tidak dapat terhubung |

### 6.2 Asumsi Data

| No | Asumsi | Risiko jika Tidak Terpenuhi |
|----|--------|----------------------------|
| 1 | Data awal aset disediakan oleh pihak sekolah | Proses implementasi tertunda |
| 2 | Akurasi data menjadi tanggung jawab pengguna | Data tidak akurat |
| 3 | Format KIB mengikuti Permendagri 19/2016 | Laporan tidak diterima oleh Dinas |

### 6.3 Asumsi Pengguna

| No | Asumsi | Risiko jika Tidak Terpenuhi |
|----|--------|----------------------------|
| 1 | Admin Sekolah bersedia mengikuti pelatihan | Penggunaan sistem tidak optimal |
| 2 | Pihak sekolah berkomitmen mengadopsi sistem | Sistem tidak digunakan |

### 6.4 Asumsi Lingkup

| No | Asumsi | Risiko jika Tidak Terpenuhi |
|----|--------|----------------------------|
| 1 | Lingkup fitur tetap stabil | Penambahan fitur menyebabkan keterlambatan |
| 2 | Format KIB tidak berubah selama pengembangan | Perubahan struktur data diperlukan |

---

## 7. Ringkasan

| Aspek | Keterangan |
|-------|------------|
| Tujuan | Sistem pengelolaan aset sekolah dengan dukungan pelaporan KIB |
| Regulasi Acuan | Permendagri Nomor 19 Tahun 2016 |
| Pengguna Utama | Admin Sekolah, Guru, Kepala Sekolah |
| Fitur Inti | CRUD, KIB A-F, KIR, Mutasi, Ekspor Excel |
| Fitur Ditunda | Pemeliharaan, Peminjaman, QR Code |
| Kendala Utama | Harus berjalan di laptop spesifikasi rendah |
| Asumsi Kritis | Format KIB mengikuti standar Permendagri |

---

*Dokumen ini merupakan bagian dari dokumentasi arsitektur Simanis62 V2.*
*Referensi: Permendagri Nomor 19 Tahun 2016 tentang Pedoman Pengelolaan Barang Milik Daerah*
