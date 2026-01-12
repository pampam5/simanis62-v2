"""
API Dependencies untuk SIMANIS62 V2.

Menyediakan dependency injection untuk:
- Database session
- Current user authentication
- Role-based authorization
- Service instances
"""

from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_session
from app.models.user import User, UserRole, UserStatus
from app.repositories.user_repository import UserRepository
from app.services.aset_service import AsetService
from app.services.auth_service import AuthService
from app.services.kib_service import KibService
from app.services.mutasi_service import MutasiService
from app.services.ruangan_service import RuanganService
from app.services.user_service import UserService

# Type alias untuk database session dependency
DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    db: DbSession,
    session_token: str | None = Cookie(None, alias="simanis62_session"),
) -> User:
    """Get current authenticated user dari session cookie.

    Args:
        db: Database session
        session_token: Session token dari cookie

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: 401 jika tidak ada session atau session invalid
    """
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tidak ada session. Silakan login terlebih dahulu.",
            headers={"WWW-Authenticate": "Cookie"},
        )

    user_id = verify_session(session_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session tidak valid atau sudah expired. Silakan login kembali.",
            headers={"WWW-Authenticate": "Cookie"},
        )

    # Get user from database
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User tidak ditemukan.",
            headers={"WWW-Authenticate": "Cookie"},
        )

    if user.status != UserStatus.AKTIF:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Akun tidak aktif. Hubungi administrator.",
            headers={"WWW-Authenticate": "Cookie"},
        )

    return user


# Type alias untuk current user dependency
CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_admin(current_user: CurrentUser) -> User:
    """Require current user to be Admin.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current user jika Admin

    Raises:
        HTTPException: 403 jika bukan Admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses ditolak. Hanya Admin yang diizinkan.",
        )
    return current_user


# Type alias untuk admin user dependency
AdminUser = Annotated[User, Depends(require_admin)]


async def require_export_permission(current_user: CurrentUser) -> User:
    """Require current user to have export permission.

    Admin atau Viewer dengan dapat_ekspor=True (Kepala Sekolah).

    Args:
        current_user: Current authenticated user

    Returns:
        User: Current user jika punya izin export

    Raises:
        HTTPException: 403 jika tidak punya izin export
    """
    if current_user.role == UserRole.ADMIN:
        return current_user

    if current_user.role == UserRole.VIEWER and current_user.dapat_ekspor:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Akses ditolak. Anda tidak memiliki izin export.",
    )


# Type alias untuk export permission dependency
ExportUser = Annotated[User, Depends(require_export_permission)]


# === Service Dependencies ===


def get_auth_service(db: DbSession) -> AuthService:
    """Get AuthService instance.

    Args:
        db: Database session

    Returns:
        AuthService: Service instance
    """
    return AuthService(db)


def get_aset_service(db: DbSession) -> AsetService:
    """Get AsetService instance.

    Args:
        db: Database session

    Returns:
        AsetService: Service instance
    """
    return AsetService(db)


def get_mutasi_service(db: DbSession) -> MutasiService:
    """Get MutasiService instance.

    Args:
        db: Database session

    Returns:
        MutasiService: Service instance
    """
    return MutasiService(db)


def get_kib_service(db: DbSession) -> KibService:
    """Get KibService instance.

    Args:
        db: Database session

    Returns:
        KibService: Service instance
    """
    return KibService(db)


def get_ruangan_service(db: DbSession) -> RuanganService:
    """Get RuanganService instance.

    Args:
        db: Database session

    Returns:
        RuanganService: Service instance
    """
    return RuanganService(db)


def get_user_service(db: DbSession) -> UserService:
    """Get UserService instance.

    Args:
        db: Database session

    Returns:
        UserService: Service instance
    """
    return UserService(db)


# Type aliases untuk service dependencies
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
AsetServiceDep = Annotated[AsetService, Depends(get_aset_service)]
MutasiServiceDep = Annotated[MutasiService, Depends(get_mutasi_service)]
KibServiceDep = Annotated[KibService, Depends(get_kib_service)]
RuanganServiceDep = Annotated[RuanganService, Depends(get_ruangan_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
