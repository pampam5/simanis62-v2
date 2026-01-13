"""
Mutasi API endpoints untuk SIMANIS62 V2.

Menyediakan operations untuk mutasi aset antar ruangan.
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.auth import AdminUser, CurrentUser
from app.core.database import get_db
from app.models.mutasi import RiwayatMutasi, StatusMutasi
from app.schemas.mutasi import MutasiCreate, MutasiResponse
from app.schemas.response import SuccessResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mutasi", tags=["Mutasi"])


@router.post(
    "/",
    response_model=SuccessResponse[MutasiResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create mutation",
    description="Membuat mutasi aset antar ruangan (Admin only).",
)
async def create_mutasi(
    data: MutasiCreate,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[MutasiResponse]:
    """Create mutasi baru.

    Args:
        data: Data mutasi yang akan dibuat
        db: Database session

    Returns:
        SuccessResponse dengan data mutasi yang dibuat

    Raises:
        HTTPException 404: Jika aset tidak ditemukan
        HTTPException 422: Jika aset sedang dalam mutasi
    """
    # Create mutasi
    mutasi = RiwayatMutasi(**data.model_dump())
    db.add(mutasi)
    await db.commit()
    await db.refresh(mutasi)

    logger.info(f"Mutasi created: {mutasi.id}")

    return SuccessResponse(
        data=MutasiResponse.model_validate(mutasi),
        message="Mutasi aset berhasil diproses",
    )


@router.get(
    "/{mutasi_id}",
    response_model=SuccessResponse[MutasiResponse],
    summary="Get mutation by ID",
    description="Mengambil detail mutasi berdasarkan ID (All authenticated users).",
)
async def get_mutasi(
    mutasi_id: UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[MutasiResponse]:
    """Get mutasi by ID.

    Args:
        mutasi_id: UUID mutasi
        db: Database session

    Returns:
        SuccessResponse dengan data mutasi

    Raises:
        HTTPException 404: Jika mutasi tidak ditemukan
    """
    result = await db.execute(select(RiwayatMutasi).where(RiwayatMutasi.id == mutasi_id))
    mutasi = result.scalar_one_or_none()

    if not mutasi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Mutasi tidak ditemukan",
            },
        )

    return SuccessResponse(data=MutasiResponse.model_validate(mutasi))


@router.put(
    "/{mutasi_id}/complete",
    response_model=SuccessResponse[MutasiResponse],
    summary="Complete mutation",
    description="Menyelesaikan mutasi aset (Admin only).",
)
async def complete_mutasi(
    mutasi_id: UUID,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[MutasiResponse]:
    """Complete mutasi.

    Args:
        mutasi_id: UUID mutasi
        db: Database session

    Returns:
        SuccessResponse dengan data mutasi yang diselesaikan

    Raises:
        HTTPException 404: Jika mutasi tidak ditemukan
        HTTPException 422: Jika mutasi tidak dalam status "Dalam Proses"
    """
    # Get mutasi
    result = await db.execute(select(RiwayatMutasi).where(RiwayatMutasi.id == mutasi_id))
    mutasi = result.scalar_one_or_none()

    if not mutasi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Mutasi tidak ditemukan",
            },
        )

    # Check status
    if mutasi.status_mutasi != StatusMutasi.DALAM_PROSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "BUSINESS_RULE_VIOLATION",
                "message": f"Mutasi tidak dapat diselesaikan karena status saat ini: {mutasi.status_mutasi}",
            },
        )

    # Update mutasi status
    mutasi.status_mutasi = StatusMutasi.SELESAI
    mutasi.selesai_mutasi = datetime.now(timezone.utc)

    # Update aset location and status
    from app.models.aset import Aset, StatusAset
    aset_result = await db.execute(select(Aset).where(Aset.id == mutasi.aset_id))
    aset = aset_result.scalar_one_or_none()
    
    if aset:
        aset.ruangan_id = mutasi.ruangan_tujuan_id
        aset.status = StatusAset.AKTIF

    await db.commit()
    await db.refresh(mutasi)

    logger.info(f"Mutasi completed: {mutasi.id}")

    return SuccessResponse(
        data=MutasiResponse.model_validate(mutasi),
        message="Mutasi aset berhasil diselesaikan",
    )


@router.put(
    "/{mutasi_id}/cancel",
    response_model=SuccessResponse[MutasiResponse],
    summary="Cancel mutation",
    description="Membatalkan mutasi aset (Admin only).",
)
async def cancel_mutasi(
    mutasi_id: UUID,
    alasan_pembatalan: str,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[MutasiResponse]:
    """Cancel mutasi.

    Args:
        mutasi_id: UUID mutasi
        alasan_pembatalan: Alasan pembatalan (min 10 karakter)
        db: Database session

    Returns:
        SuccessResponse dengan data mutasi yang dibatalkan

    Raises:
        HTTPException 404: Jika mutasi tidak ditemukan
        HTTPException 422: Jika mutasi tidak dalam status "Dalam Proses"
        HTTPException 400: Jika alasan pembatalan kurang dari 10 karakter
    """
    # Validate alasan_pembatalan
    if len(alasan_pembatalan) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "VALIDATION_ERROR",
                "message": "Alasan pembatalan minimal 10 karakter",
                "field": "alasan_pembatalan",
            },
        )

    # Get mutasi
    result = await db.execute(select(RiwayatMutasi).where(RiwayatMutasi.id == mutasi_id))
    mutasi = result.scalar_one_or_none()

    if not mutasi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Mutasi tidak ditemukan",
            },
        )

    # Check status
    if mutasi.status_mutasi != StatusMutasi.DALAM_PROSES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "BUSINESS_RULE_VIOLATION",
                "message": f"Mutasi tidak dapat dibatalkan karena status saat ini: {mutasi.status_mutasi}",
            },
        )

    # Update mutasi status
    mutasi.status_mutasi = StatusMutasi.DIBATALKAN
    mutasi.alasan_pembatalan = alasan_pembatalan
    mutasi.selesai_mutasi = datetime.now(timezone.utc)

    # Revert aset status back to Aktif
    from app.models.aset import Aset, StatusAset
    aset_result = await db.execute(select(Aset).where(Aset.id == mutasi.aset_id))
    aset = aset_result.scalar_one_or_none()
    
    if aset:
        aset.status = StatusAset.AKTIF

    await db.commit()
    await db.refresh(mutasi)

    logger.info(f"Mutasi cancelled: {mutasi.id}")

    return SuccessResponse(
        data=MutasiResponse.model_validate(mutasi),
        message="Mutasi aset berhasil dibatalkan",
    )
