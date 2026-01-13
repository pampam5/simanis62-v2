"""
Pydantic schemas untuk Mutasi endpoints.

Menyediakan request/response schemas untuk validasi data.
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.aset import Kondisi
from app.models.mutasi import StatusMutasi


class MutasiBase(BaseModel):
    """Base schema untuk Mutasi."""

    model_config = ConfigDict(from_attributes=True)

    aset_id: UUID
    ruangan_tujuan_id: UUID
    tanggal_mutasi: date
    alasan: str = Field(..., min_length=10, max_length=500)
    kondisi_saat_mutasi: Kondisi


class MutasiCreate(MutasiBase):
    """Schema untuk create mutasi."""

    ruangan_asal_id: UUID
    user_id: UUID


class MutasiResponse(MutasiBase):
    """Schema untuk response mutasi."""

    id: UUID
    ruangan_asal_id: UUID
    status_mutasi: StatusMutasi
    user_id: UUID
    mulai_mutasi: datetime
    selesai_mutasi: datetime | None = None
    alasan_pembatalan: str | None = None


class MutasiSearchParams(BaseModel):
    """Schema untuk search parameters mutasi."""

    model_config = ConfigDict(from_attributes=True)

    aset_id: UUID | None = None
    ruangan_asal_id: UUID | None = None
    ruangan_tujuan_id: UUID | None = None
    status_mutasi: StatusMutasi | None = None
    tanggal_mulai: date | None = None
    tanggal_akhir: date | None = None


class MutasiCompleteRequest(BaseModel):
    """Schema untuk complete mutasi request."""

    model_config = ConfigDict(from_attributes=True)

    kondisi_akhir: Kondisi
    catatan: str | None = Field(None, max_length=500)


class MutasiCancelRequest(BaseModel):
    """Schema untuk cancel mutasi request."""

    model_config = ConfigDict(from_attributes=True)

    alasan_pembatalan: str = Field(..., min_length=10, max_length=500)
