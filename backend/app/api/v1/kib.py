"""
KIB Report API Endpoints untuk SIMANIS62 V2.

Endpoints:
- GET /api/v1/kib/{kategori} - Get KIB report
- GET /api/v1/kib/{kategori}/export - Export KIB ke Excel (Admin/Kepala Sekolah)
"""

import logging
from pathlib import Path

from fastapi import APIRouter, Query, status
from fastapi.responses import FileResponse

from app.api.deps import CurrentUser, ExportUser, KibServiceDep
from app.models.aset import KategoriKIB
from app.schemas.kib import KibExportRequest, KibExportResponse, KibReportResponse
from app.schemas.response import SuccessResponse

router = APIRouter(prefix="/kib", tags=["KIB Report"])
logger = logging.getLogger(__name__)


@router.get(
    "/{kategori}",
    response_model=SuccessResponse[KibReportResponse],
    status_code=status.HTTP_200_OK,
    summary="Get KIB report",
    description="Get laporan KIB untuk kategori tertentu (A-F).",
)
async def get_kib_report(
    kategori: KategoriKIB,
    kib_service: KibServiceDep,
    current_user: CurrentUser,
    tahun: int | None = Query(None, ge=1900, le=2100, description="Filter tahun"),
    ruangan_id: str | None = Query(None, max_length=36, description="Filter ruangan"),
    page: int = Query(1, ge=1, description="Nomor halaman"),
    page_size: int = Query(1000, ge=1, le=10000, description="Item per halaman"),
) -> SuccessResponse[KibReportResponse]:
    """Get KIB report untuk kategori tertentu.

    Args:
        kategori: Kategori KIB (A-F)
        kib_service: KIB service instance
        current_user: Current authenticated user
        tahun: Filter berdasarkan tahun perolehan
        ruangan_id: Filter berdasarkan ruangan
        page: Nomor halaman
        page_size: Jumlah item per halaman

    Returns:
        SuccessResponse[KibReportResponse]: KIB report data
    """
    report = await kib_service.get_kib_report(
        kategori_kib=kategori,
        tahun=tahun,
        ruangan_id=ruangan_id,
        page=page,
        page_size=page_size,
    )

    logger.info(
        f"KIB {kategori.value} report generated: {report.summary.total_item} items"
    )

    return SuccessResponse(
        data=report,
        message=f"Laporan KIB {kategori.value} berhasil di-generate",
    )


@router.post(
    "/{kategori}/export",
    response_model=SuccessResponse[KibExportResponse],
    status_code=status.HTTP_200_OK,
    summary="Export KIB ke Excel",
    description="Export laporan KIB ke file Excel. Hanya Admin atau Kepala Sekolah.",
)
async def export_kib(
    kategori: KategoriKIB,
    kib_service: KibServiceDep,
    export_user: ExportUser,
    tahun_perolehan: int | None = Query(
        None, ge=1900, le=2100, description="Filter tahun"
    ),
    ruangan_id: str | None = Query(None, max_length=36, description="Filter ruangan"),
    include_rusak: bool = Query(True, description="Include aset rusak"),
) -> SuccessResponse[KibExportResponse]:
    """Export KIB ke Excel.

    Args:
        kategori: Kategori KIB (A-F)
        kib_service: KIB service instance
        export_user: User dengan izin export (Admin atau Kepala Sekolah)
        tahun_perolehan: Filter berdasarkan tahun
        ruangan_id: Filter berdasarkan ruangan
        include_rusak: Include aset dengan kondisi rusak

    Returns:
        SuccessResponse[KibExportResponse]: Export result info
    """
    request = KibExportRequest(
        kategori_kib=kategori,
        tahun_perolehan=tahun_perolehan,
        ruangan_id=ruangan_id,
        include_rusak=include_rusak,
        format="xlsx",
    )

    result = await kib_service.export_to_excel(request)

    logger.info(
        f"KIB {kategori.value} exported: {result.filename} by {export_user.username}"
    )

    return SuccessResponse(
        data=result,
        message=f"Laporan KIB {kategori.value} berhasil di-export",
    )


@router.get(
    "/{kategori}/download/{filename}",
    status_code=status.HTTP_200_OK,
    summary="Download file export",
    description="Download file Excel yang sudah di-export.",
)
async def download_kib_export(
    kategori: KategoriKIB,
    filename: str,
    export_user: ExportUser,
) -> FileResponse:
    """Download file export KIB.

    Args:
        kategori: Kategori KIB (untuk validasi)
        filename: Nama file yang akan di-download
        export_user: User dengan izin export

    Returns:
        FileResponse: File Excel untuk download

    Raises:
        HTTPException: Jika file tidak ditemukan
    """
    from fastapi import HTTPException

    from app.core.config import settings

    file_path = Path(settings.export_dir) / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File {filename} tidak ditemukan",
        )

    # Validate filename matches kategori
    if f"KIB_{kategori.value}" not in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename tidak sesuai dengan kategori KIB",
        )

    logger.info(f"KIB file downloaded: {filename} by {export_user.username}")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
