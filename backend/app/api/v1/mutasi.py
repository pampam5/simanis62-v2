"""
Mutasi API Endpoints untuk SIMANIS62 V2.

Endpoints:
- POST /api/v1/mutasi - Initiate mutation (Admin only)
- GET /api/v1/mutasi - List mutations
- GET /api/v1/mutasi/{id} - Get mutation detail
- PUT /api/v1/mutasi/{id}/complete - Complete mutation (Admin only)
- PUT /api/v1/mutasi/{id}/cancel - Cancel mutation (Admin only)
"""

import logging
from datetime import date

from fastapi import APIRouter, Query, status

from app.api.deps import AdminUser, CurrentUser, MutasiServiceDep
from app.models.mutasi import StatusMutasi
from app.schemas.mutasi import (
    MutasiCancelRequest,
    MutasiCompleteRequest,
    MutasiCreate,
    MutasiResponse,
    MutasiSearchParams,
)
from app.schemas.response import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/mutasi", tags=["Mutasi"])
logger = logging.getLogger(__name__)


@router.post(
    "",
    response_model=SuccessResponse[MutasiResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Initiate mutation",
    description="Mulai proses mutasi aset ke ruangan lain. Hanya Admin.",
)
async def initiate_mutation(
    data: MutasiCreate,
    mutasi_service: MutasiServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[MutasiResponse]:
    """Initiate mutation untuk aset.

    Args:
        data: MutasiCreate schema dengan data mutasi
        mutasi_service: Mutasi service instance
        admin_user: Current admin user

    Returns:
        SuccessResponse[MutasiResponse]: Created mutation data

    Raises:
        AssetNotFoundError: Jika aset tidak ditemukan
        RuanganNotFoundError: Jika ruangan tidak ditemukan
        AssetInMutationError: Jika aset sedang dalam mutasi
        SameRoomMutationError: Jika ruangan tujuan sama dengan asal
    """
    mutasi = await mutasi_service.initiate_mutation(data, str(admin_user.id))
    response = mutasi_service._to_response(mutasi)

    logger.info(f"Mutation initiated: {mutasi.id} by {admin_user.username}")

    return SuccessResponse(
        data=response,
        message="Mutasi berhasil dimulai",
    )


@router.get(
    "",
    response_model=PaginatedResponse[MutasiResponse],
    status_code=status.HTTP_200_OK,
    summary="List mutations",
    description="Get daftar mutasi dengan filters.",
)
async def list_mutations(
    mutasi_service: MutasiServiceDep,
    current_user: CurrentUser,
    aset_id: str | None = Query(None, max_length=36, description="Filter aset"),
    ruangan_id: str | None = Query(None, max_length=36, description="Filter ruangan"),
    status_mutasi: StatusMutasi | None = Query(None, description="Filter status"),
    tanggal_dari: date | None = Query(None, description="Filter tanggal dari"),
    tanggal_sampai: date | None = Query(None, description="Filter tanggal sampai"),
    page: int = Query(1, ge=1, description="Nomor halaman"),
    page_size: int = Query(100, ge=1, le=1000, description="Item per halaman"),
) -> PaginatedResponse[MutasiResponse]:
    """Get daftar mutasi dengan filters.

    Args:
        mutasi_service: Mutasi service instance
        current_user: Current authenticated user
        aset_id: Filter berdasarkan aset
        ruangan_id: Filter berdasarkan ruangan (asal atau tujuan)
        status_mutasi: Filter berdasarkan status
        tanggal_dari: Filter tanggal dari
        tanggal_sampai: Filter tanggal sampai
        page: Nomor halaman
        page_size: Jumlah item per halaman

    Returns:
        PaginatedResponse[MutasiResponse]: Paginated list of mutations
    """
    params = MutasiSearchParams(
        aset_id=aset_id,
        ruangan_id=ruangan_id,
        status_mutasi=status_mutasi,
        tanggal_dari=tanggal_dari,
        tanggal_sampai=tanggal_sampai,
        page=page,
        page_size=page_size,
    )

    result = await mutasi_service.get_mutation_history(params)

    logger.info(f"List mutations: {result.total} results found")
    return result


@router.get(
    "/{mutasi_id}",
    response_model=SuccessResponse[MutasiResponse],
    status_code=status.HTTP_200_OK,
    summary="Get mutation detail",
    description="Get detail mutasi berdasarkan ID.",
)
async def get_mutation(
    mutasi_id: str,
    mutasi_service: MutasiServiceDep,
    current_user: CurrentUser,
) -> SuccessResponse[MutasiResponse]:
    """Get mutation by ID.

    Args:
        mutasi_id: UUID mutasi
        mutasi_service: Mutasi service instance
        current_user: Current authenticated user

    Returns:
        SuccessResponse[MutasiResponse]: Mutation data

    Raises:
        MutationNotFoundError: Jika mutasi tidak ditemukan
    """
    mutasi = await mutasi_service.get_mutation_by_id(mutasi_id)
    response = mutasi_service._to_response(mutasi)

    return SuccessResponse(
        data=response,
        message="Mutasi ditemukan",
    )


@router.put(
    "/{mutasi_id}/complete",
    response_model=SuccessResponse[MutasiResponse],
    status_code=status.HTTP_200_OK,
    summary="Complete mutation",
    description="Selesaikan mutasi. Hanya Admin.",
)
async def complete_mutation(
    mutasi_id: str,
    mutasi_service: MutasiServiceDep,
    admin_user: AdminUser,
    request: MutasiCompleteRequest | None = None,
) -> SuccessResponse[MutasiResponse]:
    """Complete mutation.

    Args:
        mutasi_id: UUID mutasi
        mutasi_service: Mutasi service instance
        admin_user: Current admin user
        request: Optional catatan saat menyelesaikan

    Returns:
        SuccessResponse[MutasiResponse]: Completed mutation data

    Raises:
        MutationNotFoundError: Jika mutasi tidak ditemukan
        BusinessRuleError: Jika mutasi tidak dalam status DALAM_PROSES
    """
    mutasi = await mutasi_service.complete_mutation(
        mutasi_id, request, str(admin_user.id)
    )
    response = mutasi_service._to_response(mutasi)

    logger.info(f"Mutation completed: {mutasi_id} by {admin_user.username}")

    return SuccessResponse(
        data=response,
        message="Mutasi berhasil diselesaikan",
    )


@router.put(
    "/{mutasi_id}/cancel",
    response_model=SuccessResponse[MutasiResponse],
    status_code=status.HTTP_200_OK,
    summary="Cancel mutation",
    description="Batalkan mutasi. Hanya Admin.",
)
async def cancel_mutation(
    mutasi_id: str,
    request: MutasiCancelRequest,
    mutasi_service: MutasiServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[MutasiResponse]:
    """Cancel mutation.

    Args:
        mutasi_id: UUID mutasi
        request: MutasiCancelRequest dengan alasan pembatalan
        mutasi_service: Mutasi service instance
        admin_user: Current admin user

    Returns:
        SuccessResponse[MutasiResponse]: Cancelled mutation data

    Raises:
        MutationNotFoundError: Jika mutasi tidak ditemukan
        BusinessRuleError: Jika mutasi tidak dalam status DALAM_PROSES
        MutationReasonTooShortError: Jika alasan terlalu pendek
    """
    mutasi = await mutasi_service.cancel_mutation(
        mutasi_id, request, str(admin_user.id)
    )
    response = mutasi_service._to_response(mutasi)

    logger.info(f"Mutation cancelled: {mutasi_id} by {admin_user.username}")

    return SuccessResponse(
        data=response,
        message="Mutasi berhasil dibatalkan",
    )
