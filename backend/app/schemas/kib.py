"""KIB Report schemas untuk SIMANIS62 V2.

Module ini berisi Pydantic schemas untuk:
- KibReportResponse: Schema untuk response laporan KIB
- KibExportRequest: Schema untuk request export KIB ke Excel
- KibSummary: Schema untuk ringkasan KIB
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.aset import KategoriKIB

# =============================================================================
# Summary Schemas
# =============================================================================


class KibSummary(BaseModel):
    """Schema untuk ringkasan KIB.

    Attributes:
        kategori_kib: Kategori KIB (A-F).
        total_item: Total jumlah item.
        total_nilai: Total nilai dalam Rupiah.
        kondisi_baik: Jumlah item kondisi Baik.
        kondisi_rusak_ringan: Jumlah item kondisi Rusak Ringan.
        kondisi_rusak_berat: Jumlah item kondisi Rusak Berat.
    """

    kategori_kib: KategoriKIB = Field(..., description="Kategori KIB")
    total_item: int = Field(..., ge=0, description="Total jumlah item")
    total_nilai: int = Field(..., ge=0, description="Total nilai dalam Rupiah")
    kondisi_baik: int = Field(default=0, ge=0, description="Jumlah kondisi Baik")
    kondisi_rusak_ringan: int = Field(
        default=0, ge=0, description="Jumlah kondisi Rusak Ringan"
    )
    kondisi_rusak_berat: int = Field(
        default=0, ge=0, description="Jumlah kondisi Rusak Berat"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "kategori_kib": "B",
                "total_item": 150,
                "total_nilai": 2500000000,
                "kondisi_baik": 120,
                "kondisi_rusak_ringan": 25,
                "kondisi_rusak_berat": 5,
            }
        }
    )


# =============================================================================
# KIB Item Schemas (untuk report)
# =============================================================================


class KibItemBase(BaseModel):
    """Base schema untuk item KIB dalam report."""

    nomor_urut: int = Field(..., description="Nomor urut dalam laporan")
    kode_barang: str = Field(..., description="Kode barang")
    nama_barang: str = Field(..., description="Nama barang")
    nomor_register: int = Field(..., description="Nomor register")
    kondisi: str = Field(..., description="Kondisi barang (B/KB/RB)")
    tahun_perolehan: int = Field(..., description="Tahun perolehan")
    asal_usul: str = Field(..., description="Asal usul perolehan")
    harga: int = Field(..., description="Harga dalam Rupiah")
    keterangan: str | None = Field(default=None, description="Keterangan")


class KibBItem(KibItemBase):
    """Schema untuk item KIB B (Peralatan dan Mesin).

    Format BPAD DKI Jakarta dengan 18 kolom.
    """

    satuan: str | None = Field(default=None, description="Satuan")
    ukuran_cc: str | None = Field(default=None, description="Ukuran/CC")
    bahan: str | None = Field(default=None, description="Bahan")
    merk: str | None = Field(default=None, description="Merk")
    tipe: str | None = Field(default=None, description="Tipe")
    nomor_rangka: str | None = Field(default=None, description="Nomor rangka")
    nomor_mesin: str | None = Field(default=None, description="Nomor mesin")
    nomor_polisi: str | None = Field(default=None, description="Nomor polisi")
    tanggal_dokumen: date | None = Field(default=None, description="Tanggal dokumen")
    kapitalisasi: int | None = Field(default=None, description="Kapitalisasi")
    total_harga: int | None = Field(default=None, description="Total harga")

    model_config = ConfigDict(from_attributes=True)


class KibAItem(KibItemBase):
    """Schema untuk item KIB A (Tanah)."""

    luas_m2: Decimal | None = Field(default=None, description="Luas m²")
    alamat_lokasi: str | None = Field(default=None, description="Alamat lokasi")
    status_hak_tanah: str | None = Field(default=None, description="Status hak tanah")
    nomor_sertifikat: str | None = Field(default=None, description="Nomor sertifikat")

    model_config = ConfigDict(from_attributes=True)


class KibCItem(KibItemBase):
    """Schema untuk item KIB C (Gedung dan Bangunan)."""

    luas_lantai_m2: Decimal | None = Field(default=None, description="Luas lantai m²")
    alamat_lokasi: str | None = Field(default=None, description="Alamat lokasi")
    bertingkat: int | None = Field(default=None, description="Jumlah tingkat")
    beton: bool | None = Field(default=None, description="Konstruksi beton")
    kondisi_bangunan: str | None = Field(default=None, description="Kondisi bangunan")

    model_config = ConfigDict(from_attributes=True)


class KibDItem(KibItemBase):
    """Schema untuk item KIB D (Jalan, Irigasi, Jaringan)."""

    panjang_km: Decimal | None = Field(default=None, description="Panjang km")
    lebar_m: Decimal | None = Field(default=None, description="Lebar m")
    alamat_lokasi: str | None = Field(default=None, description="Alamat lokasi")
    jenis_konstruksi: str | None = Field(default=None, description="Jenis konstruksi")

    model_config = ConfigDict(from_attributes=True)


class KibEItem(KibItemBase):
    """Schema untuk item KIB E (Aset Tetap Lainnya)."""

    judul_pencipta: str | None = Field(default=None, description="Judul/pencipta")
    asal_daerah: str | None = Field(default=None, description="Asal daerah")
    jenis_hewan: str | None = Field(default=None, description="Jenis hewan")
    jumlah: int | None = Field(default=None, description="Jumlah")

    model_config = ConfigDict(from_attributes=True)


class KibFItem(KibItemBase):
    """Schema untuk item KIB F (Konstruksi dalam Pengerjaan)."""

    alamat_lokasi: str | None = Field(default=None, description="Alamat lokasi")
    persentase_selesai: int | None = Field(
        default=None, description="Persentase selesai"
    )
    jenis_bangunan: str | None = Field(default=None, description="Jenis bangunan")

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# Report Response Schemas
# =============================================================================


class KibReportResponse(BaseModel):
    """Schema untuk response laporan KIB.

    Attributes:
        kategori_kib: Kategori KIB yang diminta.
        nama_sekolah: Nama sekolah (dari config).
        tanggal_cetak: Tanggal cetak laporan.
        summary: Ringkasan KIB.
        items: Daftar item KIB.
    """

    kategori_kib: KategoriKIB = Field(..., description="Kategori KIB")
    nama_sekolah: str = Field(..., description="Nama sekolah")
    tanggal_cetak: datetime = Field(..., description="Tanggal cetak laporan")
    summary: KibSummary = Field(..., description="Ringkasan KIB")
    items: list[KibItemBase] = Field(
        default_factory=list, description="Daftar item KIB"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "kategori_kib": "B",
                "nama_sekolah": "SDN 01 Jakarta Timur",
                "tanggal_cetak": "2026-01-11T10:00:00Z",
                "summary": {
                    "kategori_kib": "B",
                    "total_item": 150,
                    "total_nilai": 2500000000,
                    "kondisi_baik": 120,
                    "kondisi_rusak_ringan": 25,
                    "kondisi_rusak_berat": 5,
                },
                "items": [],
            }
        }
    )


# =============================================================================
# Export Request Schemas
# =============================================================================


class KibExportRequest(BaseModel):
    """Schema untuk request export KIB ke Excel.

    Attributes:
        kategori_kib: Kategori KIB yang akan di-export.
        tahun_perolehan: Filter berdasarkan tahun perolehan (optional).
        ruangan_id: Filter berdasarkan ruangan (optional).
        include_rusak: Include aset dengan kondisi rusak (default True).
        format: Format export (xlsx/pdf).
    """

    kategori_kib: KategoriKIB = Field(
        ...,
        description="Kategori KIB yang akan di-export",
        examples=["B"],
    )
    tahun_perolehan: int | None = Field(
        default=None,
        ge=1900,
        le=2100,
        description="Filter berdasarkan tahun perolehan",
        examples=[2024],
    )
    ruangan_id: str | None = Field(
        default=None,
        max_length=36,
        description="Filter berdasarkan ruangan",
    )
    include_rusak: bool = Field(
        default=True,
        description="Include aset dengan kondisi rusak",
    )
    format: str = Field(
        default="xlsx",
        description="Format export (xlsx/pdf)",
        examples=["xlsx"],
    )

    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """Validate format export."""
        valid_formats = ["xlsx", "pdf"]
        if v.lower() not in valid_formats:
            raise ValueError(
                f"Format harus salah satu dari: {', '.join(valid_formats)}"
            )
        return v.lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "kategori_kib": "B",
                "tahun_perolehan": 2024,
                "include_rusak": True,
                "format": "xlsx",
            }
        }
    )


class KibExportResponse(BaseModel):
    """Schema untuk response export KIB.

    Attributes:
        filename: Nama file yang di-generate.
        file_path: Path file yang di-generate.
        file_size: Ukuran file dalam bytes.
        total_items: Total item yang di-export.
        kategori_kib: Kategori KIB yang di-export.
    """

    filename: str = Field(..., description="Nama file yang di-generate")
    file_path: str = Field(..., description="Path file yang di-generate")
    file_size: int = Field(..., ge=0, description="Ukuran file dalam bytes")
    total_items: int = Field(..., ge=0, description="Total item yang di-export")
    kategori_kib: KategoriKIB = Field(..., description="Kategori KIB yang di-export")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "KIB_B_2026-01-11.xlsx",
                "file_path": "/tmp/exports/KIB_B_2026-01-11.xlsx",
                "file_size": 102400,
                "total_items": 150,
                "kategori_kib": "B",
            }
        }
    )
