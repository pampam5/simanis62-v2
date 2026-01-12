"""Aset service untuk SIMANIS62 V2.

Module ini menyediakan AsetService untuk:
- CRUD operations untuk aset
- Search dengan multiple filters
- Validation methods
- Auto nomor_register generation
"""

import re
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AssetInMutationError,
    AssetNotEditableError,
    AssetNotFoundError,
    DeleteReasonTooShortError,
    DuplicateKodeBarangError,
    InvalidHargaError,
    InvalidKodeBarangFormatError,
    InvalidTahunPerolehanError,
    RuanganNotFoundError,
)
from app.models.aset import Aset, Kondisi, StatusAset
from app.repositories.aset_repository import AsetRepository
from app.repositories.ruangan_repository import RuanganRepository
from app.schemas.aset import (
    AsetCreate,
    AsetDeleteRequest,
    AsetResponse,
    AsetSearchParams,
    AsetUpdate,
)
from app.schemas.response import PaginatedResponse
from app.services.base import BaseService

# Constants
KODE_BARANG_PATTERN = re.compile(r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$")
CURRENT_YEAR = datetime.now().year
MAX_HARGA = 999_999_999_999
MIN_DELETE_REASON_LENGTH = 20


class AsetService(BaseService[Aset, AsetRepository]):
    """Service untuk CRUD dan search aset.

    Menyediakan:
    - create_asset: Buat aset baru dengan auto nomor_register
    - update_asset: Update aset dengan status auto-update
    - delete_asset: Soft delete aset
    - get_asset_by_id: Get aset by ID
    - search_assets: Search dengan multiple filters

    Example:
        ```python
        service = AsetService(session)
        aset = await service.create_asset(data, user_id)
        results = await service.search_assets(params, user_role)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize AsetService.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(session, AsetRepository(session), "AsetService")
        self._ruangan_repo = RuanganRepository(session)

    # =========================================================================
    # Validation Methods
    # =========================================================================

    def _validate_kode_barang_format(self, kode_barang: str) -> None:
        """Validate format kode_barang: XX.XX.XX.XXXX.

        Args:
            kode_barang: Kode barang yang akan divalidasi.

        Raises:
            InvalidKodeBarangFormatError: Jika format tidak valid.
        """
        if not KODE_BARANG_PATTERN.match(kode_barang):
            raise InvalidKodeBarangFormatError(kode_barang)

    def _validate_tahun_perolehan(self, tahun: int) -> None:
        """Validate tahun_perolehan: 1900 - current year.

        Args:
            tahun: Tahun perolehan yang akan divalidasi.

        Raises:
            InvalidTahunPerolehanError: Jika tahun tidak valid.
        """
        if tahun < 1900 or tahun > CURRENT_YEAR:
            raise InvalidTahunPerolehanError(tahun, CURRENT_YEAR)

    def _validate_harga(self, harga: int) -> None:
        """Validate harga: > 0 dan <= 999.999.999.999.

        Args:
            harga: Harga yang akan divalidasi.

        Raises:
            InvalidHargaError: Jika harga tidak valid.
        """
        if harga < 0 or harga > MAX_HARGA:
            raise InvalidHargaError(harga)

    def _validate_delete_reason(self, alasan: str) -> None:
        """Validate alasan penghapusan minimal 20 karakter.

        Args:
            alasan: Alasan penghapusan.

        Raises:
            DeleteReasonTooShortError: Jika alasan terlalu pendek.
        """
        if len(alasan.strip()) < MIN_DELETE_REASON_LENGTH:
            raise DeleteReasonTooShortError(len(alasan.strip()))

    async def _validate_kode_barang_unique(
        self, kode_barang: str, exclude_id: str | None = None
    ) -> None:
        """Validate kode_barang unik.

        Args:
            kode_barang: Kode barang yang akan dicek.
            exclude_id: ID aset yang dikecualikan (untuk update).

        Raises:
            DuplicateKodeBarangError: Jika kode_barang sudah ada.
        """
        existing = await self.repository.get_by_kode_barang(kode_barang)
        if existing and (exclude_id is None or str(existing.id) != exclude_id):
            raise DuplicateKodeBarangError(kode_barang)

    async def _validate_ruangan_exists(self, ruangan_id: str | None) -> None:
        """Validate ruangan exists jika ruangan_id diberikan.

        Args:
            ruangan_id: UUID ruangan.

        Raises:
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
        """
        if ruangan_id:
            exists = await self._ruangan_repo.exists(ruangan_id)
            if not exists:
                raise RuanganNotFoundError(ruangan_id)

    # =========================================================================
    # CRUD Operations
    # =========================================================================

    async def create_asset(self, data: AsetCreate, user_id: str) -> Aset:
        """Buat aset baru dengan auto nomor_register.

        Args:
            data: AsetCreate schema dengan data aset.
            user_id: UUID user yang membuat.

        Returns:
            Aset yang baru dibuat.

        Raises:
            InvalidKodeBarangFormatError: Jika format kode_barang tidak valid.
            DuplicateKodeBarangError: Jika kode_barang sudah ada.
            InvalidTahunPerolehanError: Jika tahun tidak valid.
            InvalidHargaError: Jika harga tidak valid.
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
        """
        self.log_info(f"Creating asset: {data.nama_barang[:50]}")

        # Validations
        self._validate_kode_barang_format(data.kode_barang)
        await self._validate_kode_barang_unique(data.kode_barang)
        self._validate_tahun_perolehan(data.tahun_perolehan)
        self._validate_harga(data.harga)
        await self._validate_ruangan_exists(data.ruangan_id)

        # Get next nomor_register
        nomor_register = await self.repository.get_next_nomor_register(
            data.kategori_kib, data.tahun_perolehan
        )

        # Create aset
        aset = Aset(
            nama_barang=data.nama_barang,
            kode_barang=data.kode_barang,
            nomor_register=nomor_register,
            kategori_kib=data.kategori_kib,
            tahun_perolehan=data.tahun_perolehan,
            asal_usul=data.asal_usul,
            harga=data.harga,
            kondisi=data.kondisi,
            status=StatusAset.AKTIF,
            keterangan=data.keterangan,
            ruangan_id=data.ruangan_id,
            created_by=user_id,
        )

        # Copy KIB-specific fields if present
        kib_fields = [
            "satuan",
            "ukuran_cc",
            "bahan",
            "merk",
            "tipe",
            "nomor_rangka",
            "nomor_mesin",
            "nomor_polisi",
            "tanggal_dokumen",
            "kapitalisasi",
            "total_harga",
            "luas_m2",
            "alamat_lokasi",
            "status_hak_tanah",
            "nomor_sertifikat",
            "luas_lantai_m2",
            "bertingkat",
            "beton",
            "kondisi_bangunan",
            "panjang_km",
            "lebar_m",
            "jenis_konstruksi",
            "judul_pencipta",
            "asal_daerah",
            "jenis_hewan",
            "jumlah",
            "persentase_selesai",
            "jenis_bangunan",
        ]
        for field in kib_fields:
            if hasattr(data, field):
                value = getattr(data, field, None)
                if value is not None and hasattr(aset, field):
                    setattr(aset, field, value)

        created = await self.repository.create(aset)
        await self.commit()

        self.log_info(f"Asset created: id={created.id}, kode={created.kode_barang}")
        return created

    async def update_asset(self, aset_id: str, data: AsetUpdate, user_id: str) -> Aset:
        """Update aset dengan status auto-update based on kondisi.

        Args:
            aset_id: UUID aset yang akan diupdate.
            data: AsetUpdate schema dengan data update.
            user_id: UUID user yang mengupdate.

        Returns:
            Aset yang diupdate.

        Raises:
            AssetNotFoundError: Jika aset tidak ditemukan.
            AssetInMutationError: Jika aset sedang dalam mutasi.
            AssetNotEditableError: Jika aset tidak bisa diedit.
        """
        self.log_info(f"Updating asset: {aset_id}")

        # Get existing aset
        aset = await self.repository.get_by_id(aset_id)
        if not aset:
            raise AssetNotFoundError(aset_id)

        # Check if editable
        if aset.status == StatusAset.MUTASI:
            raise AssetInMutationError(aset_id)
        if aset.status == StatusAset.DIHAPUS:
            raise AssetNotEditableError(aset.status.value)

        # Validate fields if provided
        if data.tahun_perolehan is not None:
            self._validate_tahun_perolehan(data.tahun_perolehan)
        if data.harga is not None:
            self._validate_harga(data.harga)
        if data.ruangan_id is not None:
            await self._validate_ruangan_exists(data.ruangan_id)

        # Build update dict
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_by"] = user_id
        update_data["updated_at"] = datetime.utcnow()

        # Auto-update status based on kondisi
        if data.kondisi is not None:
            if data.kondisi == Kondisi.RUSAK_BERAT:
                update_data["status"] = StatusAset.RUSAK

        updated = await self.repository.update(aset_id, update_data)
        if not updated:
            raise AssetNotFoundError(aset_id)
        await self.commit()

        self.log_info(f"Asset updated: id={aset_id}")
        return updated

    async def delete_asset(
        self, aset_id: str, request: AsetDeleteRequest, user_id: str
    ) -> Aset:
        """Soft delete aset.

        Args:
            aset_id: UUID aset yang akan dihapus.
            request: AsetDeleteRequest dengan alasan penghapusan.
            user_id: UUID user yang menghapus.

        Returns:
            Aset yang dihapus (soft delete).

        Raises:
            AssetNotFoundError: Jika aset tidak ditemukan.
            AssetInMutationError: Jika aset sedang dalam mutasi.
            DeleteReasonTooShortError: Jika alasan terlalu pendek.
        """
        self.log_info(f"Deleting asset: {aset_id}")

        # Get existing aset
        aset = await self.repository.get_by_id(aset_id)
        if not aset:
            raise AssetNotFoundError(aset_id)

        # Check if deletable
        if aset.status == StatusAset.MUTASI:
            raise AssetInMutationError(aset_id)

        # Validate delete reason
        self._validate_delete_reason(request.alasan_penghapusan)

        # Soft delete
        deleted = await self.repository.soft_delete(
            aset_id, request.alasan_penghapusan, user_id
        )
        if not deleted:
            raise AssetNotFoundError(aset_id)
        await self.commit()

        self.log_info(f"Asset deleted: id={aset_id}")
        return deleted

    async def get_asset_by_id(self, aset_id: str) -> Aset:
        """Get aset by ID.

        Args:
            aset_id: UUID aset.

        Returns:
            Aset jika ditemukan.

        Raises:
            AssetNotFoundError: Jika aset tidak ditemukan.
        """
        aset = await self.repository.get_by_id(aset_id)
        if not aset:
            raise AssetNotFoundError(aset_id)
        return aset

    # =========================================================================
    # Search Operations
    # =========================================================================

    async def search_assets(
        self, params: AsetSearchParams, is_admin: bool = False
    ) -> PaginatedResponse[AsetResponse]:
        """Search aset dengan multiple filters.

        Args:
            params: AsetSearchParams dengan filter criteria.
            is_admin: True jika user adalah Admin (bisa lihat deleted).

        Returns:
            PaginatedResponse dengan list AsetResponse.
        """
        self.log_debug(f"Searching assets: keyword={params.keyword}")

        # Calculate pagination
        skip = (params.page - 1) * params.page_size
        limit = params.page_size

        # Viewer tidak bisa lihat deleted
        include_deleted = params.include_deleted and is_admin

        # Search
        assets = await self.repository.search(
            keyword=params.keyword,
            kategori_kib=params.kategori_kib,
            status=params.status,
            ruangan_id=params.ruangan_id,
            tahun_perolehan=params.tahun_perolehan,
            include_deleted=include_deleted,
            skip=skip,
            limit=limit,
        )

        # Count total
        total = await self.repository.count_search(
            keyword=params.keyword,
            kategori_kib=params.kategori_kib,
            status=params.status,
            ruangan_id=params.ruangan_id,
            tahun_perolehan=params.tahun_perolehan,
            include_deleted=include_deleted,
        )

        # Convert to response
        items = [self._to_response(a) for a in assets]

        return PaginatedResponse(
            data=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=(total + params.page_size - 1) // params.page_size,
        )

    def _to_response(self, aset: Aset) -> AsetResponse:
        """Convert Aset model to AsetResponse schema.

        Args:
            aset: Aset model instance.

        Returns:
            AsetResponse schema.
        """
        return AsetResponse(
            id=str(aset.id),
            nama_barang=aset.nama_barang,
            kode_barang=aset.kode_barang,
            nomor_register=aset.nomor_register,
            kategori_kib=aset.kategori_kib,
            tahun_perolehan=aset.tahun_perolehan,
            asal_usul=aset.asal_usul,
            harga=aset.harga,
            kondisi=aset.kondisi,
            status=aset.status,
            keterangan=aset.keterangan,
            ruangan_id=aset.ruangan_id,
            created_by=aset.created_by,
            updated_by=aset.updated_by,
            deleted_by=aset.deleted_by,
            created_at=aset.created_at,
            updated_at=aset.updated_at,
            deleted_at=aset.deleted_at,
            alasan_penghapusan=aset.delete_reason,
            merk=getattr(aset, "merk", None),
            tipe=getattr(aset, "tipe", None),
        )
