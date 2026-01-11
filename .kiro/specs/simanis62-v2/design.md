# Design Document: SIMANIS62 V2

## Introduction

Dokumen ini mendefinisikan arsitektur teknis dan design patterns untuk SIMANIS62 V2 berdasarkan requirements yang sudah disetujui. Fokus utama adalah:
- **Debugging & Error Handling** - Mudah melacak dan memperbaiki masalah
- **Maintainability** - Kode mudah dipahami dan dimodifikasi
- **Clean Codebase** - Struktur yang konsisten dan terorganisir

## Design Principles

### 1. Clean Architecture (Layered Structure)

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   API Routes    │  │   WPF Views     │  │   ViewModels    │  │
│  │  (FastAPI)      │  │   (XAML)        │  │   (MVVM)        │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
└───────────┼────────────────────┼────────────────────┼───────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      Services (Business Logic)               ││
│  │  AssetService │ MutationService │ ReportService │ AuthService││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DOMAIN LAYER                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │     Models      │  │    Schemas      │  │   Exceptions    │  │
│  │   (SQLModel)    │  │   (Pydantic)    │  │   (Custom)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Repository    │  │    Database     │  │    Logging      │  │
│  │   (Data Access) │  │   (SQLite WAL)  │  │  (Structured)   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Dependency Flow Rules

- **Presentation** → depends on → **Application** → depends on → **Domain** → depends on → **Infrastructure**
- Inner layers TIDAK BOLEH depend on outer layers
- Semua dependencies di-inject melalui constructor (Dependency Injection)


---

## Backend Architecture (FastAPI + Python)

### Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── api/                       # Presentation Layer
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependency injection
│   │   ├── middleware.py          # Error handling, logging middleware
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Main router
│   │   │   ├── auth.py            # /api/v1/auth/*
│   │   │   ├── aset.py            # /api/v1/aset/*
│   │   │   ├── kib.py             # /api/v1/kib/*
│   │   │   ├── mutasi.py          # /api/v1/mutasi/*
│   │   │   └── ruangan.py         # /api/v1/ruangan/*
│   │   └── responses.py           # Standard response schemas
│   │
│   ├── services/                  # Application Layer
│   │   ├── __init__.py
│   │   ├── base.py                # BaseService class
│   │   ├── auth_service.py
│   │   ├── aset_service.py
│   │   ├── mutasi_service.py
│   │   ├── kib_service.py
│   │   └── ruangan_service.py
│   │
│   ├── models/                    # Domain Layer - SQLModel entities
│   │   ├── __init__.py
│   │   ├── base.py                # BaseModel with common fields
│   │   ├── user.py
│   │   ├── aset.py
│   │   ├── ruangan.py
│   │   ├── mutasi.py
│   │   └── audit.py
│   │
│   ├── schemas/                   # Domain Layer - Pydantic schemas
│   │   ├── __init__.py
│   │   ├── base.py                # BaseSchema
│   │   ├── auth.py
│   │   ├── aset.py
│   │   ├── kib.py
│   │   ├── mutasi.py
│   │   └── response.py            # Standard API responses
│   │
│   ├── repositories/              # Infrastructure Layer - Data Access
│   │   ├── __init__.py
│   │   ├── base.py                # BaseRepository (CRUD)
│   │   ├── aset_repository.py
│   │   ├── user_repository.py
│   │   ├── mutasi_repository.py
│   │   └── ruangan_repository.py
│   │
│   ├── core/                      # Infrastructure Layer - Cross-cutting
│   │   ├── __init__.py
│   │   ├── config.py              # Settings & configuration
│   │   ├── database.py            # SQLite connection (WAL mode)
│   │   ├── security.py            # Password hashing, session
│   │   ├── logging.py             # Structured logging setup
│   │   └── exceptions.py          # Custom exception hierarchy
│   │
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── validators.py          # Custom validators
│       └── helpers.py             # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── unit/
│   │   ├── test_services/
│   │   └── test_repositories/
│   └── integration/
│       └── test_api/
│
├── requirements.txt
├── pyproject.toml
└── .env.example
```


---

## Exception Hierarchy (Backend)

### Custom Exception Classes

```python
# app/core/exceptions.py

from typing import Optional, Dict, Any

class SimanisException(Exception):
    """Base exception untuk semua error SIMANIS62."""
    
    def __init__(
        self,
        message: str,
        error_code: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)


# === Authentication Exceptions ===
class AuthenticationError(SimanisException):
    """Error terkait autentikasi."""
    def __init__(self, message: str = "Autentikasi gagal", details: Optional[Dict] = None):
        super().__init__(message, "AUTH_ERROR", details, 401)

class InvalidCredentialsError(AuthenticationError):
    """Username atau password salah."""
    def __init__(self):
        super().__init__("Username atau password salah", {"field": "credentials"})

class SessionExpiredError(AuthenticationError):
    """Session sudah expired."""
    def __init__(self):
        super().__init__("Session telah berakhir, silakan login kembali", {"reason": "expired"})


# === Authorization Exceptions ===
class AuthorizationError(SimanisException):
    """Error terkait otorisasi."""
    def __init__(self, message: str = "Akses ditolak", details: Optional[Dict] = None):
        super().__init__(message, "AUTHZ_ERROR", details, 403)

class InsufficientPermissionError(AuthorizationError):
    """User tidak memiliki izin untuk operasi ini."""
    def __init__(self, required_role: str):
        super().__init__(
            f"Akses ditolak. Memerlukan role: {required_role}",
            {"required_role": required_role}
        )


# === Validation Exceptions ===
class ValidationError(SimanisException):
    """Error validasi input."""
    def __init__(self, message: str, field: str, details: Optional[Dict] = None):
        super().__init__(message, "VALIDATION_ERROR", {"field": field, **(details or {})}, 422)

class DuplicateKodeBarangError(ValidationError):
    """Kode barang sudah ada."""
    def __init__(self, kode_barang: str):
        super().__init__(
            f"Kode barang '{kode_barang}' sudah terdaftar",
            "kode_barang",
            {"existing_code": kode_barang}
        )

class InvalidKodeBarangFormatError(ValidationError):
    """Format kode barang tidak valid."""
    def __init__(self, kode_barang: str):
        super().__init__(
            f"Format kode barang tidak valid: '{kode_barang}'. Format: XX.XX.XX.XXXX",
            "kode_barang",
            {"invalid_value": kode_barang, "expected_format": "XX.XX.XX.XXXX"}
        )

class InvalidTahunPerolehanError(ValidationError):
    """Tahun perolehan tidak valid."""
    def __init__(self, tahun: int, current_year: int):
        super().__init__(
            f"Tahun perolehan {tahun} tidak valid. Harus antara 1900-{current_year}",
            "tahun_perolehan",
            {"invalid_value": tahun, "min": 1900, "max": current_year}
        )

class InvalidHargaError(ValidationError):
    """Harga tidak valid."""
    def __init__(self, harga: int):
        super().__init__(
            f"Harga harus lebih dari 0 dan maksimal 999.999.999.999",
            "harga",
            {"invalid_value": harga}
        )

class DeleteReasonTooShortError(ValidationError):
    """Alasan hapus terlalu pendek."""
    def __init__(self, length: int):
        super().__init__(
            f"Alasan penghapusan minimal 20 karakter (saat ini: {length})",
            "alasan_hapus",
            {"current_length": length, "min_length": 20}
        )


# === Business Logic Exceptions ===
class BusinessRuleError(SimanisException):
    """Error terkait aturan bisnis."""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "BUSINESS_ERROR", details, 400)

class AssetInMutationError(BusinessRuleError):
    """Aset sedang dalam proses mutasi."""
    def __init__(self, aset_id: str):
        super().__init__(
            "Aset sedang dalam proses mutasi dan tidak dapat diubah/dihapus",
            {"aset_id": aset_id, "status": "Mutasi"}
        )

class SameRoomMutationError(BusinessRuleError):
    """Mutasi ke ruangan yang sama."""
    def __init__(self, ruangan_id: str):
        super().__init__(
            "Ruangan tujuan tidak boleh sama dengan ruangan asal",
            {"ruangan_id": ruangan_id}
        )

class CannotDeleteSelfError(BusinessRuleError):
    """Admin tidak bisa menghapus dirinya sendiri."""
    def __init__(self):
        super().__init__("Anda tidak dapat menghapus akun sendiri")


# === Resource Exceptions ===
class ResourceNotFoundError(SimanisException):
    """Resource tidak ditemukan."""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            f"{resource_type} dengan ID '{resource_id}' tidak ditemukan",
            "NOT_FOUND",
            {"resource_type": resource_type, "resource_id": resource_id},
            404
        )

