"""Integration tests untuk Mutasi API endpoints.

Tests untuk:
- POST /api/v1/mutasi (initiate)
- GET /api/v1/mutasi (list)
- GET /api/v1/mutasi/{id}
- PUT /api/v1/mutasi/{id}/complete
- PUT /api/v1/mutasi/{id}/cancel
"""

from uuid import uuid4

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_mutasi_requires_auth(client: AsyncClient):
    """Test list mutasi requires authentication."""
    response = await client.get("/api/v1/mutasi")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_mutasi_by_id_requires_auth(client: AsyncClient):
    """Test get mutasi by ID requires authentication."""
    mutasi_id = str(uuid4())
    response = await client.get(f"/api/v1/mutasi/{mutasi_id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_mutasi_requires_auth(client: AsyncClient):
    """Test create mutasi requires authentication."""
    response = await client.post(
        "/api/v1/mutasi",
        json={
            "aset_id": str(uuid4()),
            "ruangan_tujuan_id": str(uuid4()),
            "tanggal_mutasi": "2024-01-15",
            "alasan": "Pemindahan untuk keperluan operasional",
            "kondisi_saat_mutasi": "Baik",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_complete_mutasi_requires_auth(client: AsyncClient):
    """Test complete mutasi requires authentication."""
    mutasi_id = str(uuid4())
    response = await client.put(f"/api/v1/mutasi/{mutasi_id}/complete")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_cancel_mutasi_requires_auth(client: AsyncClient):
    """Test cancel mutasi requires authentication."""
    mutasi_id = str(uuid4())
    response = await client.put(
        f"/api/v1/mutasi/{mutasi_id}/cancel",
        json={"alasan_pembatalan": "Pembatalan karena perubahan keputusan"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_mutasi_endpoint_exists(client: AsyncClient):
    """Test mutasi endpoint exists (returns 401, not 404)."""
    response = await client.get("/api/v1/mutasi")
    # Should return 401 (unauthorized) not 404 (not found)
    assert response.status_code == 401
