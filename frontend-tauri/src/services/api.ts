/**
 * Base API Client untuk SIMANIS62 V2
 * Komunikasi dengan FastAPI backend sidecar
 *
 * Development: Menggunakan Vite proxy (/api -> http://127.0.0.1:8000/api)
 * Production: Langsung ke backend sidecar
 */

import type { ApiError } from './types';

// Detect environment: Tauri production vs Vite development
const isTauriProduction = window.__TAURI_INTERNALS__ !== undefined &&
  !window.location.hostname.includes('localhost');

// Development: gunakan relative URL (Vite proxy)
// Production: gunakan absolute URL ke sidecar
const API_BASE_URL = isTauriProduction
  ? 'http://127.0.0.1:8000/api/v1'  // Tauri production - direct to sidecar
  : '/api/v1';                       // Development - use Vite proxy

const DEFAULT_TIMEOUT = 30000; // 30 detik

export class ApiClient {
  private baseUrl: string;
  private timeout: number;

  constructor(baseUrl: string = API_BASE_URL, timeout: number = DEFAULT_TIMEOUT) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
  }

  private async request<T>(
    method: string,
    endpoint: string,
    options: {
      body?: unknown;
      params?: Record<string, string | number | boolean | undefined>;
      headers?: Record<string, string>;
    } = {}
  ): Promise<T> {
    const { body, params, headers = {} } = options;

    // Build URL with query params
    let url = `${this.baseUrl}${endpoint}`;
    if (params) {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          searchParams.append(key, String(value));
        }
      });
      const queryString = searchParams.toString();
      if (queryString) {
        url += `?${queryString}`;
      }
    }

    // Setup abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
        credentials: 'include', // Include cookies for session
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({
          detail: 'Terjadi kesalahan pada server',
        }));

        const apiError: ApiError = {
          detail: errorData.detail || 'Terjadi kesalahan',
          error_code: errorData.error_code,
          status_code: response.status,
        };

        throw apiError;
      }

      // Handle empty response (204 No Content)
      if (response.status === 204) {
        return {} as T;
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof DOMException && error.name === 'AbortError') {
        throw {
          detail: 'Koneksi timeout. Silakan coba lagi.',
          error_code: 'TIMEOUT',
          status_code: 408,
        } as ApiError;
      }

      if ((error as ApiError).status_code) {
        throw error;
      }

      // Network error
      throw {
        detail: 'Tidak dapat terhubung ke server. Pastikan aplikasi backend berjalan.',
        error_code: 'NETWORK_ERROR',
        status_code: 0,
      } as ApiError;
    }
  }

  async get<T>(
    endpoint: string,
    params?: Record<string, string | number | boolean | undefined>
  ): Promise<T> {
    return this.request<T>('GET', endpoint, { params });
  }

  async post<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>('POST', endpoint, { body });
  }

  async put<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>('PUT', endpoint, { body });
  }

  async delete<T>(endpoint: string, body?: unknown): Promise<T> {
    return this.request<T>('DELETE', endpoint, { body });
  }

  // Download file (untuk export Excel)
  async downloadFile(endpoint: string, filename: string): Promise<void> {
    const url = `${this.baseUrl}${endpoint}`;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout * 2); // Double timeout for downloads

    try {
      const response = await fetch(url, {
        method: 'GET',
        credentials: 'include',
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({
          detail: 'Gagal mengunduh file',
        }));
        throw {
          detail: errorData.detail,
          status_code: response.status,
        } as ApiError;
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      await this.get('/health');
      return true;
    } catch {
      return false;
    }
  }
}

// Singleton instance
export const api = new ApiClient();
