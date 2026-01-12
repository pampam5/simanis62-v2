"""KIB Extension models untuk field spesifik per kategori.

Model ini mendefinisikan tabel extension untuk setiap kategori KIB:
- AsetKIBA: KIB A (Tanah)
- AsetKIBB: KIB B (Peralatan dan Mesin) - Format BPAD DKI Jakarta 18 kolom
- AsetKIBC: KIB C (Gedung dan Bangunan)
- AsetKIBD: KIB D (Jalan, Irigasi, dan Jaringan)
- AsetKIBE: KIB E (Aset Tetap Lainnya)
- AsetKIBF: KIB F (Konstruksi dalam Pengerjaan)
"""

from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .base import generate_uuid

if TYPE_CHECKING:
    from .aset import Aset


class AsetKIBA(SQLModel, table=True):
    """Model untuk tabel aset_kib_a (KIB A - Tanah).

    Tabel extension untuk field spesifik KIB A sesuai format BPAD DKI Jakarta.

    Attributes:
        id: UUID primary key.
        aset_id: FK ke tabel aset (one-to-one).
        luas_m2: Luas tanah dalam meter persegi.
        alamat_lokasi: Alamat/lokasi tanah.
        status_hak_tanah: Status hak tanah.
        tanggal_sertifikat: Tanggal sertifikat.
        nomor_sertifikat: Nomor sertifikat.
        penggunaan: Penggunaan tanah.
    """

    __tablename__ = "aset_kib_a"

    # Primary Key
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="UUID primary key",
    )

    # Foreign Key (One-to-One with aset)
    aset_id: str = Field(
        foreign_key="aset.id",
        unique=True,
        index=True,
        description="FK ke tabel aset (one-to-one)",
    )

    # KIB A Specific Fields (Format BPAD DKI Jakarta 14 Kolom)
    luas_m2: float = Field(
        gt=0,
        description="Luas tanah dalam meter persegi (positif)",
    )
    alamat_lokasi: str = Field(
        min_length=10,
        max_length=500,
        description="Alamat/lokasi tanah (min 10 karakter)",
    )
    status_hak_tanah: str | None = Field(
        default=None,
        max_length=100,
        description="Status hak tanah (Hak Milik/Hak Pakai/Hak Guna Bangunan)",
    )
    tanggal_sertifikat: date | None = Field(
        default=None,
        description="Tanggal sertifikat (format DD/MM/YYYY)",
    )
    nomor_sertifikat: str | None = Field(
        default=None,
        max_length=100,
        description="Nomor sertifikat tanah",
    )
    penggunaan: str | None = Field(
        default=None,
        max_length=200,
        description="Penggunaan tanah (Sekolah/Lapangan/dll)",
    )

    # Relationship
    aset: "Aset" = Relationship(back_populates="kib_a")


