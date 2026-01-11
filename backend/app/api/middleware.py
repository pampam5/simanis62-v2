"""
Middleware untuk SIMANIS62 V2.

Menyediakan error handling terpusat dan correlation ID tracking
untuk semua HTTP requests.
"""

import logging
import time
import traceback
import uuid
from collections.abc import Callable
from datetime import datetime

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import SimanisException
from app.core.logging import correlation_id_var

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware untuk menangani semua exception secara terpusat."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request dengan error handling dan correlation ID.

        Args:
            request: FastAPI request object
            call_next: Next middleware/route handler

        Returns:
            Response: HTTP response
        """
        # Generate correlation ID untuk request tracking
        correlation_id = str(uuid.uuid4())
        correlation_id_var.set(correlation_id)

        # Set ke request state untuk akses di handlers
        request.state.correlation_id = correlation_id

        # Track waktu request
        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Add correlation ID ke response header
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"

            # Log request completion
            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration_ms, 2),
                    "correlation_id": correlation_id,
                },
            )

            return response

        except SimanisException as e:
            # Custom exception - log dan return structured response
            logger.warning(
                f"Business error: {e.error_code}",
                extra={
                    "correlation_id": correlation_id,
                    "error_code": e.error_code,
                    "message": e.message,
                    "details": e.details,
                    "path": request.url.path,
                    "method": request.method,
                },
            )

            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "error_code": e.error_code,
                    "message": e.message,
                    "details": e.details,
                    "correlation_id": correlation_id,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                },
                headers={"X-Correlation-ID": correlation_id},
            )

        except Exception as e:
            # Unexpected exception - log full traceback
            logger.error(
                f"Unexpected error: {e!s}",
                extra={
                    "correlation_id": correlation_id,
                    "path": request.url.path,
                    "method": request.method,
                    "traceback": traceback.format_exc(),
                },
                exc_info=True,
            )

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error_code": "INTERNAL_ERROR",
                    "message": "Terjadi kesalahan internal. Silakan hubungi administrator.",
                    "details": {"correlation_id": correlation_id},
                    "correlation_id": correlation_id,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                },
                headers={"X-Correlation-ID": correlation_id},
            )


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware untuk logging semua incoming requests."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log incoming request details.

        Args:
            request: FastAPI request object
            call_next: Next middleware/route handler

        Returns:
            Response: HTTP response
        """
        correlation_id = getattr(request.state, "correlation_id", "unknown")

        # Log incoming request
        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_host": request.client.host if request.client else None,
                "correlation_id": correlation_id,
            },
        )

        return await call_next(request)