class AssetNotFoundError(ResourceNotFoundError):
    """Aset tidak ditemukan."""
    def __init__(self, aset_id: str):
        super().__init__("Aset", aset_id)

class UserNotFoundError(ResourceNotFoundError):
    """User tidak ditemukan."""
    def __init__(self, user_id: str):
        super().__init__("User", user_id)

class RuanganNotFoundError(ResourceNotFoundError):
    """Ruangan tidak ditemukan."""
    def __init__(self, ruangan_id: str):
        super().__init__("Ruangan", ruangan_id)


# === Database Exceptions ===
class DatabaseError(SimanisException):
    """Error terkait database."""
    def __init__(self, message: str = "Terjadi kesalahan database", details: Optional[Dict] = None):
        super().__init__(message, "DB_ERROR", details, 500)

class DatabaseConnectionError(DatabaseError):
    """Tidak dapat terhubung ke database."""
    def __init__(self):
        super().__init__("Tidak dapat terhubung ke database")

class DatabaseLockedError(DatabaseError):
    """Database sedang terkunci."""
    def __init__(self):
        super().__init__("Database sedang sibuk, silakan coba lagi")
```


---

## Error Handling Middleware (Backend)

### Global Exception Handler

```python
# app/api/middleware.py

import logging
import traceback
from uuid import uuid4
from contextvars import ContextVar
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import SimanisException
from app.schemas.response import ErrorResponse

# Context variable untuk correlation ID
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="")

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware untuk menangani semua exception secara terpusat."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate correlation ID untuk request tracking
        correlation_id = str(uuid4())[:8]
        correlation_id_ctx.set(correlation_id)
        
        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = correlation_id
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
                    "method": request.method
                }
            )
            return JSONResponse(
                status_code=e.status_code,
                content=ErrorResponse(
                    success=False,
                    error_code=e.error_code,
                    message=e.message,
                    details=e.details,
                    correlation_id=correlation_id
                ).model_dump(),
                headers={"X-Correlation-ID": correlation_id}
            )
            
        except Exception as e:
            # Unexpected exception - log full traceback
            logger.error(
                f"Unexpected error: {str(e)}",
                extra={
                    "correlation_id": correlation_id,
                    "path": request.url.path,
                    "method": request.method,
                    "traceback": traceback.format_exc()
                },
                exc_info=True
            )
            return JSONResponse(
                status_code=500,
                content=ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="Terjadi kesalahan internal. Silakan hubungi administrator.",
                    details={"correlation_id": correlation_id},
                    correlation_id=correlation_id
                ).model_dump(),
                headers={"X-Correlation-ID": correlation_id}
            )
```

### Standard Response Schemas

```python
# app/schemas/response.py

from typing import TypeVar, Generic, Optional, Dict, Any, List
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response."""
    success: bool = True
    data: T
    message: Optional[str] = None
    correlation_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response untuk list endpoints."""
    success: bool = True
    data: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    correlation_id: Optional[str] = None
```


---

## Structured Logging (Backend)

### Logging Configuration

```python
# app/core/logging.py

import logging
import sys
import json
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from app.core.config import settings
from app.api.middleware import correlation_id_ctx


class StructuredFormatter(logging.Formatter):
    """JSON formatter untuk structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id_ctx.get(""),
        }
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add location info for errors
        if record.levelno >= logging.ERROR:
            log_data["location"] = {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName
            }
        
        return json.dumps(log_data, ensure_ascii=False, default=str)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable formatter untuk development."""
    
    def format(self, record: logging.LogRecord) -> str:
        correlation_id = correlation_id_ctx.get("")
        prefix = f"[{correlation_id}] " if correlation_id else ""
        return f"{record.levelname:8} {prefix}{record.getMessage()}"


