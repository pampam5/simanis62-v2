"""Pytest fixtures untuk SIMANIS62 V2 backend tests."""

import asyncio
from collections.abc import AsyncGenerator
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.core.database import get_db
from app.main import create_app


# Mock hash_password to avoid bcrypt backend issues on Windows
def mock_hash_password(password: str) -> str:
    """Simple mock hash for testing - NOT for production use."""
    return f"$2b$12$mock_hash_{password}"


def mock_verify_password(plain_password: str, hashed_password: str) -> bool:
    """Simple mock verify for testing - NOT for production use."""
    expected_hash = f"$2b$12$mock_hash_{plain_password}"
    return hashed_password == expected_hash


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def mock_password_functions():
    """Auto-mock password functions to avoid bcrypt issues."""
    with (
        patch("app.core.security.hash_password", mock_hash_password),
        patch("app.core.security.verify_password", mock_verify_password),
        patch("app.core.security.pwd_context.hash", mock_hash_password),
        patch("app.core.security.pwd_context.verify", mock_verify_password),
    ):
        yield


@pytest_asyncio.fixture
async def async_engine():
    """Create in-memory SQLite engine for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create database session for testing."""
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(async_engine) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with in-memory database."""
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
