"""
Authentication API endpoints untuk SIMANIS62 V2.

Menyediakan login, logout, dan session management.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.auth import CurrentUser, create_session, destroy_session, get_current_user
from app.core.database import get_db
from app.core.security import verify_password
from app.models.user import User, UserStatus
from app.schemas.response import SuccessResponse
from app.schemas.user import LoginRequest, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Login",
    description="Authenticate user dan create session.",
)
async def login(
    credentials: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[UserResponse]:
    """Login user dan create session.

    Args:
        credentials: Username dan password
        response: FastAPI Response untuk set cookie
        db: Database session

    Returns:
        SuccessResponse dengan data user

    Raises:
        HTTPException 401: Jika credentials invalid
    """
    # Find user by username
    result = await db.execute(
        select(User).where(User.username == credentials.username)
    )
    user = result.scalar_one_or_none()

    # Validate user exists and is active
    if not user or user.status != UserStatus.AKTIF:
        logger.warning(f"Login failed for username: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "UNAUTHORIZED",
                "message": "Username atau password salah",
            },
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        logger.warning(f"Invalid password for user: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "UNAUTHORIZED",
                "message": "Username atau password salah",
            },
        )

    # Create session and set cookie
    session_id = await create_session(user.id, db)
    response.set_cookie(
        key="simanis62_session",
        value=session_id,
        httponly=True,
        samesite="lax",
        secure=False,  # HTTP only (localhost)
        max_age=7200,  # 2 hours
    )

    logger.info(f"User logged in: {user.username} (role: {user.role})")

    return SuccessResponse(
        data=UserResponse.model_validate(user),
        message="Login berhasil",
    )


@router.post(
    "/logout",
    response_model=SuccessResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Logout",
    description="Destroy session dan clear cookie.",
)
async def logout(
    response: Response,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[dict]:
    """Logout user dan destroy session.

    Args:
        response: FastAPI Response untuk clear cookie
        current_user: Current authenticated user
        db: Database session

    Returns:
        SuccessResponse dengan message
    """
    # Destroy session
    await destroy_session(current_user.id, db)

    # Clear cookie
    response.delete_cookie(key="simanis62_session")

    logger.info(f"User logged out: {current_user.username}")

    return SuccessResponse(
        data={},
        message="Logout berhasil",
    )


@router.get(
    "/me",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get current authenticated user info.",
)
async def get_me(
    current_user: CurrentUser,
) -> SuccessResponse[UserResponse]:
    """Get current user info.

    Args:
        current_user: Current authenticated user

    Returns:
        SuccessResponse dengan data user
    """
    return SuccessResponse(
        data=UserResponse.model_validate(current_user),
    )
