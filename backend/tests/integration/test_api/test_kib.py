"""Integration tests untuk KIB API endpoints.

Tests untuk:
- GET /api/v1/kib/{kategori} (get report)
- POST /api/v1/kib/{kategori}/export (export to Excel)
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_kib_report_requires_auth(client: AsyncClient):
    """Test get KIB report requires authentication."""
    response = await client.get("/api/v1/kib/B")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_export_kib_requires_auth(client: AsyncClient):
    """Test export KIB requires authentication (POST endpoint)."""
    # Export endpoint is POST, not GET
    response = await client.post("/api/v1/kib/B/export")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_kib_endpoint_exists(client: AsyncClient):
    """Test KIB endpoint exists (returns 401, not 404)."""
    # Test all KIB categories
    for kategori in ["A", "B", "C", "D", "E", "F"]:
        response = await client.get(f"/api/v1/kib/{kategori}")
        # Should return 401 (unauthorized) not 404 (not found)
        assert response.status_code == 401, f"KIB {kategori} endpoint should exist"


@pytest.mark.asyncio
async def test_kib_export_endpoint_exists(client: AsyncClient):
    """Test KIB export endpoint exists (POST method)."""
    response = await client.post("/api/v1/kib/B/export")
    # Should return 401 (unauthorized) not 404 (not found)
    assert response.status_code == 401
