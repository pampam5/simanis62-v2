"""Ruangan service untuk SIMANIS62 V2.

Module ini menyediakan RuanganService untuk:
- CRUD operations untuk ruangan
- Get KIR (Kartu Inventaris Ruangan) report
"""

from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    BusinessRuleError,
    RuanganNotFoundError,
    ValidationError,
)
from app.models.aset import Aset
from app.models.ruangan import Ruangan
from app.repositories.ruangan_repository import RuanganRepository
from app.schemas.response import PaginatedResponse
from app.services.base import BaseService


class RuanganCreate:
    """Schema untuk membuat ruangan baru."""

    def __init__(
        self,
        kode_ruangan: str,
        nama_ruangan: str,
        keterangan: str | None = None,
    ):
        self.kode_ruangan = kode_ruangan
        self.nama_ruangan = nama_ruangan
        self.keterangan = keterangan


class RuanganUpdate:
    """Schema untuk update ruangan."""

    def __init__(
        self,
        nama_ruangan: str | None = None,
        keterangan: str | None = None,
    ):
        self.nama_ruangan = nama_ruangan
        self.keterangan = keterangan


class RuanganResponse:
    """Schema untuk response ruangan."""

    def __init__(
        self,
        id: str,
        kode_ruangan: str,
        nama_ruangan: str,
        keterangan: str | None,
        jumlah_aset: int,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.kode_ruangan = kode_ruangan
        self.nama_ruangan = nama_ruangan
        self.keterangan = keterangan
        self.jumlah_aset = jumlah_aset
        self.created_at = created_at
        self.updated_at = updated_at


class KirReportItem:
    """Schema untuk item KIR report."""

    def __init__(
        self,
        nomor_urut: int,
        kode_barang: str,
        nama_barang: str,
        nomor_register: int,
        kondisi: str,
        tahun_perolehan: int,
        harga: int,
        keterangan: str | None,
    ):
        self.nomor_urut = nomor_urut
        self.kode_barang = kode_barang
        self.nama_barang = nama_barang
        self.nomor_register = nomor_register
        self.kondisi = kondisi
        self.tahun_perolehan = tahun_perolehan
        self.harga = harga
        self.keterangan = keterangan


class KirReportResponse:
    """Schema untuk KIR report response."""

    def __init__(
        self,
        ruangan: RuanganResponse,
        total_aset: int,
        total_nilai: int,
        items: list[KirReportItem],
        tanggal_cetak: datetime,
    ):
        self.ruangan = ruangan
        self.total_aset = total_aset
        self.total_nilai = total_nilai
        self.items = items
        self.tanggal_cetak = tanggal_cetak


class RuanganService(BaseService[Ruangan, RuanganRepository]):
    """Service untuk ruangan management.

    Menyediakan:
    - create_ruangan: Buat ruangan baru
    - update_ruangan: Update ruangan
    - delete_ruangan: Hapus ruangan
    - get_ruangan_by_id: Get ruangan by ID
    - get_all_ruangan: Get semua ruangan
    - get_kir_report: Get KIR report untuk ruangan

    Example:
        ```python
        service = RuanganService(session)
        ruangan = await service.create_ruangan(data, user_id)
        kir = await service.get_kir_report(ruangan_id)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize RuanganService.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(session, RuanganRepository(session), "RuanganService")

    # =========================================================================
    # Validation Methods
    # =========================================================================

    async def _validate_kode_unique(
        self, kode_ruangan: str, exclude_id: str | None = None
    ) -> None:
        """Validate kode_ruangan unik.

        Args:
            kode_ruangan: Kode ruangan yang akan dicek.
            exclude_id: ID ruangan yang dikecualikan (untuk update).

        Raises:
            ValidationError: Jika kode_ruangan sudah ada.
        """
        existing = await self.repository.get_by_kode(kode_ruangan)
        if existing and (exclude_id is None or str(existing.id) != exclude_id):
            raise ValidationError(
                f"Kode ruangan '{kode_ruangan}' sudah digunakan",
                "kode_ruangan",
            )

    async def _validate_no_assets(self, ruangan_id: str) -> None:
        """Validate ruangan tidak memiliki aset.

        Args:
            ruangan_id: UUID ruangan.

        Raises:
            BusinessRuleError: Jika ruangan masih memiliki aset.
        """
        count = await self.repository.count_assets_in_room(ruangan_id)
        if count > 0:
            raise BusinessRuleError(
                f"Ruangan tidak dapat dihapus karena masih memiliki {count} aset"
            )

    # =========================================================================
    # CRUD Operations
    # =========================================================================

    async def create_ruangan(self, data: RuanganCreate, created_by: str) -> Ruangan:
        """Buat ruangan baru.

        Args:
            data: RuanganCreate dengan data ruangan.
            created_by: UUID user yang membuat.

        Returns:
            Ruangan yang baru dibuat.

        Raises:
            ValidationError: Jika kode_ruangan sudah ada.
        """
        self.log_info(f"Creating ruangan: {data.kode_ruangan}")

        # Validate kode unique
        await self._validate_kode_unique(data.kode_ruangan)

        # Create ruangan
        ruangan = Ruangan(
            kode_ruangan=data.kode_ruangan,
            nama_ruangan=data.nama_ruangan,
            keterangan=data.keterangan,
        )

        created = await self.repository.create(ruangan)
        await self.commit()

        self.log_info(f"Ruangan created: id={created.id}, kode={created.kode_ruangan}")
        return created

    async def update_ruangan(
        self, ruangan_id: str, data: RuanganUpdate, updated_by: str
    ) -> Ruangan:
        """Update ruangan.

        Args:
            ruangan_id: UUID ruangan yang akan diupdate.
            data: RuanganUpdate dengan data update.
            updated_by: UUID user yang mengupdate.

        Returns:
            Ruangan yang diupdate.

        Raises:
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
        """
        self.log_info(f"Updating ruangan: {ruangan_id}")

        # Get existing ruangan
        ruangan = await self.repository.get_by_id(ruangan_id)
        if not ruangan:
            raise RuanganNotFoundError(ruangan_id)

        # Build update dict
        update_data: dict[str, Any] = {}
        if data.nama_ruangan is not None:
            update_data["nama_ruangan"] = data.nama_ruangan
        if data.keterangan is not None:
            update_data["keterangan"] = data.keterangan

        update_data["updated_at"] = datetime.utcnow()

        updated = await self.repository.update(ruangan_id, update_data)
        if not updated:
            raise RuanganNotFoundError(ruangan_id)
        await self.commit()

        self.log_info(f"Ruangan updated: id={ruangan_id}")
        return updated

    async def delete_ruangan(self, ruangan_id: str) -> bool:
        """Hapus ruangan.

        Args:
            ruangan_id: UUID ruangan yang akan dihapus.

        Returns:
            True jika berhasil dihapus.

        Raises:
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
            BusinessRuleError: Jika ruangan masih memiliki aset.
        """
        self.log_info(f"Deleting ruangan: {ruangan_id}")

        # Get existing ruangan
        ruangan = await self.repository.get_by_id(ruangan_id)
        if not ruangan:
            raise RuanganNotFoundError(ruangan_id)

        # Validate no assets
        await self._validate_no_assets(ruangan_id)

        # Delete
        deleted = await self.repository.delete(ruangan_id)
        await self.commit()

        self.log_info(f"Ruangan deleted: id={ruangan_id}")
        return deleted

    async def get_ruangan_by_id(self, ruangan_id: str) -> Ruangan:
        """Get ruangan by ID.

        Args:
            ruangan_id: UUID ruangan.

        Returns:
            Ruangan jika ditemukan.

        Raises:
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
        """
        ruangan = await self.repository.get_by_id(ruangan_id)
        if not ruangan:
            raise RuanganNotFoundError(ruangan_id)
        return ruangan

    async def get_all_ruangan(
        self, page: int = 1, page_size: int = 100
    ) -> PaginatedResponse[RuanganResponse]:
        """Get semua ruangan dengan pagination.

        Args:
            page: Nomor halaman.
            page_size: Jumlah item per halaman.

        Returns:
            PaginatedResponse dengan list RuanganResponse.
        """
        skip = (page - 1) * page_size

        ruangan_list = await self.repository.get_all(skip=skip, limit=page_size)
        total = await self.repository.count()

        items = []
        for r in ruangan_list:
            count = await self.repository.count_assets_in_room(str(r.id))
            items.append(self._to_response(r, count))

        return PaginatedResponse(
            data=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )

    # =========================================================================
    # KIR Report
    # =========================================================================

    async def get_kir_report(self, ruangan_id: str) -> KirReportResponse:
        """Get KIR (Kartu Inventaris Ruangan) report.

        Args:
            ruangan_id: UUID ruangan.

        Returns:
            KirReportResponse dengan data ruangan dan aset.

        Raises:
            RuanganNotFoundError: Jika ruangan tidak ditemukan.
        """
        self.log_info(f"Generating KIR report for ruangan: {ruangan_id}")

        # Get ruangan
        ruangan = await self.repository.get_by_id(ruangan_id)
        if not ruangan:
            raise RuanganNotFoundError(ruangan_id)

        # Get assets in room
        assets = await self.repository.get_assets_in_room(
            ruangan_id, include_deleted=False, limit=1000
        )

        # Calculate totals
        total_aset = len(assets)
        total_nilai = sum(a.harga for a in assets)

        # Convert to KIR items
        items = [self._to_kir_item(a, i + 1) for i, a in enumerate(assets)]

        # Build response
        ruangan_response = self._to_response(ruangan, total_aset)

        self.log_info(f"KIR report generated: {total_aset} items")

        return KirReportResponse(
            ruangan=ruangan_response,
            total_aset=total_aset,
            total_nilai=total_nilai,
            items=items,
            tanggal_cetak=datetime.utcnow(),
        )

    def _to_response(self, ruangan: Ruangan, jumlah_aset: int = 0) -> RuanganResponse:
        """Convert Ruangan model to RuanganResponse.

        Args:
            ruangan: Ruangan model instance.
            jumlah_aset: Jumlah aset dalam ruangan.

        Returns:
            RuanganResponse.
        """
        return RuanganResponse(
            id=str(ruangan.id),
            kode_ruangan=ruangan.kode_ruangan,
            nama_ruangan=ruangan.nama_ruangan,
            keterangan=ruangan.keterangan,
            jumlah_aset=jumlah_aset,
            created_at=ruangan.created_at,
            updated_at=ruangan.updated_at,
        )

    def _to_kir_item(self, aset: Aset, nomor_urut: int) -> KirReportItem:
        """Convert Aset to KirReportItem.

        Args:
            aset: Aset model instance.
            nomor_urut: Nomor urut dalam laporan.

        Returns:
            KirReportItem.
        """
        from app.models.aset import Kondisi

        kondisi_map = {
            Kondisi.BAIK: "B",
            Kondisi.RUSAK_RINGAN: "KB",
            Kondisi.RUSAK_BERAT: "RB",
        }

        return KirReportItem(
            nomor_urut=nomor_urut,
            kode_barang=aset.kode_barang,
            nama_barang=aset.nama_barang,
            nomor_register=aset.nomor_register,
            kondisi=kondisi_map.get(aset.kondisi, ""),
            tahun_perolehan=aset.tahun_perolehan,
            harga=aset.harga,
            keterangan=aset.keterangan,
        )
