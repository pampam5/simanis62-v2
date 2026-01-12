"""User repository untuk SIMANIS62 V2.

Module ini menyediakan UserRepository class untuk operasi
database spesifik User seperti get_by_username dan get_active_users.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserStatus
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository untuk operasi database User.

    Extends BaseRepository dengan methods spesifik untuk User:
    - get_by_username: Cari user berdasarkan username
    - get_active_users: Ambil semua user dengan status Aktif

    Example:
        ```python
        repo = UserRepository(session)
        user = await repo.get_by_username("admin")
        active_users = await repo.get_active_users()
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize UserRepository.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> User | None:
        """Get user berdasarkan username.

        Args:
            username: Username yang dicari.

        Returns:
            User jika ditemukan, None jika tidak.
        """
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_active_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        """Get semua user dengan status Aktif.

        Args:
            skip: Jumlah record yang di-skip (offset).
            limit: Maksimum jumlah record yang dikembalikan.

        Returns:
            List of active users.
        """
        result = await self.session.execute(
            select(User)
            .where(User.status == UserStatus.AKTIF)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def username_exists(self, username: str) -> bool:
        """Check apakah username sudah digunakan.

        Args:
            username: Username yang dicek.

        Returns:
            True jika sudah ada, False jika belum.
        """
        user = await self.get_by_username(username)
        return user is not None
