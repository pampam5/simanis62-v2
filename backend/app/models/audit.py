"""AuditTrail model untuk logging semua operasi CRUD.

Model ini mendefinisikan:
- Operation: Enum untuk tipe operasi
- AuditTrail: SQLModel untuk tabel audit_trail
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text
from sqlmodel import Field, Relationship, SQLModel

from .base import generate_uuid

if TYPE_CHECKING:
    from .user import User


class Operation(str, Enum):
    """Enum untuk tipe operasi audit.

    Attributes:
        CREATE: Operasi pembuatan record baru.
        UPDATE: Operasi update record.
        DELETE: Operasi penghapusan record.
    """

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class AuditTrail(SQLModel, table=True):
    """Model untuk tabel audit_trail.

    Tabel ini menyimpan log lengkap semua operasi CRUD untuk audit dan compliance.
    Record audit trail tidak dapat dimodifikasi atau dihapus.

    Attributes:
        id: UUID primary key.
        table_name: Nama tabel yang terpengaruh.
        record_id: UUID record yang terpengaruh.
        operation: Tipe operasi (CREATE/UPDATE/DELETE).
        user_id: FK ke user yang melakukan operasi.
        old_value: JSON data sebelum perubahan (untuk UPDATE/DELETE).
        new_value: JSON data setelah perubahan (untuk CREATE/UPDATE).
        timestamp: Timestamp operasi.
        ip_address: IP address user (optional).
    """

    __tablename__ = "audit_trail"

    # Primary Key
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="UUID primary key",
    )

    # Audit Info
    table_name: str = Field(
        max_length=50,
        index=True,
        description="Nama tabel yang terpengaruh (contoh: aset, users)",
    )
    record_id: str = Field(
        max_length=36,
        index=True,
        description="UUID record yang terpengaruh",
    )
    operation: Operation = Field(
        index=True,
        description="Tipe operasi: CREATE/UPDATE/DELETE",
    )

    # User Info
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="FK ke user yang melakukan operasi",
    )

    # Data Changes
    old_value: str | None = Field(
        default=None,
        sa_column=Column(Text),
        description="JSON data sebelum perubahan (untuk UPDATE/DELETE)",
    )
    new_value: str | None = Field(
        default=None,
        sa_column=Column(Text),
        description="JSON data setelah perubahan (untuk CREATE/UPDATE)",
    )

    # Timestamp
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Timestamp operasi",
    )

    # Optional
    ip_address: str | None = Field(
        default=None,
        max_length=45,
        description="IP address user (optional, supports IPv6)",
    )

    # Relationship
    user: "User" = Relationship(back_populates="audit_trail")

    @property
    def is_create(self) -> bool:
        """Check apakah operasi adalah CREATE.

        Returns:
            True jika operation adalah CREATE.
        """
        return self.operation == Operation.CREATE

    @property
    def is_update(self) -> bool:
        """Check apakah operasi adalah UPDATE.

        Returns:
            True jika operation adalah UPDATE.
        """
        return self.operation == Operation.UPDATE

    @property
    def is_delete(self) -> bool:
        """Check apakah operasi adalah DELETE.

        Returns:
            True jika operation adalah DELETE.
        """
        return self.operation == Operation.DELETE
