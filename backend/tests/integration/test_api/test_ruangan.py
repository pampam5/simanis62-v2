"""Integration tests for Ruangan API endpoints."""

import pytest
from httpx import AsyncClient
from sqlmodel import Session

from app.models.user import User


@pytest.mark.asyncio
class TestRuanganAPI:
    """Test Ruangan CRUD operations via API."""

    async def test_create_ruangan_success(
        self, client: AsyncClient, admin_user: User
    ):
        """Test creating a new ruangan."""
        # Login
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create ruangan
        response = await client.post(
            "/api/v1/ruangan",
            json={
                "nama_ruangan": "Ruang Perpustakaan",
                "kode_ruangan": "PERP-01",
                "keterangan": "Perpustakaan lantai 1",
            },
        )
        
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["nama_ruangan"] == "Ruang Perpustakaan"
        assert data["kode_ruangan"] == "PERP-01"
        assert "id" in data

    async def test_create_ruangan_duplicate_kode(
        self, client: AsyncClient, admin_user: User
    ):
        """Test creating ruangan with duplicate kode_ruangan."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create first ruangan
        await client.post(
            "/api/v1/ruangan",
            json={"nama_ruangan": "Room 1", "kode_ruangan": "R-001"},
        )
        
        # Try to create duplicate
        response = await client.post(
            "/api/v1/ruangan",
            json={"nama_ruangan": "Room 2", "kode_ruangan": "R-001"},
        )
        
        assert response.status_code == 400

    async def test_list_ruangan(self, client: AsyncClient, admin_user: User):
        """Test listing all ruangan."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create multiple ruangan
        for i in range(3):
            await client.post(
                "/api/v1/ruangan",
                json={
                    "nama_ruangan": f"Ruang {i+1}",
                    "kode_ruangan": f"R-00{i+1}",
                },
            )
        
        # List ruangan
        response = await client.get("/api/v1/ruangan")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 3

    async def test_get_ruangan_by_id(self, client: AsyncClient, admin_user: User):
        """Test getting ruangan by ID."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create ruangan
        create_response = await client.post(
            "/api/v1/ruangan",
            json={"nama_ruangan": "Test Room", "kode_ruangan": "TR-01"},
        )
        ruangan_id = create_response.json()["data"]["id"]
        
        # Get by ID
        response = await client.get(f"/api/v1/ruangan/{ruangan_id}")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == ruangan_id
        assert data["nama_ruangan"] == "Test Room"

    async def test_update_ruangan(self, client: AsyncClient, admin_user: User):
        """Test updating ruangan."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create ruangan
        create_response = await client.post(
            "/api/v1/ruangan",
            json={"nama_ruangan": "Old Name", "kode_ruangan": "ON-01"},
        )
        ruangan_id = create_response.json()["data"]["id"]
        
        # Update
        response = await client.put(
            f"/api/v1/ruangan/{ruangan_id}",
            json={"nama_ruangan": "New Name", "keterangan": "Updated"},
        )
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["nama_ruangan"] == "New Name"
        assert data["keterangan"] == "Updated"

    async def test_delete_ruangan(self, client: AsyncClient, admin_user: User):
        """Test deleting ruangan."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create ruangan
        create_response = await client.post(
            "/api/v1/ruangan",
            json={"nama_ruangan": "To Delete", "kode_ruangan": "TD-01"},
        )
        ruangan_id = create_response.json()["data"]["id"]
        
        # Delete
        response = await client.delete(f"/api/v1/ruangan/{ruangan_id}")
        
        assert response.status_code == 200
        
        # Verify deleted
        get_response = await client.get(f"/api/v1/ruangan/{ruangan_id}")
        assert get_response.status_code == 404

    async def test_get_kir_report(self, client: AsyncClient, admin_user: User):
        """Test getting KIR (Kartu Inventaris Ruangan) report."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create ruangan
        create_response = await client.post(
            "/api/v1/ruangan",
            json={"nama_ruangan": "Lab", "kode_ruangan": "LAB-01"},
        )
        ruangan_id = create_response.json()["data"]["id"]
        
        # Get KIR
        response = await client.get(f"/api/v1/ruangan/{ruangan_id}/kir")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert "ruangan" in data
        assert "aset_list" in data
