"""
User Management API Endpoints untuk SIMANIS62 V2.

Endpoints:
- GET /api/v1/users - List users (Admin only)
- GET /api/v1/users/{id} - Get user detail (Admin only)
- POST /api/v1/users - Create user (Admin only)
- PUT /api/v1/users/{id} - Update user (Admin only)
- PUT /api/v1/users/{id}/deactivate - Deactivate user (Admin only)
"""

import logging

from fastapi import APIRouter, Query, status

from app.api.deps import AdminUser, UserServiceDep
from app.models.user import UserRole, UserStatus
from app.schemas.auth import UserResponse
from app.schemas.response import PaginatedResponse, SuccessResponse
from app.schemas.user import (
    UserCreate,
    UserDeactivateRequest,
    UserSearchParams,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["User Management"])
logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List users",
    description="Get daftar users dengan filters. Hanya Admin.",
)
async def list_users(
    user_service: UserServiceDep,
    admin_user: AdminUser,
    keyword: str | None = Query(None, max_length=100, description="Search keyword"),
    role: UserRole | None = Query(None, description="Filter role"),
    user_status: UserStatus | None = Query(
        None, alias="status", description="Filter status"
    ),
    dapat_ekspor: bool | None = Query(None, description="Filter izin export"),
    page: int = Query(1, ge=1, description="Nomor halaman"),
    page_size: int = Query(100, ge=1, le=1000, description="Item per halaman"),
) -> PaginatedResponse[UserResponse]:
    """Get daftar users dengan filters."""
    params = UserSearchParams(
        keyword=keyword,
        role=role,
        status=user_status,
        dapat_ekspor=dapat_ekspor,
        page=page,
        page_size=page_size,
    )

    result = await user_service.search_users(params)
    logger.info(f"List users: {result.total} results found")
    return result


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user detail",
    description="Get detail user berdasarkan ID. Hanya Admin.",
)
async def get_user(
    user_id: str,
    user_service: UserServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[UserResponse]:
    """Get user by ID."""
    user = await user_service.get_user_by_id(user_id)
    response = user_service._to_response(user)
    return SuccessResponse(data=response, message="User ditemukan")


@router.post(
    "",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    description="Buat user baru. Hanya Admin.",
)
async def create_user(
    data: UserCreate,
    user_service: UserServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[UserResponse]:
    """Create user baru."""
    user = await user_service.create_user(data, str(admin_user.id))
    response = user_service._to_response(user)

    logger.info(f"User created: {user.id} by {admin_user.username}")
    return SuccessResponse(data=response, message="User berhasil ditambahkan")


@router.put(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Update user",
    description="Update user. Hanya Admin. Tidak bisa mengubah role sendiri.",
)
async def update_user(
    user_id: str,
    data: UserUpdate,
    user_service: UserServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[UserResponse]:
    """Update user."""
    user = await user_service.update_user(user_id, data, str(admin_user.id))
    response = user_service._to_response(user)

    logger.info(f"User updated: {user_id} by {admin_user.username}")
    return SuccessResponse(data=response, message="User berhasil diupdate")


@router.put(
    "/{user_id}/deactivate",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Deactivate user",
    description="Nonaktifkan user. Hanya Admin. Tidak bisa menonaktifkan diri sendiri.",
)
async def deactivate_user(
    user_id: str,
    user_service: UserServiceDep,
    admin_user: AdminUser,
    request: UserDeactivateRequest | None = None,
) -> SuccessResponse[UserResponse]:
    """Deactivate user."""
    user = await user_service.deactivate_user(user_id, request, str(admin_user.id))
    response = user_service._to_response(user)

    logger.info(f"User deactivated: {user_id} by {admin_user.username}")
    return SuccessResponse(data=response, message="User berhasil dinonaktifkan")
