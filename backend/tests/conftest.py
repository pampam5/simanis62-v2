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


# Shared test data fixtures
@pytest_asyncio.fixture
async def admin_user(db_session):
    """Create admin user untuk tests."""
    from datetime import UTC, datetime
    from uuid import uuid4

    from app.models.user import User, UserRole, UserStatus

    user = User(
        id=uuid4(),
        username="admin",
        password_hash="$2b$12$mock_hash_admin123",
        nama_lengkap="Admin User",
        role=UserRole.ADMIN,
        status=UserStatus.AKTIF,
        dapat_ekspor=True,
        created_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def viewer_user(db_session):
    """Create viewer user untuk tests."""
    from datetime import UTC, datetime
    from uuid import uuid4

    from app.models.user import User, UserRole, UserStatus

    user = User(
        id=uuid4(),
        username="viewer",
        password_hash="$2b$12$mock_hash_viewer123",
        nama_lengkap="Viewer User",
        role=UserRole.VIEWER,
        status=UserStatus.AKTIF,
        dapat_ekspor=False,
        created_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_ruangan(db_session):
    """Create test ruangan."""
    from datetime import UTC, datetime
    from uuid import uuid4

    from app.models.ruangan import Ruangan

    ruangan = Ruangan(
        id=uuid4(),
        kode_ruangan="R001",
        nama_ruangan="Ruang Test",
        created_at=datetime.now(UTC),
    )
    db_session.add(ruangan)
    await db_session.commit()
    await db_session.refresh(ruangan)
    return ruangan


@pytest_asyncio.fixture
async def test_aset(db_session, admin_user, test_ruangan):
    """Create test aset."""
    from datetime import UTC, datetime
    from uuid import uuid4

    from app.models.aset import Aset, KategoriKIB, Kondisi, StatusAset

    aset = Aset(
        id=uuid4(),
        nama_barang="Laptop Test",
        kode_barang="02.06.01.0001",
        nomor_register=1,
        kategori_kib=KategoriKIB.B,
        tahun_perolehan=2024,
        asal_usul="Pembelian",
        harga=15_000_000,
        kondisi=Kondisi.BAIK,
        status=StatusAset.AKTIF,
        ruangan_id=test_ruangan.id,
        created_by=admin_user.id,
        created_at=datetime.now(UTC),
    )
    db_session.add(aset)
    await db_session.commit()
    await db_session.refresh(aset)
    return aset


@pytest_asyncio.fixture
async def admin_client(client: AsyncClient, admin_user: User) -> AsyncClient:
    """Get authenticated admin client with session cookie.
    
    Returns AsyncClient with session cookie set after successful login.
    """
    # Login as admin
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "admin123",
        },
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    
    # Session cookie is automatically set by TestClient
    return client


@pytest_asyncio.fixture
async def viewer_client(client: AsyncClient, viewer_user: User) -> AsyncClient:
    """Get authenticated viewer client with session cookie.
    
    Returns AsyncClient with session cookie set after successful login.
    """
    # Login as viewer
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "viewer",
            "password": "viewer123",
        },
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    
    # Session cookie is automatically set by TestClient
    return client


@pytest_asyncio.fixture
async def kepala_sekolah_client(db_session: AsyncSession, client: AsyncClient) -> AsyncClient:
    """Get authenticated kepala sekolah client (Viewer + dapat_ekspor).
    
    Returns AsyncClient with session cookie set after successful login.
    """
    from datetime import UTC, datetime
    from uuid import uuid4

    from app.models.user import User, UserRole, UserStatus

    # Create kepala sekolah user
    user = User(
        id=uuid4(),
        username="kepala_sekolah",
        password_hash="$2b$12$mock_hash_kepsek123",
        nama_lengkap="Kepala Sekolah",
        role=UserRole.VIEWER,
        status=UserStatus.AKTIF,
        dapat_ekspor=True,  # Key difference: can export
        created_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Login as kepala sekolah
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "kepala_sekolah",
            "password": "kepsek123",
        },
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    
    # Session cookie is automatically set by TestClient
    return client


# Backward compatibility: Keep token fixtures for gradual migration
@pytest_asyncio.fixture
async def admin_token(admin_client: AsyncClient) -> str:
    """Deprecated: Use admin_client fixture instead.
    
    Returns dummy token for backward compatibility.
    Tests should migrate to using admin_client directly.
    """
    return "session_based_auth_use_client_fixture"


@pytest_asyncio.fixture
async def viewer_token(viewer_client: AsyncClient) -> str:
    """Deprecated: Use viewer_client fixture instead.
    
    Returns dummy token for backward compatibility.
    Tests should migrate to using viewer_client directly.
    """
    return "session_based_auth_use_client_fixture"


@pytest_asyncio.fixture
async def kepala_sekolah_token(kepala_sekolah_client: AsyncClient) -> str:
    """Deprecated: Use kepala_sekolah_client fixture instead.
    
    Returns dummy token for backward compatibility.
    Tests should migrate to using kepala_sekolah_client directly.
    """
    return "session_based_auth_use_client_fixture"
