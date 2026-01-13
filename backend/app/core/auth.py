"""
Authentication and Authorization dependencies untuk SIMANIS62 V2.

Menyediakan dependencies untuk:
- Session validation
- Role-based access control (RBAC)
- Permission checks
"""

import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_db
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)

# In-memory session store (for MVP)
# TODO: Move to database table for production
_sessions: dict[str, tuple[UUID, datetime]] = {}


async def create_session(user_id: UUID, db: AsyncSession) -> str:
    """Create new session for user.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        Session ID (token)
    """
    session_id = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=2)
    _sessions[session_id] = (user_id, expires_at)
    
    logger.info(f"Session created for user: {user_id}")
    return session_id


async def destroy_session(user_id: UUID, db: AsyncSession) -> None:
    """Destroy all sessions for user.

    Args:
        user_id: User ID
        db: Database session
    """
    # Remove all sessions for this user
    sessions_to_remove = [
        sid for sid, (uid, _) in _sessions.items() if uid == user_id
    ]
    for sid in sessions_to_remove:
        del _sessions[sid]
    
    logger.info(f"Sessions destroyed for user: {user_id}")


async def validate_session(session_id: str, extend_session: bool = True) -> UUID | None:
    """Validate session and return user ID.

    Implements sliding session expiration - session is extended on each valid request.

    Args:
        session_id: Session ID to validate
        extend_session: If True, extend session expiration (sliding expiration)

    Returns:
        User ID if session is valid, None otherwise
    """
    if session_id not in _sessions:
        logger.debug(f"Session not found: {session_id[:8]}...")
        return None
    
    user_id, expires_at = _sessions[session_id]
    
    # Check if session expired
    if datetime.now(timezone.utc) > expires_at:
        del _sessions[session_id]
        logger.info(f"Session expired for user: {user_id}")
        return None
    
    # Sliding session expiration - extend session on each valid request
    if extend_session:
        new_expires_at = datetime.now(timezone.utc) + timedelta(hours=2)
        _sessions[session_id] = (user_id, new_expires_at)
        logger.debug(f"Session extended for user: {user_id}")
    
    return user_id


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user from session.

    Implements sliding session expiration - session is automatically extended
    on each successful request to prevent unexpected session expiry.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException 401: If session is invalid or expired
    """
    # Get session cookie
    session_id = request.cookies.get("simanis62_session")
    
    if not session_id:
        logger.debug("No session cookie found in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "SESSION_NOT_FOUND",
                "message": "Session tidak ditemukan. Silakan login kembali.",
            },
        )

    # Validate session with sliding expiration (extends session on each request)
    user_id = await validate_session(session_id, extend_session=True)
    
    if not user_id:
        logger.warning(f"Invalid or expired session: {session_id[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "SESSION_EXPIRED",
                "message": "Session telah berakhir. Silakan login kembali.",
            },
        )
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or user.status != "Aktif":
        logger.warning(f"User not found or inactive: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "USER_INACTIVE",
                "message": "User tidak ditemukan atau tidak aktif.",
            },
        )

    return user


async def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require Admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if Admin

    Raises:
        HTTPException 403: If user is not Admin
    """
    if current_user.role != UserRole.ADMIN:
        logger.warning(
            f"Access denied for user {current_user.username} (role: {current_user.role})"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error_code": "FORBIDDEN",
                "message": "Akses ditolak. Hanya Admin yang diizinkan.",
            },
        )

    return current_user


async def require_export_permission(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require export permission (Admin or Viewer with dapat_ekspor=True).

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if has export permission

    Raises:
        HTTPException 403: If user doesn't have export permission
    """
    # Admin always has export permission
    if current_user.role == UserRole.ADMIN:
        return current_user

    # Viewer with dapat_ekspor flag (Kepala Sekolah)
    if current_user.role == UserRole.VIEWER and current_user.dapat_ekspor:
        return current_user

    logger.warning(
        f"Export access denied for user {current_user.username} "
        f"(role: {current_user.role}, dapat_ekspor: {current_user.dapat_ekspor})"
    )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error_code": "FORBIDDEN",
            "message": "Akses ditolak. Anda tidak memiliki izin export.",
        },
    )


# Type aliases for dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_admin)]
ExportUser = Annotated[User, Depends(require_export_permission)]
