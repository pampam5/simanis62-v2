"""Unit tests untuk AuthService.

Tests untuk:
- Login dengan credential validation
- Logout dan session destruction
- Session verification
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.core.exceptions import (
    InvalidCredentialsError,
    SessionExpiredError,
    UserNotFoundError,
)
from app.models.user import User, UserRole, UserStatus
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService


class TestAuthServiceLogin:
    """Tests untuk login functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = AuthService(self.mock_session)

    @pytest.mark.asyncio
    async def test_login_success(self):
        """Test login dengan credentials valid."""
        user = User(
            id=uuid4(),
            username="admin",
            password_hash="$2b$12$hashed_password",
            nama_lengkap="Admin User",
            role=UserRole.ADMIN,
            status=UserStatus.AKTIF,
            dapat_ekspor=True,
            created_at=datetime.now(UTC),
        )

        self.service.repository.get_by_username = AsyncMock(return_value=user)

        with patch("app.services.auth_service.verify_password", return_value=True):
            with patch(
                "app.services.auth_service.create_session",
                return_value="test_session_token",
            ):
                request = LoginRequest(username="admin", password="password123")
                result = await self.service.login(request)

                assert result.user.username == "admin"
                assert result.session.session_id == "test_session_token"
                assert result.message == "Login berhasil"

    @pytest.mark.asyncio
    async def test_login_user_not_found(self):
        """Test login dengan username tidak ditemukan."""
        self.service.repository.get_by_username = AsyncMock(return_value=None)

        request = LoginRequest(username="unknown", password="password123")

        with pytest.raises(InvalidCredentialsError):
            await self.service.login(request)

    @pytest.mark.asyncio
    async def test_login_user_inactive(self):
        """Test login dengan user inactive."""
        user = User(
            id=uuid4(),
            username="inactive",
            password_hash="$2b$12$hashed_password",
            nama_lengkap="Inactive User",
            role=UserRole.VIEWER,
            status=UserStatus.NONAKTIF,
            created_at=datetime.now(UTC),
        )

        self.service.repository.get_by_username = AsyncMock(return_value=user)

        request = LoginRequest(username="inactive", password="password123")

        with pytest.raises(InvalidCredentialsError):
            await self.service.login(request)

    @pytest.mark.asyncio
    async def test_login_wrong_password(self):
        """Test login dengan password salah."""
        user = User(
            id=uuid4(),
            username="admin",
            password_hash="$2b$12$hashed_password",
            nama_lengkap="Admin User",
            role=UserRole.ADMIN,
            status=UserStatus.AKTIF,
            created_at=datetime.now(UTC),
        )

        self.service.repository.get_by_username = AsyncMock(return_value=user)

        with patch("app.services.auth_service.verify_password", return_value=False):
            request = LoginRequest(username="admin", password="wrong_password")

            with pytest.raises(InvalidCredentialsError):
                await self.service.login(request)


class TestAuthServiceLogout:
    """Tests untuk logout functionality."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = AuthService(self.mock_session)

    @pytest.mark.asyncio
    async def test_logout_success(self):
        """Test logout dengan session valid."""
        with patch("app.services.auth_service.verify_session", return_value="user_id"):
            with patch("app.services.auth_service.destroy_session", return_value=True):
                result = await self.service.logout("valid_session_token")
                assert result is True

    @pytest.mark.asyncio
    async def test_logout_invalid_session(self):
        """Test logout dengan session invalid."""
        with patch("app.services.auth_service.verify_session", return_value=None):
            with patch("app.services.auth_service.destroy_session", return_value=False):
                result = await self.service.logout("invalid_session_token")
                assert result is False


class TestAuthServiceSession:
    """Tests untuk session verification."""

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_session = AsyncMock()
        self.service = AuthService(self.mock_session)

    @pytest.mark.asyncio
    async def test_get_current_user_success(self):
        """Test get current user dengan session valid."""
        user_id = str(uuid4())
        user = User(
            id=user_id,
            username="admin",
            password_hash="$2b$12$hashed_password",
            nama_lengkap="Admin User",
            role=UserRole.ADMIN,
            status=UserStatus.AKTIF,
            created_at=datetime.now(UTC),
        )

        self.service.repository.get_by_id = AsyncMock(return_value=user)

        with patch("app.services.auth_service.verify_session", return_value=user_id):
            result = await self.service.get_current_user("valid_session_token")
            assert result.username == "admin"

    @pytest.mark.asyncio
    async def test_get_current_user_expired_session(self):
        """Test get current user dengan session expired."""
        with patch("app.services.auth_service.verify_session", return_value=None):
            with pytest.raises(SessionExpiredError):
                await self.service.get_current_user("expired_session_token")

    @pytest.mark.asyncio
    async def test_get_current_user_not_found(self):
        """Test get current user - user tidak ditemukan."""
        user_id = str(uuid4())
        self.service.repository.get_by_id = AsyncMock(return_value=None)

        with patch("app.services.auth_service.verify_session", return_value=user_id):
            with pytest.raises(UserNotFoundError):
                await self.service.get_current_user("valid_session_token")

    @pytest.mark.asyncio
    async def test_get_current_user_inactive(self):
        """Test get current user - user inactive."""
        user_id = str(uuid4())
        user = User(
            id=user_id,
            username="inactive",
            password_hash="$2b$12$hashed_password",
            nama_lengkap="Inactive User",
            role=UserRole.VIEWER,
            status=UserStatus.NONAKTIF,
            created_at=datetime.now(UTC),
        )

        self.service.repository.get_by_id = AsyncMock(return_value=user)

        with patch("app.services.auth_service.verify_session", return_value=user_id):
            with pytest.raises(SessionExpiredError):
                await self.service.get_current_user("valid_session_token")

    @pytest.mark.asyncio
    async def test_verify_session_token_valid(self):
        """Test verify session token - valid."""
        user_id = str(uuid4())

        with patch("app.services.auth_service.verify_session", return_value=user_id):
            result = await self.service.verify_session_token("valid_token")
            assert result == user_id

    @pytest.mark.asyncio
    async def test_verify_session_token_invalid(self):
        """Test verify session token - invalid."""
        with patch("app.services.auth_service.verify_session", return_value=None):
            result = await self.service.verify_session_token("invalid_token")
            assert result is None
