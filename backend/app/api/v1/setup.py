"""
Setup API endpoints untuk SIMANIS62 V2.

Menyediakan First-Run Setup Wizard endpoints untuk konfigurasi awal aplikasi.
Endpoints ini TIDAK memerlukan authentication karena digunakan saat belum ada user.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User, UserRole, UserStatus
from app.schemas.response import SuccessResponse
from app.schemas.setup import CreateAdminRequest, CreateAdminResponse, SetupStatusResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/setup", tags=["Setup"])


@router.get(
    "/status",
    response_model=SuccessResponse[SetupStatusResponse],
    status_code=status.HTTP_200_OK,
    summary="Check setup status",
    description="Check apakah aplikasi memerlukan setup awal (first-run).",
)
async def get_setup_status(
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[SetupStatusResponse]:
    """Check apakah setup diperlukan.

    Setup diperlukan jika tidak ada user di database.

    Args:
        db: Database session

    Returns:
        SuccessResponse dengan SetupStatusResponse
    """
    # Count users in database
    result = await db.execute(select(func.count()).select_from(User))
    user_count = result.scalar_one()

    needs_setup = user_count == 0

    if needs_setup:
        message = "Aplikasi belum dikonfigurasi. Silakan buat akun administrator."
    else:
        message = "Aplikasi sudah dikonfigurasi."

    logger.info(f"Setup status checked: needs_setup={needs_setup}, user_count={user_count}")

    return SuccessResponse(
        data=SetupStatusResponse(
            needs_setup=needs_setup,
            message=message,
        ),
    )


@router.post(
    "/admin",
    response_model=SuccessResponse[CreateAdminResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create first admin",
    description="Buat akun administrator pertama. Hanya bisa dipanggil saat tidak ada user.",
)
async def create_first_admin(
    request: CreateAdminRequest,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[CreateAdminResponse]:
    """Buat akun administrator pertama.

    Endpoint ini hanya bisa dipanggil sekali, saat tidak ada user di database.
    Setelah admin dibuat, endpoint akan return error jika dipanggil lagi.

    Args:
        request: Data admin yang akan dibuat
        db: Database session

    Returns:
        SuccessResponse dengan data admin yang dibuat

    Raises:
        HTTPException 400: Jika setup sudah selesai (ada user)
    """
    # Check if users already exist
    result = await db.execute(select(func.count()).select_from(User))
    user_count = result.scalar_one()

    if user_count > 0:
        logger.warning("Attempt to create admin when users already exist")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "SETUP_ALREADY_DONE",
                "message": "Setup sudah selesai. Tidak dapat membuat admin baru melalui endpoint ini.",
            },
        )

    # Check if username already exists (edge case)
    existing_user = await db.execute(
        select(User).where(User.username == request.username)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "USERNAME_EXISTS",
                "message": f"Username '{request.username}' sudah digunakan.",
            },
        )

    # Create admin user
    admin = User(
        username=request.username,
        password_hash=hash_password(request.password),
        nama_lengkap=request.nama_lengkap,
        role=UserRole.ADMIN,
        status=UserStatus.AKTIF,
        dapat_ekspor=True,
    )

    db.add(admin)
    await db.commit()
    await db.refresh(admin)

    logger.info(f"First admin created: {admin.username} (id: {admin.id})")

    return SuccessResponse(
        data=CreateAdminResponse(
            id=str(admin.id),
            username=admin.username,
            nama_lengkap=admin.nama_lengkap,
            role=admin.role.value,
            status=admin.status.value,
            dapat_ekspor=admin.dapat_ekspor,
        ),
        message="Administrator berhasil dibuat. Silakan login.",
    )
