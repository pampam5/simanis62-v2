/**
 * Ruangan Service - CRUD operations untuk ruangan
 */

import { api } from './api';
import type {
  Ruangan,
  RuanganCreate,
  RuanganUpdate,
  PaginatedResponse,
} from './types';

export interface RuanganSearchParams {
  q?: string;
  page?: number;
  page_size?: number;
}

export const ruanganService = {
  /**
   * Ambil semua ruangan dengan pagination
   */
  async getAll(params?: RuanganSearchParams): Promise<PaginatedResponse<Ruangan>> {
    return api.get<PaginatedResponse<Ruangan>>('/ruangan', params as Record<string, string | number | boolean | undefined>);
  },

  /**
   * Ambil semua ruangan tanpa pagination (untuk dropdown)
   */
  async getAllForDropdown(): Promise<Ruangan[]> {
    const response = await api.get<PaginatedResponse<Ruangan>>('/ruangan', {
      page_size: 1000,
    });
    return response.items;
  },

  /**
   * Ambil ruangan berdasarkan ID
   */
  async getById(id: string): Promise<Ruangan> {
    return api.get<Ruangan>(`/ruangan/${id}`);
  },

  /**
   * Buat ruangan baru
   */
  async create(data: RuanganCreate): Promise<Ruangan> {
    return api.post<Ruangan>('/ruangan', data);
  },

  /**
   * Update ruangan
   */
  async update(id: string, data: RuanganUpdate): Promise<Ruangan> {
    return api.put<Ruangan>(`/ruangan/${id}`, data);
  },

  /**
   * Hapus ruangan
   * Catatan: Ruangan tidak bisa dihapus jika masih ada aset di dalamnya
   */
  async delete(id: string): Promise<void> {
    return api.delete<void>(`/ruangan/${id}`);
  },

  /**
   * Search ruangan
   */
  async search(query: string): Promise<Ruangan[]> {
    const response = await api.get<PaginatedResponse<Ruangan>>('/ruangan', {
      q: query,
      page_size: 50,
    });
    return response.items;
  },

  /**
   * Hitung jumlah aset di ruangan
   */
  async countAset(id: string): Promise<number> {
    const response = await api.get<{ count: number }>(`/ruangan/${id}/aset-count`);
    return response.count;
  },
};
