"""Basic health check tests untuk Phase 1-5 verification."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_app_starts(client: AsyncClient):
    """Test that FastAPI app starts successfully."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi_schema(client: AsyncClient):
    """Test that OpenAPI schema is generated."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
    # Verify key endpoints exist
    assert "/api/v1/auth/login" in data["paths"]
    assert "/api/v1/aset" in data["paths"]
    assert "/api/v1/ruangan" in data["paths"]


@pytest.mark.asyncio
async def test_auth_login_endpoint_exists(client: AsyncClient):
    """Test auth login endpoint responds (even with invalid data)."""
    response = await client.post(
        "/api/v1/auth/login", data={"username": "test", "password": "test"}
    )
    # Should return 401 (unauthorized) not 404 (not found)
    assert response.status_code in [401, 422]


@pytest.mark.asyncio
async def test_aset_list_requires_auth(client: AsyncClient):
    """Test aset list endpoint requires authentication."""
    response = await client.get("/api/v1/aset")
    # Should return 401 (unauthorized) not 404 (not found)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_ruangan_list_requires_auth(client: AsyncClient):
    """Test ruangan list endpoint requires authentication."""
    response = await client.get("/api/v1/ruangan")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_users_list_requires_auth(client: AsyncClient):
    """Test users list endpoint requires authentication."""
    response = await client.get("/api/v1/users")
    assert response.status_code == 401