class AsetKIBB(SQLModel, table=True):
    """Model untuk tabel aset_kib_b (KIB B - Peralatan dan Mesin).

    Tabel extension untuk field spesifik KIB B sesuai format BPAD DKI Jakarta 18 kolom.
    Beberapa field sudah ada di tabel utama aset (kode_barang, nama_barang, dll).

    Attributes:
        id: UUID primary key.
        aset_id: FK ke tabel aset (one-to-one).
        satuan: Satuan barang (BH/Unit/Set/Buah/Paket/Rim/Dus).
        ukuran_cc: Ukuran/CC (untuk kendaraan).
        bahan: Material/bahan barang.
        merk: Merk barang.
        tipe: Tipe/model barang.
        tanggal_dokumen: Tanggal BPKB/dokumen.
        nomor_rangka: Nomor rangka/chasis (kendaraan).
        nomor_mesin: Nomor mesin/pabrik.
        nomor_polisi: Nomor polisi (kendaraan).
        kapitalisasi: Nilai kapitalisasi.
        total_harga: Total harga.
    """

    __tablename__ = "aset_kib_b"

    # Primary Key
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="UUID primary key",
    )

    # Foreign Key (One-to-One with aset)
    aset_id: str = Field(
        foreign_key="aset.id",
        unique=True,
        index=True,
        description="FK ke tabel aset (one-to-one)",
    )

    # === KIB B Specific Fields (Format BPAD DKI Jakarta 18 Kolom) ===

    # Kolom 6: SATU-AN (Required)
    satuan: str = Field(
        max_length=20,
        description="Satuan barang: BH/Unit/Set/Buah/Paket/Rim/Dus (required)",
    )

    # Kolom 5: UKU-RAN
    ukuran_cc: str | None = Field(
        default=None,
        max_length=50,
        description="Ukuran/CC (optional)",
    )

    # Kolom 8: BA-HAN
    bahan: str | None = Field(
        default=None,
        max_length=100,
        description="Material/bahan barang (optional)",
    )

    # Kolom 9: MEREK
    merk: str | None = Field(
        default=None,
        max_length=100,
        index=True,
        description="Merk barang (optional)",
    )

    # Kolom 10: TYPE
    tipe: str | None = Field(
        default=None,
        max_length=100,
        description="Tipe/model barang (optional)",
    )

    # Kolom 11: TGL. BPKB/TGL. DOK.
    tanggal_dokumen: date | None = Field(
        default=None,
        description="Tanggal BPKB/dokumen - format DD/MM/YYYY (optional)",
    )

    # Kolom 12: NO. CHASIS/NO. RANGKA
    nomor_rangka: str | None = Field(
        default=None,
        max_length=50,
        description="Nomor rangka/chasis - untuk kendaraan (optional)",
    )

    # Kolom 13: NO. MESIN/NO. PABRIK
    nomor_mesin: str | None = Field(
        default=None,
        max_length=50,
        description="Nomor mesin/pabrik (optional)",
    )

    # Kolom 14: NOMOR POLISI
    nomor_polisi: str | None = Field(
        default=None,
        max_length=20,
        index=True,
        description="Nomor polisi - untuk kendaraan (optional)",
    )

    # Kolom 17: KAPITALISASI (Rp.)
    kapitalisasi: int | None = Field(
        default=None,
        ge=0,
        le=999999999999,
        description="Nilai kapitalisasi dalam Rupiah penuh (optional)",
    )

    # Kolom 18: TOTAL (Rp.)
    total_harga: int | None = Field(
        default=None,
        ge=0,
        le=999999999999,
        description="Total harga dalam Rupiah penuh (optional)",
    )

    # Relationship
    aset: "Aset" = Relationship(back_populates="kib_b")

    @property
    def is_kendaraan(self) -> bool:
        """Check apakah aset adalah kendaraan.

        Returns:
            True jika memiliki nomor_polisi atau nomor_rangka.
        """
        return bool(self.nomor_polisi or self.nomor_rangka)


class AsetKIBC(SQLModel, table=True):
    """Model untuk tabel aset_kib_c (KIB C - Gedung dan Bangunan).

    Tabel extension untuk field spesifik KIB C sesuai format BPAD DKI Jakarta.

    Attributes:
        id: UUID primary key.
        aset_id: FK ke tabel aset (one-to-one).
        kondisi_bangunan: Kondisi bangunan (B/KB/RB).
        bertingkat: Apakah bangunan bertingkat.
        beton: Apakah konstruksi beton.
        luas_lantai_m2: Luas lantai dalam meter persegi.
        alamat_lokasi: Alamat/lokasi bangunan.
        tanggal_dokumen: Tanggal dokumen.
        nomor_dokumen: Nomor dokumen.
        luas_tanah_m2: Luas tanah dalam meter persegi.
        status_tanah: Status tanah.
        kode_tanah: Nomor kode tanah.
    """

    __tablename__ = "aset_kib_c"

    # Primary Key
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="UUID primary key",
    )

    # Foreign Key (One-to-One with aset)
    aset_id: str = Field(
        foreign_key="aset.id",
        unique=True,
        index=True,
        description="FK ke tabel aset (one-to-one)",
    )

    # KIB C Specific Fields (Format BPAD DKI Jakarta 17 Kolom)
    kondisi_bangunan: str | None = Field(
        default=None,
        max_length=10,
        description="Kondisi bangunan: B (Baik), KB (Kurang Baik), RB (Rusak Berat)",
    )
    bertingkat: bool | None = Field(
        default=None,
        description="Apakah bangunan bertingkat (Ya/Tidak)",
    )
    beton: bool | None = Field(
        default=None,
        description="Apakah konstruksi beton (Ya/Tidak)",
    )
    luas_lantai_m2: float = Field(
        gt=0,
        description="Luas lantai dalam meter persegi (positif)",
    )
    alamat_lokasi: str = Field(
        min_length=10,
        max_length=500,
        description="Alamat/lokasi bangunan (min 10 karakter)",
    )
    tanggal_dokumen: date | None = Field(
        default=None,
        description="Tanggal dokumen (format DD/MM/YYYY)",
    )
    nomor_dokumen: str | None = Field(
        default=None,
        max_length=100,
        description="Nomor dokumen",
    )
    luas_tanah_m2: float | None = Field(
        default=None,
        gt=0,
        description="Luas tanah dalam meter persegi",
    )
    status_tanah: str | None = Field(
        default=None,
        max_length=100,
        description="Status tanah",
    )
    kode_tanah: str | None = Field(
        default=None,
        max_length=50,
        description="Nomor kode tanah",
    )

    # Relationship
    aset: "Aset" = Relationship(back_populates="kib_c")


