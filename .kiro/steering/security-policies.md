---
inclusion: always
---

# Kebijakan Keamanan - SIMANIS62 V2

## Authentication

### Session-Based Auth (BUKAN JWT)
```python
# Konfigurasi Session
SESSION_TIMEOUT = 7200  # 2 jam dalam detik
COOKIE_NAME = "simanis62_session"
COOKIE_HTTPONLY = True
COOKIE_SECURE = False  # HTTP only (localhost)
COOKIE_SAMESITE = "Lax"
```

### Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

## Authorization (RBAC)

### Role Definitions
```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Admin"      # Full access
    VIEWER = "Viewer"    # Read-only

# PENTING: Kepala Sekolah BUKAN role terpisah!
# Kepala Sekolah = Viewer dengan dapat_ekspor=True
# Field database: dapat_ekspor (boolean, default False)
```

### Permission Matrix

| Endpoint | Admin | Viewer | Viewer + dapat_ekspor |
|----------|-------|--------|----------------------|
| GET /aset | ✅ | ✅ | ✅ |
| POST /aset | ✅ | ❌ | ❌ |
| PUT /aset | ✅ | ❌ | ❌ |
| DELETE /aset | ✅ | ❌ | ❌ |
| GET /kib/export | ✅ | ❌ | ✅ |
| POST /mutasi | ✅ | ❌ | ❌ |
| GET /users | ✅ | ❌ | ❌ |

> **Catatan**: Kolom "Viewer + dapat_ekspor" adalah implementasi untuk Kepala Sekolah

### Middleware Example
```python
from fastapi import Depends, HTTPException, status

async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses ditolak. Hanya Admin yang diizinkan."
        )
    return current_user

async def require_export_permission(current_user: User = Depends(get_current_user)):
    """Izinkan Admin atau Viewer dengan dapat_ekspor=True (Kepala Sekolah)."""
    if current_user.role == UserRole.ADMIN:
        return current_user
    if current_user.role == UserRole.VIEWER and current_user.dapat_ekspor:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Akses ditolak. Anda tidak memiliki izin export."
    )
```

## Data Protection

### 🚫 JANGAN PERNAH
- Hardcode credentials di source code
- Commit file `.env` ke repository
- Simpan password dalam plain text
- Log data sensitif (password, session token)
- Expose database file ke public

### ✅ SELALU
- Gunakan environment variables untuk secrets
- Hash password dengan bcrypt
- Validasi semua input dengan Pydantic
- Sanitize output untuk mencegah XSS
- Gunakan parameterized queries (SQLModel handles this)

## File Locations

```
# Database (JANGAN commit!)
C:\ProgramData\Simanis62\simanis62.db

# Config (JANGAN commit!)
C:\ProgramData\Simanis62\config.json

# Backups
C:\ProgramData\Simanis62\backups\
```

## .gitignore Entries

```gitignore
# Database
*.db
*.db-journal
*.db-wal
*.db-shm

# Config & Secrets
.env
config.json
*.key
*.pem

# Logs
*.log
logs/
```

## Error Reporting Policy (GlitchTip)

### Data yang BOLEH Dikirim ke GlitchTip
- ✅ Stack trace dan error message
- ✅ Versi aplikasi dan OS
- ✅ Nama endpoint yang error
- ✅ Timestamp error
- ✅ User role (Admin/Viewer)

### Data yang TIDAK BOLEH Dikirim
- ❌ Password atau credentials
- ❌ Session token
- ❌ Data aset (nama, harga, kode)
- ❌ Data pribadi user (nama lengkap, email)
- ❌ IP address user

### Implementasi Filter
```python
# Backend - sentry_sdk before_send
import sentry_sdk

def before_send(event, hint):
    # Hapus data sensitif
    if 'request' in event:
        if 'data' in event['request']:
            event['request']['data'] = '[FILTERED]'
        if 'cookies' in event['request']:
            event['request']['cookies'] = '[FILTERED]'
    return event

sentry_sdk.init(
    dsn="YOUR_GLITCHTIP_DSN",
    before_send=before_send
)
```

## Remote Access Security (RustDesk)

### Aturan Remote Support
1. **User harus approve** - Setiap koneksi harus di-approve oleh user
2. **Session terbatas** - Disconnect setelah selesai support
3. **Tidak simpan password** - Jangan simpan password RustDesk user
4. **Dokumentasi** - Catat setiap sesi remote support

### Workflow Aman
```
1. User lapor masalah via WhatsApp
2. Developer minta ID RustDesk
3. User share ID (BUKAN password)
4. Developer request koneksi
5. User klik "Accept" di RustDesk
6. Selesai support → User klik "Disconnect"
```

### Yang TIDAK BOLEH Dilakukan
- ❌ Minta password RustDesk user
- ❌ Install software tanpa izin user
- ❌ Akses file di luar folder SIMANIS62
- ❌ Remote tanpa user di depan komputer

## Input Validation

```python
from pydantic import BaseModel, Field, validator

class AsetCreate(BaseModel):
    nama_barang: str = Field(..., min_length=3, max_length=200)
    kode_barang: str = Field(..., pattern=r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$")
    harga: int = Field(..., ge=0, le=999_999_999_999)
    tahun_perolehan: int = Field(..., ge=1900, le=2100)

    @validator("nama_barang")
    def sanitize_nama(cls, v):
        # Remove potential XSS
        return v.strip().replace("<", "&lt;").replace(">", "&gt;")
```

## Audit Trail

```python
class AuditTrail(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    action: str  # CREATE, UPDATE, DELETE
    table_name: str
    record_id: UUID
    old_value: Optional[str]  # JSON
    new_value: Optional[str]  # JSON
    ip_address: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Referensi

#[[file:docs/api_contract.md]]
#[[file:docs/STAKEHOLDERS.md]]
