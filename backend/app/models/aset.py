"""Aset model - Main asset table untuk semua kategori KIB.

Model ini mendefinisikan:
- KategoriKIB: Enum untuk kategori KIB (A-F)
- AsalUsul: Enum untuk asal usul aset
- Kondisi: Enum untuk kondisi aset
- StatusAset: Enum untuk status aset
- Aset: SQLModel untuk tabel aset utama
"""

import uuid
from datetime import UTC, date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from .base import generate_uuid

if TYPE_CHECKING:
    from .aset_kib import (
        AsetKIBA,
        AsetKIBB,
        AsetKIBC,
        AsetKIBD,
        AsetKIBE,
        AsetKIBF,
    )
    from .mutasi import RiwayatMutasi
    from .ruangan import Ruangan
    from .user import User


class KategoriKIB(str, Enum):
    """Enum untuk kategori KIB.

    Attributes:
        A: Tanah
        B: Peralatan dan Mesin
        C: Gedung dan Bangunan
        D: Jalan, Irigasi, dan Jaringan
        E: Aset Tetap Lainnya
        F: Konstruksi dalam Pengerjaan
    """

    A = "A"  # Tanah
    B = "B"  # Peralatan dan Mesin
    C = "C"  # Gedung dan Bangunan
    D = "D"  # Jalan, Irigasi, dan Jaringan
    E = "E"  # Aset Tetap Lainnya
    F = "F"  # Konstruksi dalam Pengerjaan


class AsalUsul(str, Enum):
    """Enum untuk asal usul perolehan aset.

    Attributes:
        PEMBELIAN: Aset diperoleh melalui pembelian.
        HIBAH: Aset diperoleh melalui hibah.
        BANTUAN: Aset diperoleh melalui bantuan.
        APBD: Aset diperoleh melalui APBD.
    """

    PEMBELIAN = "Pembelian"
    HIBAH = "Hibah"
    BANTUAN = "Bantuan"
    APBD = "APBD"


class Kondisi(str, Enum):
    """Enum untuk kondisi fisik aset.

    Attributes:
        BAIK: Kondisi baik.
        RUSAK_RINGAN: Kondisi rusak ringan.
        RUSAK_BERAT: Kondisi rusak berat.
    """

    BAIK = "Baik"
    RUSAK_RINGAN = "Rusak Ringan"
    RUSAK_BERAT = "Rusak Berat"


class StatusAset(str, Enum):
    """Enum untuk status aset.

    Attributes:
        BARU: Aset baru ditambahkan.
        AKTIF: Aset aktif dan dapat digunakan.
        MUTASI: Aset sedang dalam proses mutasi.
        RUSAK: Aset dalam kondisi rusak.
        DIHAPUS: Aset sudah dihapus (soft delete).
    """

    BARU = "Baru"
    AKTIF = "Aktif"
    MUTASI = "Mutasi"
    RUSAK = "Rusak"
    DIHAPUS = "Dihapus"


