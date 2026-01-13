"""User model untuk authentication dan authorization.

Model ini mendefinisikan:
- UserRole: Enum untuk role (Admin/Viewer)
- UserStatus: Enum untuk status (Aktif/Nonaktif)
- User: SQLModel untuk tabel users
"""

import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .base import generate_uuid

if TYPE_CHECKING:
    from .aset import Aset
    from .audit import AuditTrail
    from .mutasi import RiwayatMutasi


class UserRole(str, Enum):
    """Enum untuk role user.

    Attributes:
        ADMIN: Full access (CRUD, reports, export, user management).
        VIEWER: Read-only access.
    """

    ADMIN = "Admin"
    VIEWER = "Viewer"


class UserStatus(str, Enum):
    """Enum untuk status user.

    Attributes:
        AKTIF: User aktif dan dapat login.
        NONAKTIF: User nonaktif (soft delete).
    """

    AKTIF = "Aktif"
    NONAKTIF = "Nonaktif"


class User(SQLModel, table=True):
    """Model untuk tabel users.

    Tabel ini menyimpan data user untuk authentication dan authorization.
    Menggunakan role-based access control (RBAC) dengan 2 role: Admin dan Viewer.

    Kepala Sekolah diimplementasikan sebagai Viewer dengan dapat_ekspor=True.

    Attributes:
        id: UUID primary key.
        username: Username unik untuk login (5-50 karakter).
        password_hash: Password yang di-hash dengan bcrypt.
        nama_lengkap: Nama lengkap user.
        role: Role user (Admin/Viewer).
        status: Status user (Aktif/Nonaktif).
        dapat_ekspor: Flag izin export untuk Viewer (Kepala Sekolah).
        created_at: Timestamp pembuatan.
        updated_at: Timestamp update terakhir.
    """

    __tablename__ = "users"

    # Primary Key
    id: uuid.UUID = Field(
        default_factory=generate_uuid,
        primary_key=True,
        description="UUID primary key",
    )

    # Authentication
    username: str = Field(
        unique=True,
        min_length=5,
        max_length=50,
        index=True,
        description="Username unik untuk login (5-50 karakter)",
    )
    password_hash: str = Field(
        max_length=255,
        description="Password yang di-hash dengan bcrypt",
    )

    # User Info
    nama_lengkap: str = Field(
        max_length=200,
        description="Nama lengkap user",
    )

    # Authorization
    role: UserRole = Field(
        default=UserRole.VIEWER,
        description="Role user: Admin atau Viewer",
    )
    status: UserStatus = Field(
        default=UserStatus.AKTIF,
        description="Status user: Aktif atau Nonaktif",
    )
    dapat_ekspor: bool = Field(
        default=False,
        description="Izin export untuk Viewer (enables Kepala Sekolah functionality)",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp pembuatan user",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp update terakhir",
    )

    # Relationships
    aset_created: list["Aset"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "Aset.created_by"},
    )
    aset_updated: list["Aset"] = Relationship(
        back_populates="updater",
        sa_relationship_kwargs={"foreign_keys": "Aset.updated_by"},
    )
    aset_deleted: list["Aset"] = Relationship(
        back_populates="deleter",
        sa_relationship_kwargs={"foreign_keys": "Aset.deleted_by"},
    )
    riwayat_mutasi: list["RiwayatMutasi"] = Relationship(back_populates="user")
    audit_trail: list["AuditTrail"] = Relationship(back_populates="user")

    @property
    def is_admin(self) -> bool:
        """Check apakah user adalah Admin.

        Returns:
            True jika role adalah Admin.
        """
        return self.role == UserRole.ADMIN

    @property
    def is_active(self) -> bool:
        """Check apakah user aktif.

        Returns:
            True jika status adalah Aktif.
        """
        return self.status == UserStatus.AKTIF

    @property
    def can_export(self) -> bool:
        """Check apakah user dapat export.

        Admin selalu dapat export.
        Viewer dapat export jika dapat_ekspor=True (Kepala Sekolah).

        Returns:
            True jika user dapat export.
        """
        return self.is_admin or self.dapat_ekspor
