"""
Users API endpoints untuk SIMANIS62 V2.

Menyediakan user management operations (Admin only).
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.auth import AdminUser
from app.core.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.schemas.response import PaginatedResponse, SuccessResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=SuccessResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create new user",
    description="Membuat user baru (Admin only).",
)
async def create_user(
    data: UserCreate,
    admin_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[UserResponse]:
    """Create user baru.

    Args:
        data: Data user yang akan dibuat
        db: Database session

    Returns:
        SuccessResponse dengan data user yang dibuat

    Raises:
        HTTPException 409: Jika username sudah digunakan
    """
    # Check duplicate username
    result = await db.execute(select(User).where(User.username == data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "DUPLICATE_ENTRY",
                "message": f"Username '{data.username}' sudah digunakan",
                "field": "username",
            },
        )

    # Create user with hashed password
    from app.core.security import hash_password
    
    user_data = data.model_dump(exclude={"password"})
    user_data["password_hash"] = hash_password(data.password)
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info(f"User created: {user.id} - {user.username}")

    return SuccessResponse(
        data=UserResponse.model_validate(user),
        message="User berhasil dibuat",
    )


@router.get(
    "/",
    response_model=PaginatedResponse[UserResponse],
    summary="List users",
    description="Mengambil list users dengan pagination (Admin only).",
)
async def list_users(
    admin_user: AdminUser,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=1000, description="Items per page"),
    role: UserRole | None = Query(None, description="Filter by role"),
    status_filter: UserStatus | None = Query(None, alias="status", description="Filter by status"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[UserResponse]:
    """List users dengan pagination.

    Args:
        page: Page number (default: 1)
        page_size: Items per page (default: 100, max: 1000)
        role: Filter by role
        status_filter: Filter by status
        db: Database session

    Returns:
        PaginatedResponse dengan list users
    """
    # Build query
    query = select(User)

    # Apply filters
    if role:
        query = query.where(User.role == role)
    if status_filter:
        query = query.where(User.status == status_filter)

    # Count total
    count_result = await db.execute(select(User).where(*query.whereclause.clauses if query.whereclause else []))
    total = len(count_result.all())

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    # Execute query
    result = await db.execute(query)
    users = result.scalars().all()

    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size

    return PaginatedResponse(
        data=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    summary="Get user by ID",
    description="Mengambil detail user berdasarkan ID (Admin only).",
)
async def get_user(
    user_id: UUID,
    admin_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[UserResponse]:
    """Get user by ID.

    Args:
        user_id: UUID user
        db: Database session

    Returns:
        SuccessResponse dengan data user

    Raises:
        HTTPException 404: Jika user tidak ditemukan
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "User tidak ditemukan",
            },
        )

    return SuccessResponse(data=UserResponse.model_validate(user))


@router.put(
    "/{user_id}",
    response_model=SuccessResponse[UserResponse],
    summary="Update user",
    description="Update data user (Admin only).",
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    admin_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[UserResponse]:
    """Update user.

    Args:
        user_id: UUID user
        data: Data update
        db: Database session

    Returns:
        SuccessResponse dengan data user yang diupdate

    Raises:
        HTTPException 404: Jika user tidak ditemukan
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "User tidak ditemukan",
            },
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    logger.info(f"User updated: {user.id}")

    return SuccessResponse(
        data=UserResponse.model_validate(user),
        message="User berhasil diperbarui",
    )


@router.put(
    "/{user_id}/deactivate",
    response_model=SuccessResponse[UserResponse],
    summary="Deactivate user",
    description="Nonaktifkan user (soft delete, Admin only).",
)
async def deactivate_user(
    user_id: UUID,
    admin_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[UserResponse]:
    """Deactivate user (soft delete).

    Args:
        user_id: UUID user
        db: Database session

    Returns:
        SuccessResponse dengan data user yang dinonaktifkan

    Raises:
        HTTPException 404: Jika user tidak ditemukan
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "User tidak ditemukan",
            },
        )

    # Deactivate
    user.status = UserStatus.NONAKTIF
    await db.commit()
    await db.refresh(user)

    logger.info(f"User deactivated: {user_id}")

    return SuccessResponse(
        data=UserResponse.model_validate(user),
        message="User berhasil dinonaktifkan",
    )
