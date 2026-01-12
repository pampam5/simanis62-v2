"""Integration tests untuk Auth API endpoints.

Tests untuk:
- POST /api/v1/auth/login
- POST /api/v1/auth/logout
- GET /api/v1/auth/me

PENTING: Auth API menggunakan JSON body (bukan form data).
LoginRequest schema memerlukan:
- username: min 5 karakter, alphanumeric + underscore
- password: min 8 karakter
"""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.models.user import User, UserRole, UserStatus


@pytest_asyncio.fixture
async def test_user(db_session):
    """Create test user untuk auth tests.

    Password: password123 -> mock hash: $2b$12$mock_hash_password123
    Username harus >= 5 karakter untuk memenuhi LoginRequest schema.
    """
    user = User(
        id=uuid4(),  # UUID object, not string
        username="testadmin",  # 9 chars, valid
        password_hash="$2b$12$mock_hash_password123",  # mock hash for "password123"
        nama_lengkap="Test Admin",
        role=UserRole.ADMIN,
        status=UserStatus.AKTIF,
        dapat_ekspor=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    """Test login dengan credentials valid.

    API expects JSON body with LoginRequest schema.
    """
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "testadmin", "password": "password123"},  # JSON body
    )

    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["username"] == "testadmin"
    assert "session" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user):
    """Test login dengan password salah."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "testadmin",
            "password": "wrongpass123",
        },  # wrong password, 12 chars
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_user_not_found(client: AsyncClient):
    """Test login dengan username tidak ada."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "username": "nonexistent",
            "password": "password123",
        },  # 11 chars username
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_inactive_user(client: AsyncClient, db_session):
    """Test login dengan user inactive."""
    # Create inactive user with mock hash for "password123"
    user = User(
        id=uuid4(),  # UUID object, not string
        username="inactive_user",  # 13 chars, valid
        password_hash="$2b$12$mock_hash_password123",  # mock hash for "password123"
        nama_lengkap="Inactive User",
        role=UserRole.VIEWER,
        status=UserStatus.NONAKTIF,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "inactive_user", "password": "password123"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_without_session(client: AsyncClient):
    """Test logout tanpa session."""
    response = await client.post("/api/v1/auth/logout")

    # Should return 200 (logout success even without session)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_me_without_auth(client: AsyncClient):
    """Test get current user tanpa authentication."""
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_validation_error_short_username(client: AsyncClient):
    """Test login dengan username terlalu pendek (< 5 chars)."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "abc", "password": "password123"},  # 3 chars, invalid
    )

    # Should return 422 validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_validation_error_short_password(client: AsyncClient):
    """Test login dengan password terlalu pendek (< 8 chars)."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "short"},  # 5 chars, invalid
    )

    # Should return 422 validation error
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_validation_error_empty_fields(client: AsyncClient):
    """Test login dengan field kosong."""
    response = await client.post(
        "/api/v1/auth/login", json={"username": "", "password": ""}
    )

    # Should return 422 validation error
    assert response.status_code == 422
