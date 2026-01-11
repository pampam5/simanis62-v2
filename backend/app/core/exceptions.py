"""
Custom exceptions untuk SIMANIS62 V2.

Exception hierarchy yang komprehensif untuk error handling yang semantic
dan mudah di-debug. Semua exception inherit dari SimanisException base class.
"""

from typing import Any


class SimanisException(Exception):
    """Base exception untuk semua error SIMANIS62."""

    def __init__(
        self,
        message: str,
        error_code: str,
        details: dict[str, Any] | None = None,
        status_code: int = 500,
    ) -> None:
        """Initialize SimanisException.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Additional error context
            status_code: HTTP status code untuk error response
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)


# === Authentication Exceptions ===


class AuthenticationError(SimanisException):
    """Error terkait autentikasi."""

    def __init__(
        self, message: str = "Autentikasi gagal", details: dict[str, Any] | None = None
    ) -> None:
        """Initialize AuthenticationError."""
        super().__init__(message, "AUTH_ERROR", details, 401)


class InvalidCredentialsError(AuthenticationError):
    """Username atau password salah."""

    def __init__(self) -> None:
        """Initialize InvalidCredentialsError."""
        super().__init__("Username atau password salah", {"field": "credentials"})


class SessionExpiredError(AuthenticationError):
    """Session sudah expired."""

    def __init__(self) -> None:
        """Initialize SessionExpiredError."""
        super().__init__(
            "Session telah berakhir, silakan login kembali", {"reason": "expired"}
        )


# === Authorization Exceptions ===


class AuthorizationError(SimanisException):
    """Error terkait otorisasi."""

    def __init__(
        self, message: str = "Akses ditolak", details: dict[str, Any] | None = None
    ) -> None:
        """Initialize AuthorizationError."""
        super().__init__(message, "AUTHZ_ERROR", details, 403)


class InsufficientPermissionError(AuthorizationError):
    """User tidak memiliki izin untuk operasi ini."""

    def __init__(self, required_role: str) -> None:
        """Initialize InsufficientPermissionError."""
        super().__init__(
            f"Akses ditolak. Memerlukan role: {required_role}",
            {"required_role": required_role},
        )


# === Validation Exceptions ===


class ValidationError(SimanisException):
    """Error validasi input."""

    def __init__(
        self, message: str, field: str, details: dict[str, Any] | None = None
    ) -> None:
        """Initialize ValidationError."""
        full_details = {"field": field}
        if details:
            full_details.update(details)
        super().__init__(message, "VALIDATION_ERROR", full_details, 422)


class DuplicateKodeBarangError(ValidationError):
    """Kode barang sudah ada."""

    def __init__(self, kode_barang: str) -> None:
        """Initialize DuplicateKodeBarangError."""
        super().__init__(
            f"Kode barang '{kode_barang}' sudah terdaftar",
            "kode_barang",
            {"existing_code": kode_barang},
        )


class InvalidKodeBarangFormatError(ValidationError):
    """Format kode barang tidak valid."""

    def __init__(self, kode_barang: str) -> None:
        """Initialize InvalidKodeBarangFormatError."""
        super().__init__(
            f"Format kode barang tidak valid: '{kode_barang}'. Format: XX.XX.XX.XXXX",
            "kode_barang",
            {"invalid_value": kode_barang, "expected_format": "XX.XX.XX.XXXX"},
        )


class InvalidTahunPerolehanError(ValidationError):
    """Tahun perolehan tidak valid."""

    def __init__(self, tahun: int, current_year: int) -> None:
        """Initialize InvalidTahunPerolehanError."""
        super().__init__(
            f"Tahun perolehan {tahun} tidak valid. Harus antara 1900-{current_year}",
            "tahun_perolehan",
            {"invalid_value": tahun, "min": 1900, "max": current_year},
        )


class InvalidHargaError(ValidationError):
    """Harga tidak valid."""

    def __init__(self, harga: int) -> None:
        """Initialize InvalidHargaError."""
        super().__init__(
            "Harga harus lebih dari 0 dan maksimal 999.999.999.999",
            "harga",
            {"invalid_value": harga},
        )


class DeleteReasonTooShortError(ValidationError):
    """Alasan hapus terlalu pendek."""

    def __init__(self, length: int) -> None:
        """Initialize DeleteReasonTooShortError."""
        super().__init__(
            f"Alasan penghapusan minimal 20 karakter (saat ini: {length})",
            "alasan_hapus",
            {"current_length": length, "min_length": 20},
        )


class MutationReasonTooShortError(ValidationError):
    """Alasan mutasi terlalu pendek."""

    def __init__(self, length: int) -> None:
        """Initialize MutationReasonTooShortError."""
        super().__init__(
            f"Alasan mutasi minimal 10 karakter (saat ini: {length})",
            "alasan_mutasi",
            {"current_length": length, "min_length": 10},
        )


class FutureDateError(ValidationError):
    """Tanggal tidak boleh di masa depan."""

    def __init__(self, field: str, date_value: str) -> None:
        """Initialize FutureDateError."""
        super().__init__(
            f"Tanggal tidak boleh di masa depan: {date_value}",
            field,
            {"invalid_date": date_value},
        )


class InvalidPasswordError(ValidationError):
    """Password tidak memenuhi requirement."""

    def __init__(self, message: str = "Password minimal 8 karakter") -> None:
        """Initialize InvalidPasswordError."""
        super().__init__(message, "password", {"min_length": 8})


class DuplicateUsernameError(ValidationError):
    """Username sudah digunakan."""

    def __init__(self, username: str) -> None:
        """Initialize DuplicateUsernameError."""
        super().__init__(
            f"Username '{username}' sudah digunakan",
            "username",
            {"existing_username": username},
        )


# === Business Logic Exceptions ===


class BusinessRuleError(SimanisException):
    """Error terkait aturan bisnis."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize BusinessRuleError."""
        super().__init__(message, "BUSINESS_ERROR", details, 400)


