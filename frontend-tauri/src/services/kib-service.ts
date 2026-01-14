/**
 * KIB Service - Export KIB B dengan format BPAD DKI Jakarta 18 kolom
 */

import { api } from './api';
import type { KibBExportRow, PaginatedResponse } from './types';

export interface KibBExportParams {
  ruangan_id?: string;
  tahun_perolehan?: number;
  kondisi?: string;
}

export interface KibBExportMetadata {
  provinsi: string;
  unit_organisasi: string;
  sub_unit_organisasi: string;
  tanggal_export: string;
  total_rows: number;
  total_nilai: number;
}

export interface KibBExportResponse {
  metadata: KibBExportMetadata;
  data: KibBExportRow[];
}

export const kibService = {
  /**
   * Ambil data KIB B untuk preview
   */
  async getKibBData(params?: KibBExportParams): Promise<PaginatedResponse<KibBExportRow>> {
    return api.get<PaginatedResponse<KibBExportRow>>('/reports/kib/b', params as Record<string, string | number | boolean | undefined>);
  },

  /**
   * Export KIB B ke Excel
   * Format: 18 kolom BPAD DKI Jakarta
   * Harga dalam Rupiah penuh
   * Tanggal dalam format DD/MM/YYYY
   */
  async exportKibB(params?: KibBExportParams): Promise<void> {
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0].replace(/-/g, '');
    const filename = `KIB_B_${dateStr}.xlsx`;

    // Build query string
    const queryParams = new URLSearchParams();
    if (params?.ruangan_id) queryParams.append('ruangan_id', params.ruangan_id);
    if (params?.tahun_perolehan) queryParams.append('tahun_perolehan', String(params.tahun_perolehan));
    if (params?.kondisi) queryParams.append('kondisi', params.kondisi);

    const endpoint = `/reports/export/kib-b${queryParams.toString() ? '?' + queryParams.toString() : ''}`;

    return api.downloadFile(endpoint, filename);
  },

  /**
   * Ambil metadata export (untuk preview sebelum download)
   */
  async getExportMetadata(params?: KibBExportParams): Promise<KibBExportMetadata> {
    return api.get<KibBExportMetadata>('/reports/kib/b/metadata', params as Record<string, string | number | boolean | undefined>);
  },

  /**
   * Cek apakah user memiliki izin export
   * Admin: selalu bisa
   * Viewer: hanya jika dapat_ekspor=true
   */
  async canExport(): Promise<boolean> {
    try {
      const response = await api.get<{ can_export: boolean }>('/reports/can-export');
      return response.can_export;
    } catch {
      return false;
    }
  },
};
