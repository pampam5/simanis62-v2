"""
Auth API Endpoints untuk SIMANIS62 V2.

Endpoints:
- POST /api/v1/auth/login - Login user
- POST /api/v1/auth/logout - Logout user
- GET /api/v1/auth/me - Get current user info
"""

import logging

from fastapi import APIRouter, Cookie, Response, status

from app.api.deps import AuthServiceDep, CurrentUser
from app.core.config import settings
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse
from app.schemas.response import SuccessResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user dengan username dan password, return session cookie.",
)
async def login(
    request: LoginRequest,
    response: Response,
    auth_service: AuthServiceDep,
) -> LoginResponse:
    """Login user dan set session cookie.

    Args:
        request: Login credentials (username, password)
        response: FastAPI response untuk set cookie
        auth_service: Auth service instance

    Returns:
        LoginResponse: User data dan session info

    Raises:
        InvalidCredentialsError: Jika username/password salah
    """
    result = await auth_service.login(request)

    # Set session cookie
    response.set_cookie(
        key="simanis62_session",
        value=result.session.session_id,
        httponly=True,
        secure=False,  # HTTP only (localhost)
        samesite="lax",
        max_age=settings.session_timeout_hours * 3600,  # Convert to seconds
    )

    logger.info(f"User logged in: {request.username}")

    return result


@router.post(
    "/logout",
    response_model=SuccessResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Destroy session dan clear cookie.",
)
async def logout(
    response: Response,
    auth_service: AuthServiceDep,
    session_token: str | None = Cookie(None, alias="simanis62_session"),
) -> SuccessResponse[dict]:
    """Logout user dan clear session cookie.

    Args:
        response: FastAPI response untuk clear cookie
        auth_service: Auth service instance
        session_token: Session token dari cookie

    Returns:
        SuccessResponse: Logout success message
    """
    if session_token:
        await auth_service.logout(session_token)

    # Clear session cookie
    response.delete_cookie(
        key="simanis62_session",
        httponly=True,
        secure=False,
        samesite="lax",
    )

    logger.info("User logged out")

    return SuccessResponse(
        data={},
        message="Logout berhasil",
    )


@router.get(
    "/me",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get informasi user yang sedang login.",
)
async def get_current_user_info(
    current_user: CurrentUser,
) -> SuccessResponse[UserResponse]:
    """Get current authenticated user info.

    Args:
        current_user: Current authenticated user dari dependency

    Returns:
        SuccessResponse[UserResponse]: Current user data
    """
    user_response = UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        nama_lengkap=current_user.nama_lengkap,
        role=current_user.role,
        status=current_user.status,
        dapat_ekspor=current_user.dapat_ekspor,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )

    return SuccessResponse(
        data=user_response,
        message="User info retrieved",
    )
