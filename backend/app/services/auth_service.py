"""Authentication service untuk SIMANIS62 V2.

Module ini menyediakan AuthService untuk:
- Login dengan credential validation
- Logout dan session destruction
- Session verification
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_session, destroy_session, validate_session
from app.core.exceptions import (
    InvalidCredentialsError,
    SessionExpiredError,
    UserNotFoundError,
)
from app.core.security import verify_password
from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.services.base import BaseService


class AuthService(BaseService[User, UserRepository]):
    """Service untuk authentication dan session management.

    Menyediakan:
    - login: Validasi credentials dan create session
    - logout: Destroy session
    - verify_session: Verify session token dan return user
    - get_current_user: Get user dari session token

    Example:
        ```python
        service = AuthService(session)
        response = await service.login(LoginRequest(username="admin", password="pass"))
        user = await service.get_current_user(session_token)
        await service.logout(session_token)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize AuthService.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(session, UserRepository(session), "AuthService")

    async def login(self, request: LoginRequest) -> LoginResponse:
        """Login user dengan credential validation.

        Args:
            request: LoginRequest dengan username dan password.

        Returns:
            LoginResponse dengan user data dan session info.

        Raises:
            InvalidCredentialsError: Jika username/password salah.
        """
        self.log_info(f"Login attempt for user: {request.username}")

        # Get user by username
        user = await self.repository.get_by_username(request.username)

        if not user:
            self.log_warning(f"Login failed: user not found - {request.username}")
            raise InvalidCredentialsError()

        # Check user status
        if user.status != UserStatus.AKTIF:
            self.log_warning(f"Login failed: user inactive - {request.username}")
            raise InvalidCredentialsError()

        # Verify password
        if not verify_password(request.password, user.password_hash):
            self.log_warning(f"Login failed: invalid password - {request.username}")
            raise InvalidCredentialsError()

        # Create session
        session_token = create_session(str(user.id))

        # Update updated_at as last login indicator
        user.updated_at = datetime.now(UTC)
        await self.session.flush()

        self.log_info(f"Login successful: {request.username}")

        # Build response
        user_response = UserResponse(
            id=str(user.id),
            username=user.username,
            nama_lengkap=user.nama_lengkap,
            role=user.role,
            status=user.status,
            dapat_ekspor=user.dapat_ekspor,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        session_info = SessionInfo(
            session_id=session_token,
            user_id=str(user.id),
            expires_at=datetime.now(UTC),  # Will be set by security module
        )

        return LoginResponse(
            user=user_response,
            session=session_info,
            message="Login berhasil",
        )

    async def logout(self, session_token: str) -> bool:
        """Logout user dan destroy session.

        Args:
            session_token: Session token dari cookie.

        Returns:
            True jika logout berhasil.
        """
        user_id = verify_session(session_token)
        if user_id:
            self.log_info(f"Logout: user_id={user_id}")

        destroyed = destroy_session(session_token)

        if destroyed:
            self.log_info("Session destroyed successfully")
        else:
            self.log_warning("Session not found for logout")

        return destroyed

    async def get_current_user(self, session_token: str) -> User:
        """Get current user dari session token.

        Args:
            session_token: Session token dari cookie.

        Returns:
            User object jika session valid.

        Raises:
            SessionExpiredError: Jika session invalid atau expired.
            UserNotFoundError: Jika user tidak ditemukan.
        """
        user_id_str = verify_session(session_token)

        if not user_id_str:
            raise SessionExpiredError()

        # Convert string user_id to UUID
        import uuid
        try:
            user_id = uuid.UUID(user_id_str)
        except (ValueError, AttributeError):
            self.log_error(f"Invalid UUID format in session: {user_id_str}")
            raise SessionExpiredError()

        user = await self.repository.get_by_id(user_id)

        if not user:
            self.log_error(f"User not found for valid session: {user_id_str}")
            raise UserNotFoundError(user_id_str)

        if user.status != UserStatus.AKTIF:
            self.log_warning(f"Inactive user tried to access: {user.username}")
            raise SessionExpiredError()

        return user

    async def verify_session_token(self, session_token: str) -> str | None:
        """Verify session token dan return user_id.

        Args:
            session_token: Session token dari cookie.

        Returns:
            User ID jika session valid, None jika tidak.
        """
        return verify_session(session_token)
