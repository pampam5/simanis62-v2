"""
Database management untuk SIMANIS62 V2.

Menggunakan SQLite dengan WAL mode untuk concurrent access support,
SQLAlchemy async engine, dan SQLModel untuk ORM.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manager untuk SQLite database dengan WAL mode dan optimal settings."""

    def __init__(self) -> None:
        """Initialize DatabaseManager."""
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    async def initialize(self) -> None:
        """Initialize database connection dengan optimal SQLite settings."""
        # Ensure database directory exists
        db_path = Path(settings.DATABASE_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create async engine dengan SQLite optimizations
        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///{db_path}",
            echo=settings.DEBUG,
            connect_args={
                "check_same_thread": False,
                "timeout": 30,  # 30 seconds timeout
            },
            poolclass=StaticPool,  # Single connection pool untuk SQLite
        )

        # Configure SQLite pragmas untuk performance dan reliability
        @event.listens_for(self.engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_conn: Any, _connection_record: Any) -> None:
            """Set SQLite pragmas saat connection dibuat."""
            cursor = dbapi_conn.cursor()

            # WAL mode untuk concurrent reads
            cursor.execute("PRAGMA journal_mode=WAL")

            # Busy timeout untuk menghindari "database is locked"
            cursor.execute("PRAGMA busy_timeout=30000")  # 30 seconds

            # Synchronous NORMAL untuk balance performance/safety
            cursor.execute("PRAGMA synchronous=NORMAL")

            # Cache size (negative = KB)
            cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache

            # Foreign keys enforcement
            cursor.execute("PRAGMA foreign_keys=ON")

            # Temp store in memory
            cursor.execute("PRAGMA temp_store=MEMORY")

            # Memory-mapped I/O
            cursor.execute("PRAGMA mmap_size=268435456")  # 256MB

            cursor.close()

        # Create session factory
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

        logger.info(
            "Database initialized",
            extra={
                "database_path": str(db_path),
                "journal_mode": "WAL",
                "busy_timeout": 30000,
            },
        )

    async def create_tables(self) -> None:
        """Create all tables dari SQLModel metadata."""
        if self.engine is None:
            raise RuntimeError("Database belum di-initialize")

        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables created")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session dengan automatic cleanup.

        Yields:
            AsyncSession: Database session

        Raises:
            RuntimeError: Jika database belum di-initialize
            Exception: Jika terjadi error saat operasi database
        """
        if self.session_factory is None:
            raise RuntimeError("Database belum di-initialize")

        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            await session.close()

    async def close(self) -> None:
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")

    async def check_health(self) -> dict[str, Any]:
        """Check database health dan return status.

        Returns:
            dict: Status informasi database
        """
        try:
            if self.session_factory is None:
                return {
                    "status": "unhealthy",
                    "error": "Database belum di-initialize",
                }

            async with self.get_session() as session:
                # Check connection
                await session.execute(text("SELECT 1"))

                # Check WAL mode
                result = await session.execute(text("PRAGMA journal_mode"))
                journal_mode = result.scalar()

                # Check integrity
                result = await session.execute(text("PRAGMA integrity_check"))
                integrity = result.scalar()

                # Get database size
                db_path = Path(settings.DATABASE_PATH)
                db_size = db_path.stat().st_size if db_path.exists() else 0

                return {
                    "status": "healthy",
                    "journal_mode": journal_mode,
                    "integrity": integrity,
                    "database_size_mb": round(db_size / (1024 * 1024), 2),
                    "path": str(db_path),
                }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}


# Global database manager instance
db_manager = DatabaseManager()


# FastAPI dependency untuk database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency untuk database session.

    Yields:
        AsyncSession: Database session untuk digunakan di endpoints

    Example:
        ```python
        @router.get("/aset/{id}")
        async def get_aset(id: UUID, db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Aset).where(Aset.id == id))
            return result.scalar_one_or_none()
        ```
    """
    async with db_manager.get_session() as session:
        yield session
