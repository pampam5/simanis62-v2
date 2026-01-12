"""Aset repository untuk SIMANIS62 V2.

Module ini menyediakan AsetRepository class untuk operasi
database spesifik Aset seperti search, get_for_kib_report, dll.
"""

from datetime import UTC, datetime

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aset import Aset, KategoriKIB, StatusAset
from app.repositories.base import BaseRepository


class AsetRepository(BaseRepository[Aset]):
    """Repository untuk operasi database Aset.

    Extends BaseRepository dengan methods spesifik untuk Aset:
    - get_by_kode_barang: Cari aset berdasarkan kode_barang
    - search: Search dengan multiple filters
    - get_next_nomor_register: Generate nomor register berikutnya
    - get_for_kib_report: Ambil aset untuk laporan KIB
    - soft_delete: Soft delete aset

    Example:
        ```python
        repo = AsetRepository(session)
        aset = await repo.get_by_kode_barang("02.06.01.0001")
        results = await repo.search(keyword="laptop", kategori_kib=KategoriKIB.B)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize AsetRepository.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(Aset, session)

    async def get_by_kode_barang(self, kode_barang: str) -> Aset | None:
        """Get aset berdasarkan kode_barang.

        Args:
            kode_barang: Kode barang yang dicari (format: XX.XX.XX.XXXX).

        Returns:
            Aset jika ditemukan, None jika tidak.
        """
        result = await self.session.execute(
            select(Aset).where(Aset.kode_barang == kode_barang)
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        keyword: str | None = None,
        kategori_kib: KategoriKIB | None = None,
        status: StatusAset | None = None,
        ruangan_id: str | None = None,
        tahun_perolehan: int | None = None,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Aset]:
        """Search aset dengan multiple filters.

        Args:
            keyword: Kata kunci untuk search di nama_barang, kode_barang, merk.
            kategori_kib: Filter berdasarkan kategori KIB (A-F).
            status: Filter berdasarkan status aset.
            ruangan_id: Filter berdasarkan ruangan.
            tahun_perolehan: Filter berdasarkan tahun perolehan.
            include_deleted: Jika True, termasuk aset yang dihapus.
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of matching assets.
        """
        query = select(Aset)

        # Exclude deleted by default
        if not include_deleted:
            query = query.where(Aset.status != StatusAset.DIHAPUS)

        # Keyword search (nama_barang, kode_barang)
        if keyword:
            keyword_filter = f"%{keyword}%"
            query = query.where(
                or_(
                    Aset.nama_barang.ilike(keyword_filter),
                    Aset.kode_barang.ilike(keyword_filter),
                )
            )

        # Filter by kategori_kib
        if kategori_kib:
            query = query.where(Aset.kategori_kib == kategori_kib)

        # Filter by status
        if status:
            query = query.where(Aset.status == status)

        # Filter by ruangan
        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)

        # Filter by tahun_perolehan
        if tahun_perolehan:
            query = query.where(Aset.tahun_perolehan == tahun_perolehan)

        # Order by nomor_register
        query = query.order_by(Aset.nomor_register)

        # Pagination
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_search(
        self,
        keyword: str | None = None,
        kategori_kib: KategoriKIB | None = None,
        status: StatusAset | None = None,
        ruangan_id: str | None = None,
        tahun_perolehan: int | None = None,
        include_deleted: bool = False,
    ) -> int:
        """Count hasil search dengan filters yang sama.

        Args:
            keyword: Kata kunci untuk search.
            kategori_kib: Filter berdasarkan kategori KIB.
            status: Filter berdasarkan status aset.
            ruangan_id: Filter berdasarkan ruangan.
            tahun_perolehan: Filter berdasarkan tahun perolehan.
            include_deleted: Jika True, termasuk aset yang dihapus.

        Returns:
            Jumlah aset yang match.
        """
        query = select(func.count()).select_from(Aset)

        if not include_deleted:
            query = query.where(Aset.status != StatusAset.DIHAPUS)

        if keyword:
            keyword_filter = f"%{keyword}%"
            query = query.where(
                or_(
                    Aset.nama_barang.ilike(keyword_filter),
                    Aset.kode_barang.ilike(keyword_filter),
                )
            )

        if kategori_kib:
            query = query.where(Aset.kategori_kib == kategori_kib)

        if status:
            query = query.where(Aset.status == status)

        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)

        if tahun_perolehan:
            query = query.where(Aset.tahun_perolehan == tahun_perolehan)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_next_nomor_register(
        self,
        kategori_kib: KategoriKIB,
        tahun: int,
    ) -> int:
        """Generate nomor register berikutnya untuk kategori dan tahun tertentu.

        Nomor register adalah sequential number per kategori KIB per tahun.
        Format: 1, 2, 3, ... (auto-increment per kategori per tahun)

        Args:
            kategori_kib: Kategori KIB (A-F).
            tahun: Tahun perolehan.

        Returns:
            Nomor register berikutnya.
        """
        result = await self.session.execute(
            select(func.max(Aset.nomor_register))
            .where(Aset.kategori_kib == kategori_kib)
            .where(Aset.tahun_perolehan == tahun)
        )
        max_register = result.scalar()
        return (max_register or 0) + 1

    async def get_for_kib_report(
        self,
        kategori_kib: KategoriKIB,
        tahun: int | None = None,
        ruangan_id: str | None = None,
        skip: int = 0,
        limit: int = 1000,
    ) -> list[Aset]:
        """Get aset untuk laporan KIB.

        Hanya mengambil aset dengan status Aktif atau Rusak (bukan Dihapus).
        Sesuai dengan requirement REQ-7 sampai REQ-12.

        Args:
            kategori_kib: Kategori KIB (A-F).
            tahun: Filter berdasarkan tahun perolehan (optional).
            ruangan_id: Filter berdasarkan ruangan (optional).
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of assets untuk KIB report.
        """
        query = (
            select(Aset)
            .where(Aset.kategori_kib == kategori_kib)
            .where(
                or_(
                    Aset.status == StatusAset.AKTIF,
                    Aset.status == StatusAset.RUSAK,
                )
            )
        )

        if tahun:
            query = query.where(Aset.tahun_perolehan == tahun)

        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)

        query = query.order_by(Aset.nomor_register).offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_for_kib_report(
        self,
        kategori_kib: KategoriKIB,
        tahun: int | None = None,
        ruangan_id: str | None = None,
    ) -> int:
        """Count aset untuk laporan KIB.

        Args:
            kategori_kib: Kategori KIB (A-F).
            tahun: Filter berdasarkan tahun perolehan (optional).
            ruangan_id: Filter berdasarkan ruangan (optional).

        Returns:
            Jumlah aset untuk KIB report.
        """
        query = (
            select(func.count())
            .select_from(Aset)
            .where(Aset.kategori_kib == kategori_kib)
            .where(
                or_(
                    Aset.status == StatusAset.AKTIF,
                    Aset.status == StatusAset.RUSAK,
                )
            )
        )

        if tahun:
            query = query.where(Aset.tahun_perolehan == tahun)

        if ruangan_id:
            query = query.where(Aset.ruangan_id == ruangan_id)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def get_total_value_for_kib(
        self,
        kategori_kib: KategoriKIB,
        tahun: int | None = None,
    ) -> int:
        """Get total nilai aset untuk laporan KIB.

        Args:
            kategori_kib: Kategori KIB (A-F).
            tahun: Filter berdasarkan tahun perolehan (optional).

        Returns:
            Total nilai aset dalam Rupiah.
        """
        query = (
            select(func.sum(Aset.harga))
            .where(Aset.kategori_kib == kategori_kib)
            .where(
                or_(
                    Aset.status == StatusAset.AKTIF,
                    Aset.status == StatusAset.RUSAK,
                )
            )
        )

        if tahun:
            query = query.where(Aset.tahun_perolehan == tahun)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def soft_delete(
        self,
        aset_id: str,
        delete_reason: str,
        deleted_by: str,
    ) -> Aset | None:
        """Soft delete aset (set status ke DIHAPUS).

        Args:
            aset_id: UUID aset yang akan dihapus.
            delete_reason: Alasan penghapusan (wajib).
            deleted_by: UUID user yang menghapus.

        Returns:
            Aset yang diupdate, None jika tidak ditemukan.
        """

        aset = await self.get_by_id(aset_id)
        if not aset:
            return None

        aset.status = StatusAset.DIHAPUS
        aset.delete_reason = delete_reason
        aset.deleted_by = deleted_by
        aset.deleted_at = datetime.now(UTC)

        await self.session.flush()
        await self.session.refresh(aset)
        return aset

    async def kode_barang_exists(self, kode_barang: str) -> bool:
        """Check apakah kode_barang sudah digunakan.

        Args:
            kode_barang: Kode barang yang dicek.

        Returns:
            True jika sudah ada, False jika belum.
        """
        aset = await self.get_by_kode_barang(kode_barang)
        return aset is not None
