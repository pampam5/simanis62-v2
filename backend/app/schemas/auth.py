"""Authentication schemas untuk SIMANIS62 V2.

Module ini berisi Pydantic schemas untuk:
- LoginRequest: Request body untuk login
- LoginResponse: Response setelah login berhasil
- UserResponse: Response data user (tanpa password)
- SessionInfo: Informasi session aktif
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.user import UserRole, UserStatus


class LoginRequest(BaseModel):
    """Schema untuk request login.

    Attributes:
        username: Username untuk login (5-50 karakter).
        password: Password plain text (min 8 karakter).

    Example:
        ```python
        login_data = LoginRequest(username="admin", password="password123")
        ```
    """

    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Username untuk login",
        examples=["admin"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 karakter)",
        examples=["password123"],
    )

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username hanya alphanumeric dan underscore."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Username hanya boleh berisi huruf, angka, dan underscore")
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "password123",
            }
        }
    )


class UserResponse(BaseModel):
    """Schema untuk response data user (tanpa password).

    Digunakan untuk menampilkan informasi user di response API.

    Attributes:
        id: UUID user.
        username: Username user.
        nama_lengkap: Nama lengkap user.
        role: Role user (Admin/Viewer).
        status: Status user (Aktif/Nonaktif).
        dapat_ekspor: Flag izin export.
        created_at: Timestamp pembuatan.
        updated_at: Timestamp update terakhir.
    """

    id: str = Field(..., description="UUID user")
    username: str = Field(..., description="Username user")
    nama_lengkap: str = Field(..., description="Nama lengkap user")
    role: UserRole = Field(..., description="Role user")
    status: UserStatus = Field(..., description="Status user")
    dapat_ekspor: bool = Field(..., description="Izin export")
    created_at: datetime = Field(..., description="Timestamp pembuatan")
    updated_at: datetime = Field(..., description="Timestamp update terakhir")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "admin",
                "nama_lengkap": "Administrator",
                "role": "Admin",
                "status": "Aktif",
                "dapat_ekspor": True,
                "created_at": "2026-01-11T10:00:00Z",
                "updated_at": "2026-01-11T10:00:00Z",
            }
        },
    )


class SessionInfo(BaseModel):
    """Schema untuk informasi session.

    Attributes:
        session_id: ID session aktif.
        user_id: UUID user yang login.
        expires_at: Waktu expired session.
    """

    session_id: str = Field(..., description="ID session aktif")
    user_id: str = Field(..., description="UUID user yang login")
    expires_at: datetime = Field(..., description="Waktu expired session")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "abc123def456",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "expires_at": "2026-01-11T12:00:00Z",
            }
        }
    )


class LoginResponse(BaseModel):
    """Schema untuk response login berhasil.

    Attributes:
        user: Data user yang login.
        session: Informasi session.
        message: Pesan sukses.
    """

    user: UserResponse = Field(..., description="Data user yang login")
    session: SessionInfo = Field(..., description="Informasi session")
    message: str = Field(
        default="Login berhasil",
        description="Pesan sukses",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "admin",
                    "nama_lengkap": "Administrator",
                    "role": "Admin",
                    "status": "Aktif",
                    "dapat_ekspor": True,
                    "created_at": "2026-01-11T10:00:00Z",
                    "updated_at": "2026-01-11T10:00:00Z",
                },
                "session": {
                    "session_id": "abc123def456",
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "expires_at": "2026-01-11T12:00:00Z",
                },
                "message": "Login berhasil",
            }
        }
    )


class LogoutResponse(BaseModel):
    """Schema untuk response logout.

    Attributes:
        message: Pesan sukses logout.
    """

    message: str = Field(
        default="Logout berhasil",
        description="Pesan sukses logout",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Logout berhasil",
            }
        }
    )
