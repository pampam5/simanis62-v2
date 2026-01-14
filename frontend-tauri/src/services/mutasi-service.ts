/**
 * Mutasi Service - Workflow mutasi aset antar ruangan
 */

import { api } from './api';
import type {
  RiwayatMutasi,
  MutasiCreate,
  MutasiSelesai,
  MutasiBatal,
  PaginatedResponse,
  StatusMutasi,
} from './types';

export interface MutasiSearchParams {
  status_mutasi?: StatusMutasi;
  aset_id?: string;
  ruangan_asal_id?: string;
  ruangan_tujuan_id?: string;
  page?: number;
  page_size?: number;
}

export const mutasiService = {
  /**
   * Ambil semua mutasi dengan pagination
   */
  async getAll(params?: MutasiSearchParams): Promise<PaginatedResponse<RiwayatMutasi>> {
    return api.get<PaginatedResponse<RiwayatMutasi>>('/mutasi', params as Record<string, string | number | boolean | undefined>);
  },

  /**
   * Ambil mutasi berdasarkan ID
   */
  async getById(id: string): Promise<RiwayatMutasi> {
    return api.get<RiwayatMutasi>(`/mutasi/${id}`);
  },

  /**
   * Buat mutasi baru
   * - Status aset akan berubah menjadi "Mutasi"
   * - Kondisi saat mutasi akan dicatat
   */
  async create(data: MutasiCreate): Promise<RiwayatMutasi> {
    return api.post<RiwayatMutasi>('/mutasi', data);
  },

  /**
   * Selesaikan mutasi
   * - Status aset akan berubah menjadi "Aktif"
   * - Ruangan aset akan diupdate ke ruangan tujuan
   */
  async selesaikan(id: string, data?: MutasiSelesai): Promise<RiwayatMutasi> {
    return api.put<RiwayatMutasi>(`/mutasi/${id}/selesai`, data || {});
  },

  /**
   * Batalkan mutasi
   * - Status aset akan kembali menjadi "Aktif"
   * - Ruangan aset tetap di ruangan asal
   */
  async batalkan(id: string, data: MutasiBatal): Promise<RiwayatMutasi> {
    return api.put<RiwayatMutasi>(`/mutasi/${id}/batal`, data);
  },

  /**
   * Ambil mutasi pending (DALAM_PROSES)
   */
  async getPending(): Promise<RiwayatMutasi[]> {
    const response = await api.get<PaginatedResponse<RiwayatMutasi>>('/mutasi', {
      status_mutasi: 'DALAM_PROSES',
      page_size: 100,
    });
    return response.items;
  },

  /**
   * Ambil riwayat mutasi untuk aset tertentu
   */
  async getByAset(asetId: string): Promise<RiwayatMutasi[]> {
    const response = await api.get<PaginatedResponse<RiwayatMutasi>>('/mutasi', {
      aset_id: asetId,
      page_size: 100,
    });
    return response.items;
  },

  /**
   * Hitung jumlah mutasi pending
   */
  async countPending(): Promise<number> {
    const response = await api.get<PaginatedResponse<RiwayatMutasi>>('/mutasi', {
      status_mutasi: 'DALAM_PROSES',
      page_size: 1,
    });
    return response.total;
  },
};
