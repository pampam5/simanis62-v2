"""Base repository dengan generic CRUD operations.

Module ini menyediakan BaseRepository class yang dapat digunakan
oleh semua repository untuk operasi CRUD standar.
"""

import uuid
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """Base repository dengan generic CRUD operations.

    Class ini menyediakan operasi CRUD standar yang dapat digunakan
    oleh semua repository. Menggunakan Generic untuk type safety.

    Attributes:
        model: SQLModel class untuk repository ini.
        session: AsyncSession untuk database operations.

    Example:
        ```python
        class UserRepository(BaseRepository[User]):
            def __init__(self, session: AsyncSession):
                super().__init__(User, session)
        ```
    """

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        """Initialize repository dengan model dan session.

        Args:
            model: SQLModel class untuk repository ini.
            session: AsyncSession untuk database operations.
        """
        self.model = model
        self.session = session

    async def get_by_id(self, id: uuid.UUID) -> ModelType | None:
        """Get single record by ID.

        Args:
            id: UUID dari record.

        Returns:
            Record jika ditemukan, None jika tidak.
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
    ) -> list[ModelType]:
        """Get all records dengan pagination dan optional filters.

        Args:
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.
            filters: Dictionary filter {field_name: value}.

        Returns:
            List of records.
        """
        query = select(self.model)

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count records dengan optional filters.

        Args:
            filters: Dictionary filter {field_name: value}.

        Returns:
            Jumlah records yang match.
        """
        query = select(func.count()).select_from(self.model)

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def create(self, obj_in: ModelType) -> ModelType:
        """Create new record.

        Args:
            obj_in: SQLModel instance untuk disimpan.

        Returns:
            Record yang baru dibuat dengan ID.
        """
        self.session.add(obj_in)
        await self.session.flush()
        await self.session.refresh(obj_in)
        return obj_in

    async def update(
        self,
        id: uuid.UUID,
        obj_in: dict[str, Any],
    ) -> ModelType | None:
        """Update existing record.

        Args:
            id: UUID dari record.
            obj_in: Dictionary dengan field yang akan diupdate.

        Returns:
            Record yang diupdate, None jika tidak ditemukan.
        """
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None

        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: uuid.UUID) -> bool:
        """Hard delete record.

        Args:
            id: UUID dari record.

        Returns:
            True jika berhasil dihapus, False jika tidak ditemukan.
        """
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False

        await self.session.delete(db_obj)
        await self.session.flush()
        return True

    async def exists(self, id: uuid.UUID) -> bool:
        """Check apakah record dengan ID tertentu ada.

        Args:
            id: UUID dari record.

        Returns:
            True jika ada, False jika tidak.
        """
        result = await self.session.execute(
            select(func.count()).select_from(self.model).where(self.model.id == id)
        )
        return (result.scalar() or 0) > 0
