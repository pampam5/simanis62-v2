"""
API Dependencies untuk SIMANIS62 V2.

Menyediakan dependency injection untuk:
- Database session
- Current user authentication
- Role-based authorization
- Service instances
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import AdminUser, CurrentUser, ExportUser
from app.core.database import get_db
from app.services.aset_service import AsetService
from app.services.kib_service import KibService
from app.services.mutasi_service import MutasiService
from app.services.ruangan_service import RuanganService

# Type alias untuk database session dependency
DbSession = Annotated[AsyncSession, Depends(get_db)]


# === Service Dependencies ===


def get_aset_service(db: DbSession) -> AsetService:
    """Get AsetService instance.

    Args:
        db: Database session

    Returns:
        AsetService: Service instance
    """
    return AsetService(db)


def get_mutasi_service(db: DbSession) -> MutasiService:
    """Get MutasiService instance.

    Args:
        db: Database session

    Returns:
        MutasiService: Service instance
    """
    return MutasiService(db)


def get_kib_service(db: DbSession) -> KibService:
    """Get KibService instance.

    Args:
        db: Database session

    Returns:
        KibService: Service instance
    """
    return KibService(db)


def get_ruangan_service(db: DbSession) -> RuanganService:
    """Get RuanganService instance.

    Args:
        db: Database session

    Returns:
        RuanganService: Service instance
    """
    return RuanganService(db)


# Type aliases untuk service dependencies
AsetServiceDep = Annotated[AsetService, Depends(get_aset_service)]
MutasiServiceDep = Annotated[MutasiService, Depends(get_mutasi_service)]
KibServiceDep = Annotated[KibService, Depends(get_kib_service)]
RuanganServiceDep = Annotated[RuanganService, Depends(get_ruangan_service)]
