# Installation Checklist - SIMANIS62 V2 Testing

## Status Saat Ini

E2E workflow tests gagal karena:
1. ❌ Missing fixtures (admin_token, viewer_token, kepala_sekolah_token)
2. ❌ Missing API endpoints (belum diimplementasi)
3. ❌ Missing models (Aset, User, Ruangan, Mutasi)

## Yang Sudah Diinstall ✅

- Python 3.12
- pytest
- pytest-asyncio
- httpx
- aiosqlite
- sqlmodel
- fastapi

## Yang Perlu Diinstall di Windows

### 1. Python Dependencies (WAJIB)

```powershell
# Pastikan di virtual environment
cd D:\simanis62-v2\backend
.\.venv\Scripts\activate

# Install dependencies yang hilang
pip install bcrypt --only-binary :all:
pip install python-jose[cryptography]
pip install passlib[bcrypt]
```

### 2. Verifikasi Installation

```powershell
# Check installed packages
pip list | findstr "bcrypt\|jose\|passlib"

# Expected output:
# bcrypt           4.x.x
# passlib          1.7.4
# python-jose      3.3.0
```

## Perbaikan yang Sudah Dilakukan ✅

### 1. Update conftest.py

Menambahkan fixtures yang hilang:
- `admin_token` - Mock token untuk admin
- `viewer_token` - Mock token untuk viewer
- `kepala_sekolah_token` - Mock token untuk kepala sekolah (Viewer + dapat_ekspor)

### 2. Mock Password Functions

Sudah ada di conftest.py untuk menghindari bcrypt issues di Windows:
```python
def mock_hash_password(password: str) -> str:
    return f"$2b$12$mock_hash_{password}"

def mock_verify_password(plain_password: str, hashed_password: str) -> bool:
    expected_hash = f"$2b$12$mock_hash_{plain_password}"
    return hashed_password == expected_hash
```

### 3. Fix RuanganResponse Schema

Mengubah semua schema classes di `ruangan_service.py` dari `__init__` biasa menjadi Pydantic `BaseModel`:
- `RuanganCreate` - Sekarang menggunakan Pydantic dengan Field validation
- `RuanganUpdate` - Sekarang menggunakan Pydantic dengan Field validation
- `RuanganResponse` - Sekarang menggunakan Pydantic BaseModel (fix untuk PydanticSchemaGenerationError)
- `KirReportItem` - Sekarang menggunakan Pydantic BaseModel
- `KirReportResponse` - Sekarang menggunakan Pydantic BaseModel

## Yang Masih Perlu Diimplementasi

### Phase 2: Database Models (PRIORITAS TINGGI)

Buat models di `backend/app/models/`:

1. **aset.py** - Model Aset dengan fields:
   - id, kode_aset, nama_aset, kategori_id
   - ruangan_id, tanggal_perolehan, nilai_perolehan
   - kondisi, status, created_by, created_at

2. **user.py** - Model User dengan fields:
   - id, username, password_hash, full_name
   - role (Admin/Viewer), dapat_ekspor (boolean)
   - status (Aktif/Nonaktif), created_at

3. **ruangan.py** - Model Ruangan dengan fields:
   - id, kode_ruangan, nama_ruangan
   - luas, lokasi, created_at

4. **mutasi.py** - Model Mutasi dengan fields:
   - id, aset_id, ruangan_asal_id, ruangan_tujuan_id
   - tanggal_mutasi, alasan, created_by, created_at

### Phase 3: API Endpoints (PRIORITAS TINGGI)

Buat endpoints di `backend/app/api/`:

1. **aset.py** - CRUD endpoints:
   - POST /api/v1/aset/
   - GET /api/v1/aset/{id}
   - PUT /api/v1/aset/{id}
   - DELETE /api/v1/aset/{id}

2. **mutasi.py** - Mutation endpoints:
   - POST /api/v1/mutasi/

3. **kib.py** - Report endpoints:
   - GET /api/v1/kib/B
   - GET /api/v1/kib/B/export

4. **users.py** - User management:
   - POST /api/v1/users/
   - GET /api/v1/users/
   - PUT /api/v1/users/{id}
   - PUT /api/v1/users/{id}/deactivate

5. **ruangan.py** - Room management:
   - POST /api/v1/ruangan/
   - DELETE /api/v1/ruangan/{id}

### Phase 4: Authentication (JWT)

Implementasi JWT authentication:
- Login endpoint: POST /api/v1/auth/login
- Token generation dengan python-jose
- Token validation middleware
- Role-based access control (RBAC)

## Cara Menjalankan Tests

### 1. Unit Tests (Setelah models diimplementasi)

```powershell
cd D:\simanis62-v2\backend
pytest tests/unit/ -v
```

### 2. Integration Tests (Setelah API diimplementasi)

```powershell
pytest tests/integration/ -v
```

### 3. E2E Tests (Setelah semua diimplementasi)

```powershell
pytest tests/integration/test_e2e_workflows.py -v
```

### 4. All Tests dengan Coverage

