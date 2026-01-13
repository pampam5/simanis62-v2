"""
KIB API endpoints untuk SIMANIS62 V2.

Menyediakan endpoints untuk generate laporan KIB A-F.
"""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.auth import CurrentUser, ExportUser
from app.core.database import get_db
from app.models.aset import Aset, KategoriKIB, StatusAset
from app.schemas.response import SuccessResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/kib", tags=["KIB"])


@router.get(
    "/{kategori}",
    response_model=SuccessResponse[list[dict[str, Any]]],
    summary="Get KIB report",
    description="Generate laporan KIB berdasarkan kategori (A/B/C/D/E/F) - All authenticated users.",
)
async def get_kib_report(
    kategori: str,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[list[dict[str, Any]]]:
    """Get KIB report by category.

    Args:
        kategori: Kategori KIB (A/B/C/D/E/F)
        db: Database session

    Returns:
        SuccessResponse dengan data laporan KIB

    Raises:
        HTTPException 400: Jika kategori tidak valid
    """
    # Validate kategori
    try:
        kib_kategori = KategoriKIB(kategori.upper())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "VALIDATION_ERROR",
                "message": f"Kategori KIB tidak valid: {kategori}. Harus A/B/C/D/E/F",
                "field": "kategori",
            },
        )

    # Query aset by kategori (only Aktif and Rusak status)
    result = await db.execute(
        select(Aset)
        .where(Aset.kategori_kib == kib_kategori)
        .where(Aset.status.in_([StatusAset.AKTIF, StatusAset.RUSAK]))
        .order_by(Aset.nomor_register)
    )
    aset_list = result.scalars().all()

    # Convert to dict for response
    report_data = [
        {
            "id": str(aset.id),
            "nomor_register": aset.nomor_register,
            "kode_barang": aset.kode_barang,
            "nama_barang": aset.nama_barang,
            "tahun_perolehan": aset.tahun_perolehan,
            "asal_usul": aset.asal_usul.value,
            "harga": aset.harga,
            "kondisi": aset.kondisi.value,
            "status": aset.status.value,
        }
        for aset in aset_list
    ]

    logger.info(f"KIB {kategori} report generated: {len(report_data)} items")

    return SuccessResponse(
        data=report_data,
        message=f"Laporan KIB {kategori} berhasil di-generate",
    )


@router.get(
    "/{kategori}/export",
    response_model=SuccessResponse[dict[str, Any]],
    summary="Export KIB report",
    description="Export laporan KIB ke Excel (Admin atau Kepala Sekolah with dapat_ekspor=True).",
)
async def export_kib_report(
    kategori: str,
    current_user: ExportUser,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[dict[str, Any]]:
    """Export KIB report to Excel.

    Args:
        kategori: Kategori KIB (A/B/C/D/E/F)
        db: Database session

    Returns:
        SuccessResponse dengan info export

    Raises:
        HTTPException 400: Jika kategori tidak valid
    """
    # Validate kategori
    try:
        kib_kategori = KategoriKIB(kategori.upper())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "VALIDATION_ERROR",
                "message": f"Kategori KIB tidak valid: {kategori}. Harus A/B/C/D/E/F",
                "field": "kategori",
            },
        )

    # Query aset by kategori
    result = await db.execute(
        select(Aset)
        .where(Aset.kategori_kib == kib_kategori)
        .where(Aset.status.in_([StatusAset.AKTIF, StatusAset.RUSAK]))
        .order_by(Aset.nomor_register)
    )
    aset_list = result.scalars().all()

    # TODO: Implement actual Excel export
    # For now, return mock response
    export_info = {
        "kategori": kategori.upper(),
        "total_items": len(aset_list),
        "export_format": "xlsx",
        "status": "success",
    }

    logger.info(f"KIB {kategori} export requested: {len(aset_list)} items")

    return SuccessResponse(
        data=export_info,
        message=f"Export KIB {kategori} berhasil",
    )
