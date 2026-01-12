# AGENTS.md - Backend

**Tech Stack**: Python 3.12, FastAPI, SQLModel, SQLite (WAL mode)

---

## Code Quality Tools (WAJIB)

```bash
# Format dan lint (auto-fix) - GUNAKAN RUFF
ruff check --fix . && ruff format .

# Type checking
mypy app/

# Run tests
pytest -v --cov=app

# Run semua checks (pre-commit)
pre-commit run --all-files
```

---

## Aturan Khusus

### Coding Standards
- Gunakan **Type Hints** di semua function (Python 3.12+ syntax)
- **Async** by default untuk semua endpoint
- Pydantic models di `schemas/`, SQLModel tables di `models/`
- **JANGAN** hardcode secrets - gunakan environment variables
- **Ruff** untuk linting (bukan flake8/black/isort terpisah)
- **Google Style Docstrings** untuk dokumentasi function

### Konvensi Penamaan Database

| Konteks | Konvensi | Bahasa | Contoh |
|---------|----------|--------|--------|
| Table names | snake_case | English | `users`, `assets`, `mutations` |
| Column names | snake_case | **Bahasa Indonesia** | `nomor_register`, `tahun_perolehan`, `dapat_ekspor` |
| Function names | snake_case | English | `get_asset_by_id()`, `create_mutation()` |
| Class names | PascalCase | English | `AssetService`, `UserRepository` |

### Contoh Model SQLModel

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Aset(SQLModel, table=True):
    __tablename__ = "aset"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    kode_barang: str = Field(index=True, unique=True)
    nama_barang: str
    kategori_kib: str  # A, B, C, D, E, F
    tahun_perolehan: int
    harga: int  # Rupiah penuh, BUKAN ribuan
    kondisi: str  # Baik, Rusak Ringan, Rusak Berat
    status: str = Field(default="Baru")  # Baru, Aktif, Mutasi, Rusak, Dihapus

    # Audit trail (English field names for SQLModel/SQLAlchemy conventions)
    created_by: UUID  # FK ke users.id
    updated_by: Optional[UUID] = None
    deleted_by: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    delete_reason: Optional[str] = None  # Min 20 karakter untuk soft delete
```

### Authorization (RBAC)

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Admin"
    VIEWER = "Viewer"

# Kepala Sekolah = Viewer dengan dapat_ekspor=True
# Cek izin export:
# if user.role == UserRole.ADMIN or user.dapat_ekspor:
#     allow_export()
```

### Field Khusus per KIB

Lihat `docs/format_kib_spesifikasi.md` untuk detail field per kategori KIB.

| KIB | Kolom | Field Khusus |
|-----|-------|--------------|
| A | 14 | `luas_m2`, `status_hak_tanah`, `nomor_sertifikat` |
| B | **18** | `satuan`, `merk`, `tipe`, `kapitalisasi`, `total_harga` |
| C | 17 | `bertingkat`, `beton`, `luas_lantai_m2` |
| D | 16 | `jenis_konstruksi`, `panjang_km`, `lebar_m` |
| E | 16 | `judul_pencipta`, `jenis_hewan`, `jumlah` |
| F | 12 | `jenis_bangunan`, `info_dokumen` |

---

## Error Handling Pattern

### Custom Exceptions (WAJIB DIGUNAKAN)

```python
from app.core.exceptions import (
    NotFoundError,
    ValidationError,
    AuthorizationError,
    BusinessRuleError,
    DatabaseError
)

# ✅ BENAR - Gunakan custom exception
async def get_aset(aset_id: UUID) -> Aset:
    aset = await db.get(Aset, aset_id)
    if not aset:
        raise NotFoundError("Aset", aset_id)
    return aset

# ❌ SALAH - Generic HTTPException
async def get_aset(aset_id: UUID) -> Aset:
    aset = await db.get(Aset, aset_id)
    if not aset:
        raise HTTPException(status_code=404, detail="Not found")
    return aset
```

### Logging dengan Context

```python
import logging

logger = logging.getLogger(__name__)

# ✅ BENAR - Log dengan context
logger.info(
    "Creating aset",
    extra={"kode_barang": data.kode_barang, "user_id": str(user_id)}
)

# ❌ SALAH - Log tanpa context
logger.info(f"Creating aset {data.kode_barang}")
```

### Preserve Exception Chain

```python
# ✅ BENAR - Preserve original exception
try:
    result = await db.execute(query)
except SQLAlchemyError as e:
    logger.exception("Database error")
    raise DatabaseError("executing query", str(e)) from e

# ❌ SALAH - Kehilangan original exception
try:
    result = await db.execute(query)
except SQLAlchemyError:
    raise DatabaseError("executing query")  # Original error hilang!
```

---

*Sinkronisasi dengan: Root AGENTS.md v1.6*
