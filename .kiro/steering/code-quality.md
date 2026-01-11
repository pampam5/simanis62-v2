---
inclusion: always
---

# Code Quality Standards - SIMANIS62 V2

## Tools Wajib

| Tool | Fungsi | Versi |
|------|--------|-------|
| **Ruff** | Linting + Formatting (pengganti flake8, isort, black) | Latest |
| **MyPy** | Static type checking | Latest |
| **Black** | Code formatting (backup) | Latest |
| **Pytest** | Testing framework | Latest |
| **Pre-commit** | Git hooks automation | Latest |

---

## Konfigurasi pyproject.toml

```toml
# backend/pyproject.toml

[project]
name = "simanis62-backend"
version = "2.0.0"
requires-python = ">=3.12"

[tool.ruff]
target-version = "py312"
line-length = 88
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "migrations",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort (import sorting)
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "RET",    # flake8-return
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented code)
    "PL",     # pylint
    "RUF",    # ruff-specific rules
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # function calls in argument defaults (FastAPI Depends)
    "PLR0913", # too many arguments (common in FastAPI)
    "ARG001", # unused function argument (common in handlers)
]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ARG", "PLR2004"]  # Allow magic values in tests
"__init__.py" = ["F401"]        # Allow unused imports in __init__

[tool.ruff.lint.isort]
known-first-party = ["app"]
combine-as-imports = true
force-wrap-aliases = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = true

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "-ra",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["app"]
branch = true
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

---

## Pre-commit Configuration

```yaml
# backend/.pre-commit-config.yaml

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --show-fixes]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic
          - sqlmodel
          - fastapi
        args: [--config-file=pyproject.toml]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: detect-private-key
      - id: check-merge-conflict
```

---

## Perintah Code Quality

### Quick Commands

```bash
# Format dan lint (auto-fix)
ruff check --fix . && ruff format .

# Type checking
mypy app/

# Run tests dengan coverage
pytest --cov=app --cov-report=html

# Run semua checks (pre-commit)
pre-commit run --all-files
```

### Setup Pre-commit

```bash
# Install pre-commit hooks (sekali saja)
pip install pre-commit
pre-commit install

# Setelah ini, setiap git commit akan otomatis run checks
```

---

## Type Hints Best Practices

### 1. Selalu Gunakan Type Hints

```python
# ✅ BENAR
from typing import Optional
from uuid import UUID

async def get_aset(aset_id: UUID) -> Optional[Aset]:
    """Ambil aset berdasarkan ID."""
    return await db.get(Aset, aset_id)

# ❌ SALAH
async def get_aset(aset_id):
    return await db.get(Aset, aset_id)
```

### 2. Gunakan Modern Type Syntax (Python 3.12+)

```python
# ✅ BENAR - Python 3.12+ syntax
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ❌ SALAH - Old syntax (masih valid tapi tidak preferred)
from typing import List, Dict
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

### 3. Optional vs Union

```python
# ✅ BENAR - Explicit Optional
from typing import Optional

def find_user(user_id: UUID) -> Optional[User]:
    """Return User or None."""
    pass

# ✅ JUGA BENAR - Union syntax
def find_user(user_id: UUID) -> User | None:
    """Return User or None."""
    pass
```

### 4. Type Aliases untuk Complex Types

```python
# ✅ BENAR - Type alias untuk readability
from typing import TypeAlias

AsetDict: TypeAlias = dict[str, str | int | None]
AsetList: TypeAlias = list[AsetDict]

def export_aset() -> AsetList:
    pass
```

---

## Docstring Standards (Google Style)

```python
async def create_aset(
    data: AsetCreate,
    user_id: UUID,
    session: Session
) -> Aset:
    """Membuat aset baru di database.

    Fungsi ini memvalidasi data input, mengecek duplikasi kode barang,
    dan menyimpan aset baru ke database.

    Args:
        data: Data aset yang akan dibuat (dari request body).
        user_id: UUID user yang membuat aset.
        session: Database session untuk transaksi.

    Returns:
        Objek Aset yang baru dibuat dengan ID yang di-generate.

    Raises:
        ValidationError: Jika kode barang sudah digunakan.
        BusinessRuleError: Jika harga negatif.
        DatabaseError: Jika gagal menyimpan ke database.

    Example:
        >>> aset = await create_aset(
        ...     data=AsetCreate(nama_barang="Laptop", kode_barang="02.06.01.0001"),
        ...     user_id=UUID("..."),
        ...     session=db_session
        ... )
        >>> print(aset.id)
        UUID('...')
    """
    pass
```

