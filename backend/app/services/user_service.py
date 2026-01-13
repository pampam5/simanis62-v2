"""User service untuk SIMANIS62 V2.

Module ini menyediakan UserService untuk:
- CRUD operations untuk user
- Password hashing
- User management validations
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CannotChangeOwnRoleError,
    CannotDeleteSelfError,
    DuplicateUsernameError,
    InvalidPasswordError,
    UserNotFoundError,
)
from app.core.security import hash_password, revoke_all_user_sessions
from app.models.user import User, UserRole, UserStatus
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserResponse
from app.schemas.response import PaginatedResponse
from app.schemas.user import (
    UserCreate,
    UserDeactivateRequest,
    UserSearchParams,
    UserUpdate,
)
from app.services.base import BaseService

# Constants
MIN_PASSWORD_LENGTH = 8


class UserService(BaseService[User, UserRepository]):
    """Service untuk user management.

    Menyediakan:
    - create_user: Buat user baru dengan password hashing
    - update_user: Update user
    - deactivate_user: Nonaktifkan user
    - get_user_by_id: Get user by ID
    - search_users: Search users dengan filters

    Example:
        ```python
        service = UserService(session)
        user = await service.create_user(data, admin_id)
        await service.deactivate_user(user_id, admin_id)
        ```
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize UserService.

        Args:
            session: AsyncSession untuk database operations.
        """
        super().__init__(session, UserRepository(session), "UserService")

    # =========================================================================
    # Validation Methods
    # =========================================================================

    def _validate_password(self, password: str) -> None:
        """Validate password minimal 8 karakter.

        Args:
            password: Password yang akan divalidasi.

        Raises:
            InvalidPasswordError: Jika password tidak valid.
        """
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidPasswordError()

    async def _validate_username_unique(
        self, username: str, exclude_id: str | None = None
    ) -> None:
        """Validate username unik.

        Args:
            username: Username yang akan dicek.
            exclude_id: ID user yang dikecualikan (untuk update).

        Raises:
            DuplicateUsernameError: Jika username sudah ada.
        """
        existing = await self.repository.get_by_username(username)
        if existing and (exclude_id is None or str(existing.id) != exclude_id):
            raise DuplicateUsernameError(username)

    def _validate_not_self(self, user_id: str, current_user_id: str) -> None:
        """Validate user tidak menghapus diri sendiri.

        Args:
            user_id: ID user yang akan dioperasikan.
            current_user_id: ID user yang sedang login.

        Raises:
            CannotDeleteSelfError: Jika mencoba menghapus diri sendiri.
        """
        if user_id == current_user_id:
            raise CannotDeleteSelfError()

    def _validate_not_changing_own_role(
        self, user_id: str, current_user_id: str, new_role: UserRole | None
    ) -> None:
        """Validate user tidak mengubah role sendiri.

        Args:
            user_id: ID user yang akan diupdate.
            current_user_id: ID user yang sedang login.
            new_role: Role baru (jika ada).

        Raises:
            CannotChangeOwnRoleError: Jika mencoba mengubah role sendiri.
        """
        if user_id == current_user_id and new_role is not None:
            raise CannotChangeOwnRoleError()

    # =========================================================================
    # CRUD Operations
    # =========================================================================

    async def create_user(self, data: UserCreate, created_by: str) -> User:
        """Buat user baru dengan password hashing.

        Args:
            data: UserCreate schema dengan data user.
            created_by: UUID user yang membuat.

        Returns:
            User yang baru dibuat.

        Raises:
            DuplicateUsernameError: Jika username sudah ada.
            InvalidPasswordError: Jika password tidak valid.
        """
        self.log_info(f"Creating user: {data.username}")

        # Validations
        await self._validate_username_unique(data.username)
        self._validate_password(data.password)

        # Hash password
        password_hash = hash_password(data.password)

        # Create user
        user = User(
            username=data.username.lower(),
            password_hash=password_hash,
            nama_lengkap=data.nama_lengkap,
            role=data.role,
            dapat_ekspor=data.dapat_ekspor,
            status=UserStatus.AKTIF,
        )

        created = await self.repository.create(user)
        await self.commit()

        self.log_info(f"User created: id={created.id}, username={created.username}")
        return created

    async def update_user(
        self, user_id: str, data: UserUpdate, updated_by: str
    ) -> User:
        """Update user.

        Args:
            user_id: UUID user yang akan diupdate.
            data: UserUpdate schema dengan data update.
            updated_by: UUID user yang mengupdate.

        Returns:
            User yang diupdate.

        Raises:
            UserNotFoundError: Jika user tidak ditemukan.
            CannotChangeOwnRoleError: Jika mencoba mengubah role sendiri.
        """
        self.log_info(f"Updating user: {user_id}")

        # Get existing user
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        # Validate not changing own role
        self._validate_not_changing_own_role(user_id, updated_by, data.role)

        # Build update dict
        update_data = data.model_dump(exclude_unset=True)

        # Hash password if provided
        if update_data.get("password"):
            self._validate_password(update_data["password"])
            update_data["password_hash"] = hash_password(update_data["password"])
            del update_data["password"]

        update_data["updated_at"] = datetime.now(UTC)

        updated = await self.repository.update(user_id, update_data)
        if not updated:
            raise UserNotFoundError(user_id)
        await self.commit()

        self.log_info(f"User updated: id={user_id}")
        return updated

    async def deactivate_user(
        self, user_id: str, request: UserDeactivateRequest | None, deactivated_by: str
    ) -> User:
        """Nonaktifkan user.

        Args:
            user_id: UUID user yang akan dinonaktifkan.
            request: UserDeactivateRequest dengan alasan (optional).
            deactivated_by: UUID user yang menonaktifkan.

        Returns:
            User yang dinonaktifkan.

        Raises:
            UserNotFoundError: Jika user tidak ditemukan.
            CannotDeleteSelfError: Jika mencoba menonaktifkan diri sendiri.
        """
        self.log_info(f"Deactivating user: {user_id}")

        # Validate not self
        self._validate_not_self(user_id, deactivated_by)

        # Get existing user
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        # Deactivate
        update_data = {
            "status": UserStatus.NONAKTIF,
            "updated_at": datetime.now(UTC),
        }

        updated = await self.repository.update(user_id, update_data)
        if not updated:
            raise UserNotFoundError(user_id)

        # Revoke all sessions
        revoke_all_user_sessions(user_id)

        await self.commit()

        self.log_info(f"User deactivated: id={user_id}")
        return updated

    async def get_user_by_id(self, user_id: str) -> User:
        """Get user by ID.

        Args:
            user_id: UUID user.

        Returns:
            User jika ditemukan.

        Raises:
            UserNotFoundError: Jika user tidak ditemukan.
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    # =========================================================================
    # Search Operations
    # =========================================================================

    async def search_users(
        self, params: UserSearchParams
    ) -> PaginatedResponse[UserResponse]:
        """Search users dengan filters.

        Args:
            params: UserSearchParams dengan filter criteria.

        Returns:
            PaginatedResponse dengan list UserResponse.
        """
        self.log_debug(f"Searching users: keyword={params.keyword}")

        # Calculate pagination
        skip = (params.page - 1) * params.page_size
        limit = params.page_size

        # Build filters
        filters: dict[str, UserRole | UserStatus | bool] = {}
        if params.role:
            filters["role"] = params.role
        if params.status:
            filters["status"] = params.status
        if params.dapat_ekspor is not None:
            filters["dapat_ekspor"] = params.dapat_ekspor

        # Get users
        users = await self.repository.get_all(skip=skip, limit=limit, filters=filters)

        # Count total
        total = await self.repository.count(filters=filters)

        # Convert to response
        items = [self._to_response(u) for u in users]

        return PaginatedResponse(
            data=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=(total + params.page_size - 1) // params.page_size,
        )

    async def get_active_users(self) -> list[User]:
        """Get semua active users.

        Returns:
            List of active users.
        """
        return await self.repository.get_active_users()

    def _to_response(self, user: User) -> UserResponse:
        """Convert User model to UserResponse schema.

        Args:
            user: User model instance.

        Returns:
            UserResponse schema.
        """
        return UserResponse(
            id=str(user.id),
            username=user.username,
            nama_lengkap=user.nama_lengkap,
            role=user.role,
            status=user.status,
            dapat_ekspor=user.dapat_ekspor,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
