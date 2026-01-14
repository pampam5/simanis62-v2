/**
 * Error Handler - Penanganan error API dengan pesan Bahasa Indonesia
 */

import type { ApiError } from './types';

/**
 * Mapping error code ke pesan Bahasa Indonesia
 */
const ERROR_MESSAGES: Record<string, string> = {
  // Network errors
  NETWORK_ERROR: 'Tidak dapat terhubung ke server. Pastikan aplikasi backend berjalan.',
  TIMEOUT: 'Koneksi timeout. Silakan coba lagi.',

  // Auth errors
  UNAUTHORIZED: 'Sesi Anda telah berakhir. Silakan login kembali.',
  FORBIDDEN: 'Anda tidak memiliki izin untuk melakukan aksi ini.',
  INVALID_CREDENTIALS: 'Username atau password salah.',
  SESSION_EXPIRED: 'Sesi Anda telah berakhir. Silakan login kembali.',

  // Validation errors
  VALIDATION_ERROR: 'Data yang dimasukkan tidak valid.',
  REQUIRED_FIELD: 'Field wajib tidak boleh kosong.',
  INVALID_FORMAT: 'Format data tidak valid.',

  // Resource errors
  NOT_FOUND: 'Data tidak ditemukan.',
  ALREADY_EXISTS: 'Data sudah ada.',
  CONFLICT: 'Terjadi konflik data. Silakan refresh dan coba lagi.',

  // Business rule errors
  ASET_HAS_MUTASI: 'Aset sedang dalam proses mutasi.',
  RUANGAN_HAS_ASET: 'Ruangan tidak bisa dihapus karena masih ada aset di dalamnya.',
  DELETE_REASON_REQUIRED: 'Alasan penghapusan wajib diisi (minimal 20 karakter).',
  INVALID_STATUS_TRANSITION: 'Perubahan status tidak valid.',

  // Export errors
  EXPORT_NOT_ALLOWED: 'Anda tidak memiliki izin untuk export data.',
  EXPORT_FAILED: 'Gagal mengexport data. Silakan coba lagi.',

  // Server errors
  INTERNAL_ERROR: 'Terjadi kesalahan pada server. Silakan coba lagi nanti.',
  DATABASE_ERROR: 'Terjadi kesalahan database. Silakan hubungi administrator.',
};

/**
 * Mapping HTTP status code ke pesan default
 */
const STATUS_MESSAGES: Record<number, string> = {
  400: 'Permintaan tidak valid.',
  401: 'Sesi Anda telah berakhir. Silakan login kembali.',
  403: 'Anda tidak memiliki izin untuk melakukan aksi ini.',
  404: 'Data tidak ditemukan.',
  409: 'Terjadi konflik data.',
  422: 'Data yang dimasukkan tidak valid.',
  429: 'Terlalu banyak permintaan. Silakan tunggu sebentar.',
  500: 'Terjadi kesalahan pada server.',
  502: 'Server tidak dapat dijangkau.',
  503: 'Server sedang dalam pemeliharaan.',
  504: 'Koneksi ke server timeout.',
};

/**
 * Handle API error dan return pesan user-friendly dalam Bahasa Indonesia
 */
export function handleApiError(error: unknown): string {
  // ApiError from our API client
  if (isApiError(error)) {
    // Check for specific error code first
    if (error.error_code && ERROR_MESSAGES[error.error_code]) {
      return ERROR_MESSAGES[error.error_code];
    }

    // Check for status code message
    if (error.status_code && STATUS_MESSAGES[error.status_code]) {
      // If we have a detail message from server, use it
      if (error.detail && error.detail !== 'string') {
        return error.detail;
      }
      return STATUS_MESSAGES[error.status_code];
    }

    // Fallback to detail message
    if (error.detail) {
      return error.detail;
    }
  }

  // Generic Error
  if (error instanceof Error) {
    // Network errors
    if (error.message.includes('fetch') || error.message.includes('network')) {
      return ERROR_MESSAGES.NETWORK_ERROR;
    }
    return error.message;
  }

  // Unknown error
  return 'Terjadi kesalahan yang tidak diketahui.';
}

/**
 * Type guard untuk ApiError
 */
export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'status_code' in error &&
    typeof (error as ApiError).status_code === 'number'
  );
}

/**
 * Check apakah error adalah unauthorized (perlu login ulang)
 */
export function isUnauthorizedError(error: unknown): boolean {
  if (isApiError(error)) {
    return error.status_code === 401;
  }
  return false;
}

/**
 * Check apakah error adalah forbidden (tidak punya izin)
 */
export function isForbiddenError(error: unknown): boolean {
  if (isApiError(error)) {
    return error.status_code === 403;
  }
  return false;
}

/**
 * Check apakah error adalah not found
 */
export function isNotFoundError(error: unknown): boolean {
  if (isApiError(error)) {
    return error.status_code === 404;
  }
  return false;
}

/**
 * Check apakah error adalah validation error
 */
export function isValidationError(error: unknown): boolean {
  if (isApiError(error)) {
    return error.status_code === 422 || error.error_code === 'VALIDATION_ERROR';
  }
  return false;
}

/**
 * Check apakah error adalah network error
 */
export function isNetworkError(error: unknown): boolean {
  if (isApiError(error)) {
    return error.status_code === 0 || error.error_code === 'NETWORK_ERROR';
  }
  return false;
}
