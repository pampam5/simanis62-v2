---
inclusion: always
---

# Error Handling & Debugging - SIMANIS62 V2

## Prinsip Utama Error Handling

1. **Be Specific** - Tangkap hanya exception yang bisa ditangani dengan bermakna
2. **Handle at Right Level** - Tangani exception di level yang memiliki context cukup
3. **Don't Suppress** - Log dengan benar dan berikan feedback yang bermakna
4. **Use Custom Exceptions** - Buat exception spesifik aplikasi untuk semantic yang jelas
5. **Fail Fast** - Raise exception sedini mungkin untuk mencegah propagasi error

---

## Custom Exceptions (Backend)

### Struktur Exception Hierarchy

```python
# backend/app/core/exceptions.py
from typing import Any, Optional

class AppException(Exception):
    """Base exception untuk semua error aplikasi SIMANIS62."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
        context: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.context = context or {}
        super().__init__(self.message)


class ValidationError(AppException):
    """Error validasi input data."""

    def __init__(self, message: str, field: str, value: Any = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            context={"field": field, "value": str(value) if value else None}
        )


class NotFoundError(AppException):
    """Resource tidak ditemukan."""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            message=f"{resource} dengan ID {identifier} tidak ditemukan",
            error_code="NOT_FOUND",
            status_code=404,
            context={"resource": resource, "identifier": str(identifier)}
        )


class AuthenticationError(AppException):
    """Error autentikasi."""

    def __init__(self, message: str = "Autentikasi gagal"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401
        )


class AuthorizationError(AppException):
    """Error otorisasi (tidak punya izin)."""

    def __init__(self, action: str, resource: str = ""):
        super().__init__(
            message=f"Tidak memiliki izin untuk {action}" + (f" pada {resource}" if resource else ""),
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
            context={"action": action, "resource": resource}
        )


class DatabaseError(AppException):
    """Error operasi database."""

    def __init__(self, operation: str, detail: str = ""):
        super().__init__(
            message=f"Error database saat {operation}",
            error_code="DATABASE_ERROR",
            status_code=500,
            context={"operation": operation, "detail": detail}
        )


class BusinessRuleError(AppException):
    """Pelanggaran aturan bisnis."""

    def __init__(self, rule: str, message: str):
        super().__init__(
            message=message,
            error_code="BUSINESS_RULE_VIOLATION",
            status_code=422,
            context={"rule": rule}
        )
```

### Exception Handlers (FastAPI)

```python
# backend/app/core/exception_handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from datetime import datetime

from .exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register semua exception handlers ke aplikasi FastAPI."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """Handler untuk custom AppException."""
        correlation_id = getattr(request.state, "correlation_id", "unknown")

        logger.warning(
            "Application error: %s",
            exc.message,
            extra={
                "error_code": exc.error_code,
                "correlation_id": correlation_id,
                "context": exc.context,
                "path": request.url.path,
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "context": exc.context,
                "correlation_id": correlation_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handler untuk Pydantic validation errors."""
        correlation_id = getattr(request.state, "correlation_id", "unknown")

        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })

        logger.warning(
            "Validation error: %d fields invalid",
            len(errors),
            extra={
                "correlation_id": correlation_id,
                "path": request.url.path,
                "errors": errors
            }
        )

        return JSONResponse(
            status_code=422,
            content={
                "error": "VALIDATION_ERROR",
                "message": "Data tidak valid",
                "errors": errors,
                "correlation_id": correlation_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handler untuk HTTP exceptions."""
        correlation_id = getattr(request.state, "correlation_id", "unknown")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP_ERROR",
                "message": exc.detail,
                "correlation_id": correlation_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handler untuk unhandled exceptions."""
        correlation_id = getattr(request.state, "correlation_id", "unknown")

        # Log full error untuk debugging
        logger.exception(
            "Unhandled exception: %s",
            str(exc),
            extra={
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method
            }
        )

        # Return generic message ke client (jangan expose internal error)
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_ERROR",
                "message": "Terjadi kesalahan internal. Silakan coba lagi.",
                "correlation_id": correlation_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

---

## Structured Logging dengan Correlation ID

### Setup Logging

```python
# backend/app/core/logging.py
import logging
import sys
import uuid
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any
import json
import contextvars

# Context variable untuk correlation ID
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)


class StructuredFormatter(logging.Formatter):
    """JSON formatter untuk structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Tambahkan correlation ID jika ada
        correlation_id = correlation_id_var.get()
        if correlation_id:
            log_data["correlation_id"] = correlation_id

        # Tambahkan extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Tambahkan exception info jika ada
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False, default=str)


class DevelopmentFormatter(logging.Formatter):
    """Human-readable formatter untuk development."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        correlation_id = correlation_id_var.get()

        prefix = f"[{correlation_id[:8]}] " if correlation_id else ""

        return (
            f"{color}{record.levelname:8}{self.RESET} "
            f"{prefix}"
            f"{record.name}:{record.funcName}:{record.lineno} - "
            f"{record.getMessage()}"
        )