def setup_logging() -> None:
    """Setup logging configuration."""
    
    # Create logs directory
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # === File Handler (JSON format) ===
    file_handler = RotatingFileHandler(
        filename=log_dir / "simanis62.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(file_handler)
    
    # === Console Handler (Human-readable for dev) ===
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    console_handler.setFormatter(HumanReadableFormatter())
    root_logger.addHandler(console_handler)
    
    # === Error File Handler (Errors only) ===
    error_handler = RotatingFileHandler(
        filename=log_dir / "simanis62_error.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(error_handler)
    
    # === GlitchTip Integration ===
    if settings.GLITCHTIP_DSN:
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )
        sentry_sdk.init(
            dsn=settings.GLITCHTIP_DSN,
            integrations=[sentry_logging],
            environment=settings.ENVIRONMENT,
            before_send=filter_sensitive_data,
            traces_sample_rate=0.1
        )


def filter_sensitive_data(event: Dict, hint: Dict) -> Dict:
    """Filter data sensitif sebelum kirim ke GlitchTip."""
    
    # Filter request data
    if "request" in event:
        if "data" in event["request"]:
            event["request"]["data"] = "[FILTERED]"
        if "cookies" in event["request"]:
            event["request"]["cookies"] = "[FILTERED]"
        if "headers" in event["request"]:
            # Keep only safe headers
            safe_headers = ["content-type", "user-agent", "x-correlation-id"]
            event["request"]["headers"] = {
                k: v for k, v in event["request"]["headers"].items()
                if k.lower() in safe_headers
            }
    
    # Filter user data
    if "user" in event:
        if "email" in event["user"]:
            event["user"]["email"] = "[FILTERED]"
        if "username" in event["user"]:
            event["user"]["username"] = "[FILTERED]"
    
    return event
```

### Logging Usage Example

```python
# Contoh penggunaan logging di service

import logging
from app.api.middleware import correlation_id_ctx

logger = logging.getLogger(__name__)


class AssetService:
    async def create_asset(self, data: AssetCreate) -> Asset:
        correlation_id = correlation_id_ctx.get()
        
        logger.info(
            f"Creating asset: {data.nama_barang}",
            extra={
                "correlation_id": correlation_id,
                "action": "create_asset",
                "kategori_kib": data.kategori_kib,
                "kode_barang": data.kode_barang
            }
        )
        
        try:
            asset = await self.repository.create(data)
            logger.info(
                f"Asset created successfully: {asset.id}",
                extra={
                    "correlation_id": correlation_id,
                    "action": "create_asset",
                    "asset_id": str(asset.id),
                    "result": "success"
                }
            )
            return asset
            
        except DuplicateKodeBarangError as e:
            logger.warning(
                f"Duplicate kode_barang: {data.kode_barang}",
                extra={
                    "correlation_id": correlation_id,
                    "action": "create_asset",
                    "error": "duplicate_kode_barang",
                    "kode_barang": data.kode_barang
                }
            )
            raise
```


---

## SQLite Database Configuration (WAL Mode)

### Database Connection Manager

```python
# app/core/database.py

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manager untuk SQLite database dengan WAL mode."""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
    
    async def initialize(self) -> None:
        """Initialize database connection dengan optimal settings."""
        
        # Ensure database directory exists
        db_path = Path(settings.DATABASE_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create async engine dengan SQLite optimizations
        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///{db_path}",
            echo=settings.DEBUG,
            connect_args={
                "check_same_thread": False,
                "timeout": 30  # 30 seconds timeout
            },
            poolclass=StaticPool  # Single connection pool untuk SQLite
        )
        
        # Configure SQLite pragmas untuk performance dan reliability
        async with self.engine.begin() as conn:
            # WAL mode untuk concurrent reads
            await conn.execute("PRAGMA journal_mode=WAL")
            
            # Busy timeout untuk menghindari "database is locked"
            await conn.execute("PRAGMA busy_timeout=30000")  # 30 seconds
            
            # Synchronous NORMAL untuk balance performance/safety
            await conn.execute("PRAGMA synchronous=NORMAL")
            
            # Cache size (negative = KB, positive = pages)
            await conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
            
            # Foreign keys enforcement
            await conn.execute("PRAGMA foreign_keys=ON")
            
            # Temp store in memory
            await conn.execute("PRAGMA temp_store=MEMORY")
            
            # Memory-mapped I/O
            await conn.execute("PRAGMA mmap_size=268435456")  # 256MB
        
        # Create session factory
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )
        
        logger.info(
            "Database initialized",
            extra={
                "database_path": str(db_path),
                "journal_mode": "WAL",
                "busy_timeout": 30000
            }
        )
    
    async def create_tables(self) -> None:
        """Create all tables dari SQLModel metadata."""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables created")
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session dengan automatic cleanup."""
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            await session.close()
    
    async def close(self) -> None:
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")


# Global database manager instance
db_manager = DatabaseManager()


# Dependency untuk FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency untuk database session."""
    async with db_manager.get_session() as session:
        yield session
```

### Database Health Check

```python
# app/core/database.py (continued)

async def check_database_health() -> Dict[str, Any]:
    """Check database health dan return status."""
    try:
        async with db_manager.get_session() as session:
            # Check connection
            result = await session.execute("SELECT 1")
            
            # Check WAL mode
            wal_result = await session.execute("PRAGMA journal_mode")
            journal_mode = wal_result.scalar()
            
            # Check integrity
            integrity_result = await session.execute("PRAGMA integrity_check")
            integrity = integrity_result.scalar()
            
            # Get database size
            db_path = Path(settings.DATABASE_PATH)
            db_size = db_path.stat().st_size if db_path.exists() else 0
            
            return {
                "status": "healthy",
                "journal_mode": journal_mode,
                "integrity": integrity,
                "database_size_mb": round(db_size / (1024 * 1024), 2),
                "path": str(db_path)
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```


---

## Repository Pattern (Backend)

### Base Repository

```python
# app/repositories/base.py

from typing import TypeVar, Generic, Type, Optional, List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """Base repository dengan CRUD operations."""
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """Get single record by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == str(id))
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None
    ) -> List[ModelType]:
        """Get all records dengan pagination dan optional filters."""
        query = select(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def count(self, filters: Optional[dict] = None) -> int:
        """Count records dengan optional filters."""
        query = select(func.count()).select_from(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)
        
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def create(self, obj_in: SQLModel) -> ModelType:
        """Create new record."""
        db_obj = self.model.model_validate(obj_in)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def update(self, id: UUID, obj_in: dict) -> Optional[ModelType]:
        """Update existing record."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def delete(self, id: UUID) -> bool:
        """Hard delete record."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        
        await self.session.delete(db_obj)
        await self.session.flush()
        return True
```

### Asset Repository (Specialized)

```python
# app/repositories/aset_repository.py

from typing import Optional, List
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aset import Aset, StatusAset, KategoriKIB
from app.repositories.base import BaseRepository


class AssetRepository(BaseRepository[Aset]):
    """Repository khusus untuk Aset dengan business-specific queries."""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Aset, session)
    
    async def get_by_kode_barang(self, kode_barang: str) -> Optional[Aset]:
        """Get asset by kode_barang."""
        result = await self.session.execute(
            select(Aset).where(Aset.kode_barang == kode_barang)
        )
        return result.scalar_one_or_none()
    
    async def search(
        self,
        keyword: Optional[str] = None,
        kategori_kib: Optional[KategoriKIB] = None,
        status: Optional[StatusAset] = None,
        ruangan_id: Optional[UUID] = None,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Aset]:
        """Search assets dengan multiple filters."""
        query = select(Aset)
        
        # Exclude deleted unless explicitly requested
        if not include_deleted:
            query = query.where(Aset.status != StatusAset.DIHAPUS)
        
        # Keyword search (case-insensitive)
        if keyword:
            keyword_filter = or_(
                Aset.kode_barang.ilike(f"%{keyword}%"),
                Aset.nama_barang.ilike(f"%{keyword}%")
            )
            query = query.where(keyword_filter)
        
        # Category filter
        if kategori_kib:
            query = query.where(Aset.kategori_kib == kategori_kib)
        
        # Status filter
        if status:
            query = query.where(Aset.status == status)
        
        # Room filter
        if ruangan_id:
            query = query.where(Aset.ruangan_id == str(ruangan_id))
        
        # Pagination
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_next_nomor_register(self, kategori_kib: KategoriKIB) -> int:
        """Get next nomor_register untuk kategori KIB tertentu."""
        result = await self.session.execute(
            select(func.max(Aset.nomor_register))
            .where(Aset.kategori_kib == kategori_kib)
        )
        max_register = result.scalar() or 0
        return max_register + 1
    
    async def get_for_kib_report(
        self,
        kategori_kib: KategoriKIB
    ) -> List[Aset]:
        """Get assets untuk KIB report (status Aktif atau Rusak)."""
        result = await self.session.execute(
            select(Aset)
            .where(
                and_(
                    Aset.kategori_kib == kategori_kib,
                    Aset.status.in_([StatusAset.AKTIF, StatusAset.RUSAK])
                )
            )
            .order_by(Aset.nomor_register)
        )
        return list(result.scalars().all())
    
    async def soft_delete(
        self,
        id: UUID,
        deleted_by: UUID,
        delete_reason: str
    ) -> Optional[Aset]:
        """Soft delete asset dengan reason."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        
        db_obj.status = StatusAset.DIHAPUS
        db_obj.deleted_by = str(deleted_by)
        db_obj.deleted_at = datetime.utcnow()
        db_obj.alasan_hapus = delete_reason
        
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj
```


---

## Service Layer Pattern (Backend)

### Base Service

```python
# app/services/base.py

import logging
from typing import TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[RepositoryType]):
    """Base service dengan common functionality."""
    
    def __init__(self, repository: RepositoryType, session: AsyncSession):
        self.repository = repository
        self.session = session
        self.logger = logging.getLogger(self.__class__.__name__)
```

### Asset Service

```python
# app/services/aset_service.py

import logging
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AssetNotFoundError,
    AssetInMutationError,
    DuplicateKodeBarangError,
    InvalidKodeBarangFormatError,
    InvalidTahunPerolehanError,
    InvalidHargaError,
    DeleteReasonTooShortError
)
from app.models.aset import Aset, StatusAset, KategoriKIB, Kondisi
from app.repositories.aset_repository import AssetRepository
from app.schemas.aset import AssetCreate, AssetUpdate, AssetSearchParams
from app.services.base import BaseService
from app.api.middleware import correlation_id_ctx

logger = logging.getLogger(__name__)


