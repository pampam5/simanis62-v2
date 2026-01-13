"""
Aset API endpoints untuk SIMANIS62 V2.

Menyediakan CRUD operations untuk manajemen aset sekolah.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.auth import AdminUser, CurrentUser
from app.core.database import get_db
from app.models.aset import Aset, KategoriKIB, Kondisi, StatusAset
from app.schemas.aset import AsetCreate, AsetResponse, AsetUpdate
from app.schemas.response import MessageResponse, PaginatedResponse, SuccessResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/aset", tags=["Aset"])


@router.post(
    "/",
    response_model=SuccessResponse[AsetResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create new asset",
    description="Membuat aset baru dengan validasi lengkap (Admin only).",
)
async def create_aset(
    data: AsetCreate,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[AsetResponse]:
    """Create aset baru.

    Args:
        data: Data aset yang akan dibuat
        db: Database session

    Returns:
        SuccessResponse dengan data aset yang dibuat

    Raises:
        HTTPException 409: Jika kode_barang sudah digunakan
        HTTPException 404: Jika ruangan_id tidak ditemukan
    """
    # Check duplicate kode_barang
    result = await db.execute(
        select(Aset).where(Aset.kode_barang == data.kode_barang)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "DUPLICATE_ENTRY",
                "message": f"Kode barang {data.kode_barang} sudah digunakan",
                "field": "kode_barang",
            },
        )

    # Create aset
    aset = Aset(**data.model_dump())
    db.add(aset)
    await db.commit()
    await db.refresh(aset)

    logger.info(f"Aset created: {aset.id} - {aset.nama_barang}")

    return SuccessResponse(
        data=AsetResponse.model_validate(aset),
        message=f"Aset berhasil ditambahkan dengan Nomor Register: {aset.nomor_register}",
    )


@router.get(
    "/{aset_id}",
    response_model=SuccessResponse[AsetResponse],
    summary="Get asset by ID",
    description="Mengambil detail aset berdasarkan ID (All authenticated users).",
)
async def get_aset(
    aset_id: UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[AsetResponse]:
    """Get aset by ID.

    Args:
        aset_id: UUID aset
        db: Database session

    Returns:
        SuccessResponse dengan data aset

    Raises:
        HTTPException 404: Jika aset tidak ditemukan
    """
    result = await db.execute(select(Aset).where(Aset.id == aset_id))
    aset = result.scalar_one_or_none()

    if not aset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Aset tidak ditemukan",
            },
        )

    return SuccessResponse(data=AsetResponse.model_validate(aset))


@router.get(
    "/",
    response_model=PaginatedResponse[AsetResponse],
    summary="List assets",
    description="Mengambil list aset dengan pagination dan filtering (All authenticated users).",
)
async def list_aset(
    current_user: CurrentUser,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(100, ge=1, le=1000, description="Items per page"),
    kategori_kib: KategoriKIB | None = Query(None, description="Filter by KIB category"),
    status_filter: StatusAset | None = Query(None, alias="status", description="Filter by status"),
    ruangan_id: UUID | None = Query(None, description="Filter by room"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[AsetResponse]:
    """List aset dengan pagination.

    Args:
        page: Page number (default: 1)
        page_size: Items per page (default: 100, max: 1000)
        kategori_kib: Filter by KIB category
        status_filter: Filter by status
        ruangan_id: Filter by room
        db: Database session

    Returns:
        PaginatedResponse dengan list aset
    """
    # Build query
    query = select(Aset)

    # Apply filters
    if kategori_kib:
        query = query.where(Aset.kategori_kib == kategori_kib)
    if status_filter:
        query = query.where(Aset.status == status_filter)
    if ruangan_id:
        query = query.where(Aset.ruangan_id == ruangan_id)

    # Count total
    count_result = await db.execute(select(Aset).where(*query.whereclause.clauses if query.whereclause else []))
    total = len(count_result.all())

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    # Execute query
    result = await db.execute(query)
    aset_list = result.scalars().all()

    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size

    return PaginatedResponse(
        data=[AsetResponse.model_validate(a) for a in aset_list],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.put(
    "/{aset_id}",
    response_model=SuccessResponse[AsetResponse],
    summary="Update asset",
    description="Update data aset (Admin only).",
)
async def update_aset(
    aset_id: UUID,
    data: AsetUpdate,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[AsetResponse]:
    """Update aset.

    Args:
        aset_id: UUID aset
        data: Data update
        db: Database session

    Returns:
        SuccessResponse dengan data aset yang diupdate

    Raises:
        HTTPException 404: Jika aset tidak ditemukan
    """
    result = await db.execute(select(Aset).where(Aset.id == aset_id))
    aset = result.scalar_one_or_none()

    if not aset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Aset tidak ditemukan",
            },
        )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(aset, field, value)

    await db.commit()
    await db.refresh(aset)

    logger.info(f"Aset updated: {aset.id}")

    return SuccessResponse(
        data=AsetResponse.model_validate(aset),
        message="Aset berhasil diperbarui",
    )


@router.delete(
    "/{aset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete asset",
    description="Soft delete aset (Admin only).",
)
async def delete_aset(
    aset_id: UUID,
    current_user: AdminUser,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete aset (soft delete).

    Args:
        aset_id: UUID aset
        db: Database session

    Raises:
        HTTPException 404: Jika aset tidak ditemukan
        HTTPException 422: Jika aset sedang dalam mutasi
    """
    result = await db.execute(select(Aset).where(Aset.id == aset_id))
    aset = result.scalar_one_or_none()

    if not aset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Aset tidak ditemukan",
            },
        )

    # Check if in mutation
    if aset.status == StatusAset.MUTASI:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "BUSINESS_RULE_VIOLATION",
                "message": "Aset tidak dapat dihapus karena sedang dalam proses mutasi",
            },
        )

    # Soft delete
    aset.status = StatusAset.DIHAPUS
    await db.commit()

    logger.info(f"Aset deleted: {aset_id}")
