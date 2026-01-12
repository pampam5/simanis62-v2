"""
Ruangan API Endpoints untuk SIMANIS62 V2.

Endpoints:
- GET /api/v1/ruangan - List ruangan
- GET /api/v1/ruangan/{id} - Get ruangan detail
- POST /api/v1/ruangan - Create ruangan (Admin only)
- PUT /api/v1/ruangan/{id} - Update ruangan (Admin only)
- DELETE /api/v1/ruangan/{id} - Delete ruangan (Admin only)
- GET /api/v1/ruangan/{id}/kir - Get KIR report for room
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Query, status
from pydantic import BaseModel, ConfigDict, Field

from app.api.deps import AdminUser, CurrentUser, RuanganServiceDep
from app.schemas.response import PaginatedResponse, SuccessResponse

router = APIRouter(prefix="/ruangan", tags=["Ruangan"])
logger = logging.getLogger(__name__)


# Pydantic schemas for API
class RuanganCreateRequest(BaseModel):
    """Schema untuk membuat ruangan baru."""

    kode_ruangan: str = Field(..., min_length=2, max_length=20)
    nama_ruangan: str = Field(..., min_length=3, max_length=100)
    keterangan: str | None = Field(None, max_length=500)


class RuanganUpdateRequest(BaseModel):
    """Schema untuk update ruangan."""

    nama_ruangan: str | None = Field(None, min_length=3, max_length=100)
    keterangan: str | None = Field(None, max_length=500)


class RuanganResponseSchema(BaseModel):
    """Schema untuk response ruangan."""

    id: str
    kode_ruangan: str
    nama_ruangan: str
    keterangan: str | None
    jumlah_aset: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class KirItemSchema(BaseModel):
    """Schema untuk item KIR report."""

    nomor_urut: int
    kode_barang: str
    nama_barang: str
    nomor_register: int
    kondisi: str
    tahun_perolehan: int
    harga: int
    keterangan: str | None


class KirReportSchema(BaseModel):
    """Schema untuk KIR report response."""

    ruangan: RuanganResponseSchema
    total_aset: int
    total_nilai: int
    items: list[KirItemSchema]
    tanggal_cetak: datetime


@router.get(
    "",
    response_model=PaginatedResponse[RuanganResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="List ruangan",
    description="Get daftar ruangan dengan pagination.",
)
async def list_ruangan(
    ruangan_service: RuanganServiceDep,
    current_user: CurrentUser,
    page: int = Query(1, ge=1, description="Nomor halaman"),
    page_size: int = Query(100, ge=1, le=1000, description="Item per halaman"),
) -> PaginatedResponse[RuanganResponseSchema]:
    """Get daftar ruangan."""
    result = await ruangan_service.get_all_ruangan(page=page, page_size=page_size)

    # Convert to schema
    items = [
        RuanganResponseSchema(
            id=r.id,
            kode_ruangan=r.kode_ruangan,
            nama_ruangan=r.nama_ruangan,
            keterangan=r.keterangan,
            jumlah_aset=r.jumlah_aset,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in result.data
    ]

    return PaginatedResponse(
        data=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        total_pages=result.total_pages,
    )


@router.get(
    "/{ruangan_id}",
    response_model=SuccessResponse[RuanganResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get ruangan detail",
    description="Get detail ruangan berdasarkan ID.",
)
async def get_ruangan(
    ruangan_id: str,
    ruangan_service: RuanganServiceDep,
    current_user: CurrentUser,
) -> SuccessResponse[RuanganResponseSchema]:
    """Get ruangan by ID."""

    ruangan = await ruangan_service.get_ruangan_by_id(ruangan_id)
    count = await ruangan_service.repository.count_assets_in_room(ruangan_id)

    response = RuanganResponseSchema(
        id=str(ruangan.id),
        kode_ruangan=ruangan.kode_ruangan,
        nama_ruangan=ruangan.nama_ruangan,
        keterangan=ruangan.keterangan,
        jumlah_aset=count,
        created_at=ruangan.created_at,
        updated_at=ruangan.updated_at,
    )

    return SuccessResponse(data=response, message="Ruangan ditemukan")


@router.post(
    "",
    response_model=SuccessResponse[RuanganResponseSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Create ruangan",
    description="Buat ruangan baru. Hanya Admin.",
)
async def create_ruangan(
    data: RuanganCreateRequest,
    ruangan_service: RuanganServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[RuanganResponseSchema]:
    """Create ruangan baru."""
    from app.services.ruangan_service import RuanganCreate

    create_data = RuanganCreate(
        kode_ruangan=data.kode_ruangan,
        nama_ruangan=data.nama_ruangan,
        keterangan=data.keterangan,
    )

    ruangan = await ruangan_service.create_ruangan(create_data, str(admin_user.id))

    response = RuanganResponseSchema(
        id=str(ruangan.id),
        kode_ruangan=ruangan.kode_ruangan,
        nama_ruangan=ruangan.nama_ruangan,
        keterangan=ruangan.keterangan,
        jumlah_aset=0,
        created_at=ruangan.created_at,
        updated_at=ruangan.updated_at,
    )

    logger.info(f"Ruangan created: {ruangan.id} by {admin_user.username}")
    return SuccessResponse(data=response, message="Ruangan berhasil ditambahkan")


@router.put(
    "/{ruangan_id}",
    response_model=SuccessResponse[RuanganResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Update ruangan",
    description="Update ruangan. Hanya Admin.",
)
async def update_ruangan(
    ruangan_id: str,
    data: RuanganUpdateRequest,
    ruangan_service: RuanganServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[RuanganResponseSchema]:
    """Update ruangan."""
    from app.services.ruangan_service import RuanganUpdate

    update_data = RuanganUpdate(
        nama_ruangan=data.nama_ruangan, keterangan=data.keterangan
    )

    ruangan = await ruangan_service.update_ruangan(
        ruangan_id, update_data, str(admin_user.id)
    )
    count = await ruangan_service.repository.count_assets_in_room(ruangan_id)

    response = RuanganResponseSchema(
        id=str(ruangan.id),
        kode_ruangan=ruangan.kode_ruangan,
        nama_ruangan=ruangan.nama_ruangan,
        keterangan=ruangan.keterangan,
        jumlah_aset=count,
        created_at=ruangan.created_at,
        updated_at=ruangan.updated_at,
    )

    logger.info(f"Ruangan updated: {ruangan_id} by {admin_user.username}")
    return SuccessResponse(data=response, message="Ruangan berhasil diupdate")


@router.delete(
    "/{ruangan_id}",
    response_model=SuccessResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Delete ruangan",
    description="Hapus ruangan. Hanya Admin. Ruangan tidak boleh memiliki aset.",
)
async def delete_ruangan(
    ruangan_id: str,
    ruangan_service: RuanganServiceDep,
    admin_user: AdminUser,
) -> SuccessResponse[dict]:
    """Delete ruangan."""
    await ruangan_service.delete_ruangan(ruangan_id)

    logger.info(f"Ruangan deleted: {ruangan_id} by {admin_user.username}")
    return SuccessResponse(data={}, message="Ruangan berhasil dihapus")


@router.get(
    "/{ruangan_id}/kir",
    response_model=SuccessResponse[KirReportSchema],
    status_code=status.HTTP_200_OK,
    summary="Get KIR report",
    description="Get Kartu Inventaris Ruangan (KIR) report untuk ruangan.",
)
async def get_kir_report(
    ruangan_id: str,
    ruangan_service: RuanganServiceDep,
    current_user: CurrentUser,
) -> SuccessResponse[KirReportSchema]:
    """Get KIR report untuk ruangan."""
    kir = await ruangan_service.get_kir_report(ruangan_id)

    ruangan_schema = RuanganResponseSchema(
        id=kir.ruangan.id,
        kode_ruangan=kir.ruangan.kode_ruangan,
        nama_ruangan=kir.ruangan.nama_ruangan,
        keterangan=kir.ruangan.keterangan,
        jumlah_aset=kir.ruangan.jumlah_aset,
        created_at=kir.ruangan.created_at,
        updated_at=kir.ruangan.updated_at,
    )

    items = [
        KirItemSchema(
            nomor_urut=item.nomor_urut,
            kode_barang=item.kode_barang,
            nama_barang=item.nama_barang,
            nomor_register=item.nomor_register,
            kondisi=item.kondisi,
            tahun_perolehan=item.tahun_perolehan,
            harga=item.harga,
            keterangan=item.keterangan,
        )
        for item in kir.items
    ]

    response = KirReportSchema(
        ruangan=ruangan_schema,
        total_aset=kir.total_aset,
        total_nilai=kir.total_nilai,
        items=items,
        tanggal_cetak=kir.tanggal_cetak,
    )

    logger.info(f"KIR report generated for ruangan: {ruangan_id}")
    return SuccessResponse(data=response, message="KIR report berhasil di-generate")