class Aset(SQLModel, table=True):
    """Model untuk tabel aset utama.

    Tabel ini menyimpan data aset untuk semua kategori KIB (A-F).
    Field spesifik per kategori disimpan di tabel extension (aset_kib_a sampai aset_kib_f).

    Attributes:
        id: UUID primary key.
        kode_barang: Kode unik aset (format: XX.XX.XX.XXXX).
        nama_barang: Nama/deskripsi aset.
        nomor_register: Nomor urut per kategori KIB.
        kategori_kib: Kategori KIB (A/B/C/D/E/F).
        tahun_perolehan: Tahun perolehan aset.
        tanggal_perolehan: Tanggal lengkap perolehan.
        asal_usul: Sumber perolehan aset.
        harga: Nilai perolehan dalam Rupiah penuh.
        kondisi: Kondisi fisik aset.
        status: Status aset.
        keterangan: Catatan tambahan.
        ruangan_id: FK ke tabel ruangan.
        created_by: FK ke user yang membuat.
        updated_by: FK ke user yang mengupdate.
        deleted_by: FK ke user yang menghapus.
        created_at: Timestamp pembuatan.
        updated_at: Timestamp update terakhir.
        deleted_at: Timestamp penghapusan.
        delete_reason: Alasan penghapusan.
    """

    __tablename__ = "aset"

    # Primary Key
    id: uuid.UUID = Field(
        default_factory=generate_uuid,
        primary_key=True,
        description="UUID primary key",
    )

    # Asset Identification
    kode_barang: str = Field(
        unique=True,
        max_length=20,
        index=True,
        description="Kode unik aset (format: XX.XX.XX.XXXX)",
    )
    nama_barang: str = Field(
        min_length=3,
        max_length=200,
        index=True,
        description="Nama/deskripsi aset (3-200 karakter)",
    )
    nomor_register: int = Field(
        ge=1,
        index=True,
        description="Nomor urut per kategori KIB (auto-increment)",
    )
    kategori_kib: KategoriKIB = Field(
        index=True,
        description="Kategori KIB: A/B/C/D/E/F",
    )

    # Asset Details
    tahun_perolehan: int = Field(
        ge=1900,
        le=2100,
        description="Tahun perolehan aset (1900-2100)",
    )
    tanggal_perolehan: date | None = Field(
        default=None,
        description="Tanggal lengkap perolehan (format DD/MM/YYYY untuk laporan)",
    )
    asal_usul: AsalUsul = Field(
        description="Sumber perolehan: Pembelian/Hibah/Bantuan/APBD",
    )
    harga: int = Field(
        gt=0,
        le=999999999999,
        description="Nilai perolehan dalam Rupiah penuh (max 999.999.999.999)",
    )
    kondisi: Kondisi = Field(
        description="Kondisi fisik: Baik/Rusak Ringan/Rusak Berat",
    )
    status: StatusAset = Field(
        default=StatusAset.BARU,
        index=True,
        description="Status: Baru/Aktif/Mutasi/Rusak/Dihapus",
    )
    keterangan: str | None = Field(
        default=None,
        max_length=500,
        description="Catatan tambahan (max 500 karakter)",
    )

    # Foreign Keys
    ruangan_id: uuid.UUID = Field(
        foreign_key="ruangan.id",
        index=True,
        description="FK ke ruangan lokasi aset",
    )
    created_by: uuid.UUID = Field(
        foreign_key="users.id",
        description="FK ke user yang membuat",
    )
    updated_by: uuid.UUID | None = Field(
        default=None,
        foreign_key="users.id",
        description="FK ke user yang mengupdate",
    )
    deleted_by: uuid.UUID | None = Field(
        default=None,
        foreign_key="users.id",
        description="FK ke user yang menghapus",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp pembuatan aset",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp update terakhir",
    )
    deleted_at: datetime | None = Field(
        default=None,
        description="Timestamp soft delete",
    )

    # Soft Delete
    delete_reason: str | None = Field(
        default=None,
        max_length=500,
        description="Alasan penghapusan (min 20 karakter)",
    )

    # Relationships
    ruangan: "Ruangan" = Relationship(back_populates="aset")
    creator: "User" = Relationship(
        back_populates="aset_created",
        sa_relationship_kwargs={"foreign_keys": "[Aset.created_by]"},
    )
    updater: Optional["User"] = Relationship(
        back_populates="aset_updated",
        sa_relationship_kwargs={"foreign_keys": "[Aset.updated_by]"},
    )
    deleter: Optional["User"] = Relationship(
        back_populates="aset_deleted",
        sa_relationship_kwargs={"foreign_keys": "[Aset.deleted_by]"},
    )

    # KIB Extensions (One-to-One)
    kib_a: Optional["AsetKIBA"] = Relationship(back_populates="aset")
    kib_b: Optional["AsetKIBB"] = Relationship(back_populates="aset")
    kib_c: Optional["AsetKIBC"] = Relationship(back_populates="aset")
    kib_d: Optional["AsetKIBD"] = Relationship(back_populates="aset")
    kib_e: Optional["AsetKIBE"] = Relationship(back_populates="aset")
    kib_f: Optional["AsetKIBF"] = Relationship(back_populates="aset")

    # Mutation History
    riwayat_mutasi: list["RiwayatMutasi"] = Relationship(back_populates="aset")

    @property
    def is_deleted(self) -> bool:
        """Check apakah aset sudah dihapus (soft delete).

        Returns:
            True jika status adalah Dihapus.
        """
        return self.status == StatusAset.DIHAPUS

    @property
    def is_in_mutation(self) -> bool:
        """Check apakah aset sedang dalam proses mutasi.

        Returns:
            True jika status adalah Mutasi.
        """
        return self.status == StatusAset.MUTASI

    @property
    def is_valid_for_report(self) -> bool:
        """Check apakah aset valid untuk laporan KIB.

        Hanya aset dengan status Aktif atau Rusak yang masuk laporan.

        Returns:
            True jika status adalah Aktif atau Rusak.
        """
        return self.status in (StatusAset.AKTIF, StatusAset.RUSAK)