class AssetService(BaseService[AssetRepository]):
    """Service untuk business logic Aset."""
    
    def __init__(self, session: AsyncSession):
        repository = AssetRepository(session)
        super().__init__(repository, session)
    
    # === Validation Methods ===
    
    def _validate_kode_barang_format(self, kode_barang: str) -> None:
        """Validate format kode_barang (XX.XX.XX.XXXX)."""
        import re
        pattern = r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$"
        if not re.match(pattern, kode_barang):
            raise InvalidKodeBarangFormatError(kode_barang)
    
    def _validate_tahun_perolehan(self, tahun: int) -> None:
        """Validate tahun_perolehan (1900 - current year)."""
        current_year = datetime.now().year
        if tahun < 1900 or tahun > current_year:
            raise InvalidTahunPerolehanError(tahun, current_year)
    
    def _validate_harga(self, harga: int) -> None:
        """Validate harga (positive, max 999.999.999.999)."""
        if harga <= 0 or harga > 999_999_999_999:
            raise InvalidHargaError(harga)
    
    def _validate_delete_reason(self, reason: str) -> None:
        """Validate delete reason (min 20 characters)."""
        if len(reason) < 20:
            raise DeleteReasonTooShortError(len(reason))
    
    # === CRUD Operations ===
    
    async def create_asset(
        self,
        data: AssetCreate,
        created_by: UUID
    ) -> Aset:
        """Create new asset dengan validasi."""
        correlation_id = correlation_id_ctx.get()
        
        # Validations
        self._validate_kode_barang_format(data.kode_barang)
        self._validate_tahun_perolehan(data.tahun_perolehan)
        self._validate_harga(data.harga)
        
        # Check duplicate kode_barang
        existing = await self.repository.get_by_kode_barang(data.kode_barang)
        if existing:
            raise DuplicateKodeBarangError(data.kode_barang)
        
        # Get next nomor_register
        nomor_register = await self.repository.get_next_nomor_register(data.kategori_kib)
        
        # Create asset
        asset_data = data.model_dump()
        asset_data.update({
            "nomor_register": nomor_register,
            "status": StatusAset.BARU,
            "created_by": str(created_by),
            "created_at": datetime.utcnow()
        })
        
        asset = await self.repository.create(Aset(**asset_data))
        
        logger.info(
            f"Asset created: {asset.id}",
            extra={
                "correlation_id": correlation_id,
                "action": "create_asset",
                "asset_id": str(asset.id),
                "kode_barang": asset.kode_barang,
                "kategori_kib": asset.kategori_kib,
                "created_by": str(created_by)
            }
        )
        
        return asset
    
    async def update_asset(
        self,
        asset_id: UUID,
        data: AssetUpdate,
        updated_by: UUID
    ) -> Aset:
        """Update existing asset dengan validasi."""
        correlation_id = correlation_id_ctx.get()
        
        # Get existing asset
        asset = await self.repository.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundError(str(asset_id))
        
        # Cannot update if in mutation
        if asset.status == StatusAset.MUTASI:
            raise AssetInMutationError(str(asset_id))
        
        # Validate fields if provided
        if data.tahun_perolehan:
            self._validate_tahun_perolehan(data.tahun_perolehan)
        if data.harga:
            self._validate_harga(data.harga)
        
        # Check duplicate kode_barang if changed
        if data.kode_barang and data.kode_barang != asset.kode_barang:
            self._validate_kode_barang_format(data.kode_barang)
            existing = await self.repository.get_by_kode_barang(data.kode_barang)
            if existing:
                raise DuplicateKodeBarangError(data.kode_barang)
        
        # Auto-update status based on kondisi
        update_data = data.model_dump(exclude_unset=True)
        if "kondisi" in update_data:
            kondisi = update_data["kondisi"]
            if kondisi in [Kondisi.RUSAK_RINGAN, Kondisi.RUSAK_BERAT]:
                update_data["status"] = StatusAset.RUSAK
            elif kondisi == Kondisi.BAIK and asset.status == StatusAset.RUSAK:
                update_data["status"] = StatusAset.AKTIF
        
        update_data.update({
            "updated_by": str(updated_by),
            "updated_at": datetime.utcnow()
        })
        
        updated_asset = await self.repository.update(asset_id, update_data)
        
        logger.info(
            f"Asset updated: {asset_id}",
            extra={
                "correlation_id": correlation_id,
                "action": "update_asset",
                "asset_id": str(asset_id),
                "updated_fields": list(update_data.keys()),
                "updated_by": str(updated_by)
            }
        )
        
        return updated_asset
    
    async def delete_asset(
        self,
        asset_id: UUID,
        delete_reason: str,
        deleted_by: UUID
    ) -> Aset:
        """Soft delete asset dengan reason."""
        correlation_id = correlation_id_ctx.get()
        
        # Validate reason
        self._validate_delete_reason(delete_reason)
        
        # Get existing asset
        asset = await self.repository.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundError(str(asset_id))
        
        # Cannot delete if in mutation
        if asset.status == StatusAset.MUTASI:
            raise AssetInMutationError(str(asset_id))
        
        # Soft delete
        deleted_asset = await self.repository.soft_delete(
            asset_id, deleted_by, delete_reason
        )
        
        logger.info(
            f"Asset deleted: {asset_id}",
            extra={
                "correlation_id": correlation_id,
                "action": "delete_asset",
                "asset_id": str(asset_id),
                "delete_reason": delete_reason[:50],  # Truncate for log
                "deleted_by": str(deleted_by)
            }
        )
        
        return deleted_asset
    
    async def search_assets(
        self,
        params: AssetSearchParams,
        include_deleted: bool = False
    ) -> tuple[List[Aset], int]:
        """Search assets dengan pagination."""
        assets = await self.repository.search(
            keyword=params.keyword,
            kategori_kib=params.kategori_kib,
            status=params.status,
            ruangan_id=params.ruangan_id,
            include_deleted=include_deleted,
            skip=params.skip,
            limit=params.limit
        )
        
        total = await self.repository.count({
            "kategori_kib": params.kategori_kib,
            "status": params.status
        })
        
        return assets, total
```

### Mutation Service

```python
# app/services/mutasi_service.py

from datetime import datetime, timedelta
from app.models.mutasi import Mutation, StatusMutasi

class MutationService(BaseService[MutationRepository]):
    """Service untuk logic mutasi aset."""
    
    async def create_request(self, data: MutationCreate, user_id: UUID) -> Mutation:
        """Create request mutasi baru."""
        # Logic implementation
        pass

    async def cleanup_expired_mutations(self) -> int:
        """Auto-cancel pending mutations older than 7 days (Startup Job)."""
        # Logic: Update status to CANCELLED for expired mutations
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        return await self.repository.cancel_expired(cutoff_date)
```


---

## Dependency Injection (Backend)

### FastAPI Dependencies

```python
# app/api/deps.py

from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_session
from app.core.exceptions import AuthenticationError, AuthorizationError, InsufficientPermissionError
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.services.aset_service import AssetService
from app.services.auth_service import AuthService
from app.services.mutasi_service import MutationService
from app.services.kib_service import KibService


# === Database Session ===
SessionDep = Annotated[AsyncSession, Depends(get_db)]


# === Authentication ===
async def get_current_user(
    session: SessionDep,
    simanis62_session: Optional[str] = Cookie(None)
) -> User:
    """Get current authenticated user dari session cookie."""
    if not simanis62_session:
        raise AuthenticationError("Session tidak ditemukan")
    
    # Verify session
    user_id = await verify_session(simanis62_session)
    if not user_id:
        raise AuthenticationError("Session tidak valid atau sudah expired")
    
    # Get user
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(UUID(user_id))
    
    if not user:
        raise AuthenticationError("User tidak ditemukan")
    
    if user.status != "Aktif":
        raise AuthenticationError("Akun tidak aktif")
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


# === Authorization ===
async def require_admin(current_user: CurrentUser) -> User:
    """Require Admin role."""
    if current_user.role != UserRole.ADMIN:
        raise InsufficientPermissionError("Admin")
    return current_user


async def require_export_permission(current_user: CurrentUser) -> User:
    """Require export permission (Admin atau Viewer dengan dapat_ekspor=True)."""
    if current_user.role == UserRole.ADMIN:
        return current_user
    
    if current_user.role == UserRole.VIEWER and current_user.dapat_ekspor:
        return current_user
    
    raise InsufficientPermissionError("Admin atau Kepala Sekolah")


AdminUser = Annotated[User, Depends(require_admin)]
ExportUser = Annotated[User, Depends(require_export_permission)]


# === Service Dependencies ===
def get_asset_service(session: SessionDep) -> AssetService:
    """Get AssetService instance."""
    return AssetService(session)


def get_auth_service(session: SessionDep) -> AuthService:
    """Get AuthService instance."""
    return AuthService(session)


def get_mutation_service(session: SessionDep) -> MutationService:
    """Get MutationService instance."""
    return MutationService(session)


def get_kib_service(session: SessionDep) -> KibService:
    """Get KibService instance."""
    return KibService(session)


