"""Aset schemas untuk SIMANIS62 V2.

Module ini berisi Pydantic schemas untuk:
- AsetBase: Base schema dengan common fields
- AsetCreate: Schema untuk membuat aset baru
- AsetUpdate: Schema untuk update aset (partial)
- AsetResponse: Schema untuk response aset
- AsetSearchParams: Schema untuk parameter search
- KIB-specific schemas (A-F)
"""

import re
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.aset import AsalUsul, KategoriKIB, Kondisi, StatusAset

# =============================================================================
# Validators
# =============================================================================

KODE_BARANG_PATTERN = re.compile(r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$")
CURRENT_YEAR = datetime.now().year


def validate_kode_barang(v: str) -> str:
    """Validate format kode_barang: XX.XX.XX.XXXX."""
    if not KODE_BARANG_PATTERN.match(v):
        raise ValueError(
            "Format kode_barang tidak valid. Gunakan format XX.XX.XX.XXXX "
            "(contoh: 02.06.01.0001)"
        )
    return v


def validate_tahun_perolehan(v: int) -> int:
    """Validate tahun_perolehan: 1900 - current year."""
    if v < 1900 or v > CURRENT_YEAR:
        raise ValueError(f"Tahun perolehan harus antara 1900 dan {CURRENT_YEAR}")
    return v


def validate_harga(v: int) -> int:
    """Validate harga: > 0 dan <= 999.999.999.999."""
    if v < 0:
        raise ValueError("Harga tidak boleh negatif")
    if v > 999_999_999_999:
        raise ValueError("Harga maksimal Rp 999.999.999.999")
    return v


# =============================================================================
# Base Schemas
# =============================================================================


class AsetBase(BaseModel):
    """Base schema untuk Aset dengan common fields.

    Semua field yang shared antara Create, Update, dan Response.
    """

    nama_barang: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Nama barang (3-200 karakter)",
        examples=["Laptop ASUS ROG"],
    )
    kode_barang: str = Field(
        ...,
        max_length=20,
        description="Kode barang format XX.XX.XX.XXXX",
        examples=["02.06.01.0001"],
    )
    kategori_kib: KategoriKIB = Field(
        ...,
        description="Kategori KIB (A-F)",
        examples=["B"],
    )
    tahun_perolehan: int = Field(
        ...,
        ge=1900,
        le=CURRENT_YEAR,
        description=f"Tahun perolehan (1900-{CURRENT_YEAR})",
        examples=[2024],
    )
    asal_usul: AsalUsul = Field(
        ...,
        description="Asal usul perolehan",
        examples=["Pembelian"],
    )
    harga: int = Field(
        ...,
        ge=0,
        le=999_999_999_999,
        description="Harga dalam Rupiah penuh (max 999.999.999.999)",
        examples=[15000000],
    )
    kondisi: Kondisi = Field(
        default=Kondisi.BAIK,
        description="Kondisi barang",
        examples=["Baik"],
    )
    keterangan: str | None = Field(
        default=None,
        max_length=500,
        description="Keterangan tambahan (max 500 karakter)",
        examples=["Laptop untuk lab komputer"],
    )
    ruangan_id: str | None = Field(
        default=None,
        max_length=36,
        description="UUID ruangan tempat aset berada",
    )

    # Validators
    _validate_kode_barang = field_validator("kode_barang")(validate_kode_barang)
    _validate_tahun = field_validator("tahun_perolehan")(validate_tahun_perolehan)
    _validate_harga = field_validator("harga")(validate_harga)