class AsetKIBD(SQLModel, table=True):
    """Model untuk tabel aset_kib_d (KIB D - Jalan, Irigasi, dan Jaringan).

    Tabel extension untuk field spesifik KIB D sesuai format BPAD DKI Jakarta.

    Attributes:
        id: UUID primary key.
        aset_id: FK ke tabel aset (one-to-one).
        jenis_konstruksi: Jenis konstruksi.
        panjang_km: Panjang dalam kilometer.
        lebar_m: Lebar dalam meter.
        luas_m2: Luas dalam meter persegi.
        alamat_lokasi: Alamat/lokasi.
        tanggal_dokumen: Tanggal dokumen.
        nomor_dokumen: Nomor dokumen.
        status_tanah: Status tanah.
        kode_tanah: Nomor kode tanah.
    """

    __tablename__ = "aset_kib_d"

    # Primary Key
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="UUID primary key",
    )

    # Foreign Key (One-to-One with aset)
    aset_id: str = Field(
        foreign_key="aset.id",
        unique=True,
        index=True,
        description="FK ke tabel aset (one-to-one)",
    )

    # KIB D Specific Fields (Format BPAD DKI Jakarta 16 Kolom)
    jenis_konstruksi: str | None = Field(
        default=None,
        max_length=100,
        description="Jenis konstruksi",
    )
    panjang_km: float | None = Field(
        default=None,
        gt=0,
        description="Panjang dalam kilometer (positif)",
    )
    lebar_m: float | None = Field(
        default=None,
        gt=0,
        description="Lebar dalam meter (positif)",
    )
    luas_m2: float | None = Field(
        default=None,
        gt=0,
        description="Luas dalam meter persegi (positif)",
    )
    alamat_lokasi: str = Field(
        min_length=10,
        max_length=500,
        description="Alamat/lokasi (min 10 karakter)",
    )
    tanggal_dokumen: date | None = Field(
        default=None,
        description="Tanggal dokumen (format DD/MM/YYYY)",
    )
    nomor_dokumen: str | None = Field(
        default=None,
        max_length=100,
        description="Nomor dokumen",
    )
    status_tanah: str | None = Field(
        default=None,
        max_length=100,
        description="Status tanah",
    )
    kode_tanah: str | None = Field(
        default=None,
        max_length=50,
        description="Nomor kode tanah",
    )

    # Relationship
    aset: "Aset" = Relationship(back_populates="kib_d")


