"""Mutasi schemas untuk SIMANIS62 V2.

Module ini berisi Pydantic schemas untuk:
- MutasiCreate: Schema untuk membuat mutasi baru
- MutasiResponse: Schema untuk response mutasi
- MutasiCancelRequest: Schema untuk membatalkan mutasi
- MutasiCompleteRequest: Schema untuk menyelesaikan mutasi
- MutasiSearchParams: Schema untuk parameter search mutasi
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.aset import Kondisi
from app.models.mutasi import StatusMutasi

# =============================================================================
# Validators
# =============================================================================


def validate_alasan_min_length(v: str, min_length: int = 10) -> str:
    """Validate alasan minimal 10 karakter."""
    if len(v.strip()) < min_length:
        raise ValueError(f"Alasan harus minimal {min_length} karakter")
    return v.strip()


def validate_tanggal_not_future(v: date) -> date:
    """Validate tanggal tidak boleh di masa depan."""
    if v > date.today():
        raise ValueError("Tanggal mutasi tidak boleh di masa depan")
    return v


# =============================================================================
# Request Schemas
# =============================================================================


class MutasiCreate(BaseModel):
    """Schema untuk membuat mutasi baru.

    Business Rules:
    - Ruangan asal dan tujuan harus berbeda.
    - Alasan mutasi minimal 10 karakter.
    - Tanggal mutasi tidak boleh di masa depan.
    - Aset tidak boleh sedang dalam proses mutasi lain.

    Attributes:
        aset_id: UUID aset yang akan dimutasi.
        ruangan_tujuan_id: UUID ruangan tujuan.
        tanggal_mutasi: Tanggal mutasi (tidak boleh di masa depan).
        alasan: Alasan mutasi (min 10 karakter).
        kondisi_saat_mutasi: Kondisi aset saat mutasi.
    """

    aset_id: str = Field(
        ...,
        max_length=36,
        description="UUID aset yang akan dimutasi",
    )
    ruangan_tujuan_id: str = Field(
        ...,
        max_length=36,
        description="UUID ruangan tujuan",
    )
    tanggal_mutasi: date = Field(
        ...,
        description="Tanggal mutasi (tidak boleh di masa depan)",
        examples=["2026-01-11"],
    )
    alasan: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Alasan mutasi (min 10 karakter)",
        examples=["Pemindahan aset ke ruangan baru untuk keperluan praktikum"],
    )
    kondisi_saat_mutasi: Kondisi = Field(
        default=Kondisi.BAIK,
        description="Kondisi aset saat mutasi",
        examples=["Baik"],
    )

    # Validators
    @field_validator("alasan")
    @classmethod
    def validate_alasan(cls, v: str) -> str:
        """Validate alasan minimal 10 karakter."""
        return validate_alasan_min_length(v, 10)

    @field_validator("tanggal_mutasi")
    @classmethod
    def validate_tanggal(cls, v: date) -> date:
        """Validate tanggal tidak boleh di masa depan."""
        return validate_tanggal_not_future(v)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "aset_id": "550e8400-e29b-41d4-a716-446655440000",
                "ruangan_tujuan_id": "550e8400-e29b-41d4-a716-446655440001",
                "tanggal_mutasi": "2026-01-11",
                "alasan": "Pemindahan aset ke ruangan baru untuk keperluan praktikum",
                "kondisi_saat_mutasi": "Baik",
            }
        }
    )


class MutasiCancelRequest(BaseModel):
    """Schema untuk membatalkan mutasi.

    Attributes:
        alasan_pembatalan: Alasan pembatalan (min 10 karakter).
    """

    alasan_pembatalan: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Alasan pembatalan mutasi (min 10 karakter)",
        examples=["Pembatalan karena ruangan tujuan sedang dalam renovasi"],
    )

    @field_validator("alasan_pembatalan")
    @classmethod
    def validate_alasan(cls, v: str) -> str:
        """Validate alasan pembatalan minimal 10 karakter."""
        return validate_alasan_min_length(v, 10)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "alasan_pembatalan": "Pembatalan karena ruangan tujuan sedang dalam renovasi",
            }
        }
    )


class MutasiCompleteRequest(BaseModel):
    """Schema untuk menyelesaikan mutasi.

    Attributes:
        catatan: Catatan tambahan saat menyelesaikan mutasi (optional).
    """

    catatan: str | None = Field(
        default=None,
        max_length=500,
        description="Catatan tambahan saat menyelesaikan mutasi",
        examples=["Aset sudah diterima dengan baik di ruangan tujuan"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "catatan": "Aset sudah diterima dengan baik di ruangan tujuan",
            }
        }
    )


# =============================================================================
# Response Schemas
# =============================================================================


class RuanganBrief(BaseModel):
    """Schema brief untuk ruangan dalam response mutasi."""

    id: str = Field(..., description="UUID ruangan")
    kode_ruangan: str = Field(..., description="Kode ruangan")
    nama_ruangan: str = Field(..., description="Nama ruangan")

    model_config = ConfigDict(from_attributes=True)


class AsetBrief(BaseModel):
    """Schema brief untuk aset dalam response mutasi."""

    id: str = Field(..., description="UUID aset")
    nama_barang: str = Field(..., description="Nama barang")
    kode_barang: str = Field(..., description="Kode barang")
    nomor_register: int = Field(..., description="Nomor register")

    model_config = ConfigDict(from_attributes=True)


class UserBrief(BaseModel):
    """Schema brief untuk user dalam response mutasi."""

    id: str = Field(..., description="UUID user")
    username: str = Field(..., description="Username")
    nama_lengkap: str = Field(..., description="Nama lengkap")

    model_config = ConfigDict(from_attributes=True)


class MutasiResponse(BaseModel):
    """Schema untuk response mutasi.

    Includes semua field dari model plus related entities.
    """

    id: str = Field(..., description="UUID mutasi")
    aset_id: str = Field(..., description="UUID aset")
    ruangan_asal_id: str = Field(..., description="UUID ruangan asal")
    ruangan_tujuan_id: str = Field(..., description="UUID ruangan tujuan")
    user_id: str = Field(..., description="UUID user yang memproses")
    tanggal_mutasi: date = Field(..., description="Tanggal mutasi")
    alasan: str = Field(..., description="Alasan mutasi")
    kondisi_saat_mutasi: Kondisi = Field(..., description="Kondisi aset saat mutasi")
    status_mutasi: StatusMutasi = Field(..., description="Status mutasi")
    mulai_mutasi: datetime = Field(..., description="Timestamp mulai mutasi")
    selesai_mutasi: datetime | None = Field(
        default=None, description="Timestamp selesai mutasi"
    )
    alasan_pembatalan: str | None = Field(default=None, description="Alasan pembatalan")

    # Related entities (optional, populated when needed)
    aset: AsetBrief | None = Field(default=None, description="Data aset")
    ruangan_asal: RuanganBrief | None = Field(
        default=None, description="Data ruangan asal"
    )
    ruangan_tujuan: RuanganBrief | None = Field(
        default=None, description="Data ruangan tujuan"
    )
    user: UserBrief | None = Field(default=None, description="Data user")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440010",
                "aset_id": "550e8400-e29b-41d4-a716-446655440000",
                "ruangan_asal_id": "550e8400-e29b-41d4-a716-446655440001",
                "ruangan_tujuan_id": "550e8400-e29b-41d4-a716-446655440002",
                "user_id": "550e8400-e29b-41d4-a716-446655440003",
                "tanggal_mutasi": "2026-01-11",
                "alasan": "Pemindahan aset ke ruangan baru untuk keperluan praktikum",
                "kondisi_saat_mutasi": "Baik",
                "status_mutasi": "Dalam Proses",
                "mulai_mutasi": "2026-01-11T10:00:00Z",
                "selesai_mutasi": None,
                "alasan_pembatalan": None,
            }
        },
    )


# =============================================================================
# Search Params
# =============================================================================


class MutasiSearchParams(BaseModel):
    """Schema untuk parameter search mutasi.

    Digunakan sebagai query parameters di endpoint GET /mutasi.
    """

    aset_id: str | None = Field(
        default=None,
        max_length=36,
        description="Filter berdasarkan aset",
    )
    ruangan_id: str | None = Field(
        default=None,
        max_length=36,
        description="Filter berdasarkan ruangan (asal atau tujuan)",
    )
    status_mutasi: StatusMutasi | None = Field(
        default=None,
        description="Filter berdasarkan status mutasi",
        examples=["Dalam Proses"],
    )
    tanggal_dari: date | None = Field(
        default=None,
        description="Filter tanggal mutasi dari",
        examples=["2026-01-01"],
    )
    tanggal_sampai: date | None = Field(
        default=None,
        description="Filter tanggal mutasi sampai",
        examples=["2026-01-31"],
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Nomor halaman",
        examples=[1],
    )
    page_size: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Jumlah item per halaman (max 1000)",
        examples=[100],
    )

    @model_validator(mode="after")
    def validate_date_range(self) -> "MutasiSearchParams":
        """Validate tanggal_dari <= tanggal_sampai."""
        if self.tanggal_dari and self.tanggal_sampai:
            if self.tanggal_dari > self.tanggal_sampai:
                raise ValueError("tanggal_dari harus <= tanggal_sampai")
        return self

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status_mutasi": "Dalam Proses",
                "page": 1,
                "page_size": 100,
            }
        }
    )
