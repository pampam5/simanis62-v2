/**
 * TypeScript types untuk SIMANIS62 V2
 * Sesuai dengan backend models dan docs/data_schema.md
 */

// ============================================================================
// Enums
// ============================================================================

export type KategoriKIB = 'A' | 'B' | 'C' | 'D' | 'E' | 'F';

export type Kondisi = 'Baik' | 'Kurang Baik' | 'Rusak Berat';

export type StatusAset = 'Aktif' | 'Mutasi' | 'Dihapus';

export type AsalUsul = 'Pembelian' | 'Hibah' | 'Sumbangan' | 'Produksi';

export type UserRole = 'Admin' | 'Viewer';

export type UserStatus = 'Aktif' | 'Nonaktif';

export type StatusMutasi = 'DALAM_PROSES' | 'SELESAI' | 'DIBATALKAN';

export type Operation = 'CREATE' | 'UPDATE' | 'DELETE';

// ============================================================================
// Base Types
// ============================================================================

export interface User {
  id: string;
  username: string;
  nama_lengkap: string;
  role: UserRole;
  status: UserStatus;
  dapat_ekspor: boolean;
  created_at: string;
  updated_at: string;
}

export interface Ruangan {
  id: string;
  nama_ruangan: string;
  kode_ruangan: string;
  keterangan?: string;
  created_at: string;
  updated_at: string;
}


export interface Aset {
  id: string;
  kode_barang: string;
  nama_barang: string;
  nomor_register: number;
  kategori_kib: KategoriKIB;
  tahun_perolehan: number;
  tanggal_perolehan?: string;
  asal_usul: AsalUsul;
  harga: number;
  kondisi: Kondisi;
  status: StatusAset;
  keterangan?: string;
  ruangan_id: string;
  created_by: string;
  updated_by?: string;
  deleted_by?: string;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
  delete_reason?: string;
  // Relations
  ruangan?: Ruangan;
}

export interface RiwayatMutasi {
  id: string;
  aset_id: string;
  ruangan_asal_id: string;
  ruangan_tujuan_id: string;
  user_id: string;
  tanggal_mutasi: string;
  alasan: string;
  kondisi_saat_mutasi: Kondisi;
  status_mutasi: StatusMutasi;
  mulai_mutasi: string;
  selesai_mutasi?: string;
  alasan_pembatalan?: string;
  // Relations
  aset?: Aset;
  ruangan_asal?: Ruangan;
  ruangan_tujuan?: Ruangan;
  user?: User;
}

export interface AuditTrail {
  id: string;
  table_name: string;
  record_id: string;
  operation: Operation;
  user_id: string;
  old_value?: string;
  new_value?: string;
  timestamp: string;
  ip_address?: string;
  // Relations
  user?: User;
}


// ============================================================================
// KIB Extension Types (KIB A-F)
// ============================================================================

export interface AsetKibA {
  id: string;
  aset_id: string;
  luas_m2: number;
  alamat_lokasi: string;
  status_hak_tanah?: string;
  tanggal_sertifikat?: string;
  nomor_sertifikat?: string;
  penggunaan?: string;
}

export interface AsetKibB {
  id: string;
  aset_id: string;
  satuan: string;
  ukuran_cc?: string;
  bahan?: string;
  merk?: string;
  tipe?: string;
  tanggal_dokumen?: string;
  nomor_rangka?: string;
  nomor_mesin?: string;
  nomor_polisi?: string;
  kapitalisasi?: number;
  total_harga?: number;
}

export interface AsetKibC {
  id: string;
  aset_id: string;
  kondisi_bangunan?: string;
  bertingkat?: boolean;
  beton?: boolean;
  luas_lantai_m2: number;
  alamat_lokasi: string;
  tanggal_dokumen?: string;
  nomor_dokumen?: string;
  luas_tanah_m2?: number;
  status_tanah?: string;
  kode_tanah?: string;
}

