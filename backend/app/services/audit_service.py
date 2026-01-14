"""Audit Service untuk SIMANIS62 V2.

Module ini menyediakan AuditService dan decorator untuk auto-logging operasi CRUD.
"""

import functools
import json
import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditTrail, Operation
from app.repositories.audit_repository import AuditRepository
from app.services.base import BaseService

logger = logging.getLogger(__name__)

T = TypeVar("T")


class AuditService(BaseService[AuditTrail, AuditRepository]):
    """Service untuk audit trail operations.

    Menyediakan:
    - log_create: Log operasi CREATE
    - log_update: Log operasi UPDATE dengan old/new values
    - log_delete: Log operasi DELETE
    - get_history: Get audit history untuk record
    - get_user_activity: Get aktivitas user

    Example:
        ```python
        service = AuditService(session)
        await service.log_create(user_id, "aset", aset_id, new_data)
        history = await service.get_history(aset_id, "aset")
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize AuditService.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(session, AuditRepository(session), "AuditService")

    async def log_create(
        self,
        user_id: str,
        table_name: str,
        record_id: str,
        new_value: dict[str, Any] | None = None,
        ip_address: str | None = None,
    ) -> AuditTrail:
        """Log operasi CREATE.

        Args:
            user_id: UUID user yang melakukan operasi.
            table_name: Nama tabel.
            record_id: UUID record yang dibuat.
            new_value: Data baru (optional).
            ip_address: IP address user (optional).

        Returns:
            AuditTrail entry yang dibuat.
        """
        self.log_info(f"Logging CREATE: {table_name}/{record_id}")

        audit = await self.repository.log_operation(
            user_id=user_id,
            operation=Operation.CREATE,
            table_name=table_name,
            record_id=record_id,
            old_value=None,
            new_value=self._serialize(new_value),
            ip_address=ip_address,
        )

        await self.commit()
        return audit

    async def log_update(
        self,
        user_id: str,
        table_name: str,
        record_id: str,
        old_value: dict[str, Any] | None = None,
        new_value: dict[str, Any] | None = None,
        ip_address: str | None = None,
    ) -> AuditTrail:
        """Log operasi UPDATE.

        Args:
            user_id: UUID user yang melakukan operasi.
            table_name: Nama tabel.
            record_id: UUID record yang diupdate.
            old_value: Data lama (optional).
            new_value: Data baru (optional).
            ip_address: IP address user (optional).

        Returns:
            AuditTrail entry yang dibuat.
        """
        self.log_info(f"Logging UPDATE: {table_name}/{record_id}")

        audit = await self.repository.log_operation(
            user_id=user_id,
            operation=Operation.UPDATE,
            table_name=table_name,
            record_id=record_id,
            old_value=self._serialize(old_value),
            new_value=self._serialize(new_value),
            ip_address=ip_address,
        )

        await self.commit()
        return audit

    async def log_delete(
        self,
        user_id: str,
        table_name: str,
        record_id: str,
        old_value: dict[str, Any] | None = None,
        ip_address: str | None = None,
    ) -> AuditTrail:
        """Log operasi DELETE.

        Args:
            user_id: UUID user yang melakukan operasi.
            table_name: Nama tabel.
            record_id: UUID record yang dihapus.
            old_value: Data yang dihapus (optional).
            ip_address: IP address user (optional).

        Returns:
            AuditTrail entry yang dibuat.
        """
        self.log_info(f"Logging DELETE: {table_name}/{record_id}")

        audit = await self.repository.log_operation(
            user_id=user_id,
            operation=Operation.DELETE,
            table_name=table_name,
            record_id=record_id,
            old_value=self._serialize(old_value),
            new_value=None,
            ip_address=ip_address,
        )

        await self.commit()
        return audit

    async def get_history(
        self,
        record_id: str,
        table_name: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditTrail]:
        """Get audit history untuk record.

        Args:
            record_id: UUID record.
            table_name: Filter berdasarkan tabel (optional).
            skip: Offset untuk pagination.
            limit: Limit untuk pagination.

        Returns:
            List of AuditTrail entries.
        """
        return await self.repository.get_by_record_id(
            record_id=record_id,
            table_name=table_name,
            skip=skip,
            limit=limit,
        )

    async def get_user_activity(
        self,
        user_id: str,
        operation: Operation | None = None,
        tanggal_dari: datetime | None = None,
        tanggal_sampai: datetime | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditTrail]:
        """Get aktivitas user.

        Args:
            user_id: UUID user.
            operation: Filter berdasarkan operasi (optional).
            tanggal_dari: Filter tanggal mulai (optional).
            tanggal_sampai: Filter tanggal akhir (optional).
            skip: Offset untuk pagination.
            limit: Limit untuk pagination.

        Returns:
            List of AuditTrail entries.
        """
        return await self.repository.get_by_user_id(
            user_id=user_id,
            operation=operation,
            tanggal_dari=tanggal_dari,
            tanggal_sampai=tanggal_sampai,
            skip=skip,
            limit=limit,
        )

    async def get_recent_activity(
        self,
        table_name: str | None = None,
        operation: Operation | None = None,
        limit: int = 50,
    ) -> list[AuditTrail]:
        """Get aktivitas terbaru.

        Args:
            table_name: Filter berdasarkan tabel (optional).
            operation: Filter berdasarkan operasi (optional).
            limit: Maksimum jumlah record.

        Returns:
            List of AuditTrail entries.
        """
        return await self.repository.get_recent_activity(
            table_name=table_name,
            operation=operation,
            limit=limit,
        )

    def _serialize(self, data: dict[str, Any] | None) -> str | None:
        """Serialize dict ke JSON string.

        Args:
            data: Dict to serialize.

        Returns:
            JSON string atau None.
        """
        if data is None:
            return None

        # Convert non-serializable types
        def convert(obj: Any) -> Any:
            if isinstance(obj, datetime):
                return obj.isoformat()
            if hasattr(obj, "value"):  # Enum
                return obj.value
            if hasattr(obj, "__dict__"):
                return str(obj)
            return obj

        try:
            return json.dumps(data, default=convert, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            logger.warning(f"Failed to serialize audit data: {e}")
            return json.dumps({"error": "Failed to serialize data"})


def audit_operation(
    operation: Operation,
    table_name: str,
    get_record_id: Callable[..., str] | None = None,
    get_old_value: Callable[..., dict[str, Any] | None] | None = None,
    get_new_value: Callable[..., dict[str, Any] | None] | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator untuk auto-logging operasi CRUD.

    Usage:
        ```python
        @audit_operation(
            operation=Operation.CREATE,
            table_name="aset",
            get_record_id=lambda result: str(result.id),
            get_new_value=lambda result: result.model_dump(),
        )
        async def create_aset(self, data: AsetCreate, user_id: str) -> Aset: ...
        ```

    Args:
        operation: Jenis operasi (CREATE/UPDATE/DELETE).
        table_name: Nama tabel.
        get_record_id: Function untuk extract record_id dari result.
        get_old_value: Function untuk extract old_value.
        get_new_value: Function untuk extract new_value dari result.

    Returns:
        Decorated function.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> T:
            # Execute original function
            result = await func(self, *args, **kwargs)

            # Try to log audit
            try:
                # Get session from self
                session = getattr(self, "session", None) or getattr(
                    self, "_session", None
                )
                if not session:
                    logger.warning("No session found for audit logging")
                    return result

                # Get user_id from kwargs or args
                user_id = kwargs.get("user_id")
                if not user_id and len(args) > 0:
                    # Try to find user_id in args
                    for arg in args:
                        if isinstance(arg, str) and len(arg) == 36:  # UUID length
                            user_id = arg
                            break

                if not user_id:
                    user_id = "SYSTEM"

                # Get record_id
                record_id = ""
                if get_record_id:
                    record_id = get_record_id(result)
                elif hasattr(result, "id"):
                    record_id = str(result.id)

                # Get values
                old_value = get_old_value(result) if get_old_value else None
                new_value = get_new_value(result) if get_new_value else None

                # Log audit
                audit_service = AuditService(session)

                if operation == Operation.CREATE:
                    await audit_service.log_create(
                        user_id=user_id,
                        table_name=table_name,
                        record_id=record_id,
                        new_value=new_value,
                    )
                elif operation == Operation.UPDATE:
                    await audit_service.log_update(
                        user_id=user_id,
                        table_name=table_name,
                        record_id=record_id,
                        old_value=old_value,
                        new_value=new_value,
                    )
                elif operation == Operation.DELETE:
                    await audit_service.log_delete(
                        user_id=user_id,
                        table_name=table_name,
                        record_id=record_id,
                        old_value=old_value,
                    )

            except Exception as e:
                # Don't fail the operation if audit logging fails
                logger.error(f"Failed to log audit: {e}")

            return result

        return wrapper

    return decorator
