"""RiwayatMutasi model untuk tracking perpindahan aset.

Model ini mendefinisikan:
- StatusMutasi: Enum untuk status mutasi
- RiwayatMutasi: SQLModel untuk tabel riwayat_mutasi
"""

import uuid
from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .aset import Kondisi
from .base import generate_uuid

if TYPE_CHECKING:
    from .aset import Aset
    from .ruangan import Ruangan
    from .user import User


class StatusMutasi(str, Enum):
    """Enum untuk status mutasi.

    Attributes:
        DALAM_PROSES: Mutasi sedang dalam proses.
        SELESAI: Mutasi selesai, aset sudah dipindahkan.
        DIBATALKAN: Mutasi dibatalkan.
    """

    DALAM_PROSES = "Dalam Proses"
    SELESAI = "Selesai"
    DIBATALKAN = "Dibatalkan"


class RiwayatMutasi(SQLModel, table=True):
    """Model untuk tabel riwayat_mutasi.

    Tabel ini menyimpan history perpindahan aset antar ruangan.
    Setiap mutasi memiliki status: Dalam Proses, Selesai, atau Dibatalkan.

    Business Rules:
    - Ruangan asal dan tujuan harus berbeda.
    - Alasan mutasi minimal 10 karakter.
    - Mutasi harus dikonfirmasi dalam 7 hari, jika tidak akan auto-cancel.
    - Satu aset hanya boleh memiliki satu mutasi pending.

    Attributes:
        id: UUID primary key.
        aset_id: FK ke aset yang dimutasi.
        ruangan_asal_id: FK ke ruangan asal.
        ruangan_tujuan_id: FK ke ruangan tujuan.
        user_id: FK ke user yang memproses.
        tanggal_mutasi: Tanggal mutasi.
        alasan: Alasan mutasi (min 10 karakter).
        kondisi_saat_mutasi: Kondisi aset saat mutasi.
        status_mutasi: Status mutasi.
        mulai_mutasi: Timestamp mulai mutasi.
        selesai_mutasi: Timestamp selesai mutasi.
        alasan_pembatalan: Alasan pembatalan (jika dibatalkan).
    """

    __tablename__ = "riwayat_mutasi"

    # Primary Key
    id: uuid.UUID = Field(
        default_factory=generate_uuid,
        primary_key=True,
        description="UUID primary key",
    )

    # Foreign Keys
    aset_id: uuid.UUID = Field(
        foreign_key="aset.id",
        index=True,
        description="FK ke aset yang dimutasi",
    )
    ruangan_asal_id: uuid.UUID = Field(
        foreign_key="ruangan.id",
        index=True,
        description="FK ke ruangan asal",
    )
    ruangan_tujuan_id: uuid.UUID = Field(
        foreign_key="ruangan.id",
        index=True,
        description="FK ke ruangan tujuan",
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        description="FK ke user yang memproses mutasi",
    )

    # Mutation Details
    tanggal_mutasi: date = Field(
        description="Tanggal mutasi",
    )
    alasan: str = Field(
        min_length=10,
        max_length=500,
        description="Alasan mutasi (min 10 karakter)",
    )
    kondisi_saat_mutasi: Kondisi = Field(
        description="Kondisi aset saat mutasi",
    )
    status_mutasi: StatusMutasi = Field(
        default=StatusMutasi.DALAM_PROSES,
        index=True,
        description="Status mutasi: Dalam Proses/Selesai/Dibatalkan",
    )

    # Timestamps
    mulai_mutasi: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp mulai mutasi",
    )
    selesai_mutasi: datetime | None = Field(
        default=None,
        description="Timestamp selesai mutasi",
    )

    # Cancellation
    alasan_pembatalan: str | None = Field(
        default=None,
        max_length=500,
        description="Alasan pembatalan (jika dibatalkan)",
    )

    # Relationships
    aset: "Aset" = Relationship(back_populates="riwayat_mutasi")
    ruangan_asal: "Ruangan" = Relationship(
        back_populates="riwayat_mutasi_asal",
        sa_relationship_kwargs={"foreign_keys": "[RiwayatMutasi.ruangan_asal_id]"},
    )
    ruangan_tujuan: "Ruangan" = Relationship(
        back_populates="riwayat_mutasi_tujuan",
        sa_relationship_kwargs={"foreign_keys": "[RiwayatMutasi.ruangan_tujuan_id]"},
    )
    user: "User" = Relationship(back_populates="riwayat_mutasi")

    @property
    def is_pending(self) -> bool:
        """Check apakah mutasi masih pending.

        Returns:
            True jika status adalah Dalam Proses.
        """
        return self.status_mutasi == StatusMutasi.DALAM_PROSES

    @property
    def is_completed(self) -> bool:
        """Check apakah mutasi sudah selesai.

        Returns:
            True jika status adalah Selesai.
        """
        return self.status_mutasi == StatusMutasi.SELESAI

    @property
    def is_cancelled(self) -> bool:
        """Check apakah mutasi dibatalkan.

        Returns:
            True jika status adalah Dibatalkan.
        """
        return self.status_mutasi == StatusMutasi.DIBATALKAN
