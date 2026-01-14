/**
 * Aset Service - CRUD operations untuk aset
 */

import { api } from './api';
import type {
  Aset,
  AsetCreate,
  AsetUpdate,
  AsetSearchParams,
  AsetStats,
  PaginatedResponse,
  DeleteRequest,
  RecentAset,
} from './types';

export const asetService = {
  /**
   * Ambil semua aset dengan pagination
   */
  async getAll(params?: AsetSearchParams): Promise<PaginatedResponse<Aset>> {
    return api.get<PaginatedResponse<Aset>>('/aset', params as Record<string, string | number | boolean | undefined>);
  },

  /**
   * Ambil aset berdasarkan ID
   */
  async getById(id: string): Promise<Aset> {
    return api.get<Aset>(`/aset/${id}`);
  },

  /**
   * Buat aset baru
   */
  async create(data: AsetCreate): Promise<Aset> {
    return api.post<Aset>('/aset', data);
  },

  /**
   * Update aset
   */
  async update(id: string, data: AsetUpdate): Promise<Aset> {
    return api.put<Aset>(`/aset/${id}`, data);
  },

  /**
   * Soft delete aset (dengan alasan)
   */
  async delete(id: string, reason: string): Promise<void> {
    const body: DeleteRequest = { reason };
    return api.delete<void>(`/aset/${id}`, body);
  },

  /**
   * Search aset
   */
  async search(query: string, params?: Omit<AsetSearchParams, 'q'>): Promise<PaginatedResponse<Aset>> {
    return api.get<PaginatedResponse<Aset>>('/aset/search', {
      q: query,
      ...params,
    } as Record<string, string | number | boolean | undefined>);
  },

  /**
   * Ambil statistik aset
   */
  async getStats(): Promise<AsetStats> {
    const response = await api.get<{ data: AsetStats }>('/aset/stats');
    return response.data;
  },

  /**
   * Ambil aset terbaru untuk dashboard
   */
  async getRecent(limit: number = 5): Promise<RecentAset[]> {
    const response = await api.get<{ data: RecentAset[] }>('/aset/recent', { limit });
    return response.data;
  },

  /**
   * Ambil aset berdasarkan ruangan
   */
  async getByRuangan(ruanganId: string, params?: AsetSearchParams): Promise<PaginatedResponse<Aset>> {
    return api.get<PaginatedResponse<Aset>>('/aset', {
      ruangan_id: ruanganId,
      ...params,
    } as Record<string, string | number | boolean | undefined>);
  },

  /**
   * Ambil aset berdasarkan kategori KIB
   */
  async getByKategori(kategori: string, params?: AsetSearchParams): Promise<PaginatedResponse<Aset>> {
    return api.get<PaginatedResponse<Aset>>('/aset', {
      kategori_kib: kategori,
      ...params,
    } as Record<string, string | number | boolean | undefined>);
  },
};