class AsetKIBE(SQLModel, table=True):
    """Model untuk tabel aset_kib_e (KIB E - Aset Tetap Lainnya).

    Tabel extension untuk field spesifik KIB E sesuai format BPAD DKI Jakarta.
    Termasuk buku perpustakaan, barang bercorak, hewan/ternak.

    Attributes:
        id: UUID primary key.
        aset_id: FK ke tabel aset (one-to-one).
        judul_pencipta: Judul/pencipta (untuk buku).
        spesifikasi_buku: Spesifikasi buku.
        asal_daerah: Asal daerah (untuk barang bercorak).
        pencipta: Pencipta (untuk barang bercorak).
        bahan: Bahan (untuk barang bercorak).
        jenis_hewan: Jenis hewan/ternak.
        ukuran_hewan: Ukuran hewan/ternak.
        jumlah: Jumlah barang.
    """

    __tablename__ = "aset_kib_e"

    # Primary Key
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="UUID primary key",
    )

    # Foreign Key (One-to-One with aset)
    aset_id: str = Field(
        foreign_key="aset.id",
        unique=True,
        index=True,
        description="FK ke tabel aset (one-to-one)",
    )

    # KIB E Specific Fields (Format BPAD DKI Jakarta 16 Kolom)
    # Untuk Buku
    judul_pencipta: str | None = Field(
        default=None,
        max_length=200,
        description="Judul/pencipta (untuk buku)",
    )
    spesifikasi_buku: str | None = Field(
        default=None,
        max_length=200,
        description="Spesifikasi buku",
    )

    # Untuk Barang Bercorak
    asal_daerah: str | None = Field(
        default=None,
        max_length=100,
        description="Asal daerah (untuk barang bercorak)",
    )
    pencipta: str | None = Field(
        default=None,
        max_length=100,
        description="Pencipta (untuk barang bercorak)",
    )
    bahan: str | None = Field(
        default=None,
        max_length=100,
        description="Bahan (untuk barang bercorak)",
    )

    # Untuk Hewan/Ternak
    jenis_hewan: str | None = Field(
        default=None,
        max_length=100,
        description="Jenis hewan/ternak",
    )
    ukuran_hewan: str | None = Field(
        default=None,
        max_length=50,
        description="Ukuran hewan/ternak",
    )

    # Jumlah
    jumlah: int | None = Field(
        default=None,
        gt=0,
        description="Jumlah barang (positif)",
    )

    # Relationship
    aset: "Aset" = Relationship(back_populates="kib_e")


class AsetKIBF(SQLModel, table=True):
    """Model untuk tabel aset_kib_f (KIB F - Konstruksi dalam Pengerjaan).

    Tabel extension untuk field spesifik KIB F sesuai format BPAD DKI Jakarta.

    Attributes:
        id: UUID primary key.
        aset_id: FK ke tabel aset (one-to-one).
        jenis_bangunan: Jenis bangunan.
        bertingkat: Apakah bangunan bertingkat.
        beton: Apakah konstruksi beton.
        luas_m2: Luas dalam meter persegi.
        alamat_lokasi: Alamat/lokasi konstruksi.
        info_dokumen: Informasi dokumen (tanggal/nomor).
    """

    __tablename__ = "aset_kib_f"

    # Primary Key
    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="UUID primary key",
    )

    # Foreign Key (One-to-One with aset)
    aset_id: str = Field(
        foreign_key="aset.id",
        unique=True,
        index=True,
        description="FK ke tabel aset (one-to-one)",
    )

    # KIB F Specific Fields (Format BPAD DKI Jakarta 12 Kolom)
    jenis_bangunan: str | None = Field(
        default=None,
        max_length=100,
        description="Jenis bangunan",
    )
    bertingkat: bool | None = Field(
        default=None,
        description="Apakah bangunan bertingkat (Ya/Tidak)",
    )
    beton: bool | None = Field(
        default=None,
        description="Apakah konstruksi beton (Ya/Tidak)",
    )
    luas_m2: float | None = Field(
        default=None,
        gt=0,
        description="Luas dalam meter persegi (positif)",
    )
    alamat_lokasi: str = Field(
        min_length=10,
        max_length=500,
        description="Alamat/lokasi konstruksi (min 10 karakter)",
    )
    info_dokumen: str | None = Field(
        default=None,
        max_length=200,
        description="Informasi dokumen (tanggal/nomor)",
    )

    # Relationship
    aset: "Aset" = Relationship(back_populates="kib_f")