AssetServiceDep = Annotated[AssetService, Depends(get_asset_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
MutationServiceDep = Annotated[MutationService, Depends(get_mutation_service)]
KibServiceDep = Annotated[KibService, Depends(get_kib_service)]
```

### API Route Example

```python
# app/api/v1/aset.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.deps import (
    CurrentUser, AdminUser, AssetServiceDep
)
from app.schemas.aset import (
    AssetCreate, AssetUpdate, AssetResponse, AssetSearchParams
)
from app.schemas.response import SuccessResponse, PaginatedResponse

router = APIRouter(prefix="/aset", tags=["Aset"])


@router.post(
    "/",
    response_model=SuccessResponse[AssetResponse],
    status_code=status.HTTP_201_CREATED
)
async def create_asset(
    data: AssetCreate,
    service: AssetServiceDep,
    current_user: AdminUser  # Only Admin can create
):
    """Create new asset."""
    asset = await service.create_asset(data, current_user.id)
    return SuccessResponse(
        data=AssetResponse.model_validate(asset),
        message="Aset berhasil ditambahkan"
    )


@router.get(
    "/",
    response_model=PaginatedResponse[AssetResponse]
)
async def search_assets(
    service: AssetServiceDep,
    current_user: CurrentUser,  # All authenticated users
    keyword: str = Query(None, min_length=1),
    kategori_kib: str = Query(None),
    status: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100)
):
    """Search assets dengan filters."""
    params = AssetSearchParams(
        keyword=keyword,
        kategori_kib=kategori_kib,
        status=status,
        skip=(page - 1) * page_size,
        limit=page_size
    )
    
    # Viewer tidak bisa lihat deleted assets
    include_deleted = current_user.role == "Admin"
    
    assets, total = await service.search_assets(params, include_deleted)
    
    return PaginatedResponse(
        data=[AssetResponse.model_validate(a) for a in assets],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get(
    "/{asset_id}",
    response_model=SuccessResponse[AssetResponse]
)
async def get_asset(
    asset_id: UUID,
    service: AssetServiceDep,
    current_user: CurrentUser
):
    """Get asset by ID."""
    asset = await service.get_asset_by_id(asset_id)
    return SuccessResponse(data=AssetResponse.model_validate(asset))


@router.put(
    "/{asset_id}",
    response_model=SuccessResponse[AssetResponse]
)
async def update_asset(
    asset_id: UUID,
    data: AssetUpdate,
    service: AssetServiceDep,
    current_user: AdminUser  # Only Admin can update
):
    """Update existing asset."""
    asset = await service.update_asset(asset_id, data, current_user.id)
    return SuccessResponse(
        data=AssetResponse.model_validate(asset),
        message="Aset berhasil diperbarui"
    )


@router.delete(
    "/{asset_id}",
    response_model=SuccessResponse[AssetResponse]
)
async def delete_asset(
    asset_id: UUID,
    delete_reason: str = Query(..., min_length=20),
    service: AssetServiceDep,
    current_user: AdminUser  # Only Admin can delete
):
    """Soft delete asset."""
    asset = await service.delete_asset(asset_id, delete_reason, current_user.id)
    return SuccessResponse(
        data=AssetResponse.model_validate(asset),
        message="Aset berhasil dihapus"
    )
```


---

## Frontend Architecture (WPF .NET 8)

### Directory Structure

```
frontend/Simanis62.WPF/
├── App.xaml                       # Application entry
├── App.xaml.cs                    # App startup, DI setup
├── MainWindow.xaml                # Main window shell
│
├── Core/                          # Infrastructure Layer
│   ├── Configuration/
│   │   └── AppSettings.cs         # Configuration model
│   ├── Exceptions/
│   │   ├── SimanisException.cs    # Base exception
│   │   ├── ApiException.cs        # API error wrapper
│   │   └── ValidationException.cs # Validation errors
│   ├── Logging/
│   │   └── LoggingService.cs      # Serilog setup
│   └── Extensions/
│       └── ServiceCollectionExtensions.cs
│
├── Services/                      # Application Layer
│   ├── Interfaces/
│   │   ├── IApiService.cs
│   │   ├── IAuthService.cs
│   │   ├── IAssetService.cs
│   │   └── INavigationService.cs
│   ├── ApiService.cs              # Refit HTTP client
│   ├── AuthService.cs
│   ├── AssetService.cs
│   └── NavigationService.cs
│
├── Models/                        # Domain Layer
│   ├── User.cs
│   ├── Asset.cs
│   ├── Mutation.cs
│   ├── Room.cs
│   └── ApiResponse.cs
│
├── ViewModels/                    # Presentation Layer
│   ├── Base/
│   │   ├── ViewModelBase.cs       # Base with INotifyPropertyChanged
│   │   └── AsyncRelayCommand.cs   # Async command support
│   ├── LoginViewModel.cs
│   ├── DashboardViewModel.cs
│   ├── AssetListViewModel.cs
│   ├── AssetDetailViewModel.cs
│   ├── AssetFormViewModel.cs
│   ├── MutationViewModel.cs
│   └── KibReportViewModel.cs
│
├── Views/                         # Presentation Layer (XAML)
│   ├── LoginView.xaml
│   ├── DashboardView.xaml
│   ├── AssetListView.xaml
│   ├── AssetDetailView.xaml
│   ├── AssetFormView.xaml
│   ├── MutationView.xaml
│   └── KibReportView.xaml
│
├── Controls/                      # Reusable UI Components
│   ├── LoadingOverlay.xaml
│   ├── ErrorDisplay.xaml
│   └── PaginationControl.xaml
│
├── Converters/                    # Value Converters
│   ├── BoolToVisibilityConverter.cs
│   ├── StatusToColorConverter.cs
│   └── CurrencyConverter.cs
│
└── Resources/                     # Styles & Resources
    ├── Styles/
    │   └── CommonStyles.xaml
    └── Themes/
        └── MaterialDesignTheme.xaml
```


### Exception Hierarchy (Frontend)

```csharp
// Core/Exceptions/SimanisException.cs

namespace Simanis62.WPF.Core.Exceptions;

/// <summary>
/// Base exception untuk semua error SIMANIS62 WPF.
/// </summary>
public class SimanisException : Exception
{
    public string ErrorCode { get; }
    public Dictionary<string, object>? Details { get; }
    public string? CorrelationId { get; }

    public SimanisException(
        string message,
        string errorCode,
        Dictionary<string, object>? details = null,
        string? correlationId = null,
        Exception? innerException = null)
        : base(message, innerException)
    {
        ErrorCode = errorCode;
        Details = details;
        CorrelationId = correlationId;
    }
}

/// <summary>
/// Exception untuk error dari API.
/// </summary>
public class ApiException : SimanisException
{
    public int StatusCode { get; }

    public ApiException(
        string message,
        string errorCode,
        int statusCode,
        Dictionary<string, object>? details = null,
        string? correlationId = null)
        : base(message, errorCode, details, correlationId)
    {
        StatusCode = statusCode;
    }

    public static ApiException FromResponse(ApiErrorResponse response)
    {
        return new ApiException(
            response.Message,
            response.ErrorCode,
            response.StatusCode,
            response.Details,
            response.CorrelationId
        );
    }
}

/// <summary>
/// Exception untuk error koneksi.
/// </summary>
public class ConnectionException : SimanisException
{
    public ConnectionException(string message, Exception? innerException = null)
        : base(message, "CONNECTION_ERROR", null, null, innerException)
    {
    }
}

/// <summary>
/// Exception untuk session expired.
/// </summary>
public class SessionExpiredException : SimanisException
{
    public SessionExpiredException()
        : base("Session telah berakhir, silakan login kembali", "SESSION_EXPIRED")
    {
    }
}

/// <summary>
/// Exception untuk validasi input.
/// </summary>
public class ValidationException : SimanisException
{
    public string FieldName { get; }

    public ValidationException(string message, string fieldName)
        : base(message, "VALIDATION_ERROR", new Dictionary<string, object> { { "field", fieldName } })
    {
        FieldName = fieldName;
    }
}
```

### Global Error Handler (Frontend)

```csharp
// App.xaml.cs

public partial class App : Application
{
    private IServiceProvider _serviceProvider = null!;
    private ILogger<App> _logger = null!;

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // Setup DI
        var services = new ServiceCollection();
        ConfigureServices(services);
        _serviceProvider = services.BuildServiceProvider();
        _logger = _serviceProvider.GetRequiredService<ILogger<App>>();

        // Setup global exception handlers
        SetupExceptionHandlers();

        // Show main window
        var mainWindow = _serviceProvider.GetRequiredService<MainWindow>();
        mainWindow.Show();
    }

    private void SetupExceptionHandlers()
    {
        // UI Thread exceptions
        DispatcherUnhandledException += OnDispatcherUnhandledException;

        // Non-UI Thread exceptions
        AppDomain.CurrentDomain.UnhandledException += OnUnhandledException;

        // Task exceptions
        TaskScheduler.UnobservedTaskException += OnUnobservedTaskException;
    }

    private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
    {
        HandleException(e.Exception, "UI Thread");
        e.Handled = true;
    }

    private void OnUnhandledException(object sender, UnhandledExceptionEventArgs e)
    {
        if (e.ExceptionObject is Exception ex)
        {
            HandleException(ex, "AppDomain");
        }
    }

    private void OnUnobservedTaskException(object? sender, UnobservedTaskExceptionEventArgs e)
    {
        HandleException(e.Exception, "Task");
        e.SetObserved();
    }

    private void HandleException(Exception exception, string source)
    {
        var correlationId = Guid.NewGuid().ToString()[..8];

        // Log exception
        _logger.LogError(
            exception,
            "Unhandled exception from {Source}. CorrelationId: {CorrelationId}",
            source,
            correlationId
        );

        // Determine user message
        string userMessage = exception switch
        {
            SimanisException simanisEx => simanisEx.Message,
            HttpRequestException => "Tidak dapat terhubung ke server. Periksa koneksi jaringan.",
            TaskCanceledException => "Operasi dibatalkan atau timeout.",
            _ => $"Terjadi kesalahan. Kode referensi: {correlationId}"
        };

        // Show error dialog
        Application.Current.Dispatcher.Invoke(() =>
        {
            MessageBox.Show(
                userMessage,
                "Error",
                MessageBoxButton.OK,
                MessageBoxImage.Error
            );
        });

        // Handle session expired
        if (exception is SessionExpiredException)
        {
            Application.Current.Dispatcher.Invoke(() =>
            {
                var navigationService = _serviceProvider.GetRequiredService<INavigationService>();
                navigationService.NavigateTo<LoginViewModel>();
            });
        }
    }

    private void ConfigureServices(IServiceCollection services)
    {
        // Logging
        services.AddLogging(builder =>
        {
            builder.AddSerilog(new LoggerConfiguration()
                .MinimumLevel.Information()
                .WriteTo.File(
                    "logs/simanis62-wpf.log",
                    rollingInterval: RollingInterval.Day,
                    retainedFileCountLimit: 7,
                    outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff} [{Level:u3}] {Message:lj}{NewLine}{Exception}"
                )
                .WriteTo.Sentry(o =>
                {
                    o.Dsn = Configuration["GlitchTip:Dsn"];
                    o.MinimumEventLevel = LogEventLevel.Error;
                })
                .CreateLogger()
            );
        });

        // HTTP Client with Polly
        services.AddHttpClient<IApiService, ApiService>(client =>
        {
            client.BaseAddress = new Uri(Configuration["Api:BaseUrl"]!);
            client.Timeout = TimeSpan.FromSeconds(30);
        })
        .AddTransientHttpErrorPolicy(policy =>
            policy.WaitAndRetryAsync(3, retryAttempt =>
                TimeSpan.FromSeconds(Math.Pow(2, retryAttempt))
            )
        );

        // Services
        services.AddSingleton<INavigationService, NavigationService>();
        services.AddTransient<IAuthService, AuthService>();
        services.AddTransient<IAssetService, AssetService>();

        // ViewModels
        services.AddTransient<LoginViewModel>();
        services.AddTransient<DashboardViewModel>();
        services.AddTransient<AssetListViewModel>();

        // Views
        services.AddTransient<MainWindow>();
        services.AddTransient<LoginView>();
        services.AddTransient<DashboardView>();
    }
}
```


### ViewModel Base Class

```csharp
// ViewModels/Base/ViewModelBase.cs

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Extensions.Logging;

