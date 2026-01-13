"""Base model dengan common fields untuk SIMANIS62 V2.

Module ini menyediakan:
- BaseModel: Base class dengan UUID primary key
- TimestampMixin: Mixin untuk created_at dan updated_at
"""

import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def generate_uuid() -> uuid.UUID:
    """Generate UUID untuk primary key.

    Returns:
        UUID v4 object.
    """
    return uuid.uuid4()


class TimestampMixin(SQLModel):
    """Mixin untuk timestamp fields.

    Attributes:
        created_at: Timestamp pembuatan record.
        updated_at: Timestamp update terakhir.
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp pembuatan record",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp update terakhir",
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )


class BaseModel(TimestampMixin):
    """Base model dengan UUID primary key dan timestamps.

    Semua model database harus inherit dari class ini untuk
    mendapatkan UUID primary key dan timestamp fields secara otomatis.

    Attributes:
        id: UUID primary key (auto-generated).
        created_at: Timestamp pembuatan record.
        updated_at: Timestamp update terakhir.
    """

    id: uuid.UUID = Field(
        default_factory=generate_uuid,
        primary_key=True,
        description="UUID primary key",
    )


class SoftDeleteMixin(SQLModel):
    """Mixin untuk soft delete functionality.

    Attributes:
        deleted_at: Timestamp penghapusan (soft delete).
        deleted_by: User ID yang menghapus.
        delete_reason: Alasan penghapusan (min 20 karakter).
    """

    deleted_at: datetime | None = Field(
        default=None,
        description="Timestamp soft delete",
    )
    deleted_by: uuid.UUID | None = Field(
        default=None,
        description="User ID yang menghapus",
    )
    delete_reason: str | None = Field(
        default=None,
        max_length=500,
        description="Alasan penghapusan (min 20 karakter)",
    )
