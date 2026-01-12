"""
Main API Router untuk SIMANIS62 V2.

Menggabungkan semua routers dan menyediakan health check endpoint.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, status

from app.core.config import settings
from app.core.database import db_manager
from app.schemas.response import HealthResponse

from .aset import router as aset_router
from .auth import router as auth_router
from .kib import router as kib_router
from .mutasi import router as mutasi_router
from .ruangan import router as ruangan_router
from .users import router as users_router

logger = logging.getLogger(__name__)

# Main v1 router
api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(aset_router)
api_router.include_router(kib_router)
api_router.include_router(mutasi_router)
api_router.include_router(ruangan_router)
api_router.include_router(users_router)


@api_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check API dan database health status.",
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse: Status API dan database
    """
    db_health = await db_manager.check_health()

    overall_status = "healthy" if db_health.get("status") == "healthy" else "unhealthy"

    return HealthResponse(
        status=overall_status,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database=db_health,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