namespace Simanis62.WPF.ViewModels.Base;

/// <summary>
/// Base ViewModel dengan common functionality.
/// </summary>
public abstract partial class ViewModelBase : ObservableObject
{
    protected readonly ILogger Logger;

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(IsNotBusy))]
    private bool _isBusy;

    [ObservableProperty]
    private string? _errorMessage;

    [ObservableProperty]
    private bool _hasError;

    public bool IsNotBusy => !IsBusy;

    protected ViewModelBase(ILogger logger)
    {
        Logger = logger;
    }

    /// <summary>
    /// Execute async operation dengan error handling.
    /// </summary>
    protected async Task ExecuteAsync(
        Func<Task> operation,
        string operationName,
        bool showBusy = true)
    {
        if (showBusy) IsBusy = true;
        ClearError();

        try
        {
            await operation();
        }
        catch (ValidationException ex)
        {
            SetError(ex.Message);
            Logger.LogWarning("Validation error in {Operation}: {Message}", operationName, ex.Message);
        }
        catch (ApiException ex)
        {
            SetError(ex.Message);
            Logger.LogWarning(
                "API error in {Operation}: {ErrorCode} - {Message}. CorrelationId: {CorrelationId}",
                operationName, ex.ErrorCode, ex.Message, ex.CorrelationId
            );
        }
        catch (ConnectionException ex)
        {
            SetError("Tidak dapat terhubung ke server. Periksa koneksi jaringan.");
            Logger.LogError(ex, "Connection error in {Operation}", operationName);
        }
        catch (SessionExpiredException)
        {
            // Re-throw untuk di-handle oleh global handler
            throw;
        }
        catch (Exception ex)
        {
            var correlationId = Guid.NewGuid().ToString()[..8];
            SetError($"Terjadi kesalahan. Kode: {correlationId}");
            Logger.LogError(ex, "Unexpected error in {Operation}. CorrelationId: {CorrelationId}",
                operationName, correlationId);
        }
        finally
        {
            if (showBusy) IsBusy = false;
        }
    }

    /// <summary>
    /// Execute async operation dengan return value.
    /// </summary>
    protected async Task<T?> ExecuteAsync<T>(
        Func<Task<T>> operation,
        string operationName,
        bool showBusy = true)
    {
        if (showBusy) IsBusy = true;
        ClearError();

        try
        {
            return await operation();
        }
        catch (ValidationException ex)
        {
            SetError(ex.Message);
            Logger.LogWarning("Validation error in {Operation}: {Message}", operationName, ex.Message);
            return default;
        }
        catch (ApiException ex)
        {
            SetError(ex.Message);
            Logger.LogWarning(
                "API error in {Operation}: {ErrorCode} - {Message}",
                operationName, ex.ErrorCode, ex.Message
            );
            return default;
        }
        catch (ConnectionException ex)
        {
            SetError("Tidak dapat terhubung ke server.");
            Logger.LogError(ex, "Connection error in {Operation}", operationName);
            return default;
        }
        catch (SessionExpiredException)
        {
            throw;
        }
        catch (Exception ex)
        {
            var correlationId = Guid.NewGuid().ToString()[..8];
            SetError($"Terjadi kesalahan. Kode: {correlationId}");
            Logger.LogError(ex, "Unexpected error in {Operation}. CorrelationId: {CorrelationId}",
                operationName, correlationId);
            return default;
        }
        finally
        {
            if (showBusy) IsBusy = false;
        }
    }

    protected void SetError(string message)
    {
        ErrorMessage = message;
        HasError = true;
    }

    protected void ClearError()
    {
        ErrorMessage = null;
        HasError = false;
    }
}
```

### Example ViewModel Implementation

```csharp
// ViewModels/AssetListViewModel.cs

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.Extensions.Logging;
using System.Collections.ObjectModel;

namespace Simanis62.WPF.ViewModels;

public partial class AssetListViewModel : ViewModelBase
{
    private readonly IAssetService _assetService;
    private readonly INavigationService _navigationService;

    [ObservableProperty]
    private ObservableCollection<AssetModel> _assets = new();

    [ObservableProperty]
    private string? _searchKeyword;

    [ObservableProperty]
    private string? _selectedKategoriKib;

    [ObservableProperty]
    private int _currentPage = 1;

    [ObservableProperty]
    private int _totalPages;

    [ObservableProperty]
    private int _totalItems;

    public AssetListViewModel(
        IAssetService assetService,
        INavigationService navigationService,
        ILogger<AssetListViewModel> logger)
        : base(logger)
    {
        _assetService = assetService;
        _navigationService = navigationService;
    }

    [RelayCommand]
    private async Task LoadAssetsAsync()
    {
        await ExecuteAsync(async () =>
        {
            var result = await _assetService.SearchAssetsAsync(
                keyword: SearchKeyword,
                kategoriKib: SelectedKategoriKib,
                page: CurrentPage,
                pageSize: 100
            );

            Assets = new ObservableCollection<AssetModel>(result.Data);
            TotalItems = result.Total;
            TotalPages = result.TotalPages;

            Logger.LogInformation(
                "Loaded {Count} assets. Page {Page}/{TotalPages}",
                result.Data.Count, CurrentPage, TotalPages
            );
        }, "LoadAssets");
    }

    [RelayCommand]
    private async Task SearchAsync()
    {
        CurrentPage = 1;
        await LoadAssetsAsync();
    }

    [RelayCommand]
    private async Task NextPageAsync()
    {
        if (CurrentPage < TotalPages)
        {
            CurrentPage++;
            await LoadAssetsAsync();
        }
    }

    [RelayCommand]
    private async Task PreviousPageAsync()
    {
        if (CurrentPage > 1)
        {
            CurrentPage--;
            await LoadAssetsAsync();
        }
    }

    [RelayCommand]
    private void ViewAssetDetail(AssetModel asset)
    {
        _navigationService.NavigateTo<AssetDetailViewModel>(asset.Id);
    }

    [RelayCommand]
    private void CreateNewAsset()
    {
        _navigationService.NavigateTo<AssetFormViewModel>();
    }
}
```


---

## API Service with Refit (Frontend)

### Refit Interface

```csharp
// Services/Interfaces/IApiService.cs

using Refit;

namespace Simanis62.WPF.Services.Interfaces;

public interface IApiService
{
    // === Auth ===
    [Post("/api/v1/auth/login")]
    Task<ApiResponse<LoginResponse>> LoginAsync([Body] LoginRequest request);

    [Post("/api/v1/auth/logout")]
    Task<ApiResponse<object>> LogoutAsync();

    // === Assets ===
    [Get("/api/v1/aset")]
    Task<ApiResponse<PaginatedResponse<AssetModel>>> GetAssetsAsync(
        [Query] string? keyword = null,
        [Query] string? kategori_kib = null,
        [Query] string? status = null,
        [Query] int page = 1,
        [Query] int page_size = 100
    );

