---
inclusion: fileMatch
fileMatchPattern: "**/*.py"
---

# Standar API Python - SIMANIS62 V2

## Gaya Kode Python

### Type Hints (WAJIB)
```python
# ✅ BENAR
async def get_aset_by_id(aset_id: UUID) -> Aset:
    pass

# ❌ SALAH
async def get_aset_by_id(aset_id):
    pass
```

### Docstring (Google Style)
```python
async def create_aset(data: AsetCreate, db: Session) -> Aset:
    """Membuat aset baru di database.
    
    Args:
        data: Data aset yang akan dibuat.
        db: Session database.
        
    Returns:
        Objek Aset yang baru dibuat.
        
    Raises:
        HTTPException: Jika validasi gagal.
    """
    pass
```

### Naming Convention
- Variabel: `snake_case` → `nama_barang`, `harga_perolehan`
- Class: `PascalCase` → `AsetService`, `UserModel`
- Konstanta: `UPPER_SNAKE_CASE` → `MAX_PAGE_SIZE`, `SESSION_TIMEOUT`

## Struktur Endpoint FastAPI

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID

from app.core.database import get_session
from app.models.aset import Aset
from app.schemas.aset import AsetCreate, AsetResponse
from app.services.aset_service import AsetService

router = APIRouter(prefix="/api/v1/aset", tags=["Aset"])

@router.get("/{aset_id}", response_model=AsetResponse)
async def get_aset(
    aset_id: UUID,
    db: Session = Depends(get_session)
) -> AsetResponse:
    """Mengambil data aset berdasarkan ID."""
    service = AsetService(db)
    aset = await service.get_by_id(aset_id)
    if not aset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aset tidak ditemukan"
        )
    return AsetResponse(success=True, data=aset)
```

## Struktur SQLModel

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from enum import Enum

class StatusAset(str, Enum):
    BARU = "Baru"
    AKTIF = "Aktif"
    MUTASI = "Mutasi"
    RUSAK = "Rusak"
    DIHAPUS = "Dihapus"

class Aset(SQLModel, table=True):
    __tablename__ = "aset"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nama_barang: str = Field(max_length=200, index=True)
    kode_barang: str = Field(max_length=50, unique=True)
    harga: int = Field(ge=0)
    status: StatusAset = Field(default=StatusAset.BARU)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
```

## Response Format

```python
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: dict
```

## Error Handling

```python
from fastapi import HTTPException, status

# Validation Error
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": "VALIDATION_ERROR",
        "message": "Nama barang harus diisi",
        "field": "nama_barang"
    }
)

# Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"code": "NOT_FOUND", "message": "Aset tidak ditemukan"}
)

# Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={"code": "UNAUTHORIZED", "message": "Session tidak valid"}
)
```

## Referensi

#[[file:docs/api_contract.md]]
#[[file:docs/data_schema.md]]

## Logging Standards

### Setup Logging
```python
# app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

# Sentry/GlitchTip integration
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above
    event_level=logging.ERROR  # Send errors to GlitchTip
)

sentry_sdk.init(
    dsn="YOUR_GLITCHTIP_DSN",  # Dari environment variable
    integrations=[sentry_logging],
    traces_sample_rate=0.1,    # 10% performance monitoring
    environment="production"
)

# File logging
def setup_logging():
    logger = logging.getLogger("simanis62")
    logger.setLevel(logging.INFO)
    
    # Rotating file handler (10MB, keep 5 files)
    file_handler = RotatingFileHandler(
        "logs/simanis62.log",
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    logger.addHandler(file_handler)
    return logger
```

### Penggunaan di Endpoint
```python
from app.core.logging import setup_logging

logger = setup_logging()

@router.post("/", response_model=AsetResponse)
async def create_aset(data: AsetCreate, db: Session = Depends(get_session)):
    logger.info(f"Creating aset: {data.nama_barang[:20]}...")  # Truncate untuk privacy
    try:
        result = await service.create(data)
        logger.info(f"Aset created: {result.id}")
        return AsetResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Failed to create aset: {str(e)}")
        sentry_sdk.capture_exception(e)  # Kirim ke GlitchTip
        raise
```

### Apa yang Di-log
| Level | Contoh | Kirim ke GlitchTip? |
|-------|--------|---------------------|
| DEBUG | Query SQL detail | ❌ |
| INFO | Login success, CRUD operations | ❌ |
| WARNING | Slow query, retry attempt | ❌ |
| ERROR | Exception, validation failed | ✅ |
| CRITICAL | Database connection lost | ✅ |

### Yang TIDAK BOLEH Di-log
```python
# ❌ SALAH - Log password
logger.info(f"Login attempt: {username}, password: {password}")

# ✅ BENAR - Tanpa password
logger.info(f"Login attempt: {username}")

# ❌ SALAH - Log data lengkap
logger.info(f"Created aset: {aset.dict()}")

# ✅ BENAR - Hanya ID
logger.info(f"Created aset: {aset.id}")
```
