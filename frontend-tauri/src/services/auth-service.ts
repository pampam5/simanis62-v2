/**
 * Auth Service - Authentication dan session management
 */

import { api } from './api';
import type { User, LoginRequest, LoginResponse } from './types';

export const authService = {
  /**
   * Login user
   * Session disimpan di cookie HttpOnly
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    return api.post<LoginResponse>('/auth/login', credentials);
  },

  /**
   * Logout user
   * Menghapus session cookie
   */
  async logout(): Promise<void> {
    return api.post<void>('/auth/logout');
  },

  /**
   * Ambil user yang sedang login
   * Return null jika tidak ada session
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      return await api.get<User>('/auth/me');
    } catch {
      return null;
    }
  },

  /**
   * Cek apakah user sudah login
   */
  async isAuthenticated(): Promise<boolean> {
    const user = await this.getCurrentUser();
    return user !== null;
  },

  /**
   * Cek apakah user adalah Admin
   */
  async isAdmin(): Promise<boolean> {
    const user = await this.getCurrentUser();
    return user?.role === 'Admin';
  },

  /**
   * Cek apakah user bisa export
   * Admin: selalu bisa
   * Viewer: hanya jika dapat_ekspor=true
   */
  async canExport(): Promise<boolean> {
    const user = await this.getCurrentUser();
    if (!user) return false;
    return user.role === 'Admin' || user.dapat_ekspor;
  },

  /**
   * Refresh session (extend timeout)
   */
  async refreshSession(): Promise<void> {
    return api.post<void>('/auth/refresh');
  },
};
