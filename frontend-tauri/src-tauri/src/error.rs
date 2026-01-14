//! Error types untuk SIMANIS62 Tauri application.
//!
//! Semua error messages dalam Bahasa Indonesia untuk user-friendly experience.

use thiserror::Error;

/// Error types untuk sidecar management
#[derive(Error, Debug)]
pub enum SidecarError {
    #[error("Gagal menjalankan server backend: {0}")]
    SpawnFailed(String),

    #[error("Server backend tidak merespons setelah {0} detik")]
    HealthCheckTimeout(u64),

    #[error("Server backend berhenti secara tidak terduga: {0}")]
    UnexpectedExit(String),

    #[error("Gagal menghentikan server backend: {0}")]
    ShutdownFailed(String),

    #[error("Koneksi ke server backend gagal: {0}")]
    ConnectionFailed(String),
}

/// Error types untuk API calls
#[derive(Error, Debug)]
pub enum ApiError {
    #[error("Koneksi ke server gagal. Pastikan aplikasi berjalan dengan benar.")]
    ConnectionFailed,

    #[error("Request timeout. Server tidak merespons dalam waktu yang ditentukan.")]
    Timeout,

    #[error("Data tidak ditemukan: {0}")]
    NotFound(String),

    #[error("Akses ditolak. Anda tidak memiliki izin untuk operasi ini.")]
    Unauthorized,

    #[error("Validasi gagal: {0}")]
    ValidationError(String),

    #[error("Terjadi kesalahan pada server: {0}")]
    ServerError(String),

    #[error("Format data tidak valid: {0}")]
    ParseError(String),
}

/// Convert SidecarError ke string untuk Tauri command response
impl From<SidecarError> for String {
    fn from(err: SidecarError) -> Self {
        err.to_string()
    }
}

/// Convert ApiError ke string untuk Tauri command response
impl From<ApiError> for String {
    fn from(err: ApiError) -> Self {
        err.to_string()
    }
}
