/**
 * Services Index - Export semua services untuk SIMANIS62 V2
 */

// Base API client
export { api, ApiClient } from './api';

// Services
export { asetService } from './aset-service';
export { authService } from './auth-service';
export { kibService } from './kib-service';
export { mutasiService } from './mutasi-service';
export { ruanganService } from './ruangan-service';

// Error handling
export {
  handleApiError,
  isApiError,
  isUnauthorizedError,
  isForbiddenError,
  isNotFoundError,
  isValidationError,
  isNetworkError,
} from './error-handler';

// Types
export type {
  // Enums
  KategoriKIB,
  Kondisi,
  StatusAset,
  AsalUsul,
  UserRole,
  UserStatus,
  StatusMutasi,
  Operation,
  // Base types
  User,
  Ruangan,
  Aset,
  RiwayatMutasi,
  AuditTrail,
  // KIB types
  AsetKibA,
  AsetKibB,
  AsetKibC,
  AsetKibD,
  AsetKibE,
  AsetKibF,
  // API types
  PaginatedResponse,
  AsetCreate,
  AsetUpdate,
  AsetSearchParams,
  AsetStats,
  KibBCreate,
  KibBExportRow,
  MutasiCreate,
  MutasiSelesai,
  MutasiBatal,
  LoginRequest,
  LoginResponse,
  RuanganCreate,
  RuanganUpdate,
  DeleteRequest,
  ApiError,
  DashboardStats,
  RecentAset,
} from './types';
