"""Audit repository untuk SIMANIS62 V2.

Module ini menyediakan AuditRepository class untuk operasi
database spesifik AuditTrail seperti get_by_record_id,
get_by_user_id, dan get_recent_activity.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditTrail, Operation
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository[AuditTrail]):
    """Repository untuk operasi database AuditTrail.

    Extends BaseRepository dengan methods spesifik untuk Audit:
    - get_by_record_id: Ambil audit trail untuk record tertentu
    - get_by_user_id: Ambil audit trail untuk user tertentu
    - get_recent_activity: Ambil aktivitas terbaru

    Example:
        ```python
        repo = AuditRepository(session)
        history = await repo.get_by_record_id(aset_id, "aset")
        user_activity = await repo.get_by_user_id(user_id)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize AuditRepository.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(AuditTrail, session)

    async def get_by_record_id(
        self,
        record_id: str,
        table_name: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditTrail]:
        """Get audit trail untuk record tertentu.

        Args:
            record_id: UUID record yang dicari.
            table_name: Filter berdasarkan nama tabel (optional).
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of audit entries untuk record tersebut.
        """
        query = select(AuditTrail).where(AuditTrail.record_id == record_id)

        if table_name:
            query = query.where(AuditTrail.table_name == table_name)

        query = query.order_by(AuditTrail.timestamp.desc())
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_user_id(
        self,
        user_id: str,
        operation: Operation | None = None,
        tanggal_dari: datetime | None = None,
        tanggal_sampai: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditTrail]:
        """Get audit trail untuk user tertentu.

        Args:
            user_id: UUID user.
            operation: Filter berdasarkan jenis operasi (optional).
            tanggal_dari: Filter tanggal mulai (optional).
            tanggal_sampai: Filter tanggal akhir (optional).
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of audit entries untuk user tersebut.
        """
        query = select(AuditTrail).where(AuditTrail.user_id == user_id)

        if operation:
            query = query.where(AuditTrail.operation == operation)

        if tanggal_dari:
            query = query.where(AuditTrail.timestamp >= tanggal_dari)

        if tanggal_sampai:
            query = query.where(AuditTrail.timestamp <= tanggal_sampai)

        query = query.order_by(AuditTrail.timestamp.desc())
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_recent_activity(
        self,
        table_name: str | None = None,
        operation: Operation | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[AuditTrail]:
        """Get aktivitas terbaru.

        Args:
            table_name: Filter berdasarkan nama tabel (optional).
            operation: Filter berdasarkan jenis operasi (optional).
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of recent audit entries.
        """
        query = select(AuditTrail)

        if table_name:
            query = query.where(AuditTrail.table_name == table_name)

        if operation:
            query = query.where(AuditTrail.operation == operation)

        query = query.order_by(AuditTrail.timestamp.desc())
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_changes_for_record(
        self,
        record_id: str,
        table_name: str,
    ) -> list[dict]:
        """Get semua perubahan untuk record tertentu dalam format ringkas.

        Berguna untuk menampilkan history perubahan di UI.

        Args:
            record_id: UUID record.
            table_name: Nama tabel.

        Returns:
            List of change summaries.
        """
        entries = await self.get_by_record_id(record_id, table_name)

        changes = []
        for entry in entries:
            changes.append(
                {
                    "id": entry.id,
                    "operation": entry.operation.value,
                    "user_id": entry.user_id,
                    "timestamp": entry.timestamp.isoformat()
                    if entry.timestamp
                    else None,
                    "old_value": entry.old_value,
                    "new_value": entry.new_value,
                }
            )

        return changes

    async def log_operation(
        self,
        user_id: str,
        operation: Operation,
        table_name: str,
        record_id: str,
        old_value: str | None = None,
        new_value: str | None = None,
        ip_address: str | None = None,
    ) -> AuditTrail:
        """Log operasi ke audit trail.

        Helper method untuk membuat audit entry dengan mudah.

        Args:
            user_id: UUID user yang melakukan operasi.
            operation: Jenis operasi (CREATE, UPDATE, DELETE).
            table_name: Nama tabel yang dioperasikan.
            record_id: UUID record yang dioperasikan.
            old_value: Nilai lama dalam JSON (untuk UPDATE/DELETE).
            new_value: Nilai baru dalam JSON (untuk CREATE/UPDATE).
            ip_address: IP address user (optional).

        Returns:
            AuditTrail entry yang baru dibuat.
        """
        audit = AuditTrail(
            user_id=user_id,
            operation=operation,
            table_name=table_name,
            record_id=record_id,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
        )

        return await self.create(audit)