    [Get("/api/v1/aset/{id}")]
    Task<ApiResponse<SuccessResponse<AssetModel>>> GetAssetByIdAsync(Guid id);

    [Post("/api/v1/aset")]
    Task<ApiResponse<SuccessResponse<AssetModel>>> CreateAssetAsync([Body] AssetCreateRequest request);

    [Put("/api/v1/aset/{id}")]
    Task<ApiResponse<SuccessResponse<AssetModel>>> UpdateAssetAsync(Guid id, [Body] AssetUpdateRequest request);

    [Delete("/api/v1/aset/{id}")]
    Task<ApiResponse<SuccessResponse<AssetModel>>> DeleteAssetAsync(Guid id, [Query] string delete_reason);

    // === KIB Reports ===
    [Get("/api/v1/kib/{kategori}")]
    Task<ApiResponse<SuccessResponse<List<AssetModel>>>> GetKibReportAsync(string kategori);

    [Get("/api/v1/kib/{kategori}/export")]
    Task<HttpResponseMessage> ExportKibToExcelAsync(string kategori);

    // === Mutations ===
    [Post("/api/v1/mutasi")]
    Task<ApiResponse<SuccessResponse<MutationModel>>> CreateMutationAsync([Body] MutationCreateRequest request);

    [Put("/api/v1/mutasi/{id}/complete")]
    Task<ApiResponse<SuccessResponse<MutationModel>>> CompleteMutationAsync(Guid id);

    [Put("/api/v1/mutasi/{id}/cancel")]
    Task<ApiResponse<SuccessResponse<MutationModel>>> CancelMutationAsync(Guid id, [Body] MutationCancelRequest request);

    // === Rooms ===
    [Get("/api/v1/ruangan")]
    Task<ApiResponse<SuccessResponse<List<RoomModel>>>> GetRoomsAsync();
}
```

### API Service Implementation with Error Handling

```csharp
// Services/ApiService.cs

using Microsoft.Extensions.Logging;
using Refit;
using System.Net;
using System.Text.Json;

namespace Simanis62.WPF.Services;

public class ApiService : IAssetService
{
    private readonly IApiService _api;
    private readonly ILogger<ApiService> _logger;

    public ApiService(HttpClient httpClient, ILogger<ApiService> logger)
    {
        _api = RestService.For<IApiService>(httpClient, new RefitSettings
        {
            ContentSerializer = new SystemTextJsonContentSerializer(new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
            })
        });
        _logger = logger;
    }

    public async Task<PaginatedResponse<AssetModel>> SearchAssetsAsync(
        string? keyword = null,
        string? kategoriKib = null,
        int page = 1,
        int pageSize = 100)
    {
        try
        {
            var response = await _api.GetAssetsAsync(keyword, kategoriKib, null, page, pageSize);

            if (response.IsSuccessStatusCode && response.Content != null)
            {
                return response.Content;
            }

            throw await HandleErrorResponseAsync(response);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Connection error while searching assets");
            throw new ConnectionException("Tidak dapat terhubung ke server", ex);
        }
        catch (ApiException)
        {
            throw;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unexpected error while searching assets");
            throw;
        }
    }

    public async Task<AssetModel> CreateAssetAsync(AssetCreateRequest request)
    {
        try
        {
            var response = await _api.CreateAssetAsync(request);

            if (response.IsSuccessStatusCode && response.Content?.Data != null)
            {
                _logger.LogInformation("Asset created: {AssetId}", response.Content.Data.Id);
                return response.Content.Data;
            }

            throw await HandleErrorResponseAsync(response);
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Connection error while creating asset");
            throw new ConnectionException("Tidak dapat terhubung ke server", ex);
        }
    }

    public async Task<byte[]> ExportKibToExcelAsync(string kategori)
    {
        try
        {
            var response = await _api.ExportKibToExcelAsync(kategori);

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsByteArrayAsync();
            }

            // Handle error response
            var errorContent = await response.Content.ReadAsStringAsync();
            var errorResponse = JsonSerializer.Deserialize<ApiErrorResponse>(errorContent);

            throw new ApiException(
                errorResponse?.Message ?? "Export gagal",
                errorResponse?.ErrorCode ?? "EXPORT_ERROR",
                (int)response.StatusCode,
                errorResponse?.Details,
                errorResponse?.CorrelationId
            );
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Connection error while exporting KIB {Kategori}", kategori);
            throw new ConnectionException("Tidak dapat terhubung ke server", ex);
        }
    }

    private async Task<ApiException> HandleErrorResponseAsync<T>(IApiResponse<T> response)
    {
        var errorContent = response.Error?.Content ?? "";

        try
        {
            var errorResponse = JsonSerializer.Deserialize<ApiErrorResponse>(errorContent);

            // Handle session expired
            if (response.StatusCode == HttpStatusCode.Unauthorized)
            {
                throw new SessionExpiredException();
            }

            return new ApiException(
                errorResponse?.Message ?? "Terjadi kesalahan",
                errorResponse?.ErrorCode ?? "UNKNOWN_ERROR",
                (int)response.StatusCode,
                errorResponse?.Details,
                errorResponse?.CorrelationId
            );
        }
        catch (JsonException)
        {
            return new ApiException(
                "Terjadi kesalahan pada server",
                "SERVER_ERROR",
                (int)response.StatusCode
            );
        }
    }
}
```


---

## Correctness Properties

Berdasarkan requirements, berikut adalah correctness properties yang harus dipenuhi:

### Authentication & Authorization

| ID | Property | Verification |
|----|----------|--------------|
| CP-AUTH-01 | Session timeout setelah 2 jam inaktivitas | Unit test dengan mock time |
| CP-AUTH-02 | Invalid credentials mengembalikan error 401 | Integration test |
| CP-AUTH-03 | Admin dapat akses semua endpoint | Integration test |
| CP-AUTH-04 | Viewer tidak dapat akses CRUD endpoints | Integration test |
| CP-AUTH-05 | Viewer dengan dapat_ekspor=true dapat export | Integration test |

### Asset Management

| ID | Property | Verification |
|----|----------|--------------|
| CP-ASET-01 | kode_barang harus unik | Database constraint + unit test |
| CP-ASET-02 | kode_barang format XX.XX.XX.XXXX | Pydantic validator + unit test |
| CP-ASET-03 | nomor_register auto-increment per kategori_kib | Service layer test |
| CP-ASET-04 | tahun_perolehan antara 1900 dan tahun sekarang | Pydantic validator |
| CP-ASET-05 | harga > 0 dan <= 999.999.999.999 | Pydantic validator |
| CP-ASET-06 | Aset dengan status "Mutasi" tidak dapat diubah/dihapus | Service layer test |
| CP-ASET-07 | Soft delete memerlukan alasan minimal 20 karakter | Pydantic validator |
| CP-ASET-08 | Update kondisi ke "Rusak" otomatis set status "Rusak" | Service layer test |

### Mutation

| ID | Property | Verification |
|----|----------|--------------|
| CP-MUT-01 | Mutasi ke ruangan yang sama ditolak | Service layer test |
| CP-MUT-02 | Alasan mutasi minimal 10 karakter | Pydantic validator |
| CP-MUT-03 | Tanggal mutasi tidak boleh di masa depan | Pydantic validator |
| CP-MUT-04 | Selesai mutasi mengubah ruangan_id aset | Integration test |
| CP-MUT-05 | Batal mutasi mengembalikan status aset ke "Aktif" | Integration test |

### KIB Reports

| ID | Property | Verification |
|----|----------|--------------|
| CP-KIB-01 | KIB report hanya menampilkan status "Aktif" atau "Rusak" | Repository query test |
| CP-KIB-02 | KIB B memiliki 18 kolom sesuai BPAD DKI Jakarta | Export unit test |
| CP-KIB-03 | Harga dalam Rupiah penuh (bukan ribuan) | Export unit test |
| CP-KIB-04 | Generate report < 10 detik untuk 1000 aset | Performance test |
| CP-KIB-05 | Export Excel < 15 detik untuk 1000 aset | Performance test |

### Performance

| ID | Property | Verification |
|----|----------|--------------|
| CP-PERF-01 | Search aset < 5 detik | Performance test |
| CP-PERF-02 | Login < 2 detik | Performance test |
| CP-PERF-03 | View asset detail < 2 detik | Performance test |

### Data Integrity

| ID | Property | Verification |
|----|----------|--------------|
| CP-DATA-01 | Audit trail mencatat semua operasi CRUD | Integration test |
| CP-DATA-02 | Audit trail tidak dapat dimodifikasi | Database constraint |
| CP-DATA-03 | Foreign key constraints enforced | Database constraint |
| CP-DATA-04 | Soft deleted assets tidak muncul di list (kecuali Admin) | Repository query test |

---

## Testing Strategy

### Unit Tests (Backend)

```python
# tests/unit/test_services/test_aset_service.py

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from app.services.aset_service import AssetService
from app.core.exceptions import (
    DuplicateKodeBarangError,
    InvalidKodeBarangFormatError,
    InvalidTahunPerolehanError,
    AssetInMutationError
)
from app.models.aset import StatusAset