class AssetInMutationError(BusinessRuleError):
    """Aset sedang dalam proses mutasi."""

    def __init__(self, aset_id: str) -> None:
        """Initialize AssetInMutationError."""
        super().__init__(
            "Aset sedang dalam proses mutasi dan tidak dapat diubah/dihapus",
            {"aset_id": aset_id, "status": "Mutasi"},
        )


class SameRoomMutationError(BusinessRuleError):
    """Mutasi ke ruangan yang sama."""

    def __init__(self, ruangan_id: str) -> None:
        """Initialize SameRoomMutationError."""
        super().__init__(
            "Ruangan tujuan tidak boleh sama dengan ruangan asal",
            {"ruangan_id": ruangan_id},
        )


class CannotDeleteSelfError(BusinessRuleError):
    """Admin tidak bisa menghapus dirinya sendiri."""

    def __init__(self) -> None:
        """Initialize CannotDeleteSelfError."""
        super().__init__("Anda tidak dapat menghapus akun sendiri")


class CannotChangeOwnRoleError(BusinessRuleError):
    """Admin tidak bisa mengubah role sendiri."""

    def __init__(self) -> None:
        """Initialize CannotChangeOwnRoleError."""
        super().__init__("Anda tidak dapat mengubah role akun sendiri")


class AssetNotEditableError(BusinessRuleError):
    """Aset tidak bisa diedit karena status tertentu."""

    def __init__(self, status: str) -> None:
        """Initialize AssetNotEditableError."""
        super().__init__(
            f"Aset dengan status '{status}' tidak dapat diedit",
            {"status": status},
        )


# === Resource Exceptions ===


class ResourceNotFoundError(SimanisException):
    """Resource tidak ditemukan."""

    def __init__(self, resource_type: str, resource_id: str) -> None:
        """Initialize ResourceNotFoundError."""
        super().__init__(
            f"{resource_type} dengan ID '{resource_id}' tidak ditemukan",
            "NOT_FOUND",
            {"resource_type": resource_type, "resource_id": resource_id},
            404,
        )


class AssetNotFoundError(ResourceNotFoundError):
    """Aset tidak ditemukan."""

    def __init__(self, aset_id: str) -> None:
        """Initialize AssetNotFoundError."""
        super().__init__("Aset", aset_id)


class UserNotFoundError(ResourceNotFoundError):
    """User tidak ditemukan."""

    def __init__(self, user_id: str) -> None:
        """Initialize UserNotFoundError."""
        super().__init__("User", user_id)


class RuanganNotFoundError(ResourceNotFoundError):
    """Ruangan tidak ditemukan."""

    def __init__(self, ruangan_id: str) -> None:
        """Initialize RuanganNotFoundError."""
        super().__init__("Ruangan", ruangan_id)


class MutationNotFoundError(ResourceNotFoundError):
    """Mutasi tidak ditemukan."""

    def __init__(self, mutasi_id: str) -> None:
        """Initialize MutationNotFoundError."""
        super().__init__("Mutasi", mutasi_id)


# === Database Exceptions ===


class DatabaseError(SimanisException):
    """Error terkait database."""

    def __init__(
        self,
        message: str = "Terjadi kesalahan database",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize DatabaseError."""
        super().__init__(message, "DB_ERROR", details, 500)


class DatabaseConnectionError(DatabaseError):
    """Tidak dapat terhubung ke database."""

    def __init__(self) -> None:
        """Initialize DatabaseConnectionError."""
        super().__init__("Tidak dapat terhubung ke database")


class DatabaseLockedError(DatabaseError):
    """Database sedang terkunci."""

    def __init__(self) -> None:
        """Initialize DatabaseLockedError."""
        super().__init__("Database sedang sibuk, silakan coba lagi")


class IntegrityError(DatabaseError):
    """Database integrity constraint violation."""

    def __init__(self, message: str, constraint: str | None = None) -> None:
        """Initialize IntegrityError."""
        details = {"constraint": constraint} if constraint else {}
        super().__init__(message, details)
