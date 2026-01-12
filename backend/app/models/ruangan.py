"""Ruangan model untuk room/location management.

Model ini mendefinisikan tabel ruangan untuk tracking lokasi fisik aset.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .base import generate_uuid

if TYPE_CHECKING:
    from .aset import Aset
    from .mutasi import RiwayatMutasi


class Ruangan(SQLModel, table=True):
    """Model untuk tabel ruangan.

    Tabel ini menyimpan data ruangan/lokasi untuk tracking posisi aset.
    Setiap aset harus berada di satu ruangan.

    Attributes:
        id: UUID primary key.
        nama_ruangan: Nama ruangan (unik).
        kode_ruangan: Kode ruangan (unik).
        keterangan: Deskripsi/catatan ruangan.
        created_at: Timestamp pembuatan.
        updated_at: Timestamp update terakhir.
    """

    __tablename__ = "ruangan"

    # Primary Key
    id: uuid.UUID = Field(
        default_factory=generate_uuid,
        primary_key=True,
        description="UUID primary key",
    )

    # Room Info
    nama_ruangan: str = Field(
        unique=True,
        max_length=200,
        index=True,
        description="Nama ruangan (contoh: Lab Komputer, Ruang Guru)",
    )
    kode_ruangan: str = Field(
        unique=True,
        max_length=50,
        index=True,
        description="Kode ruangan (contoh: LAB-01, RG-02)",
    )
    keterangan: str | None = Field(
        default=None,
        max_length=500,
        description="Deskripsi/catatan ruangan",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp pembuatan ruangan",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp update terakhir",
    )

    # Relationships
    aset: list["Aset"] = Relationship(back_populates="ruangan")
    riwayat_mutasi_asal: list["RiwayatMutasi"] = Relationship(
        back_populates="ruangan_asal",
        sa_relationship_kwargs={"foreign_keys": "RiwayatMutasi.ruangan_asal_id"},
    )
    riwayat_mutasi_tujuan: list["RiwayatMutasi"] = Relationship(
        back_populates="ruangan_tujuan",
        sa_relationship_kwargs={"foreign_keys": "RiwayatMutasi.ruangan_tujuan_id"},
    )

    @property
    def total_aset(self) -> int:
        """Hitung total aset di ruangan ini.

        Returns:
            Jumlah aset di ruangan.
        """
        return len(self.aset) if self.aset else 0
