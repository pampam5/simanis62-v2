"""Ruangan repository untuk SIMANIS62 V2.

Module ini menyediakan RuanganRepository class untuk operasi
database spesifik Ruangan seperti get_by_kode dan get_assets_in_room.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aset import Aset, StatusAset
from app.models.ruangan import Ruangan
from app.repositories.base import BaseRepository


class RuanganRepository(BaseRepository[Ruangan]):
    """Repository untuk operasi database Ruangan.

    Extends BaseRepository dengan methods spesifik untuk Ruangan:
    - get_by_kode: Cari ruangan berdasarkan kode_ruangan
    - get_assets_in_room: Ambil semua aset dalam ruangan (untuk KIR)

    Example:
        ```python
        repo = RuanganRepository(session)
        ruangan = await repo.get_by_kode("R001")
        assets = await repo.get_assets_in_room(ruangan_id)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize RuanganRepository.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(Ruangan, session)

    async def get_by_kode(self, kode_ruangan: str) -> Ruangan | None:
        """Get ruangan berdasarkan kode_ruangan.

        Args:
            kode_ruangan: Kode ruangan yang dicari.

        Returns:
            Ruangan jika ditemukan, None jika tidak.
        """
        result = await self.session.execute(
            select(Ruangan).where(Ruangan.kode_ruangan == kode_ruangan)
        )
        return result.scalar_one_or_none()

    async def get_assets_in_room(
        self,
        ruangan_id: str,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Aset]:
        """Get semua aset dalam ruangan tertentu (untuk KIR report).

        Args:
            ruangan_id: UUID ruangan (as string).
            include_deleted: Jika True, termasuk aset yang dihapus.
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of assets dalam ruangan.
        """
        from uuid import UUID
        ruangan_uuid = UUID(ruangan_id)
        query = select(Aset).where(Aset.ruangan_id == ruangan_uuid)

        if not include_deleted:
            query = query.where(Aset.status != StatusAset.DIHAPUS)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count_assets_in_room(
        self,
        ruangan_id: str,
        include_deleted: bool = False,
    ) -> int:
        """Count jumlah aset dalam ruangan.

        Args:
            ruangan_id: UUID ruangan (as string).
            include_deleted: Jika True, termasuk aset yang dihapus.

        Returns:
            Jumlah aset dalam ruangan.
        """
        from uuid import UUID
        ruangan_uuid = UUID(ruangan_id)
        query = (
            select(func.count()).select_from(Aset).where(Aset.ruangan_id == ruangan_uuid)
        )

        if not include_deleted:
            query = query.where(Aset.status != StatusAset.DIHAPUS)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def kode_exists(self, kode_ruangan: str) -> bool:
        """Check apakah kode_ruangan sudah digunakan.

        Args:
            kode_ruangan: Kode ruangan yang dicek.

        Returns:
            True jika sudah ada, False jika belum.
        """
        ruangan = await self.get_by_kode(kode_ruangan)
        return ruangan is not None