```powershell
pytest --cov=app --cov-report=html
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'app.models.aset'"

**Solusi**: Implementasi models belum ada. Tunggu Phase 2.

### Error: "404 Not Found" di tests

**Solusi**: API endpoints belum diimplementasi. Tunggu Phase 3.

### Error: "bcrypt backend not available"

**Solusi**: 
```powershell
pip uninstall bcrypt
pip install bcrypt --only-binary :all:
```

### Error: "fixture 'admin_token' not found"

**Solusi**: Sudah diperbaiki di conftest.py. Pull latest changes.

## Next Steps

1. ✅ Install bcrypt dengan binary wheel
2. ✅ Update conftest.py dengan missing fixtures
3. ⏳ Implementasi Phase 2: Database Models
4. ⏳ Implementasi Phase 3: API Endpoints
5. ⏳ Implementasi Phase 4: JWT Authentication
6. ⏳ Run e2e tests dan verify semua passing

## Referensi

- [AGENTS.md](AGENTS.md) - Project guidelines
- [.kiro/steering/tech.md](.kiro/steering/tech.md) - Tech stack
- [docs/data_schema.md](docs/data_schema.md) - Database schema
- [docs/api_contract.md](docs/api_contract.md) - API specifications

---

**Last Updated**: 2026-01-11
**Status**: Fixtures fixed, waiting for models & API implementation


---

## Progress Update (2026-01-12 14:30)

### ✅ Fixed Issues

1. **Dependencies installed**: 
   - bcrypt 5.0.0
   - python-jose 3.5.0
   - passlib 1.7.4

2. **Test fixtures added** (`backend/tests/conftest.py`):
   - `admin_token` - Returns mock token "mock_admin_token_12345"
   - `viewer_token` - Returns mock token "mock_viewer_token_67890"
   - `kepala_sekolah_token` - Creates kepala sekolah user (Viewer + dapat_ekspor=True) and returns mock token

3. **Pydantic models fixed** (`backend/app/services/ruangan_service.py`):
   - Converted `RuanganCreate` from plain class to `BaseModel`
   - Converted `RuanganUpdate` from plain class to `BaseModel`
   - Converted `RuanganResponse` from plain class to `BaseModel`
   - Fixed PydanticSchemaGenerationError

4. **UUID serialization fixed** (`backend/tests/integration/test_e2e_workflows.py`):
   - All UUID objects in test data converted to strings using `str(uuid_object)`
   - Fixed TypeError: Object of type UUID is not JSON serializable

### ⚠️ Current Issue: Missing API Endpoints

**Symptom**: Tests are getting HTTP 307 (Temporary Redirect) responses instead of expected status codes.

**Root Cause**: The API endpoints referenced in tests don't exist yet:
- `/api/v1/aset/*` - Not implemented
- `/api/v1/users/*` - Not implemented  
- `/api/v1/mutasi/*` - Not implemented
- `/api/v1/kib/*` - Not implemented

**Test Output**:
```
tests/integration/test_e2e_workflows.py::TestCompleteAsetWorkflow::test_complete_aset_lifecycle FAILED
E   assert 307 == 201
E    +  where 307 = <Response [307 Temporary Redirect]>.status_code
```

### 📋 Next Steps (Priority Order)

#### 1. Implement Phase 3: API Endpoints (CRITICAL)

Create the following endpoint files:

```
backend/app/api/
├── aset.py      # POST, GET, PUT, DELETE /api/v1/aset/*
├── users.py     # POST, GET, PUT /api/v1/users/*
├── mutasi.py    # POST, GET /api/v1/mutasi/*
└── kib.py       # GET /api/v1/kib/{kategori}
```

**Required endpoints**:
- `POST /api/v1/aset/` - Create aset
- `GET /api/v1/aset/{aset_id}` - Get aset by ID
- `PUT /api/v1/aset/{aset_id}` - Update aset
- `DELETE /api/v1/aset/{aset_id}` - Delete aset
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - List users
- `PUT /api/v1/users/{user_id}` - Update user
- `PUT /api/v1/users/{user_id}/deactivate` - Deactivate user
- `POST /api/v1/mutasi/` - Create mutation
- `POST /api/v1/ruangan/` - Create ruangan
- `DELETE /api/v1/ruangan/{ruangan_id}` - Delete ruangan
- `GET /api/v1/kib/B` - Get KIB B report
- `GET /api/v1/kib/B/export` - Export KIB B

#### 2. Implement Phase 2: Complete Database Models

- Aset model with all KIB relationships
- User model with RBAC (partially done)
- RiwayatMutasi model
- Service layer for each model

#### 3. Implement Authentication Middleware

- Token validation
- Role-based access control (RBAC)
- Session management
- Permission checks (Admin vs Viewer vs Kepala Sekolah)

#### 4. Re-run e2e tests

After endpoints are implemented, run:
```powershell
cd backend
pytest tests/integration/test_e2e_workflows.py -v
```

### 🎯 Success Criteria

Tests should pass with:
- ✅ Status code 201 for POST requests
- ✅ Status code 200 for GET requests
- ✅ Status code 204 for DELETE requests
- ✅ Status code 403/401 for unauthorized access
- ✅ Proper JSON responses with expected data structure

---

## Troubleshooting

### Issue: Tests still failing after fixes

**Cause**: API endpoints not implemented yet.

**Solution**: Implement Phase 3 (API Endpoints) before running e2e tests. Unit tests for models and services can be run independently.

### Issue: Import errors for bcrypt/jose

**Cause**: Dependencies not installed.

**Solution**: Run installation commands in "Yang Perlu Diinstall di Windows" section above.