def setup_logging(
    level: str = "INFO",
    log_file: str = "logs/simanis62.log",
    json_format: bool = True
) -> None:
    """Setup logging configuration."""

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if json_format:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(DevelopmentFormatter())
    root_logger.addHandler(console_handler)

    # File handler dengan rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(file_handler)

    # Reduce noise dari library
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
```

### Middleware untuk Correlation ID

```python
# backend/app/core/middleware.py
import uuid
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from .logging import correlation_id_var

logger = logging.getLogger(__name__)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware untuk menambahkan correlation ID ke setiap request."""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate atau ambil correlation ID dari header
        correlation_id = request.headers.get(
            "X-Correlation-ID",
            str(uuid.uuid4())
        )

        # Set ke context variable
        correlation_id_var.set(correlation_id)

        # Set ke request state untuk akses di handlers
        request.state.correlation_id = correlation_id

        # Track waktu request
        start_time = time.perf_counter()

        # Process request
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
                "correlation_id": correlation_id
            }
        )

        return response
```

---

## Contoh Penggunaan di Service Layer

```python
# backend/app/services/aset_service.py
import logging
from uuid import UUID
from typing import Optional

from sqlmodel import Session, select

from app.models.aset import Aset
from app.schemas.aset import AsetCreate, AsetUpdate
from app.core.exceptions import (
    NotFoundError,
    ValidationError,
    BusinessRuleError,
    DatabaseError
)

logger = logging.getLogger(__name__)


class AsetService:
    def __init__(self, session: Session):
        self.session = session

    async def get_by_id(self, aset_id: UUID) -> Aset:
        """Ambil aset berdasarkan ID."""
        logger.debug("Fetching aset", extra={"aset_id": str(aset_id)})

        aset = self.session.get(Aset, aset_id)
        if not aset:
            raise NotFoundError("Aset", aset_id)

        return aset

    async def create(self, data: AsetCreate, user_id: UUID) -> Aset:
        """Buat aset baru."""
        logger.info(
            "Creating new aset",
            extra={"kode_barang": data.kode_barang, "user_id": str(user_id)}
        )

        # Validasi kode barang unik
        existing = self.session.exec(
            select(Aset).where(Aset.kode_barang == data.kode_barang)
        ).first()

        if existing:
            raise ValidationError(
                message=f"Kode barang {data.kode_barang} sudah digunakan",
                field="kode_barang",
                value=data.kode_barang
            )

        # Validasi aturan bisnis
        if data.harga < 0:
            raise BusinessRuleError(
                rule="HARGA_POSITIF",
                message="Harga aset tidak boleh negatif"
            )

        try:
            aset = Aset(**data.model_dump(), created_by=user_id)
            self.session.add(aset)
            self.session.commit()
            self.session.refresh(aset)

            logger.info(
                "Aset created successfully",
                extra={"aset_id": str(aset.id), "kode_barang": aset.kode_barang}
            )

            return aset

        except Exception as e:
            logger.exception("Failed to create aset")
            raise DatabaseError("membuat aset", str(e)) from e
```

---

## Best Practices Debugging

### 1. Gunakan Correlation ID untuk Tracing

```python
# Setiap log entry akan memiliki correlation_id yang sama untuk satu request
# Memudahkan tracing di log aggregator

# Request masuk → correlation_id: abc-123
logger.info("Processing request")           # correlation_id: abc-123
logger.info("Validating input")             # correlation_id: abc-123
logger.info("Saving to database")           # correlation_id: abc-123
logger.info("Request completed")            # correlation_id: abc-123
```

### 2. Log di Boundary Points

```python
# ✅ BENAR - Log di entry/exit points
async def create_aset(data: AsetCreate) -> Aset:
    logger.info("Creating aset", extra={"kode_barang": data.kode_barang})
    # ... logic ...
    logger.info("Aset created", extra={"aset_id": str(aset.id)})
    return aset

# ❌ SALAH - Log terlalu banyak di dalam loop
for item in items:
    logger.debug(f"Processing item {item.id}")  # Bisa ribuan log!
```

### 3. Preserve Exception Chain

```python
# ✅ BENAR - Preserve original exception
try:
    result = await external_api.call()
except ExternalAPIError as e:
    logger.error("External API failed", extra={"error": str(e)})
    raise DatabaseError("calling external API", str(e)) from e

# ❌ SALAH - Kehilangan original exception
try:
    result = await external_api.call()
except ExternalAPIError:
    raise DatabaseError("calling external API")  # Original error hilang!
```

### 4. Jangan Log Data Sensitif

```python
# ✅ BENAR
logger.info("User login attempt", extra={"username": username})

# ❌ SALAH
logger.info(f"User login: {username} with password {password}")
```

---

## Referensi

#[[file:backend/AGENTS.md]]
#[[file:.kiro/steering/security-policies.md]]
