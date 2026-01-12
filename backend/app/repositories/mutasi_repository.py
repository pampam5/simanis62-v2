"""Mutasi repository untuk SIMANIS62 V2.

Module ini menyediakan MutasiRepository class untuk operasi
database spesifik RiwayatMutasi seperti get_by_aset_id,
get_pending_mutations, dan get_mutation_history.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mutasi import RiwayatMutasi, StatusMutasi
from app.repositories.base import BaseRepository


class MutasiRepository(BaseRepository[RiwayatMutasi]):
    """Repository untuk operasi database RiwayatMutasi.

    Extends BaseRepository dengan methods spesifik untuk Mutasi:
    - get_by_aset_id: Ambil semua mutasi untuk aset tertentu
    - get_pending_mutations: Ambil mutasi yang masih pending
    - get_mutation_history: Ambil history mutasi dengan filters
    - get_expired_mutations: Ambil mutasi yang sudah expired (> 7 hari)

    Example:
        ```python
        repo = MutasiRepository(session)
        mutations = await repo.get_by_aset_id(aset_id)
        pending = await repo.get_pending_mutations()
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize MutasiRepository.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(RiwayatMutasi, session)

    async def get_by_aset_id(
        self,
        aset_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RiwayatMutasi]:
        """Get semua mutasi untuk aset tertentu.

        Args:
            aset_id: UUID aset.
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of mutations untuk aset tersebut.
        """
        result = await self.session.execute(
            select(RiwayatMutasi)
            .where(RiwayatMutasi.aset_id == aset_id)
            .order_by(RiwayatMutasi.tanggal_mutasi.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_pending_mutations(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RiwayatMutasi]:
        """Get semua mutasi dengan status DALAM_PROSES.

        Args:
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of pending mutations.
        """
        result = await self.session.execute(
            select(RiwayatMutasi)
            .where(RiwayatMutasi.status_mutasi == StatusMutasi.DALAM_PROSES)
            .order_by(RiwayatMutasi.tanggal_mutasi.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_pending_mutations(self) -> int:
        """Count jumlah mutasi yang masih pending.

        Returns:
            Jumlah pending mutations.
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(RiwayatMutasi)
            .where(RiwayatMutasi.status_mutasi == StatusMutasi.DALAM_PROSES)
        )
        return result.scalar() or 0

    async def get_mutation_history(
        self,
        aset_id: str | None = None,
        ruangan_asal_id: str | None = None,
        ruangan_tujuan_id: str | None = None,
        status: StatusMutasi | None = None,
        tanggal_dari: datetime | None = None,
        tanggal_sampai: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[RiwayatMutasi]:
        """Get history mutasi dengan filters.

        Args:
            aset_id: Filter berdasarkan aset (optional).
            ruangan_asal_id: Filter berdasarkan ruangan asal (optional).
            ruangan_tujuan_id: Filter berdasarkan ruangan tujuan (optional).
            status: Filter berdasarkan status mutasi (optional).
            tanggal_dari: Filter tanggal mulai (optional).
            tanggal_sampai: Filter tanggal akhir (optional).
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of mutations matching filters.
        """
        query = select(RiwayatMutasi)

        if aset_id:
            query = query.where(RiwayatMutasi.aset_id == aset_id)

        if ruangan_asal_id:
            query = query.where(RiwayatMutasi.ruangan_asal_id == ruangan_asal_id)

        if ruangan_tujuan_id:
            query = query.where(RiwayatMutasi.ruangan_tujuan_id == ruangan_tujuan_id)

        if status:
            query = query.where(RiwayatMutasi.status_mutasi == status)

        if tanggal_dari:
            query = query.where(RiwayatMutasi.tanggal_mutasi >= tanggal_dari)

        if tanggal_sampai:
            query = query.where(RiwayatMutasi.tanggal_mutasi <= tanggal_sampai)

        query = query.order_by(RiwayatMutasi.tanggal_mutasi.desc())
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def has_pending_mutation(self, aset_id: str) -> bool:
        """Check apakah aset memiliki mutasi yang masih pending.

        Digunakan untuk validasi sebelum membuat mutasi baru.
        Aset tidak boleh memiliki lebih dari satu mutasi pending.

        Args:
            aset_id: UUID aset.

        Returns:
            True jika ada pending mutation, False jika tidak.
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(RiwayatMutasi)
            .where(RiwayatMutasi.aset_id == aset_id)
            .where(RiwayatMutasi.status_mutasi == StatusMutasi.DALAM_PROSES)
        )
        return (result.scalar() or 0) > 0

    async def get_expired_mutations(
        self,
        days: int = 7,
    ) -> list[RiwayatMutasi]:
        """Get mutasi yang sudah expired (pending > X hari).

        Digunakan untuk auto-cancel mutasi yang tidak diselesaikan.
        Sesuai dengan US-013 (Auto-cancel 7 days).

        Args:
            days: Jumlah hari sebelum dianggap expired (default: 7).

        Returns:
            List of expired mutations.
        """
        cutoff_date = datetime.now(UTC) - timedelta(days=days)

        result = await self.session.execute(
            select(RiwayatMutasi)
            .where(RiwayatMutasi.status_mutasi == StatusMutasi.DALAM_PROSES)
            .where(RiwayatMutasi.mulai_mutasi < cutoff_date)
        )
        return list(result.scalars().all())

    async def complete_mutation(
        self,
        mutasi_id: str,
    ) -> RiwayatMutasi | None:
        """Complete mutasi (set status ke SELESAI).

        Args:
            mutasi_id: UUID mutasi.

        Returns:
            Mutasi yang diupdate, None jika tidak ditemukan.
        """
        mutasi = await self.get_by_id(mutasi_id)
        if not mutasi:
            return None

        mutasi.status_mutasi = StatusMutasi.SELESAI
        mutasi.selesai_mutasi = datetime.now(UTC)

        await self.session.flush()
        await self.session.refresh(mutasi)
        return mutasi

    async def cancel_mutation(
        self,
        mutasi_id: str,
        alasan_pembatalan: str,
    ) -> RiwayatMutasi | None:
        """Cancel mutasi (set status ke DIBATALKAN).

        Args:
            mutasi_id: UUID mutasi.
            alasan_pembatalan: Alasan pembatalan (wajib).

        Returns:
            Mutasi yang diupdate, None jika tidak ditemukan.
        """
        mutasi = await self.get_by_id(mutasi_id)
        if not mutasi:
            return None

        mutasi.status_mutasi = StatusMutasi.DIBATALKAN
        mutasi.alasan_pembatalan = alasan_pembatalan

        await self.session.flush()
        await self.session.refresh(mutasi)
        return mutasi
