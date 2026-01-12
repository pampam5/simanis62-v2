"""Entry point FastAPI untuk SIMANIS62 V2.

Menginisialisasi aplikasi, middleware, logging, dan routing.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware import ErrorHandlingMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import db_manager
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager untuk startup dan shutdown events.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup
    logger.info("Starting SIMANIS62 V2 API...")

    # Initialize database
    await db_manager.initialize()
    await db_manager.create_tables()

    # Cancel expired mutations on startup
    try:
        from app.services.mutasi_service import MutasiService

        async with db_manager.get_session() as session:
            mutasi_service = MutasiService(session)
            cancelled = await mutasi_service.cancel_expired_mutations()
            if cancelled > 0:
                logger.info(f"Cancelled {cancelled} expired mutations on startup")
    except Exception as e:
        logger.warning(f"Failed to cancel expired mutations: {e}")

    logger.info(
        f"SIMANIS62 V2 API started - version: {settings.APP_VERSION}, "
        f"environment: {settings.ENVIRONMENT}, debug: {settings.DEBUG}"
    )

    yield

    # Shutdown
    logger.info("Shutting down SIMANIS62 V2 API...")
    await db_manager.close()
    logger.info("SIMANIS62 V2 API shutdown complete")


def create_app() -> FastAPI:
    """Factory function untuk membuat instance FastAPI.

    Returns:
        FastAPI: Configured FastAPI application
    """
    # Setup logging
    setup_logging(
        level=settings.LOG_LEVEL,
        log_file=settings.LOG_FILE,
        json_format=not settings.DEBUG,
    )

    # Create FastAPI app
    app = FastAPI(
        title="SIMANIS62 V2 API",
        description="Sistem Manajemen Aset Sekolah - REST API",
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Add CORS middleware (untuk development)
    if settings.DEBUG:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add error handling middleware
    app.add_middleware(ErrorHandlingMiddleware)

    # Include API router
    app.include_router(api_router)

    logger.info("FastAPI application created")
    return app


app = create_app()
