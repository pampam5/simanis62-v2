"""
Aset API Endpoints untuk SIMANIS62 V2.

Endpoints:
- GET /api/v1/aset - Search aset dengan filters
- GET /api/v1/aset/{id} - Get aset by ID
- POST /api/v1/aset - Create aset baru (Admin only)
- PUT /api/v1/aset/{id} - Update aset (Admin only)
- DELETE /api/v1/aset/{id} - Soft delete aset (Admin only)
"""

import logging

from fastapi import APIRouter, Query, status

from app.api.deps import AdminUser, AsetServiceDep, CurrentUser
from app.models.aset import KategoriKIB, Kondisi, StatusAset
from app.models.user import UserRole
from app.schemas.aset import (
    AsetCreate,
    AsetDeleteRequest,
    AsetResponse,
    AsetSearchParams,
    AsetUpdate,
)
from app.schemas.response import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/aset", tags=["Aset"])
logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=PaginatedResponse[AsetResponse],
    status_code=status.HTTP_200_OK,
    summary="Search aset",
    description="Search aset dengan multiple filters dan pagination.",
)
async def search_aset(
    aset_service: AsetServiceDep,
    current_user: CurrentUser,
    keyword: str | None = Query(None, max_length=100, description="Kata kunci search"),
    kategori_kib: KategoriKIB | None = Query(None, description="Filter kategori KIB"),
    status_aset: StatusAset | None = Query(
        None, alias="status", description="Filter status"
    ),
    kondisi: Kondisi | None = Query(None, description="Filter kondisi"),
    ruangan_id: str | None = Query(None, max_length=36, description="Filter ruangan"),
    tahun_perolehan: int | None = Query(
        None, ge=1900, le=2100, description="Filter tahun"
    ),
    include_deleted: bool = Query(False, description="Include deleted (Admin only)"),
    page: int = Query(1, ge=1, description="Nomor halaman"),
    page_size: int = Query(100, ge=1, le=1000, description="Item per halaman"),
) -> PaginatedResponse[AsetResponse]:
    """Search aset dengan filters.

    Args:
        aset_service: Aset service instance
        current_user: Current authenticated user
        keyword: Kata kunci search (nama, kode, merk)
        kategori_kib: Filter berdasarkan kategori KIB
        status_aset: Filter berdasarkan status
        kondisi: Filter berdasarkan kondisi
        ruangan_id: Filter berdasarkan ruangan
        tahun_perolehan: Filter berdasarkan tahun
        include_deleted: Include deleted assets (Admin only)
        page: Nomor halaman
        page_size: Jumlah item per halaman

    Returns:
        PaginatedResponse[AsetResponse]: Paginated list of assets
    """
    params = AsetSearchParams(
        keyword=keyword,
        kategori_kib=kategori_kib,
        status=status_aset,
        kondisi=kondisi,
        ruangan_id=ruangan_id,
        tahun_perolehan=tahun_perolehan,
        include_deleted=include_deleted,
        page=page,
        page_size=page_size,
    )

    is_admin = current_user.role == UserRole.ADMIN
    result = await aset_service.search_assets(params, is_admin)

    logger.info(f"Search aset: {result.total} results found")
    return result


@router.get(
    "/{aset_id}",
    response_model=SuccessResponse[AsetResponse],
    status_code=status.HTTP_200_OK,
    summary="Get aset by ID",
    description="Get detail aset berdasarkan ID.",
)
async def get_aset(
    aset_id: str,
    aset_service: AsetServiceDep,
    current_user: CurrentUser,
) -> SuccessResponse[AsetResponse]:
    """Get aset by ID.

    Args:
        aset_id: UUID aset
        aset_service: Aset service instance
        current_user: Current authenticated user

    Returns:
        SuccessResponse[AsetResponse]: Asset data

    Raises:
        AssetNotFoundError: Jika aset tidak ditemukan
    """
    aset = await aset_service.get_asset_by_id(aset_id)
    response = aset_service._to_response(aset)

    return SuccessResponse(
        data=response,
        message="Aset ditemukan",
    )


@router.post(
    "",
    response_model=SuccessResponse[AsetResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create aset baru",
    description="Buat aset baru. Hanya Admin yang diizinkan.",
)
async def create_aset(
    data: AsetCreate,
    aset_service: AsetServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[AsetResponse]:
    """Create aset baru.

    Args:
        data: AsetCreate schema dengan data aset
        aset_service: Aset service instance
        admin_user: Current admin user

    Returns:
        SuccessResponse[AsetResponse]: Created asset data

    Raises:
        InvalidKodeBarangFormatError: Jika format kode_barang tidak valid
        DuplicateKodeBarangError: Jika kode_barang sudah ada
        InvalidTahunPerolehanError: Jika tahun tidak valid
        InvalidHargaError: Jika harga tidak valid
        RuanganNotFoundError: Jika ruangan tidak ditemukan
    """
    aset = await aset_service.create_asset(data, str(admin_user.id))
    response = aset_service._to_response(aset)

    logger.info(f"Aset created: {aset.id} by {admin_user.username}")

    return SuccessResponse(
        data=response,
        message="Aset berhasil ditambahkan",
    )


@router.put(
    "/{aset_id}",
    response_model=SuccessResponse[AsetResponse],
    status_code=status.HTTP_200_OK,
    summary="Update aset",
    description="Update aset yang ada. Hanya Admin yang diizinkan.",
)
async def update_aset(
    aset_id: str,
    data: AsetUpdate,
    aset_service: AsetServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[AsetResponse]:
    """Update aset.

    Args:
        aset_id: UUID aset yang akan diupdate
        data: AsetUpdate schema dengan data update
        aset_service: Aset service instance
        admin_user: Current admin user

    Returns:
        SuccessResponse[AsetResponse]: Updated asset data

    Raises:
        AssetNotFoundError: Jika aset tidak ditemukan
        AssetInMutationError: Jika aset sedang dalam mutasi
        AssetNotEditableError: Jika aset tidak bisa diedit
    """
    aset = await aset_service.update_asset(aset_id, data, str(admin_user.id))
    response = aset_service._to_response(aset)

    logger.info(f"Aset updated: {aset_id} by {admin_user.username}")

    return SuccessResponse(
        data=response,
        message="Aset berhasil diupdate",
    )


@router.delete(
    "/{aset_id}",
    response_model=SuccessResponse[AsetResponse],
    status_code=status.HTTP_200_OK,
    summary="Delete aset",
    description="Soft delete aset. Hanya Admin yang diizinkan.",
)
async def delete_aset(
    aset_id: str,
    request: AsetDeleteRequest,
    aset_service: AsetServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[AsetResponse]:
    """Soft delete aset.

    Args:
        aset_id: UUID aset yang akan dihapus
        request: AsetDeleteRequest dengan alasan penghapusan
        aset_service: Aset service instance
        admin_user: Current admin user

    Returns:
        SuccessResponse[AsetResponse]: Deleted asset data

    Raises:
        AssetNotFoundError: Jika aset tidak ditemukan
        AssetInMutationError: Jika aset sedang dalam mutasi
        DeleteReasonTooShortError: Jika alasan terlalu pendek
    """
    aset = await aset_service.delete_asset(aset_id, request, str(admin_user.id))
    response = aset_service._to_response(aset)

    logger.info(f"Aset deleted: {aset_id} by {admin_user.username}")

    return SuccessResponse(
        data=response,
        message="Aset berhasil dihapus",
    )
