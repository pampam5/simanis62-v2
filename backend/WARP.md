# WARP.md - Backend (Python FastAPI)
# Aturan spesifik untuk folder backend/

## Tech Stack

- Python 3.12 (`py -3.12`)
- FastAPI + Uvicorn
- SQLModel (ORM) + SQLite WAL
- Pydantic v2 (validasi)
- Ruff (lint), MyPy (type check)

## Perintah

```bash
# Development
uvicorn app.main:app --reload --port 8000

# Quality
ruff check --fix . && ruff format .
mypy app/
pytest -v --cov=app

# Pre-commit
pre-commit run --all-files
```

## Struktur

```
app/
├── api/        # Endpoint routes (1 file per resource)
├── models/     # SQLModel entities
├── schemas/    # Pydantic request/response
├── services/   # Business logic
└── core/       # Config, security, logging, exceptions
```

## Konvensi Kode

- **Type hints WAJIB** di semua function
- **Google style docstrings**
- **snake_case** untuk variabel dan function
- **PascalCase** untuk class
- Line length: 88 (Ruff default)

## Contoh Pattern

```python
async def get_aset_by_id(aset_id: UUID) -> Aset:
    """Mengambil aset berdasarkan ID.

    Args:
        aset_id: UUID dari aset.

    Returns:
        Objek Aset jika ditemukan.

    Raises:
        NotFoundError: Jika aset tidak ditemukan.
    """
    aset = await db.get(Aset, aset_id)
    if not aset:
        raise NotFoundError("Aset", aset_id)
    return aset
```

## Custom Exceptions

Gunakan hierarchy di `app/core/exceptions.py`:
- `AppException` → Base
- `NotFoundError` → 404
- `ValidationError` → 400
- `AuthorizationError` → 403
- `BusinessRuleError` → 422

## Database Fields (Bahasa Indonesia)

```python
# Contoh SQLModel
class Aset(SQLModel, table=True):
    nomor_register: str
    kode_barang: str  # XX.XX.XX.XXXX
    nama_barang: str
    tahun_perolehan: int
    harga: int  # Rupiah penuh
```

## 🚫 JANGAN

- Gunakan PostgreSQL (pakai SQLite)
- Raw SQL queries (pakai SQLModel)
- Hardcode credentials
- Log password/session token

---

*Referensi: `backend/AGENTS.md`, `.kiro/steering/api-standards.md`*
