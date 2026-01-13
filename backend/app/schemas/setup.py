"""Setup schemas untuk SIMANIS62 V2.

Module ini berisi Pydantic schemas untuk First-Run Setup Wizard:
- SetupStatusResponse: Response untuk check setup status
- CreateAdminRequest: Request body untuk create first admin
- CreateAdminResponse: Response setelah admin dibuat
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SetupStatusResponse(BaseModel):
    """Schema untuk response setup status.

    Attributes:
        needs_setup: True jika setup diperlukan (no users exist).
        message: Pesan informatif untuk user.
    """

    needs_setup: bool = Field(..., description="True jika setup diperlukan")
    message: str = Field(..., description="Pesan untuk user")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "needs_setup": True,
                "message": "Aplikasi belum dikonfigurasi. Silakan buat akun administrator.",
            }
        }
    )


class CreateAdminRequest(BaseModel):
    """Schema untuk request create first admin.

    Attributes:
        username: Username untuk admin (5-50 karakter, alphanumeric + underscore).
        password: Password plain text (min 8 karakter).
        nama_lengkap: Nama lengkap admin (3-100 karakter).
    """

    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Username untuk admin",
        examples=["admin"],
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
        max_length=100,
        description="Nama lengkap admin",
        examples=["Administrator Sekolah"],
    )

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username hanya alphanumeric dan underscore."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Username hanya boleh berisi huruf, angka, dan underscore")
        return v.lower()

    @field_validator("nama_lengkap")
    @classmethod
    def nama_not_empty(cls, v: str) -> str:
        """Validate nama lengkap tidak hanya whitespace."""
        if not v.strip():
            raise ValueError("Nama lengkap tidak boleh kosong")
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "password123",
                "nama_lengkap": "Administrator Sekolah",
            }
        }
    )


class CreateAdminResponse(BaseModel):
    """Schema untuk response setelah admin dibuat.

    Attributes:
        id: UUID admin yang dibuat.
        username: Username admin.
        nama_lengkap: Nama lengkap admin.
        role: Role admin (selalu "Admin").
        status: Status admin (selalu "Aktif").
        dapat_ekspor: Flag izin export (selalu True untuk admin).
    """

    id: str = Field(..., description="UUID admin")
    username: str = Field(..., description="Username admin")
    nama_lengkap: str = Field(..., description="Nama lengkap admin")
    role: str = Field(..., description="Role admin")
    status: str = Field(..., description="Status admin")
    dapat_ekspor: bool = Field(..., description="Izin export")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "admin",
                "nama_lengkap": "Administrator Sekolah",
                "role": "Admin",
                "status": "Aktif",
                "dapat_ekspor": True,
            }
        },
    )
