"""
Integration tests untuk Setup API endpoints.

Tests untuk First-Run Setup Wizard:
- GET /api/v1/setup/status
- POST /api/v1/setup/admin
"""

import pytest
from httpx import AsyncClient


class TestSetupStatus:
    """Tests untuk GET /api/v1/setup/status endpoint."""

    @pytest.mark.asyncio
    async def test_setup_status_needs_setup_when_no_users(self, client: AsyncClient):
        """Test setup status returns needs_setup=true when no users exist.
        
        Note: client fixture starts with empty database, so needs_setup should be true.
        """
        response = await client.get("/api/v1/setup/status")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["needs_setup"] is True
        assert "administrator" in data["data"]["message"].lower()

    @pytest.mark.asyncio
    async def test_setup_status_no_setup_when_users_exist(
        self, admin_client: AsyncClient
    ):
        """Test setup status returns needs_setup=false when users exist."""
        response = await admin_client.get("/api/v1/setup/status")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["needs_setup"] is False


class TestCreateFirstAdmin:
    """Tests untuk POST /api/v1/setup/admin endpoint."""

    @pytest.mark.asyncio
    async def test_create_admin_success_when_no_users(self, client: AsyncClient):
        """Test create admin succeeds when no users exist.
        
        Note: client fixture starts with empty database.
        """
        response = await client.post(
            "/api/v1/setup/admin",
            json={
                "username": "newadmin",
                "password": "password123",
                "nama_lengkap": "New Administrator",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["username"] == "newadmin"
        assert data["data"]["nama_lengkap"] == "New Administrator"
        assert data["data"]["role"] == "Admin"
        assert data["data"]["status"] == "Aktif"
        assert data["data"]["dapat_ekspor"] is True
        assert "berhasil" in data["message"].lower()

    @pytest.mark.asyncio
    async def test_create_admin_fails_when_users_exist(
        self, admin_client: AsyncClient
    ):
        """Test create admin fails when users already exist."""
        response = await admin_client.post(
            "/api/v1/setup/admin",
            json={
                "username": "anotheradmin",
                "password": "password123",
                "nama_lengkap": "Another Admin",
            },
        )

        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error_code"] == "SETUP_ALREADY_DONE"

    @pytest.mark.asyncio
    async def test_create_admin_validates_username_length(self, client: AsyncClient):
        """Test create admin validates username minimum length."""
        response = await client.post(
            "/api/v1/setup/admin",
            json={
                "username": "ab",  # Too short (min 5)
                "password": "password123",
                "nama_lengkap": "Test Admin",
            },
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_admin_validates_password_length(self, client: AsyncClient):
        """Test create admin validates password minimum length."""
        response = await client.post(
            "/api/v1/setup/admin",
            json={
                "username": "testadmin",
                "password": "short",  # Too short (min 8)
                "nama_lengkap": "Test Admin",
            },
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_create_admin_validates_username_format(self, client: AsyncClient):
        """Test create admin validates username format (alphanumeric + underscore)."""
        response = await client.post(
            "/api/v1/setup/admin",
            json={
                "username": "admin@test",  # Invalid character
                "password": "password123",
                "nama_lengkap": "Test Admin",
            },
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_created_admin_can_login(self, client: AsyncClient):
        """Test that created admin can successfully login."""
        # Create admin first
        create_response = await client.post(
            "/api/v1/setup/admin",
            json={
                "username": "logintest",
                "password": "logintest123",
                "nama_lengkap": "Login Test Admin",
            },
        )
        assert create_response.status_code == 201

        # Try to login - note: password is mocked in tests
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "logintest",
                "password": "logintest123",
            },
        )

        assert login_response.status_code == 200
        data = login_response.json()
        assert data["success"] is True
        assert data["data"]["username"] == "logintest"
