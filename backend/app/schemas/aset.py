"""
Pydantic schemas untuk Aset endpoints.

Menyediakan request/response schemas untuk validasi data.
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.aset import AsalUsul, KategoriKIB, Kondisi, StatusAset


class AsetBase(BaseModel):
    """Base schema untuk Aset."""

    model_config = ConfigDict(from_attributes=True)

    kode_barang: str = Field(..., min_length=13, max_length=13, pattern=r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$")
    nama_barang: str = Field(..., min_length=3, max_length=200)
    kategori_kib: KategoriKIB
    tahun_perolehan: int = Field(..., ge=1900, le=2100)
    tanggal_perolehan: date | None = None
    asal_usul: AsalUsul
    harga: int = Field(..., gt=0, le=999999999999)
    kondisi: Kondisi
    keterangan: str | None = Field(None, max_length=500)
    ruangan_id: UUID


class AsetCreate(AsetBase):
    """Schema untuk create aset."""

    nomor_register: int = Field(..., ge=1)
    created_by: UUID


class AsetUpdate(BaseModel):
    """Schema untuk update aset."""

    model_config = ConfigDict(from_attributes=True)

    nama_barang: str | None = Field(None, min_length=3, max_length=200)
    kondisi: Kondisi | None = None
    keterangan: str | None = Field(None, max_length=500)
    updated_by: UUID | None = None


class AsetDeleteRequest(BaseModel):
    """Schema untuk delete aset request."""

    model_config = ConfigDict(from_attributes=True)

    alasan_penghapusan: str = Field(..., min_length=20, max_length=500)


class AsetResponse(AsetBase):
    """Schema untuk response aset."""

    id: UUID
    nomor_register: int
    status: StatusAset
    created_by: UUID
    updated_by: UUID | None = None
    deleted_by: UUID | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    delete_reason: str | None = None