---

## Import Organization

Ruff akan otomatis mengurutkan imports dengan aturan:

```python
# 1. Standard library imports
import json
import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

# 2. Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select

# 3. Local application imports
from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.models.aset import Aset
from app.schemas.aset import AsetCreate, AsetResponse
```

---

## Code Patterns yang Direkomendasikan

### 1. Early Return Pattern

```python
# ✅ BENAR - Early return
async def get_aset(aset_id: UUID) -> Aset:
    aset = await db.get(Aset, aset_id)
    if not aset:
        raise NotFoundError("Aset", aset_id)
    return aset

# ❌ SALAH - Nested if
async def get_aset(aset_id: UUID) -> Aset:
    aset = await db.get(Aset, aset_id)
    if aset:
        return aset
    else:
        raise NotFoundError("Aset", aset_id)
```

### 2. Context Manager untuk Resources

```python
# ✅ BENAR - Context manager
async with get_session() as session:
    aset = await session.get(Aset, aset_id)
    # session otomatis di-close

# ❌ SALAH - Manual close
session = get_session()
try:
    aset = await session.get(Aset, aset_id)
finally:
    session.close()
```

### 3. Comprehensions vs Loops

```python
# ✅ BENAR - List comprehension (untuk simple transformations)
active_aset = [a for a in aset_list if a.status == "Aktif"]

# ✅ JUGA BENAR - Loop (untuk complex logic)
result = []
for aset in aset_list:
    if aset.status == "Aktif":
        processed = process_aset(aset)
        if processed.is_valid:
            result.append(processed)
```

### 4. F-strings untuk String Formatting

```python
# ✅ BENAR - f-string
message = f"Aset {aset.nama_barang} berhasil disimpan"

# ❌ SALAH - .format() atau %
message = "Aset {} berhasil disimpan".format(aset.nama_barang)
message = "Aset %s berhasil disimpan" % aset.nama_barang
```

---

## Testing Standards

### Test File Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_api/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_aset.py
│   └── test_kib.py
├── test_services/
│   ├── __init__.py
│   ├── test_aset_service.py
│   └── test_kib_service.py
└── test_models/
    ├── __init__.py
    └── test_aset.py
```

### Test Naming Convention

```python
# Format: test_<what>_<condition>_<expected>

def test_create_aset_with_valid_data_returns_aset():
    """Test membuat aset dengan data valid."""
    pass

def test_create_aset_with_duplicate_kode_raises_validation_error():
    """Test membuat aset dengan kode duplikat."""
    pass

def test_get_aset_with_invalid_id_raises_not_found():
    """Test mengambil aset dengan ID tidak valid."""
    pass
```

### Fixture Pattern

```python
# conftest.py
import pytest
from sqlmodel import Session, create_engine
from app.models import Aset

@pytest.fixture
def db_session():
    """Create in-memory database session for testing."""
    engine = create_engine("sqlite:///:memory:")
    with Session(engine) as session:
        yield session

@pytest.fixture
def sample_aset(db_session: Session) -> Aset:
    """Create sample aset for testing."""
    aset = Aset(
        nama_barang="Laptop Test",
        kode_barang="02.06.01.0001",
        harga=15000000,
        tahun_perolehan=2024
    )
    db_session.add(aset)
    db_session.commit()
    return aset
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/backend-ci.yml

name: Backend CI

on:
  push:
    branches: [main, develop]
    paths: ['backend/**']
  pull_request:
    branches: [main]
    paths: ['backend/**']

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install ruff mypy pytest pytest-cov

      - name: Run Ruff (lint + format check)
        run: |
          ruff check .
          ruff format --check .

      - name: Run MyPy
        run: mypy app/

      - name: Run Tests
        run: pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

---

## Referensi

#[[file:backend/AGENTS.md]]
#[[file:backend/requirements.txt]]
#[[file:.kiro/steering/DBHUB_GUIDE.md]]
