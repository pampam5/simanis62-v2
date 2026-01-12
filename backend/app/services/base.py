"""Base service untuk SIMANIS62 V2.

Module ini menyediakan BaseService class sebagai base class
untuk semua services dengan common functionality.
"""

import logging
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
RepoType = TypeVar("RepoType", bound=BaseRepository)


class BaseService(Generic[ModelType, RepoType]):
    """Base service dengan common functionality.

    Menyediakan:
    - Logger per service
    - Repository access
    - Common helper methods

    Attributes:
        session: AsyncSession untuk database operations.
        repository: Repository instance untuk model.
        logger: Logger instance untuk service.

    Example:
        ```python
        class AsetService(BaseService[Aset, AsetRepository]):
            def __init__(self, session: AsyncSession):
                super().__init__(session, AsetRepository(session), "AsetService")
        ```
    """

    def __init__(
        self,
        session: AsyncSession,
        repository: RepoType,
        service_name: str,
    ) -> None:
        """Initialize BaseService.

        Args:
            session: AsyncSession untuk database operations.
            repository: Repository instance untuk model.
            service_name: Nama service untuk logging.
        """
        self.session = session
        self.repository = repository
        self.logger = logging.getLogger(f"simanis62.services.{service_name}")

    async def commit(self) -> None:
        """Commit current transaction."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback current transaction."""
        await self.session.rollback()

    def log_info(self, message: str, **kwargs) -> None:
        """Log info message dengan extra context.

        Args:
            message: Log message.
            **kwargs: Extra context untuk logging (akan diabaikan untuk avoid conflicts).
        """
        self.logger.info(message)

    def log_warning(self, message: str, **kwargs) -> None:
        """Log warning message dengan extra context.

        Args:
            message: Log message.
            **kwargs: Extra context untuk logging (akan diabaikan untuk avoid conflicts).
        """
        self.logger.warning(message)

    def log_error(self, message: str, **kwargs) -> None:
        """Log error message dengan extra context.

        Args:
            message: Log message.
            **kwargs: Extra context untuk logging (akan diabaikan untuk avoid conflicts).
        """
        self.logger.error(message)

    def log_debug(self, message: str, **kwargs) -> None:
        """Log debug message dengan extra context.

        Args:
            message: Log message.
            **kwargs: Extra context untuk logging (akan diabaikan untuk avoid conflicts).
        """
        self.logger.debug(message)
