"""Integration tests untuk Aset API endpoints.

Tests untuk:
- GET /api/v1/aset (search)
- GET /api/v1/aset/{id}
- POST /api/v1/aset (create)
- PUT /api/v1/aset/{id} (update)
- DELETE /api/v1/aset/{id} (soft delete)
"""

import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.asyncio
async def test_list_aset_requires_auth(client: AsyncClient):
    """Test list aset requires authentication."""
    response = await client.get("/api/v1/aset")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_aset_by_id_requires_auth(client: AsyncClient, test_aset):
    """Test get aset by ID requires authentication."""
    response = await client.get(f"/api/v1/aset/{test_aset.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_aset_requires_auth(client: AsyncClient):
    """Test create aset requires authentication."""
    response = await client.post(
        "/api/v1/aset",
        json={
            "nama_barang": "New Laptop",
            "kode_barang": "02.06.01.0002",
            "kategori_kib": "B",
            "tahun_perolehan": 2024,
            "asal_usul": "Pembelian",
            "harga": 10000000,
            "kondisi": "Baik",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_aset_requires_auth(client: AsyncClient, test_aset):
    """Test update aset requires authentication."""
    response = await client.put(
        f"/api/v1/aset/{test_aset.id}", json={"nama_barang": "Updated Laptop"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_aset_requires_auth(client: AsyncClient, test_aset):
    """Test delete aset requires authentication."""
    # DELETE with body needs to use request method
    response = await client.request(
        "DELETE",
        f"/api/v1/aset/{test_aset.id}",
        json={"alasan_penghapusan": "Aset rusak berat dan tidak dapat diperbaiki"},
    )
    assert response.status_code == 401


# Note: Full authenticated tests would require session management
# which is complex to test in integration tests.
# The tests above verify that endpoints exist and require auth.
