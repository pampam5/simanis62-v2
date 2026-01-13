"""Integration tests for User Management API endpoints."""

import pytest
from httpx import AsyncClient
from sqlmodel import Session

from app.models.user import User, UserRole


@pytest.mark.asyncio
class TestUserManagementAPI:
    """Test User CRUD operations via API."""

    async def test_create_user_as_admin(
        self, client: AsyncClient, admin_user: User
    ):
        """Test admin can create new users."""
        # Login as admin
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create user
        response = await client.post(
            "/api/v1/users",
            json={
                "username": "newuser01",
                "password": "password123",
                "nama_lengkap": "New User",
                "role": "Viewer",
                "dapat_ekspor": False,
            },
        )
        
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["username"] == "newuser01"
        assert data["role"] == "Viewer"
        assert data["dapat_ekspor"] is False
        assert "password" not in data  # Password should not be returned

    async def test_create_user_duplicate_username(
        self, client: AsyncClient, admin_user: User
    ):
        """Test creating user with duplicate username fails."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create first user
        await client.post(
            "/api/v1/users",
            json={
                "username": "duplicate",
                "password": "pass123456",
                "nama_lengkap": "User 1",
                "role": "Viewer",
            },
        )
        
        # Try to create duplicate
        response = await client.post(
            "/api/v1/users",
            json={
                "username": "duplicate",
                "password": "pass123456",
                "nama_lengkap": "User 2",
                "role": "Viewer",
            },
        )
        
        assert response.status_code == 400

    async def test_list_users(self, client: AsyncClient, admin_user: User):
        """Test listing all users."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create multiple users
        for i in range(3):
            await client.post(
                "/api/v1/users",
                json={
                    "username": f"user{i}",
                    "password": "pass123456",
                    "nama_lengkap": f"User {i}",
                    "role": "Viewer",
                },
            )
        
        # List users
        response = await client.get("/api/v1/users")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 4  # admin + 3 new users

    async def test_get_user_by_id(self, client: AsyncClient, admin_user: User):
        """Test getting user by ID."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create user
        create_response = await client.post(
            "/api/v1/users",
            json={
                "username": "testuser",
                "password": "pass123456",
                "nama_lengkap": "Test User",
                "role": "Viewer",
            },
        )
        user_id = create_response.json()["data"]["id"]
        
        # Get by ID
        response = await client.get(f"/api/v1/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == user_id
        assert data["username"] == "testuser"

    async def test_update_user(self, client: AsyncClient, admin_user: User):
        """Test updating user details."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create user
        create_response = await client.post(
            "/api/v1/users",
            json={
                "username": "updateme",
                "password": "pass123456",
                "nama_lengkap": "Old Name",
                "role": "Viewer",
            },
        )
        user_id = create_response.json()["data"]["id"]
        
        # Update
        response = await client.put(
            f"/api/v1/users/{user_id}",
            json={"nama_lengkap": "New Name", "dapat_ekspor": True},
        )
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["nama_lengkap"] == "New Name"
        assert data["dapat_ekspor"] is True

    async def test_deactivate_user(self, client: AsyncClient, admin_user: User):
        """Test deactivating a user."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create user
        create_response = await client.post(
            "/api/v1/users",
            json={
                "username": "deactivateme",
                "password": "pass123456",
                "nama_lengkap": "To Deactivate",
                "role": "Viewer",
            },
        )
        user_id = create_response.json()["data"]["id"]
        
        # Deactivate
        response = await client.put(f"/api/v1/users/{user_id}/deactivate")
        
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "Nonaktif"

    async def test_viewer_cannot_create_user(
        self, client: AsyncClient, db_session: Session
    ):
        """Test viewer role cannot create users."""
        # Create viewer user
        viewer = User(
            username="viewer_test",
            password_hash="$2b$12$dummy",
            nama_lengkap="Viewer",
            role=UserRole.VIEWER,
            dapat_ekspor=False,
        )
        db_session.add(viewer)
        await db_session.commit()
        
        # Login as viewer
        await client.post(
            "/api/v1/auth/login",
            json={"username": "viewer_test", "password": "viewer123"},
        )
        
        # Try to create user
        response = await client.post(
            "/api/v1/users",
            json={
                "username": "newuser",
                "password": "pass123456",
                "nama_lengkap": "New",
                "role": "Viewer",
            },
        )
        
        assert response.status_code == 403  # Forbidden

    async def test_create_kepala_sekolah_user(
        self, client: AsyncClient, admin_user: User
    ):
        """Test creating Kepala Sekolah (Viewer with dapat_ekspor=True)."""
        await client.post(
            "/api/v1/auth/login",
            json={"username": admin_user.username, "password": "admin123"},
        )
        
        # Create kepala sekolah
        response = await client.post(
            "/api/v1/users",
            json={
                "username": "kepsek",
                "password": "kepsek123456",
                "nama_lengkap": "Dr. Kepala Sekolah",
                "role": "Viewer",
                "dapat_ekspor": True,  # Key difference
            },
        )
        
        assert response.status_code == 201
        data = response.json()["data"]
        assert data["role"] == "Viewer"
        assert data["dapat_ekspor"] is True
