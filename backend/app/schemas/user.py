"""User Management schemas untuk SIMANIS62 V2.

Module ini berisi Pydantic schemas untuk:
- UserCreate: Schema untuk membuat user baru
- UserUpdate: Schema untuk update user
- UserResponse: Schema untuk response user (re-export dari auth.py)
- UserSearchParams: Schema untuk parameter search user
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.user import UserRole, UserStatus
from app.schemas.auth import UserResponse  # Re-export untuk konsistensi

# =============================================================================
# Validators
# =============================================================================


def validate_username(v: str) -> str:
    """Validate username hanya alphanumeric dan underscore."""
    if not v.replace("_", "").isalnum():
        raise ValueError("Username hanya boleh berisi huruf, angka, dan underscore")
    return v.lower()


def validate_password_strength(v: str) -> str:
    """Validate password minimal 8 karakter."""
    if len(v) < 8:
        raise ValueError("Password harus minimal 8 karakter")
    return v


# =============================================================================
# Request Schemas
# =============================================================================


class UserCreate(BaseModel):
    """Schema untuk membuat user baru.

    Attributes:
        username: Username unik (5-50 karakter, alphanumeric + underscore).
        password: Password plain text (min 8 karakter).
        nama_lengkap: Nama lengkap user.
        role: Role user (Admin/Viewer).
        dapat_ekspor: Izin export untuk Viewer (Kepala Sekolah).
    """

    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Username unik (5-50 karakter)",
        examples=["admin_sekolah"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 karakter)",
        examples=["password123"],
    )
    nama_lengkap: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Nama lengkap user",
        examples=["Budi Santoso"],
    )
    role: UserRole = Field(
        default=UserRole.VIEWER,
        description="Role user (Admin/Viewer)",
        examples=["Viewer"],
    )
    dapat_ekspor: bool = Field(
        default=False,
        description="Izin export untuk Viewer (Kepala Sekolah)",
    )

    # Validators
    @field_validator("username")
    @classmethod
    def validate_username_field(cls, v: str) -> str:
        """Validate username."""
        return validate_username(v)

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str) -> str:
        """Validate password strength."""
        return validate_password_strength(v)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin_sekolah",
                "password": "password123",
                "nama_lengkap": "Budi Santoso",
                "role": "Admin",
                "dapat_ekspor": True,
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema untuk update user (partial update).

    Semua field optional karena partial update.
    Username tidak bisa diubah.
    """

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=100,
        description="Password baru (min 8 karakter)",
    )
    nama_lengkap: str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
        description="Nama lengkap user",
    )
    role: UserRole | None = Field(
        default=None,
        description="Role user (Admin/Viewer)",
    )
    dapat_ekspor: bool | None = Field(
        default=None,
        description="Izin export untuk Viewer",
    )
    status: UserStatus | None = Field(
        default=None,
        description="Status user (Aktif/Nonaktif)",
    )

    @field_validator("password")
    @classmethod
    def validate_password_field(cls, v: str | None) -> str | None:
        """Validate password strength jika ada."""
        if v is not None:
            return validate_password_strength(v)
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama_lengkap": "Budi Santoso, S.Pd",
                "dapat_ekspor": True,
            }
        }
    )


class UserDeactivateRequest(BaseModel):
    """Schema untuk menonaktifkan user.

    Attributes:
        alasan: Alasan penonaktifan (optional).
    """

    alasan: str | None = Field(
        default=None,
        max_length=500,
        description="Alasan penonaktifan user",
        examples=["User sudah tidak aktif di sekolah"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "alasan": "User sudah tidak aktif di sekolah",
            }
        }
    )


# =============================================================================
# Search Params
# =============================================================================


class UserSearchParams(BaseModel):
    """Schema untuk parameter search user.

    Digunakan sebagai query parameters di endpoint GET /users.
    """

    keyword: str | None = Field(
        default=None,
        max_length=100,
        description="Kata kunci search (username, nama)",
        examples=["admin"],
    )
    role: UserRole | None = Field(
        default=None,
        description="Filter berdasarkan role",
        examples=["Admin"],
    )
    status: UserStatus | None = Field(
        default=None,
        description="Filter berdasarkan status",
        examples=["Aktif"],
    )
    dapat_ekspor: bool | None = Field(
        default=None,
        description="Filter berdasarkan izin export",
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Nomor halaman",
        examples=[1],
    )
    page_size: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Jumlah item per halaman (max 1000)",
        examples=[100],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "Admin",
                "status": "Aktif",
                "page": 1,
                "page_size": 100,
            }
        }
    )


__all__ = [
    "UserCreate",
    "UserDeactivateRequest",
    "UserResponse",
    "UserSearchParams",
    "UserUpdate",
]