export interface AsetKibD {
  id: string;
  aset_id: string;
  jenis_konstruksi?: string;
  panjang_km?: number;
  lebar_m?: number;
  luas_m2?: number;
  alamat_lokasi: string;
  tanggal_dokumen?: string;
  nomor_dokumen?: string;
  status_tanah?: string;
  kode_tanah?: string;
}

export interface AsetKibE {
  id: string;
  aset_id: string;
  judul_pencipta?: string;
  spesifikasi_buku?: string;
  asal_daerah?: string;
  pencipta?: string;
  bahan?: string;
  jenis_hewan?: string;
  ukuran_hewan?: string;
  jumlah?: number;
}

export interface AsetKibF {
  id: string;
  aset_id: string;
  jenis_bangunan?: string;
  bertingkat?: boolean;
  beton?: boolean;
  luas_m2?: number;
  alamat_lokasi: string;
  info_dokumen?: string;
}

// ============================================================================
// API Request/Response Types
// ============================================================================

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface AsetCreate {
  kode_barang: string;
  nama_barang: string;
  nomor_register: number;
  kategori_kib: KategoriKIB;
  tahun_perolehan: number;
  tanggal_perolehan?: string;
  asal_usul: AsalUsul;
  harga: number;
  kondisi: Kondisi;
  keterangan?: string;
  ruangan_id: string;
}

export interface AsetUpdate {
  nama_barang?: string;
  kondisi?: Kondisi;
  keterangan?: string;
  ruangan_id?: string;
  harga?: number;
}

export interface AsetSearchParams {
  q?: string;
  kategori_kib?: KategoriKIB;
  kondisi?: Kondisi;
  status?: StatusAset;
  ruangan_id?: string;
  tahun_perolehan?: number;
  page?: number;
  page_size?: number;
}

export interface AsetStats {
  total_aset: number;
  kondisi_baik: number;
  kondisi_rusak_ringan: number;
  kondisi_rusak_berat: number;
  total_nilai: number;
}

export interface KibBCreate {
  satuan: string;
  ukuran_cc?: string;
  bahan?: string;
  merk?: string;
  tipe?: string;
  tanggal_dokumen?: string;
  nomor_rangka?: string;
  nomor_mesin?: string;
  nomor_polisi?: string;
  kapitalisasi?: number;
  total_harga?: number;
}

// KIB B Export Row (18 kolom BPAD DKI Jakarta)
export interface KibBExportRow {
  no: number;
  kode_barang: string;
  nama_barang: string;
  nomor_register: string;
  ukuran_cc: string;
  satuan: string;
  tahun_perolehan: number;
  bahan: string;
  merk: string;
  tipe: string;
  tanggal_dokumen: string;
  nomor_rangka: string;
  nomor_mesin: string;
  nomor_polisi: string;
  kondisi: string;
  harga: number;
  kapitalisasi: number;
  total_harga: number;
}

export interface MutasiCreate {
  aset_id: string;
  ruangan_tujuan_id: string;
  alasan: string;
}

export interface MutasiSelesai {
  catatan?: string;
}

export interface MutasiBatal {
  alasan_pembatalan: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  message: string;
}

export interface RuanganCreate {
  nama_ruangan: string;
  kode_ruangan: string;
  keterangan?: string;
}

export interface RuanganUpdate {
  nama_ruangan?: string;
  keterangan?: string;
}

export interface DeleteRequest {
  reason: string;
}

export interface ApiError {
  detail: string;
  error_code?: string;
  status_code: number;
}

export interface DashboardStats {
  total_aset: number;
  total_nilai: number;
  aset_baik: number;
  aset_kurang_baik: number;
  aset_rusak_berat: number;
  mutasi_pending: number;
}

export interface RecentAset {
  id: string;
  nama_barang: string;
  kode_barang: string;
  kondisi: Kondisi;
  harga: number;
  created_at: string;
  ruangan?: Ruangan;
}