class AsetCreate(AsetBase):
    """Schema untuk membuat aset baru.

    Extends AsetBase dengan field tambahan untuk create.
    nomor_register akan di-generate otomatis oleh sistem.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama_barang": "Laptop ASUS ROG Strix",
                "kode_barang": "02.06.01.0001",
                "kategori_kib": "B",
                "tahun_perolehan": 2024,
                "asal_usul": "Pembelian",
                "harga": 15000000,
                "kondisi": "Baik",
                "keterangan": "Laptop untuk lab komputer",
                "ruangan_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }
    )


class AsetUpdate(BaseModel):
    """Schema untuk update aset (partial update).

    Semua field optional karena partial update.
    kode_barang dan kategori_kib tidak bisa diubah.
    """

    nama_barang: str | None = Field(
        default=None,
        min_length=3,
        max_length=200,
        description="Nama barang (3-200 karakter)",
    )
    tahun_perolehan: int | None = Field(
        default=None,
        ge=1900,
        le=CURRENT_YEAR,
        description=f"Tahun perolehan (1900-{CURRENT_YEAR})",
    )
    asal_usul: AsalUsul | None = Field(
        default=None,
        description="Asal usul perolehan",
    )
    harga: int | None = Field(
        default=None,
        ge=0,
        le=999_999_999_999,
        description="Harga dalam Rupiah penuh",
    )
    kondisi: Kondisi | None = Field(
        default=None,
        description="Kondisi barang",
    )
    keterangan: str | None = Field(
        default=None,
        max_length=500,
        description="Keterangan tambahan",
    )
    ruangan_id: str | None = Field(
        default=None,
        max_length=36,
        description="UUID ruangan tempat aset berada",
    )

    # Validators
    @field_validator("tahun_perolehan")
    @classmethod
    def validate_tahun(cls, v: int | None) -> int | None:
        """Validate tahun_perolehan jika ada."""
        if v is not None:
            return validate_tahun_perolehan(v)
        return v

    @field_validator("harga")
    @classmethod
    def validate_harga_field(cls, v: int | None) -> int | None:
        """Validate harga jika ada."""
        if v is not None:
            return validate_harga(v)
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nama_barang": "Laptop ASUS ROG Strix G15",
                "kondisi": "Rusak Ringan",
                "keterangan": "Keyboard rusak",
            }
        }
    )


class AsetResponse(BaseModel):
    """Schema untuk response aset.

    Includes semua field dari model plus computed fields.
    """

    id: str = Field(..., description="UUID aset")
    nama_barang: str = Field(..., description="Nama barang")
    kode_barang: str = Field(..., description="Kode barang")
    nomor_register: int = Field(..., description="Nomor register sequential")
    kategori_kib: KategoriKIB = Field(..., description="Kategori KIB")
    tahun_perolehan: int = Field(..., description="Tahun perolehan")
    asal_usul: AsalUsul = Field(..., description="Asal usul perolehan")
    harga: int = Field(..., description="Harga dalam Rupiah")
    kondisi: Kondisi = Field(..., description="Kondisi barang")
    status: StatusAset = Field(..., description="Status aset")
    keterangan: str | None = Field(default=None, description="Keterangan")
    ruangan_id: str | None = Field(default=None, description="UUID ruangan")

    # Audit fields
    created_by: str | None = Field(default=None, description="UUID pembuat")
    updated_by: str | None = Field(default=None, description="UUID pengubah")
    deleted_by: str | None = Field(default=None, description="UUID penghapus")
    created_at: datetime = Field(..., description="Timestamp pembuatan")
    updated_at: datetime = Field(..., description="Timestamp update")
    deleted_at: datetime | None = Field(default=None, description="Timestamp hapus")
    alasan_penghapusan: str | None = Field(default=None, description="Alasan hapus")

    # KIB-specific fields (optional, depends on kategori_kib)
    merk: str | None = Field(default=None, description="Merk barang (KIB B)")
    tipe: str | None = Field(default=None, description="Tipe barang (KIB B)")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nama_barang": "Laptop ASUS ROG Strix",
                "kode_barang": "02.06.01.0001",
                "nomor_register": 1,
                "kategori_kib": "B",
                "tahun_perolehan": 2024,
                "asal_usul": "Pembelian",
                "harga": 15000000,
                "kondisi": "Baik",
                "status": "Aktif",
                "keterangan": "Laptop untuk lab komputer",
                "ruangan_id": "550e8400-e29b-41d4-a716-446655440001",
                "created_by": "550e8400-e29b-41d4-a716-446655440002",
                "created_at": "2026-01-11T10:00:00Z",
                "updated_at": "2026-01-11T10:00:00Z",
            }
        },
    )


class AsetSearchParams(BaseModel):
    """Schema untuk parameter search aset.

    Digunakan sebagai query parameters di endpoint GET /aset.
    """

    keyword: str | None = Field(
        default=None,
        max_length=100,
        description="Kata kunci search (nama, kode, merk)",
        examples=["laptop"],
    )
    kategori_kib: KategoriKIB | None = Field(
        default=None,
        description="Filter berdasarkan kategori KIB",
        examples=["B"],
    )
    status: StatusAset | None = Field(
        default=None,
        description="Filter berdasarkan status",
        examples=["Aktif"],
    )
    kondisi: Kondisi | None = Field(
        default=None,
        description="Filter berdasarkan kondisi",
        examples=["Baik"],
    )
    ruangan_id: str | None = Field(
        default=None,
        max_length=36,
        description="Filter berdasarkan ruangan",
    )
    tahun_perolehan: int | None = Field(
        default=None,
        ge=1900,
        le=CURRENT_YEAR,
        description="Filter berdasarkan tahun perolehan",
        examples=[2024],
    )
    include_deleted: bool = Field(
        default=False,
        description="Include aset yang sudah dihapus (Admin only)",
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "keyword": "laptop",
                "kategori_kib": "B",
                "status": "Aktif",
                "page": 1,
                "page_size": 100,
            }
        }
    )


class AsetDeleteRequest(BaseModel):
    """Schema untuk request delete aset.

    Soft delete memerlukan alasan penghapusan.
    """

    alasan_penghapusan: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Alasan penghapusan (min 20 karakter)",
        examples=["Barang rusak berat dan tidak dapat diperbaiki lagi"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "alasan_penghapusan": "Barang rusak berat dan tidak dapat diperbaiki lagi",
            }
        }
    )


# =============================================================================
# KIB-Specific Schemas
# =============================================================================


class KIBAFields(BaseModel):
    """Schema untuk fields spesifik KIB A (Tanah).

    Attributes:
        luas_m2: Luas tanah dalam meter persegi.
        alamat_lokasi: Alamat lokasi tanah.
        status_hak_tanah: Status hak tanah (SHM, HGB, dll).
        nomor_sertifikat: Nomor sertifikat tanah.
    """

    luas_m2: Decimal = Field(
        ...,
        gt=0,
        description="Luas tanah dalam m² (harus > 0)",
        examples=[1000.5],
    )
    alamat_lokasi: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Alamat lokasi tanah (min 10 karakter)",
        examples=["Jl. Pendidikan No. 1, Jakarta Timur"],
    )
    status_hak_tanah: str | None = Field(
        default=None,
        max_length=50,
        description="Status hak tanah (SHM, HGB, dll)",
        examples=["SHM"],
    )
    nomor_sertifikat: str | None = Field(
        default=None,
        max_length=100,
        description="Nomor sertifikat tanah",
        examples=["12345/2024"],
    )


class KIBBFields(BaseModel):
    """Schema untuk fields spesifik KIB B (Peralatan dan Mesin).

    Format BPAD DKI Jakarta dengan 18 kolom.
    """

    satuan: str = Field(
        ...,
        max_length=20,
        description="Satuan barang (BH/Unit/Set/Buah)",
        examples=["Unit"],
    )
    ukuran_cc: str | None = Field(
        default=None,
        max_length=50,
        description="Ukuran/CC untuk kendaraan",
        examples=["1500 CC"],
    )
    bahan: str | None = Field(
        default=None,
        max_length=100,
        description="Bahan material",
        examples=["Aluminium"],
    )
    merk: str | None = Field(
        default=None,
        max_length=100,
        description="Merk barang",
        examples=["ASUS"],
    )
    tipe: str | None = Field(
        default=None,
        max_length=100,
        description="Tipe/model barang",
        examples=["ROG Strix G15"],
    )
    nomor_rangka: str | None = Field(
        default=None,
        max_length=100,
        description="Nomor rangka/chasis (untuk kendaraan)",
        examples=["MHFM1BA3J8K123456"],
    )
    nomor_mesin: str | None = Field(
        default=None,
        max_length=100,
        description="Nomor mesin/pabrik",
        examples=["2NR-U123456"],
    )
    nomor_polisi: str | None = Field(
        default=None,
        max_length=20,
        description="Nomor polisi (untuk kendaraan)",
        examples=["B 1234 ABC"],
    )
    tanggal_dokumen: date | None = Field(
        default=None,
        description="Tanggal BPKB/dokumen",
        examples=["2024-01-15"],
    )
    kapitalisasi: int | None = Field(
        default=None,
        ge=0,
        description="Nilai kapitalisasi",
        examples=[15000000],
    )
    total_harga: int | None = Field(
        default=None,
        ge=0,
        description="Total harga",
        examples=[15000000],
    )

    @field_validator("satuan")
    @classmethod
    def validate_satuan(cls, v: str) -> str:
        """Validate satuan adalah nilai yang valid."""
        valid_satuan = ["BH", "Unit", "Set", "Buah", "Lembar", "Pasang", "Rim", "Dus"]
        if v not in valid_satuan:
            raise ValueError(f"Satuan harus salah satu dari: {', '.join(valid_satuan)}")
        return v


class KIBCFields(BaseModel):
    """Schema untuk fields spesifik KIB C (Gedung dan Bangunan)."""

    luas_lantai_m2: Decimal = Field(
        ...,
        gt=0,
        description="Luas lantai dalam m²",
        examples=[500.0],
    )
    alamat_lokasi: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Alamat lokasi gedung",
        examples=["Jl. Pendidikan No. 1, Jakarta Timur"],
    )
    bertingkat: int | None = Field(
        default=None,
        ge=1,
        le=100,
        description="Jumlah tingkat/lantai",
        examples=[3],
    )
    beton: bool = Field(
        default=False,
        description="Apakah konstruksi beton",
    )
    kondisi_bangunan: str | None = Field(
        default=None,
        max_length=50,
        description="Kondisi bangunan (B/KB/RB)",
        examples=["B"],
    )


class KIBDFields(BaseModel):
    """Schema untuk fields spesifik KIB D (Jalan, Irigasi, Jaringan)."""

    panjang_km: Decimal = Field(
        ...,
        gt=0,
        description="Panjang dalam kilometer",
        examples=[1.5],
    )
    lebar_m: Decimal = Field(
        ...,
        gt=0,
        description="Lebar dalam meter",
        examples=[6.0],
    )
    alamat_lokasi: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Alamat lokasi",
        examples=["Jl. Pendidikan, Jakarta Timur"],
    )
    jenis_konstruksi: str | None = Field(
        default=None,
        max_length=100,
        description="Jenis konstruksi",
        examples=["Aspal"],
    )


class KIBEFields(BaseModel):
    """Schema untuk fields spesifik KIB E (Aset Tetap Lainnya)."""

    judul_pencipta: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Judul/nama pencipta",
        examples=["Lukisan Pemandangan"],
    )
    asal_daerah: str | None = Field(
        default=None,
        max_length=100,
        description="Asal daerah",
        examples=["Bali"],
    )
    jenis_hewan: str | None = Field(
        default=None,
        max_length=100,
        description="Jenis hewan (untuk hewan ternak)",
        examples=["Sapi"],
    )
    jumlah: int = Field(
        default=1,
        ge=1,
        description="Jumlah item",
        examples=[1],
    )


class KIBFFields(BaseModel):
    """Schema untuk fields spesifik KIB F (Konstruksi dalam Pengerjaan)."""

    alamat_lokasi: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Alamat lokasi konstruksi",
        examples=["Jl. Pendidikan No. 1, Jakarta Timur"],
    )
    persentase_selesai: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Persentase penyelesaian (0-100)",
        examples=[75],
    )
    jenis_bangunan: str | None = Field(
        default=None,
        max_length=100,
        description="Jenis bangunan yang dikerjakan",
        examples=["Gedung Sekolah"],
    )


# =============================================================================
# Combined Create Schemas with KIB Fields
# =============================================================================


class AsetCreateKIBA(AsetCreate, KIBAFields):
    """Schema untuk membuat aset KIB A (Tanah)."""

    kategori_kib: KategoriKIB = Field(default=KategoriKIB.A)


class AsetCreateKIBB(AsetCreate, KIBBFields):
    """Schema untuk membuat aset KIB B (Peralatan dan Mesin)."""

    kategori_kib: KategoriKIB = Field(default=KategoriKIB.B)


class AsetCreateKIBC(AsetCreate, KIBCFields):
    """Schema untuk membuat aset KIB C (Gedung dan Bangunan)."""

    kategori_kib: KategoriKIB = Field(default=KategoriKIB.C)


class AsetCreateKIBD(AsetCreate, KIBDFields):
    """Schema untuk membuat aset KIB D (Jalan, Irigasi, Jaringan)."""

    kategori_kib: KategoriKIB = Field(default=KategoriKIB.D)


class AsetCreateKIBE(AsetCreate, KIBEFields):
    """Schema untuk membuat aset KIB E (Aset Tetap Lainnya)."""

    kategori_kib: KategoriKIB = Field(default=KategoriKIB.E)


class AsetCreateKIBF(AsetCreate, KIBFFields):
    """Schema untuk membuat aset KIB F (Konstruksi dalam Pengerjaan)."""

    kategori_kib: KategoriKIB = Field(default=KategoriKIB.F)
