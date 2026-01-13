"""
Pydantic schemas untuk User endpoints.

Menyediakan request/response schemas untuk validasi data.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole, UserStatus


class UserBase(BaseModel):
    """Base schema untuk User."""

    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=5, max_length=50)
    nama_lengkap: str = Field(..., max_length=200)
    role: UserRole = UserRole.VIEWER
    dapat_ekspor: bool = False


class UserCreate(UserBase):
    """Schema untuk create user."""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema untuk update user."""

    model_config = ConfigDict(from_attributes=True)

    nama_lengkap: str | None = Field(None, max_length=200)
    role: UserRole | None = None
    status: UserStatus | None = None
    dapat_ekspor: bool | None = None


class LoginRequest(BaseModel):
    """Schema untuk login request."""

    username: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """Schema untuk response user."""

    id: UUID
    status: UserStatus
    created_at: datetime
    updated_at: datetime


class UserSearchParams(BaseModel):
    """Schema untuk search parameters user."""

    model_config = ConfigDict(from_attributes=True)

    username: str | None = None
    nama_lengkap: str | None = None
    role: UserRole | None = None
    status: UserStatus | None = None


class UserDeactivateRequest(BaseModel):
    """Schema untuk deactivate user request."""

    model_config = ConfigDict(from_attributes=True)

    alasan: str | None = Field(None, max_length=500)