class TestAssetServiceValidation:
    """Test validation methods."""

    def test_validate_kode_barang_format_valid(self):
        service = AssetService(MagicMock())
        # Should not raise
        service._validate_kode_barang_format("01.02.03.0001")

    def test_validate_kode_barang_format_invalid(self):
        service = AssetService(MagicMock())
        with pytest.raises(InvalidKodeBarangFormatError):
            service._validate_kode_barang_format("invalid")

    def test_validate_tahun_perolehan_valid(self):
        service = AssetService(MagicMock())
        current_year = datetime.now().year
        service._validate_tahun_perolehan(current_year)

    def test_validate_tahun_perolehan_future(self):
        service = AssetService(MagicMock())
        with pytest.raises(InvalidTahunPerolehanError):
            service._validate_tahun_perolehan(2100)


class TestAssetServiceCreate:
    """Test create asset."""

    @pytest.mark.asyncio
    async def test_create_asset_duplicate_kode_barang(self):
        mock_session = AsyncMock()
        service = AssetService(mock_session)
        service.repository.get_by_kode_barang = AsyncMock(return_value=MagicMock())

        with pytest.raises(DuplicateKodeBarangError):
            await service.create_asset(
                AssetCreate(
                    kode_barang="01.02.03.0001",
                    nama_barang="Test Asset",
                    kategori_kib="B",
                    tahun_perolehan=2024,
                    asal_usul="Pembelian",
                    harga=1000000,
                    kondisi="Baik",
                    ruangan_id="uuid"
                ),
                created_by="user-uuid"
            )


class TestAssetServiceUpdate:
    """Test update asset."""

    @pytest.mark.asyncio
    async def test_update_asset_in_mutation_rejected(self):
        mock_session = AsyncMock()
        service = AssetService(mock_session)

        mock_asset = MagicMock()
        mock_asset.status = StatusAset.MUTASI
        service.repository.get_by_id = AsyncMock(return_value=mock_asset)

        with pytest.raises(AssetInMutationError):
            await service.update_asset(
                "asset-uuid",
                AssetUpdate(nama_barang="Updated"),
                "user-uuid"
            )
```

### Integration Tests (Backend)

```python
# tests/integration/test_api/test_aset_api.py

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
class TestAssetAPI:
    """Integration tests untuk Asset API."""

    async def test_create_asset_as_admin(self, client: AsyncClient, admin_token: str):
        response = await client.post(
            "/api/v1/aset",
            json={
                "kode_barang": "01.02.03.0001",
                "nama_barang": "Komputer Desktop",
                "kategori_kib": "B",
                "tahun_perolehan": 2024,
                "asal_usul": "Pembelian",
                "harga": 15000000,
                "kondisi": "Baik",
                "ruangan_id": "room-uuid"
            },
            cookies={"simanis62_session": admin_token}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["kode_barang"] == "01.02.03.0001"
        assert data["data"]["nomor_register"] == 1

    async def test_create_asset_as_viewer_rejected(self, client: AsyncClient, viewer_token: str):
        response = await client.post(
            "/api/v1/aset",
            json={
                "kode_barang": "01.02.03.0002",
                "nama_barang": "Test",
                "kategori_kib": "B",
                "tahun_perolehan": 2024,
                "asal_usul": "Pembelian",
                "harga": 1000000,
                "kondisi": "Baik",
                "ruangan_id": "room-uuid"
            },
            cookies={"simanis62_session": viewer_token}
        )

        assert response.status_code == 403
        assert response.json()["error_code"] == "AUTHZ_ERROR"

    async def test_search_assets_performance(self, client: AsyncClient, admin_token: str):
        import time

        start = time.time()
        response = await client.get(
            "/api/v1/aset",
            params={"keyword": "komputer"},
            cookies={"simanis62_session": admin_token}
        )
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 5.0  # CP-PERF-01: < 5 detik
```


---

## Configuration Management

### Backend Configuration

```python
# app/core/config.py

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings dari environment variables dan config file."""

    # === Application ===
    APP_NAME: str = "SIMANIS62"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = Field(default="development", env="SIMANIS_ENV")
    DEBUG: bool = Field(default=False)

    # === API ===
    API_HOST: str = Field(default="127.0.0.1")
    API_PORT: int = Field(default=8000)
    API_PREFIX: str = "/api/v1"

    # === Database ===
    DATABASE_PATH: str = Field(
        default="C:/ProgramData/Simanis62/simanis62.db"
    )

    # === Security ===
    SESSION_SECRET_KEY: str = Field(default="change-me-in-production")
    SESSION_TIMEOUT_SECONDS: int = Field(default=7200)  # 2 hours
    COOKIE_NAME: str = "simanis62_session"

    # === Logging ===
    LOG_LEVEL: str = Field(default="INFO")
    LOG_DIR: str = Field(default="logs")

    # === GlitchTip ===
    GLITCHTIP_DSN: Optional[str] = Field(default=None)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
```

### Frontend Configuration

```csharp
// Core/Configuration/AppSettings.cs

namespace Simanis62.WPF.Core.Configuration;

public class AppSettings
{
    public ApiSettings Api { get; set; } = new();
    public LoggingSettings Logging { get; set; } = new();
    public GlitchTipSettings GlitchTip { get; set; } = new();
}

public class ApiSettings
{
    public string BaseUrl { get; set; } = "http://127.0.0.1:8000";
    public int TimeoutSeconds { get; set; } = 30;
    public int RetryCount { get; set; } = 3;
}

public class LoggingSettings
{
    public string Level { get; set; } = "Information";
    public string LogDirectory { get; set; } = "logs";
    public int RetainedFileCount { get; set; } = 7;
}

public class GlitchTipSettings
{
    public string? Dsn { get; set; }
    public string Environment { get; set; } = "development";
}
```

### Config Files

```json
// configs/development.json
{
  "api": {
    "host": "127.0.0.1",
    "port": 8000,
    "debug": true
  },
  "database": {
    "path": "C:\\ProgramData\\Simanis62\\simanis62_dev.db"
  },
  "logging": {
    "level": "DEBUG"
  },
  "glitchtip": {
    "dsn": null
  }
}
```

```json
// configs/production.json
{
  "api": {
    "host": "127.0.0.1",
    "port": 8000,
    "debug": false
  },
  "database": {
    "path": "C:\\ProgramData\\Simanis62\\simanis62.db"
  },
  "logging": {
    "level": "INFO"
  },
  "glitchtip": {
    "dsn": "https://your-glitchtip-dsn"
  }
}
```

---

## Summary

Design document ini mendefinisikan arsitektur teknis SIMANIS62 V2 dengan fokus pada:

### Backend (FastAPI + Python)
- **Clean Architecture** dengan 4 layer: Presentation → Application → Domain → Infrastructure
- **Custom Exception Hierarchy** untuk error handling yang konsisten
- **Structured Logging** dengan JSON format dan correlation IDs
- **SQLite WAL Mode** dengan optimal pragmas untuk performance
- **Repository Pattern** untuk data access abstraction
- **Service Layer** untuk business logic encapsulation
- **Dependency Injection** via FastAPI Depends

### Frontend (WPF .NET 8)
- **MVVM Pattern** dengan CommunityToolkit.Mvvm
- **Global Exception Handler** untuk unhandled exceptions
- **ViewModelBase** dengan built-in error handling
- **Refit** untuk type-safe HTTP client
- **Polly** untuk retry policies
- **Serilog** untuk structured logging

### Key Design Decisions
1. **Session-based auth** (bukan JWT) untuk simplicity
2. **Soft delete** untuk audit trail
3. **Correlation IDs** untuk request tracing
4. **Centralized error handling** di middleware
5. **Config-driven** untuk environment flexibility

### Correctness Properties
- 25+ properties yang harus dipenuhi
- Verification melalui unit tests, integration tests, dan performance tests

---

*Dokumen ini adalah bagian dari `.kiro/specs/simanis62-v2/` dan harus dibaca bersama dengan `requirements.md`.*

*Terakhir diupdate: 10 Januari 2026*
*Versi: 1.0*
