# API Contract Simanis62 V2

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 6 Januari 2026 | Architecture Engineer | API contract awal berdasarkan analisis RAG 6 dokumen arsitektur |
| **2.0** | **10 Januari 2026** | **Kiro AI** | **Sinkronisasi dengan data_schema.md v2.0: Update KIB B 13 field, fix naming convention (dapat_ekspor), fix kode_barang length (13 char)** |

---

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

Dokumen ini mendefinisikan kontrak API lengkap untuk sistem Simanis62 V2 berdasarkan analisis mendalam dari 6 dokumen arsitektur:
1. Tujuan Bisnis, Peta Pemangku Kepentingan, Kendala & Asumsi
2. Pemilik Kebenaran, Masalah Inti, Konteks & Batasan
3. Alur Kerja & Aturan Main (business rules lengkap)
4. STAKEHOLDERS (roles dan permissions)
5. Data Schema (11 tabel dengan relasi lengkap)
6. Tech Stack (FastAPI + SQLModel + SQLite)

Dokumen ini mencakup:
- **Base URL dan Versioning**
- **Authentication & Authorization**
- **Endpoint Specifications** (request/response schemas)
- **Error Handling** (error codes dan HTTP status)
- **Pagination, Filtering, Sorting**
- **Validation Rules**
- **Performance Targets**

### 1.2 Prinsip Desain API

| Prinsip | Implementasi | Alasan |
|---------|--------------|--------|
| **RESTful** | Resource-based URLs, proper HTTP methods | Industry standard, easy to understand |
| **Consistent** | Uniform response format, error handling | Predictable behavior for clients |
| **Secure** | Session-based auth, role-based access | Protect sensitive data |
| **Performant** | Pagination, indexing, caching | Meet performance targets (< 5s search) |
| **Documented** | Complete request/response examples | Easy integration for frontend |


### 1.3 Teknologi Stack

| Komponen | Teknologi | Versi | Keterangan |
|----------|-----------|-------|------------|
| Backend | FastAPI | Latest | REST API framework |
| ORM | SQLModel | Latest | SQLAlchemy + Pydantic integration |
| Database | SQLite | 3.x | WAL mode untuk concurrency |
| Authentication | Session-based | - | Cookie dengan HttpOnly flag |
| Serialization | JSON | - | Standard format |
| **DB Management** | **DBHub** | **Latest** | **Visual database explorer & MCP integration (development/testing tool)** |

**DBHub Note:** DBHub dapat digunakan untuk testing API endpoints dengan database queries. Konfigurasi tersedia di `dbhub.toml`. Lihat `.kiro/steering/DBHUB_GUIDE.md` untuk detail lengkap.

---

## 2. Base URL dan Versioning

### 2.1 Base URL

**Development/Production (Single-user):**
```
http://127.0.0.1:8000/api/v1
```

**Multi-user Setup (Optional):**
```
http://{server-ip}:8000/api/v1
```

### 2.2 API Versioning

- **Current Version:** v1
- **Versioning Strategy:** URL path versioning (e.g., `/api/v1`, `/api/v2`)
- **Backward Compatibility:** Major version changes only for breaking changes
- **Future Versions:** v2, v3 (when needed)

### 2.3 Content-Type

**Request:**
- `Content-Type: application/json` (for POST, PUT requests)

**Response:**
- `Content-Type: application/json` (default)
- `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (Excel export)


---

## 3. Authentication & Authorization

### 3.1 Authentication Strategy

**Session-based Authentication** dengan cookie (BUKAN JWT).

**Alasan:**
- Deployment model: Desktop app dengan backend lokal
- Security: Cookie dengan HttpOnly flag lebih aman
- Simplicity: Tidak perlu token refresh logic
- Performance: Session di SQLite cukup untuk < 10 concurrent users

### 3.2 Authentication Flow

```text
1. Client → POST /api/v1/auth/login (username, password)
2. Server → Validate credentials
3. Server → Create session, set cookie
4. Server → Response with user info
5. Client → Subsequent requests include cookie automatically
6. Server → Validate session on each request
7. Client → POST /api/v1/auth/logout
8. Server → Destroy session
```

### 3.3 Session Configuration

| Parameter | Value | Keterangan |
|-----------|-------|------------|
| Session Timeout | 2 jam | Sesuai dokumentasi stakeholder |
| Cookie Name | `simanis62_session` | Custom name |
| HttpOnly | `true` | Prevent XSS attacks |
| Secure | `false` | HTTP only (localhost) |
| SameSite | `Lax` | CSRF protection |

### 3.4 Authorization (Role-based Access Control)

| Role | Permissions | Endpoints |
|------|-------------|-----------|
| **Admin** | Full CRUD, Reports, Export, User Management | All endpoints |
| **Viewer (Guru)** | Read-only, Search | GET endpoints only |
| **Kepala Sekolah** | Read-only, Reports, Export | GET endpoints + Export |

**Implementation Note (v2.0):**
Kepala Sekolah menggunakan role **"Viewer"** dengan flag `dapat_ekspor=true` di database. Sistem menggunakan 2 technical roles (Admin, Viewer) untuk mendukung 3 business roles. Middleware API akan check `role == "Viewer" AND dapat_ekspor == true` untuk memberikan akses export kepada Kepala Sekolah.

> **Catatan Naming Convention:** Field database menggunakan snake_case Bahasa Indonesia (`dapat_ekspor`) sesuai standar proyek di AGENTS.md.

**Authorization Logic:**
```python
# Admin: Full access
if user.role == "Admin":
    return allow_all()

# Kepala Sekolah: Viewer with export permission
if user.role == "Viewer" and user.dapat_ekspor:
    return allow_read_and_export()

# Guru (Viewer): Read-only
if user.role == "Viewer":
    return allow_read_only()
```


---

## 4. Response Format

### 4.1 Success Response

**Format:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

**Example (Single Resource):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nama_barang": "Laptop HP Pavilion",
    "kode_barang": "32.01.02.0001",
    "status": "Aktif"
  },
  "message": "Aset berhasil ditambahkan"
}
```

**Example (List with Pagination):**
```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pagination": {
      "total": 1250,
      "page": 1,
      "limit": 100,
      "total_pages": 13
    }
  }
}
```

### 4.2 Error Response

**Format:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "field": "field_name",
    "details": { ... }
  }
}
```

**Example (Validation Error):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Tahun perolehan harus antara 1900 - 2026",
    "field": "tahun_perolehan",
    "details": {
      "min": 1900,
      "max": 2026,
      "provided": 2030
    }
  }
}
```


**Example (Multiple Validation Errors):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Terdapat 2 kesalahan validasi",
    "errors": [
      {
        "field": "nama_barang",
        "message": "Nama barang harus diisi (minimal 3 karakter)"
      },
      {
        "field": "harga",
        "message": "Harga harus lebih besar dari 0"
      }
    ]
  }
}
```

### 4.3 HTTP Status Codes

| Status Code | Meaning | Usage |
|-------------|---------|-------|
| 200 OK | Success | GET, PUT requests |
| 201 Created | Resource created | POST requests |
| 204 No Content | Success, no body | DELETE requests |
| 400 Bad Request | Validation error | Invalid input data |
| 401 Unauthorized | Not authenticated | Missing/invalid session |
| 403 Forbidden | Not authorized | Wrong role/permission |
| 404 Not Found | Resource not found | Invalid ID |
| 409 Conflict | Duplicate resource | Unique constraint violated |
| 422 Unprocessable Entity | Business rule violation | Semantic error |
| 500 Internal Server Error | Server error | Database error, unexpected |

### 4.4 Error Codes

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| VALIDATION_ERROR | 400 | Input validation failed |
| BUSINESS_RULE_VIOLATION | 422 | Business rule violated |
| DUPLICATE_ENTRY | 409 | Unique constraint violated |
| NOT_FOUND | 404 | Resource not found |
| UNAUTHORIZED | 401 | Not authenticated |
| FORBIDDEN | 403 | Not authorized |
| DATABASE_ERROR | 500 | Database operation failed |
| INTERNAL_ERROR | 500 | Unexpected error |


---

## 5. Pagination, Filtering, Sorting

### 5.1 Pagination

**Query Parameters:**
- `page` (integer, default: 1) - Page number
- `limit` (integer, default: 100, max: 100) - Items per page

**Example Request:**
```
GET /api/v1/aset?page=2&limit=50
```

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pagination": {
      "total": 1250,
      "page": 2,
      "limit": 50,
      "total_pages": 25
    }
  }
}
```

### 5.2 Filtering

**Common Filters (for /api/v1/aset):**
- `kategori_kib` (string) - Filter by KIB category (A/B/C/D/E/F)
- `status` (string) - Filter by status (Baru/Aktif/Mutasi/Rusak/Dihapus)
- `ruangan_id` (UUID) - Filter by room
- `kondisi` (string) - Filter by condition (Baik/Rusak Ringan/Rusak Berat)
- `tahun_perolehan` (integer) - Filter by acquisition year
- `tahun_min` (integer) - Filter by minimum year
- `tahun_max` (integer) - Filter by maximum year
- `asal_usul` (string) - Filter by origin (Pembelian/Hibah/Bantuan)

**Example Request:**
```
GET /api/v1/aset?kategori_kib=B&status=Aktif&kondisi=Baik
```

### 5.3 Sorting

**Query Parameters:**
- `sort_by` (string, default: created_at) - Field to sort by
- `sort_order` (string, default: desc) - Sort order (asc/desc)

**Sortable Fields:**
- `created_at`, `updated_at`, `nama_barang`, `nomor_register`, `harga`, `tahun_perolehan`

**Example Request:**
```
GET /api/v1/aset?sort_by=nama_barang&sort_order=asc
```

### 5.4 Search

**Endpoint:** `GET /api/v1/aset/search`

**Query Parameters:**
- `q` (string, required) - Search term
- `page`, `limit` - Pagination (same as above)

**Search Fields:** `nama_barang`, `kode_barang`, `keterangan`

**Performance Target:** < 5 detik (sesuai dokumentasi)

**Example Request:**
```
GET /api/v1/aset/search?q=laptop&page=1&limit=50
```


---

## 6. API Endpoints

### 6.1 Authentication Endpoints

#### 6.1.1 Login

**Endpoint:** `POST /api/v1/auth/login`

**Permission:** Public

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "admin",
      "nama_lengkap": "Administrator Sekolah",
      "role": "Admin",
      "status": "Aktif"
    }
  },
  "message": "Login berhasil"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Username atau password salah"
  }
}
```

**Notes:**
- Session cookie set automatically in response header
- Cookie name: `simanis62_session`
- HttpOnly: true, SameSite: Lax

#### 6.1.2 Logout

**Endpoint:** `POST /api/v1/auth/logout`

**Permission:** Authenticated users

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout berhasil"
}
```

**Notes:**
- Session destroyed on server
- Cookie cleared


#### 6.1.3 Get Current User

**Endpoint:** `GET /api/v1/auth/me`

**Permission:** Authenticated users

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "nama_lengkap": "Administrator Sekolah",
    "role": "Admin",
    "status": "Aktif",
    "dapat_ekspor": true,
    "created_at": "2026-01-01T00:00:00Z"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Session tidak valid atau sudah kadaluarsa"
  }
}
```

---

### 6.2 User Management Endpoints

#### 6.2.1 List Users

**Endpoint:** `GET /api/v1/users`

**Permission:** Admin only

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 100, max: 100)
- `role` (string, optional) - Filter by role (Admin/Viewer)
- `status` (string, optional) - Filter by status (Aktif/Nonaktif)

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "username": "admin",
        "nama_lengkap": "Administrator Sekolah",
        "role": "Admin",
        "status": "Aktif",
        "dapat_ekspor": true,
        "created_at": "2026-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "total": 5,
      "page": 1,
      "limit": 100,
      "total_pages": 1
    }
  }
}
```


#### 6.2.2 Create User

**Endpoint:** `POST /api/v1/users`

**Permission:** Admin only

**Request Body:**
```json
{
  "username": "guru01",
  "password": "password123",
  "nama_lengkap": "Budi Santoso",
  "role": "Viewer",
  "dapat_ekspor": false
}
```

**Validation Rules:**
- `username`: 5-50 characters, unique, alphanumeric + underscore
- `password`: Minimum 8 characters, must contain letters and numbers
- `nama_lengkap`: Required, max 200 characters
- `role`: Must be "Admin" or "Viewer"
- `dapat_ekspor`: Boolean, default false (set true for Kepala Sekolah)

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "username": "guru01",
    "nama_lengkap": "Budi Santoso",
    "role": "Viewer",
    "status": "Aktif",
    "dapat_ekspor": false,
    "created_at": "2026-01-06T10:30:00Z"
  },
  "message": "User berhasil dibuat"
}
```

**Error Response (409 Conflict):**
```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_ENTRY",
    "message": "Username 'guru01' sudah digunakan",
    "field": "username"
  }
}
```

#### 6.2.3 Get User Detail

**Endpoint:** `GET /api/v1/users/{id}`

**Permission:** Admin only

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "nama_lengkap": "Administrator Sekolah",
    "role": "Admin",
    "status": "Aktif",
    "dapat_ekspor": true,
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-05T15:20:00Z"
  }
}
```


#### 6.2.4 Update User

**Endpoint:** `PUT /api/v1/users/{id}`

**Permission:** Admin only

**Request Body:**
```json
{
  "nama_lengkap": "Budi Santoso Updated",
  "role": "Viewer",
  "status": "Aktif",
  "dapat_ekspor": true
}
```

**Notes:**
- Password update requires separate endpoint (for security)
- Cannot update own role or status (prevent lockout)
- Set `dapat_ekspor: true` to grant export permission (Kepala Sekolah)

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "username": "guru01",
    "nama_lengkap": "Budi Santoso Updated",
    "role": "Viewer",
    "status": "Aktif",
    "dapat_ekspor": true,
    "updated_at": "2026-01-06T11:00:00Z"
  },
  "message": "User berhasil diperbarui"
}
```

#### 6.2.5 Delete User (Soft Delete)

**Endpoint:** `DELETE /api/v1/users/{id}`

**Permission:** Admin only

**Notes:**
- Soft delete: Set status to "Nonaktif"
- Cannot delete self (prevent lockout)
- Cannot delete if user has created assets (referential integrity)

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "User berhasil dinonaktifkan"
}
```

**Error Response (422 Unprocessable Entity):**
```json
{
  "success": false,
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "Tidak dapat menghapus user sendiri"
  }
}
```


---

### 6.3 Room Management Endpoints

#### 6.3.1 List Rooms

**Endpoint:** `GET /api/v1/ruangan`

**Permission:** All authenticated users

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 100, max: 100)

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "nama_ruangan": "Lab Komputer",
        "kode_ruangan": "LAB-01",
        "keterangan": "Laboratorium komputer lantai 2",
        "created_at": "2026-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "total": 15,
      "page": 1,
      "limit": 100,
      "total_pages": 1
    }
  }
}
```

#### 6.3.2 Create Room

**Endpoint:** `POST /api/v1/ruangan`

**Permission:** Admin only

**Request Body:**
```json
{
  "nama_ruangan": "Lab Komputer",
  "kode_ruangan": "LAB-01",
  "keterangan": "Laboratorium komputer lantai 2"
}
```

**Validation Rules:**
- `nama_ruangan`: Required, max 200 characters, unique
- `kode_ruangan`: Required, max 50 characters, unique
- `keterangan`: Optional, max 500 characters

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "nama_ruangan": "Lab Komputer",
    "kode_ruangan": "LAB-01",
    "keterangan": "Laboratorium komputer lantai 2",
    "created_at": "2026-01-06T10:30:00Z"
  },
  "message": "Ruangan berhasil dibuat"
}
```


#### 6.3.3 Get Room Detail

**Endpoint:** `GET /api/v1/ruangan/{id}`

**Permission:** All authenticated users

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "nama_ruangan": "Lab Komputer",
    "kode_ruangan": "LAB-01",
    "keterangan": "Laboratorium komputer lantai 2",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-01-05T15:20:00Z",
    "jumlah_aset": 25
  }
}
```

#### 6.3.4 Update Room

**Endpoint:** `PUT /api/v1/ruangan/{id}`

**Permission:** Admin only

**Request Body:**
```json
{
  "nama_ruangan": "Lab Komputer Updated",
  "kode_ruangan": "LAB-01",
  "keterangan": "Laboratorium komputer lantai 2 (renovasi)"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "nama_ruangan": "Lab Komputer Updated",
    "kode_ruangan": "LAB-01",
    "keterangan": "Laboratorium komputer lantai 2 (renovasi)",
    "updated_at": "2026-01-06T11:00:00Z"
  },
  "message": "Ruangan berhasil diperbarui"
}
```

#### 6.3.5 Delete Room

**Endpoint:** `DELETE /api/v1/ruangan/{id}`

**Permission:** Admin only

**Notes:**
- Cannot delete if room contains assets (referential integrity)
- If deleted, assets moved to "Ruangan Tidak Diketahui"

**Success Response (204 No Content)**

**Error Response (422 Unprocessable Entity):**
```json
{
  "success": false,
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "Tidak dapat menghapus ruangan yang masih berisi aset. Pindahkan aset terlebih dahulu."
  }
}
```


---

### 6.4 Asset Management Endpoints

#### 6.4.1 List Assets

**Endpoint:** `GET /api/v1/aset`

**Permission:** All authenticated users

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 100, max: 100)
- `kategori_kib` (string) - Filter by KIB category (A/B/C/D/E/F)
- `status` (string) - Filter by status (Baru/Aktif/Mutasi/Rusak/Dihapus)
- `ruangan_id` (UUID) - Filter by room
- `kondisi` (string) - Filter by condition
- `sort_by` (string, default: created_at)
- `sort_order` (string, default: desc)

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "880e8400-e29b-41d4-a716-446655440003",
        "kode_barang": "32.01.02.0001",
        "nama_barang": "Laptop HP Pavilion",
        "nomor_register": 1,
        "kategori_kib": "B",
        "tahun_perolehan": 2024,
        "asal_usul": "Pembelian",
        "harga": 8500000,
        "kondisi": "Baik",
        "status": "Aktif",
        "ruangan": {
          "id": "770e8400-e29b-41d4-a716-446655440002",
          "nama_ruangan": "Lab Komputer",
          "kode_ruangan": "LAB-01"
        },
        "created_at": "2026-01-05T10:00:00Z"
      }
    ],
    "pagination": {
      "total": 1250,
      "page": 1,
      "limit": 100,
      "total_pages": 13
    }
  }
}
```


#### 6.4.2 Create Asset

**Endpoint:** `POST /api/v1/aset`

**Permission:** Admin only

**Request Body (KIB B Example):**
```json
{
  "kode_barang": "32.01.02.0001",
  "nama_barang": "Laptop HP Pavilion",
  "kategori_kib": "B",
  "tahun_perolehan": 2024,
  "tanggal_perolehan": "2024-03-15",
  "asal_usul": "Pembelian",
  "harga": 8500000,
  "kondisi": "Baik",
  "keterangan": "Laptop untuk lab komputer",
  "ruangan_id": "770e8400-e29b-41d4-a716-446655440002",
  "kib_b": {
    "satuan": "BH",
    "ukuran_cc": null,
    "tanggal_dokumen": null,
    "bahan": "Plastik",
    "merk": "HP",
    "tipe": "Pavilion 14",
    "nomor_rangka": null,
    "nomor_mesin": null,
    "nomor_polisi": null,
    "kapitalisasi": null,
    "total_harga": 8500000
  }
}
```

**Validation Rules:**
- `kode_barang`: Format XX.XX.XX.XXXX, unique
- `nama_barang`: 3-200 characters
- `kategori_kib`: Must be A/B/C/D/E/F
- `tahun_perolehan`: 1900 - current year
- `asal_usul`: Must be Pembelian/Hibah/Bantuan
- `harga`: Positive integer, max 999999999999
- `kondisi`: Must be Baik/Rusak Ringan/Rusak Berat
- `ruangan_id`: Must exist in database
- `kib_x`: Required fields based on kategori_kib (see section 7)

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "kode_barang": "32.01.02.0001",
    "nama_barang": "Laptop HP Pavilion",
    "nomor_register": 1,
    "kategori_kib": "B",
    "status": "Baru",
    "created_at": "2026-01-06T10:30:00Z",
    "created_by": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nama_lengkap": "Administrator Sekolah"
    }
  },
  "message": "Aset berhasil ditambahkan dengan Nomor Register: 1"
}
```

**Error Response (409 Conflict):**
```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_ENTRY",
    "message": "Kode barang 32.01.02.0001 sudah digunakan",
    "field": "kode_barang"
  }
}
```


#### 6.4.3 Get Asset Detail

**Endpoint:** `GET /api/v1/aset/{id}`

**Permission:** All authenticated users

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "kode_barang": "32.01.02.0001",
    "nama_barang": "Laptop HP Pavilion",
    "nomor_register": 1,
    "kategori_kib": "B",
    "tahun_perolehan": 2024,
    "tanggal_perolehan": "2024-03-15",
    "asal_usul": "Pembelian",
    "harga": 8500000,
    "kondisi": "Baik",
    "status": "Aktif",
    "keterangan": "Laptop untuk lab komputer",
    "ruangan": {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "nama_ruangan": "Lab Komputer",
      "kode_ruangan": "LAB-01"
    },
    "kib_b": {
      "satuan": "BH",
      "ukuran_cc": null,
      "tanggal_dokumen": null,
      "bahan": "Plastik",
      "merk": "HP",
      "tipe": "Pavilion 14",
      "nomor_rangka": null,
      "nomor_mesin": null,
      "nomor_polisi": null,
      "kapitalisasi": null,
      "total_harga": 8500000
    },
    "created_by": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nama_lengkap": "Administrator Sekolah"
    },
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T15:20:00Z"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Aset dengan ID tersebut tidak ditemukan"
  }
}
```


#### 6.4.4 Update Asset

**Endpoint:** `PUT /api/v1/aset/{id}`

**Permission:** Admin only

**Request Body:**
```json
{
  "nama_barang": "Laptop HP Pavilion Updated",
  "kondisi": "Rusak Ringan",
  "keterangan": "Keyboard rusak, perlu perbaikan",
  "kib_b": {
    "satuan": "BH",
    "ukuran_cc": null,
    "tanggal_dokumen": null,
    "bahan": "Plastik",
    "merk": "HP",
    "tipe": "Pavilion 14",
    "nomor_rangka": null,
    "nomor_mesin": null,
    "nomor_polisi": null,
    "kapitalisasi": null,
    "total_harga": 8500000
  }
}
```

**Notes:**
- Cannot update `kode_barang` (immutable)
- Cannot update `nomor_register` (auto-generated)
- Cannot update `kategori_kib` (immutable)
- Status auto-updated based on kondisi (Rusak Ringan/Berat → status Rusak)

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "nama_barang": "Laptop HP Pavilion Updated",
    "kondisi": "Rusak Ringan",
    "status": "Rusak",
    "updated_at": "2026-01-06T11:00:00Z",
    "updated_by": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nama_lengkap": "Administrator Sekolah"
    }
  },
  "message": "Aset berhasil diperbarui"
}
```

#### 6.4.5 Delete Asset (Soft Delete)

**Endpoint:** `DELETE /api/v1/aset/{id}`

**Permission:** Admin only

**Request Body:**
```json
{
  "delete_reason": "Aset sudah tidak layak pakai dan tidak dapat diperbaiki lagi"
}
```

**Validation Rules:**
- `delete_reason`: Required, minimum 20 characters
- Cannot delete if status = "Mutasi" (asset in transit)

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Aset berhasil dihapus dari inventaris aktif"
}
```

**Error Response (422 Unprocessable Entity):**
```json
{
  "success": false,
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "Aset tidak dapat dihapus karena sedang dalam proses mutasi"
  }
}
```


#### 6.4.6 Search Assets

**Endpoint:** `GET /api/v1/aset/search`

**Permission:** All authenticated users

**Query Parameters:**
- `q` (string, required) - Search term
- `page` (integer, default: 1)
- `limit` (integer, default: 100, max: 100)

**Search Fields:** `nama_barang`, `kode_barang`, `keterangan`

**Performance Target:** < 5 detik

**Example Request:**
```
GET /api/v1/aset/search?q=laptop&page=1&limit=50
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pagination": {
      "total": 25,
      "page": 1,
      "limit": 50,
      "total_pages": 1
    },
    "search_term": "laptop"
  }
}
```

#### 6.4.7 Get Asset History

**Endpoint:** `GET /api/v1/aset/{id}/history`

**Permission:** All authenticated users

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "aset_id": "880e8400-e29b-41d4-a716-446655440003",
    "mutations": [
      {
        "id": "990e8400-e29b-41d4-a716-446655440004",
        "ruangan_asal": {
          "id": "770e8400-e29b-41d4-a716-446655440002",
          "nama_ruangan": "Lab Komputer"
        },
        "ruangan_tujuan": {
          "id": "770e8400-e29b-41d4-a716-446655440005",
          "nama_ruangan": "Ruang Guru"
        },
        "tanggal_mutasi": "2026-01-05",
        "alasan": "Perpindahan aset ke ruang guru",
        "status_mutasi": "Selesai",
        "user": {
          "nama_lengkap": "Administrator Sekolah"
        },
        "selesai_mutasi": "2026-01-05T16:00:00Z"
      }
    ]
  }
}
```


---

### 6.5 Mutation Endpoints

#### 6.5.1 Create Mutation

**Endpoint:** `POST /api/v1/mutasi`

**Permission:** Admin only

**Request Body:**
```json
{
  "aset_id": "880e8400-e29b-41d4-a716-446655440003",
  "ruangan_tujuan_id": "770e8400-e29b-41d4-a716-446655440005",
  "tanggal_mutasi": "2026-01-06",
  "alasan": "Perpindahan aset ke ruang guru",
  "kondisi_saat_mutasi": "Baik"
}
```

**Validation Rules:**
- `aset_id`: Must exist and status != "Mutasi" (cannot mutate asset already in transit)
- `ruangan_tujuan_id`: Must exist and different from current room
- `tanggal_mutasi`: Cannot be in the future
- `alasan`: Minimum 10 characters
- `kondisi_saat_mutasi`: Must be Baik/Rusak Ringan/Rusak Berat

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "990e8400-e29b-41d4-a716-446655440004",
    "aset_id": "880e8400-e29b-41d4-a716-446655440003",
    "status_mutasi": "Dalam Proses",
    "mulai_mutasi": "2026-01-06T10:30:00Z"
  },
  "message": "Mutasi aset berhasil diproses"
}
```

**Error Response (422 Unprocessable Entity):**
```json
{
  "success": false,
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "Aset tidak dapat dimutasi karena sedang dalam proses mutasi lain"
  }
}
```

**Notes:**
- Asset status automatically changed to "Mutasi"
- Mutation status set to "Dalam Proses"


#### 6.5.2 Get Mutation Detail

**Endpoint:** `GET /api/v1/mutasi/{id}`

**Permission:** All authenticated users

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "990e8400-e29b-41d4-a716-446655440004",
    "aset": {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "kode_barang": "32.01.02.0001",
      "nama_barang": "Laptop HP Pavilion"
    },
    "ruangan_asal": {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "nama_ruangan": "Lab Komputer"
    },
    "ruangan_tujuan": {
      "id": "770e8400-e29b-41d4-a716-446655440005",
      "nama_ruangan": "Ruang Guru"
    },
    "tanggal_mutasi": "2026-01-06",
    "alasan": "Perpindahan aset ke ruang guru",
    "kondisi_saat_mutasi": "Baik",
    "status_mutasi": "Dalam Proses",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nama_lengkap": "Administrator Sekolah"
    },
    "mulai_mutasi": "2026-01-06T10:30:00Z",
    "selesai_mutasi": null
  }
}
```

#### 6.5.3 Complete Mutation

**Endpoint:** `PUT /api/v1/mutasi/{id}/complete`

**Permission:** Admin only

**Request Body:** None

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "990e8400-e29b-41d4-a716-446655440004",
    "status_mutasi": "Selesai",
    "selesai_mutasi": "2026-01-06T16:00:00Z"
  },
  "message": "Mutasi aset berhasil diselesaikan"
}
```

**Notes:**
- Asset `ruangan_id` updated to `ruangan_tujuan_id`
- Asset status changed from "Mutasi" to "Aktif"
- Mutation status changed to "Selesai"


#### 6.5.4 Cancel Mutation

**Endpoint:** `PUT /api/v1/mutasi/{id}/cancel`

**Permission:** Admin only

**Request Body:**
```json
{
  "alasan_pembatalan": "Aset tidak jadi dipindahkan karena masih dibutuhkan di ruangan asal"
}
```

**Validation Rules:**
- `alasan_pembatalan`: Required, minimum 10 characters
- Can only cancel if status_mutasi = "Dalam Proses"

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "990e8400-e29b-41d4-a716-446655440004",
    "status_mutasi": "Dibatalkan",
    "alasan_pembatalan": "Aset tidak jadi dipindahkan karena masih dibutuhkan di ruangan asal"
  },
  "message": "Mutasi aset berhasil dibatalkan"
}
```

**Notes:**
- Asset status changed from "Mutasi" back to "Aktif"
- Asset remains in original room
- Mutation status changed to "Dibatalkan"

#### 6.5.5 List Mutations

**Endpoint:** `GET /api/v1/mutasi`

**Permission:** All authenticated users

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 100, max: 100)
- `status_mutasi` (string) - Filter by status (Dalam Proses/Selesai/Dibatalkan)
- `aset_id` (UUID) - Filter by asset

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pagination": {
      "total": 50,
      "page": 1,
      "limit": 100,
      "total_pages": 1
    }
  }
}
```


---

### 6.6 Report Endpoints

#### 6.6.1 Get KIB Report

**Endpoint:** `GET /api/v1/kib/{kategori}`

**Permission:** All authenticated users

**Path Parameters:**
- `kategori` (string, required) - KIB category (A/B/C/D/E/F)

**Query Parameters:**
- `tahun_perolehan` (integer, optional) - Filter by acquisition year
- `kondisi` (string, optional) - Filter by condition
- `ruangan_id` (UUID, optional) - Filter by room

**Performance Target:** < 10 detik untuk 1000 aset

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "kategori": "B",
    "nama_kategori": "Peralatan dan Mesin",
    "items": [
      {
        "nomor_register": 1,
        "kode_barang": "32.01.02.0001",
        "nama_barang": "Laptop HP Pavilion",
        "tahun_perolehan": 2024,
        "tanggal_perolehan": "2024-03-15",
        "asal_usul": "Pembelian",
        "harga": 8500000,
        "kondisi": "Baik",
        "ruangan": {
          "nama_ruangan": "Lab Komputer",
          "kode_ruangan": "LAB-01"
        },
        "kib_b": {
          "satuan": "BH",
          "ukuran_cc": null,
          "tanggal_dokumen": null,
          "bahan": "Plastik",
          "merk": "HP",
          "tipe": "Pavilion 14",
          "nomor_rangka": null,
          "nomor_mesin": null,
          "nomor_polisi": null,
          "kapitalisasi": null,
          "total_harga": 8500000
        }
      }
    ],
    "summary": {
      "total_aset": 125,
      "total_nilai": 1250000000,
      "kondisi_baik": 100,
      "kondisi_rusak_ringan": 20,
      "kondisi_rusak_berat": 5
    }
  }
}
```


#### 6.6.2 Export KIB to Excel

**Endpoint:** `GET /api/v1/kib/{kategori}/export`

**Permission:** Admin, Kepala Sekolah

**Path Parameters:**
- `kategori` (string, required) - KIB category (A/B/C/D/E/F)

**Query Parameters:**
- Same as GET /api/v1/kib/{kategori}

**Performance Target:** < 15 detik untuk 1000 aset

**Success Response (200 OK):**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Content-Disposition: `attachment; filename="KIB_B_20260106.xlsx"`
- Body: Excel file binary

**Notes:**
- Format Excel sesuai **BPAD DKI Jakarta** (18 kolom untuk KIB B)
- Harga dalam **Rupiah penuh** (BUKAN ribuan)
- Format tanggal: DD/MM/YYYY
- Include header with school info
- Include footer with signature section

#### 6.6.3 Get KIR Report (per Room)

**Endpoint:** `GET /api/v1/kir/{ruangan_id}`

**Permission:** All authenticated users

**Path Parameters:**
- `ruangan_id` (UUID, required) - Room ID

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "ruangan": {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "nama_ruangan": "Lab Komputer",
      "kode_ruangan": "LAB-01"
    },
    "items": [
      {
        "nomor_register": 1,
        "kode_barang": "32.01.02.0001",
        "nama_barang": "Laptop HP Pavilion",
        "kategori_kib": "B",
        "tahun_perolehan": 2024,
        "harga": 8500000,
        "kondisi": "Baik"
      }
    ],
    "summary": {
      "total_aset": 25,
      "total_nilai": 250000000
    }
  }
}
```


#### 6.6.4 Export KIR to Excel

**Endpoint:** `GET /api/v1/kir/{ruangan_id}/export`

**Permission:** Admin, Kepala Sekolah

**Path Parameters:**
- `ruangan_id` (UUID, required) - Room ID

**Success Response (200 OK):**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Content-Disposition: `attachment; filename="KIR_Lab_Komputer_20260106.xlsx"`
- Body: Excel file binary

---

### 6.7 Audit Trail Endpoints

#### 6.7.1 List Audit Logs

**Endpoint:** `GET /api/v1/audit`

**Permission:** Admin only

**Query Parameters:**
- `page` (integer, default: 1)
- `limit` (integer, default: 100, max: 100)
- `table_name` (string, optional) - Filter by table (aset/users/ruangan/etc)
- `operation` (string, optional) - Filter by operation (CREATE/UPDATE/DELETE)
- `user_id` (UUID, optional) - Filter by user
- `start_date` (date, optional) - Filter by date range (start)
- `end_date` (date, optional) - Filter by date range (end)

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "aa0e8400-e29b-41d4-a716-446655440006",
        "table_name": "aset",
        "record_id": "880e8400-e29b-41d4-a716-446655440003",
        "operation": "UPDATE",
        "user": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "nama_lengkap": "Administrator Sekolah"
        },
        "old_value": {
          "kondisi": "Baik"
        },
        "new_value": {
          "kondisi": "Rusak Ringan"
        },
        "timestamp": "2026-01-06T11:00:00Z",
        "ip_address": "127.0.0.1"
      }
    ],
    "pagination": {
      "total": 500,
      "page": 1,
      "limit": 100,
      "total_pages": 5
    }
  }
}
```


#### 6.7.2 Get Audit Detail

**Endpoint:** `GET /api/v1/audit/{id}`

**Permission:** Admin only

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "aa0e8400-e29b-41d4-a716-446655440006",
    "table_name": "aset",
    "record_id": "880e8400-e29b-41d4-a716-446655440003",
    "operation": "UPDATE",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "admin",
      "nama_lengkap": "Administrator Sekolah"
    },
    "old_value": {
      "kondisi": "Baik",
      "status": "Aktif"
    },
    "new_value": {
      "kondisi": "Rusak Ringan",
      "status": "Rusak"
    },
    "timestamp": "2026-01-06T11:00:00Z",
    "ip_address": "127.0.0.1"
  }
}
```

---

### 6.8 System Endpoints

#### 6.8.1 Health Check

**Endpoint:** `GET /api/v1/health`

**Permission:** Public

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "ok",
    "database": "connected",
    "version": "1.0.0",
    "timestamp": "2026-01-06T10:30:00Z"
  }
}
```

#### 6.8.2 Backup Database

**Endpoint:** `POST /api/v1/system/backup`

**Permission:** Admin only

**Success Response (200 OK):**
- Content-Type: `application/x-sqlite3`
- Content-Disposition: `attachment; filename="simanis62_backup_20260106_103000.db"`
- Body: SQLite database file binary

**Notes:**
- Creates a copy of the current database
- Filename includes timestamp


---

## 7. KIB-Specific Field Requirements

### 7.1 KIB A (Tanah)

**Required Fields in `kib_a` object:**
```json
{
  "luas_m2": 1000.50,
  "alamat_lokasi": "Jl. Pendidikan No. 123, Kota ABC",
  "sertifikat": "SHM No. 12345/2020"
}
```

**Validation Rules:**
- `luas_m2`: Positive decimal, required
- `alamat_lokasi`: Minimum 10 characters, required
- `sertifikat`: Optional, max 100 characters

### 7.2 KIB B (Peralatan dan Mesin) - Format BPAD DKI Jakarta 18 Kolom

**Sumber Format:** PDF Resmi BPAD DKI Jakarta (Update form: 07/04/2022, Rekon Semester 1 Tahun 2024)
**URL:** https://bkddki.jakarta.go.id/download/detail/N3Q3NR1JDVVKMY9

**Catatan:** Beberapa field KIB B sudah ada di tabel utama `aset` (kode_barang, nama_barang, tanggal_perolehan, asal_usul, harga). Object `kib_b` hanya menyimpan field spesifik KIB B yang tidak ada di tabel utama.

**Required Fields in `kib_b` object:**
```json
{
  "satuan": "BH",
  "ukuran_cc": null,
  "tanggal_dokumen": null,
  "bahan": "Plastik",
  "merk": "HP",
  "tipe": "Pavilion 14",
  "nomor_rangka": null,
  "nomor_mesin": null,
  "nomor_polisi": null,
  "kapitalisasi": null,
  "total_harga": 8500000
}
```

**Mapping ke Format BPAD DKI Jakarta (18 Kolom):**

| No | Kolom BPAD | Field Database | Lokasi | Wajib? |
|----|------------|----------------|--------|--------|
| 1 | NO. | (auto-increment) | - | Ya |
| 2 | KODE BARANG | kode_barang | aset | Ya |
| 3 | REG. | nomor_register | aset | Ya |
| 4 | JENIS BARANG | nama_barang | aset | Ya |
| 5 | UKU-RAN | ukuran_cc | kib_b | Tidak |
| 6 | SATU-AN | satuan | kib_b | **Ya** |
| 7 | TGL. OLEH | tanggal_perolehan | aset | Ya |
| 8 | BA-HAN | bahan | kib_b | Tidak |
| 9 | MEREK | merk | kib_b | Tidak |
| 10 | TYPE | tipe | kib_b | Tidak |
| 11 | TGL. BPKB/DOK. | tanggal_dokumen | kib_b | Tidak |
| 12 | NO. CHASIS/RANGKA | nomor_rangka | kib_b | Tidak |
| 13 | NO. MESIN/PABRIK | nomor_mesin | kib_b | Tidak |
| 14 | NOMOR POLISI | nomor_polisi | kib_b | Tidak |
| 15 | ASAL OLEH | asal_usul | aset | Ya |
| 16 | HARGA (Rp.) | harga | aset | Ya |
| 17 | KAPITALISASI (Rp.) | kapitalisasi | kib_b | Tidak |
| 18 | TOTAL (Rp.) | total_harga | kib_b | Ya |

**Validation Rules:**
- `satuan`: Required, max 20 characters (BH/Unit/Set/Buah/Paket/Rim/Dus)
- `ukuran_cc`: Optional, max 50 characters
- `tanggal_dokumen`: Optional, format YYYY-MM-DD (display DD/MM/YYYY)
- `bahan`: Optional, max 100 characters
- `merk`: Optional, max 100 characters
- `tipe`: Optional, max 100 characters
- `nomor_rangka`: Optional, max 50 characters (untuk kendaraan)
- `nomor_mesin`: Optional, max 50 characters
- `nomor_polisi`: Optional, max 20 characters (untuk kendaraan)
- `kapitalisasi`: Optional, positive integer (Rupiah penuh)
- `total_harga`: Optional, positive integer (Rupiah penuh)

**Catatan Penting:**
- Harga dalam **Rupiah penuh** (BUKAN ribuan) - sesuai format BPAD DKI Jakarta
- Field `nomor_rangka`, `nomor_mesin`, `nomor_polisi` khusus untuk kendaraan (boleh kosong untuk non-kendaraan)
- Format tanggal: DD/MM/YYYY untuk display di laporan Excel

### 7.3 KIB C (Gedung dan Bangunan)

**Required Fields in `kib_c` object:**
```json
{
  "luas_m2": 500.00,
  "alamat_lokasi": "Jl. Pendidikan No. 123, Kota ABC",
  "bertingkat": 2
}
```

**Validation Rules:**
- `luas_m2`: Positive decimal, required
- `alamat_lokasi`: Minimum 10 characters, required
- `bertingkat`: Integer 1-10, optional

### 7.4 KIB D (Jalan, Irigasi, Jaringan)

**Required Fields in `kib_d` object:**
```json
{
  "panjang_m": 100.00,
  "lebar_m": 5.00,
  "alamat_lokasi": "Jl. Pendidikan No. 123, Kota ABC"
}
```

**Validation Rules:**
- `panjang_m`: Positive decimal, required
- `lebar_m`: Positive decimal, required
- `alamat_lokasi`: Minimum 10 characters, required


### 7.5 KIB E (Aset Tetap Lainnya)

**Required Fields in `kib_e` object:**
```json
{
  "judul_nama": "Buku Perpustakaan: Matematika Kelas 10",
  "penerbit": "Penerbit Erlangga"
}
```

**Validation Rules:**
- `judul_nama`: 3-200 characters, required
- `penerbit`: Optional, max 200 characters

### 7.6 KIB F (Konstruksi dalam Pengerjaan)

**Required Fields in `kib_f` object:**
```json
{
  "alamat_lokasi": "Jl. Pendidikan No. 123, Kota ABC",
  "persentase_selesai": 75
}
```

**Validation Rules:**
- `alamat_lokasi`: Minimum 10 characters, required
- `persentase_selesai`: Integer 0-100, required

---

## 8. Validation Rules Summary

### 8.1 Common Field Validations

| Field | Type | Min | Max | Pattern | Required |
|-------|------|-----|-----|---------|----------|
| kode_barang | string | 13 | 13 | XX.XX.XX.XXXX | Yes |
| nama_barang | string | 3 | 200 | - | Yes |
| tahun_perolehan | integer | 1900 | current year | - | Yes |
| tanggal_perolehan | date | - | - | YYYY-MM-DD | No |
| harga | integer | 1 | 999999999999 | - | Yes |
| kondisi | enum | - | - | Baik/Rusak Ringan/Rusak Berat | Yes |
| asal_usul | enum | - | - | Pembelian/Hibah/Bantuan | Yes |
| kategori_kib | enum | - | - | A/B/C/D/E/F | Yes |
| keterangan | string | 0 | 500 | - | No |
| delete_reason | string | 20 | 500 | - | Yes (for delete) |

> **Catatan:** `kode_barang` format XX.XX.XX.XXXX = 2+1+2+1+2+1+4 = **13 karakter** (termasuk titik pemisah)

### 8.2 User Field Validations

| Field | Type | Min | Max | Pattern | Required |
|-------|------|-----|-----|---------|----------|
| username | string | 5 | 50 | alphanumeric + underscore | Yes |
| password | string | 8 | - | letters + numbers | Yes |
| nama_lengkap | string | 1 | 200 | - | Yes |
| role | enum | - | - | Admin/Viewer | Yes |
| dapat_ekspor | boolean | - | - | true/false | No (default: false) |


### 8.3 Room Field Validations

| Field | Type | Min | Max | Pattern | Required |
|-------|------|-----|-----|---------|----------|
| nama_ruangan | string | 1 | 200 | - | Yes |
| kode_ruangan | string | 1 | 50 | - | Yes |
| keterangan | string | 0 | 500 | - | No |

### 8.4 Mutation Field Validations

| Field | Type | Min | Max | Pattern | Required |
|-------|------|-----|-----|---------|----------|
| alasan | string | 10 | 500 | - | Yes |
| alasan_pembatalan | string | 10 | 500 | - | Yes (for cancel) |
| kondisi_saat_mutasi | enum | - | - | Baik/Rusak Ringan/Rusak Berat | Yes |

---

## 9. Business Rules

### 9.1 Asset Status Transitions

**Valid Transitions:**
```text
Baru → Aktif (after verification)
Aktif → Mutasi (when mutation starts)
Mutasi → Aktif (when mutation completes)
Aktif → Rusak (when kondisi = Rusak Ringan/Berat)
Rusak → Aktif (when repaired, kondisi = Baik)
Aktif → Dihapus (soft delete)
Rusak → Dihapus (soft delete)
```

**Invalid Transitions:**
- Mutasi → Dihapus (cannot delete asset in transit)
- Dihapus → Any (soft deleted assets cannot be restored via API)

### 9.2 Mutation Rules

1. Cannot mutate asset with status "Mutasi" (already in transit)
2. Cannot mutate to same room (ruangan_tujuan must be different)
3. Cannot delete asset with status "Mutasi"
4. Mutation can only be cancelled if status = "Dalam Proses"
5. Completing mutation updates asset's ruangan_id and status

### 9.3 Deletion Rules

1. Soft delete only (status = "Dihapus", deleted_at timestamp)
2. Delete reason required (minimum 20 characters)
3. Cannot delete if status = "Mutasi"
4. Deleted assets excluded from reports by default
5. Deleted assets remain in database for audit trail


### 9.4 Uniqueness Constraints

1. `users.username` - Must be unique
2. `ruangan.nama_ruangan` - Must be unique
3. `ruangan.kode_ruangan` - Must be unique
4. `aset.kode_barang` - Must be unique across all assets
5. `aset.nomor_register` - Auto-generated, sequential per kategori_kib

### 9.5 Referential Integrity

1. `aset.ruangan_id` → `ruangan.id` (ON DELETE RESTRICT)
2. `aset.created_by` → `users.id` (ON DELETE RESTRICT)
3. `riwayat_mutasi.aset_id` → `aset.id` (ON DELETE RESTRICT)
4. `riwayat_mutasi.user_id` → `users.id` (ON DELETE RESTRICT)

### 9.6 Auto-Generated Fields

1. `id` - UUID generated automatically
2. `nomor_register` - Sequential per kategori_kib (application-level)
3. `created_at` - Timestamp on creation
4. `updated_at` - Timestamp on update
5. `status` - Default "Baru" for new assets

---

## 10. Performance Targets

### 10.1 Response Time Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Authentication | < 1 second | Login/logout |
| List assets (100 items) | < 2 seconds | With pagination |
| Search assets | < 5 seconds | Full-text search |
| Create asset | < 2 seconds | Including validation |
| Update asset | < 2 seconds | Including validation |
| Generate KIB report | < 10 seconds | For 1000 assets |
| Export Excel | < 15 seconds | For 1000 assets |
| Mutation operations | < 2 seconds | Create/complete/cancel |

### 10.2 Concurrency

- **Target:** 10 concurrent users
- **Database:** SQLite with WAL mode
- **Session:** In-memory or SQLite-based
- **Read operations:** Unlimited concurrent reads
- **Write operations:** Sequential (SQLite limitation)


### 10.3 Pagination Limits

- **Default limit:** 100 items per page
- **Maximum limit:** 100 items per page
- **Reason:** Balance between performance and usability

### 10.4 Database Optimization

1. **Indexes:**
   - `aset.kode_barang` (unique)
   - `aset.nama_barang` (search)
   - `aset.kategori_kib` (filtering)
   - `aset.status` (filtering)
   - `aset.ruangan_id` (foreign key)
   - `users.username` (unique)
   - `ruangan.nama_ruangan` (unique)

2. **Query Optimization:**
   - Use JOIN for related data (avoid N+1 queries)
   - Use pagination for large result sets
   - Use indexes for frequently queried fields

3. **Caching:**
   - Cache frequently accessed data (rooms, users)
   - Cache duration: 5 minutes
   - Invalidate on update

---

## 11. Security Considerations

### 11.1 Authentication

- **Session-based** with HttpOnly cookies
- **Session timeout:** 2 hours of inactivity
- **Password hashing:** bcrypt with salt
- **Password policy:** Minimum 8 characters, letters + numbers

### 11.2 Authorization

- **Role-based access control (RBAC)**
- **Admin:** Full CRUD access
- **Viewer:** Read-only access
- **Kepala Sekolah:** Read + Export access

### 11.3 Input Validation

- **Client-side:** Real-time validation for UX
- **Server-side:** Final validation before database
- **Sanitization:** Prevent SQL injection, XSS

### 11.4 Audit Trail

- **All CRUD operations logged** in audit_trail table
- **Immutable:** Audit logs cannot be deleted
- **Fields logged:** user_id, timestamp, operation, old_value, new_value


### 11.5 Data Protection

- **Soft delete:** Data never physically deleted
- **Backup:** Automatic daily backup at 23:00
- **Retention:** 30 days backup retention
- **Encryption:** Database file encryption (optional)

---

## 12. Error Handling Examples

### 12.1 Validation Error (Single Field)

**Request:**
```json
POST /api/v1/aset
{
  "nama_barang": "AB",
  "tahun_perolehan": 2030
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Terdapat 2 kesalahan validasi",
    "errors": [
      {
        "field": "nama_barang",
        "message": "Nama barang harus minimal 3 karakter"
      },
      {
        "field": "tahun_perolehan",
        "message": "Tahun perolehan harus antara 1900 - 2026"
      }
    ]
  }
}
```

### 12.2 Business Rule Violation

**Request:**
```json
DELETE /api/v1/aset/880e8400-e29b-41d4-a716-446655440003
{
  "delete_reason": "Aset rusak"
}
```

**Response (422 Unprocessable Entity):**
```json
{
  "success": false,
  "error": {
    "code": "BUSINESS_RULE_VIOLATION",
    "message": "Aset tidak dapat dihapus karena sedang dalam proses mutasi. Selesaikan atau batalkan mutasi terlebih dahulu."
  }
}
```

### 12.3 Duplicate Entry

**Request:**
```json
POST /api/v1/aset
{
  "kode_barang": "32.01.02.0001",
  ...
}
```

**Response (409 Conflict):**
```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_ENTRY",
    "message": "Kode barang 32.01.02.0001 sudah digunakan",
    "field": "kode_barang"
  }
}
```


### 12.4 Not Found

**Request:**
```
GET /api/v1/aset/invalid-uuid
```

**Response (404 Not Found):**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Aset dengan ID tersebut tidak ditemukan"
  }
}
```

### 12.5 Unauthorized

**Request:**
```
GET /api/v1/aset
(without session cookie)
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Session tidak valid atau sudah kadaluarsa. Silakan login kembali."
  }
}
```

### 12.6 Forbidden

**Request:**
```
POST /api/v1/users
(as Viewer role)
```

**Response (403 Forbidden):**
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Anda tidak memiliki akses untuk melakukan operasi ini. Hanya Admin yang dapat mengelola user."
  }
}
```

### 12.7 Database Error

**Response (500 Internal Server Error):**
```json
{
  "success": false,
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Terjadi kesalahan saat menyimpan data. Silakan coba lagi dalam beberapa saat."
  }
}
```

**Notes:**
- Technical details (SQL query, stack trace) NOT exposed to client
- Logged to server log file for debugging


---

## 13. API Endpoint Summary

### 13.1 Authentication (3 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| POST | /api/v1/auth/login | Public | User login |
| POST | /api/v1/auth/logout | Authenticated | User logout |
| GET | /api/v1/auth/me | Authenticated | Get current user |

### 13.2 User Management (5 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | /api/v1/users | Admin | List users |
| POST | /api/v1/users | Admin | Create user |
| GET | /api/v1/users/{id} | Admin | Get user detail |
| PUT | /api/v1/users/{id} | Admin | Update user |
| DELETE | /api/v1/users/{id} | Admin | Delete user (soft) |

### 13.3 Room Management (5 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | /api/v1/ruangan | All | List rooms |
| POST | /api/v1/ruangan | Admin | Create room |
| GET | /api/v1/ruangan/{id} | All | Get room detail |
| PUT | /api/v1/ruangan/{id} | Admin | Update room |
| DELETE | /api/v1/ruangan/{id} | Admin | Delete room |

### 13.4 Asset Management (7 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | /api/v1/aset | All | List assets |
| POST | /api/v1/aset | Admin | Create asset |
| GET | /api/v1/aset/{id} | All | Get asset detail |
| PUT | /api/v1/aset/{id} | Admin | Update asset |
| DELETE | /api/v1/aset/{id} | Admin | Delete asset (soft) |
| GET | /api/v1/aset/search | All | Search assets |
| GET | /api/v1/aset/{id}/history | All | Get asset history |

### 13.5 Mutation (5 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| POST | /api/v1/mutasi | Admin | Create mutation |
| GET | /api/v1/mutasi/{id} | All | Get mutation detail |
| PUT | /api/v1/mutasi/{id}/complete | Admin | Complete mutation |
| PUT | /api/v1/mutasi/{id}/cancel | Admin | Cancel mutation |
| GET | /api/v1/mutasi | All | List mutations |


### 13.6 Reports (4 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | /api/v1/kib/{kategori} | All | Get KIB report |
| GET | /api/v1/kib/{kategori}/export | Admin, Kepala Sekolah | Export KIB to Excel |
| GET | /api/v1/kir/{ruangan_id} | All | Get KIR report |
| GET | /api/v1/kir/{ruangan_id}/export | Admin, Kepala Sekolah | Export KIR to Excel |

### 13.7 Audit Trail (2 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | /api/v1/audit | Admin | List audit logs |
| GET | /api/v1/audit/{id} | Admin | Get audit detail |

### 13.8 System (2 endpoints)

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | /api/v1/health | Public | Health check |
| POST | /api/v1/system/backup | Admin | Backup database |

**Total: 33 endpoints**

---

## 14. Implementation Checklist

### 14.1 Backend (FastAPI)

- [ ] Setup FastAPI project structure
- [ ] Configure SQLModel with SQLite (WAL mode)
- [ ] Implement session-based authentication
- [ ] Implement role-based authorization middleware
- [ ] Create database models (11 tables)
- [ ] Implement CRUD endpoints for all resources
- [ ] Implement validation logic (client + server)
- [ ] Implement business rules enforcement
- [ ] Implement audit trail logging
- [ ] Implement pagination, filtering, sorting
- [ ] Implement search functionality
- [ ] Implement KIB/KIR report generation
- [ ] Implement Excel export (ClosedXML)
- [ ] Implement error handling
- [ ] Write unit tests (pytest)
- [ ] Write integration tests
- [ ] Performance testing (< 5s search, < 10s reports)


### 14.2 Frontend (WPF .NET 8)

- [ ] Setup WPF project with MVVM pattern
- [ ] Implement HTTP client (Refit)
- [ ] Implement session management (cookie handling)
- [ ] Create ViewModels for all screens
- [ ] Implement client-side validation
- [ ] Implement error handling and display
- [ ] Implement pagination UI
- [ ] Implement search UI
- [ ] Implement filtering and sorting UI
- [ ] Implement KIB/KIR report preview
- [ ] Implement Excel export download
- [ ] Implement mutation workflow UI
- [ ] Write UI tests

### 14.3 Integration

- [ ] Test authentication flow
- [ ] Test all CRUD operations
- [ ] Test business rules enforcement
- [ ] Test error handling
- [ ] Test pagination, filtering, sorting
- [ ] Test search functionality
- [ ] Test report generation
- [ ] Test Excel export
- [ ] Test mutation workflow
- [ ] Test audit trail logging
- [ ] Performance testing (10 concurrent users)
- [ ] User acceptance testing (UAT)

---

## 15. Referensi Silang Dokumen

### 15.1 Mapping ke Dokumentasi Arsitektur

| API Contract Section | Source Document | Section |
|---------------------|-----------------|---------|
| Authentication & Authorization | STAKEHOLDERS.md | Section 3 (Roles) |
| Asset Endpoints | data_schema.md | Section 4.3 (aset table) |
| KIB-Specific Fields | data_schema.md | Sections 4.4-4.9 (KIB tables) |
| Mutation Endpoints | data_schema.md | Section 4.10 (riwayat_mutasi) |
| Business Rules | Alur Kerja_Aturan Main.md | Section 5 (Business Rules) |
| Error Handling | Alur Kerja_Aturan Main.md | Section 7 (Error Handling) |
| Performance Targets | Alur Kerja_Aturan Main.md | Section 8.4 (Performa) |
| Validation Rules | Alur Kerja_Aturan Main.md | Section 5 (Validasi) |


### 15.2 Konsistensi dengan Dokumentasi

**Validasi Konsistensi:**

✅ **Database Schema:** Semua endpoint mengikuti struktur 11 tabel di data_schema.md
✅ **Business Rules:** Semua validasi sesuai dengan Alur Kerja_Aturan Main.md
✅ **Roles & Permissions:** Authorization sesuai dengan STAKEHOLDERS.md
✅ **Tech Stack:** FastAPI + SQLModel + SQLite sesuai tech_stack.md
✅ **Performance Targets:** < 5s search, < 10s reports sesuai dokumentasi
✅ **Error Handling:** Format error sesuai Alur Kerja_Aturan Main.md
✅ **Audit Trail:** Logging sesuai data_schema.md (audit_trail table)

---

## 16. Kesimpulan

### 16.1 Ringkasan API Contract

API Contract Simanis62 V2 ini mendefinisikan **33 endpoints** yang mencakup:

1. **Authentication & Authorization** (3 endpoints) - Session-based auth dengan role-based access
2. **User Management** (5 endpoints) - CRUD users dengan soft delete
3. **Room Management** (5 endpoints) - CRUD rooms dengan referential integrity
4. **Asset Management** (7 endpoints) - CRUD assets dengan KIB extensions, search, history
5. **Mutation** (5 endpoints) - Asset movement workflow dengan status tracking
6. **Reports** (4 endpoints) - KIB A-F dan KIR reports dengan Excel export
7. **Audit Trail** (2 endpoints) - Complete audit logging untuk compliance
8. **System** (2 endpoints) - Health check dan database backup

### 16.2 Prinsip Desain yang Diterapkan

✅ **RESTful** - Resource-based URLs, proper HTTP methods
✅ **Consistent** - Uniform response format, error handling
✅ **Secure** - Session-based auth, role-based access, audit trail
✅ **Performant** - Pagination, indexing, caching (< 5s search, < 10s reports)
✅ **Documented** - Complete request/response examples, validation rules
✅ **Realistic** - Sesuai dengan tech stack (SQLite, FastAPI) dan deployment model

### 16.3 Kesiapan Implementasi

Dokumen ini **SIAP** digunakan sebagai panduan implementasi dengan:

✅ Endpoint specifications lengkap dengan request/response schemas
✅ Validation rules detail untuk setiap field
✅ Business rules enforcement yang jelas
✅ Error handling strategy yang konsisten
✅ Performance targets yang realistis
✅ Implementation checklist untuk backend dan frontend

---

*Dokumen ini merupakan bagian dari dokumentasi arsitektur Simanis62 V2.*
*Referensi: 6 dokumen arsitektur (Tujuan Bisnis, Masalah Inti, Alur Kerja, STAKEHOLDERS, Data Schema, Tech Stack)*
ted** - Complete request/response examples

### 16.3 Kepatuhan Regulasi

API ini dirancang untuk mendukung kepatuhan terhadap:
- **Permendagri No. 19/2016** - Pedoman Pengelolaan BMD
- **Permendagri No. 47/2021** - Perubahan Permendagri 19/2016
- **Permendagri No. 7/2024** - Perubahan Kedua
- **Format BPAD DKI Jakarta** - 18 kolom KIB B

---

## 17. Setup Endpoints (First-Run Configuration)

### 17.1 Overview

Setup endpoints digunakan untuk konfigurasi pertama kali saat aplikasi baru diinstal. Endpoints ini memungkinkan pembuatan akun Administrator pertama tanpa memerlukan autentikasi.

**Catatan Keamanan:**
- Endpoints ini TIDAK memerlukan autentikasi (karena belum ada user)
- Setelah admin pertama dibuat, endpoints ini akan menolak request berikutnya
- Hanya dapat digunakan sekali saat database masih kosong

### 17.2 Check Setup Status

**Endpoint:** `GET /api/v1/setup/status`

**Permission:** Public (No authentication required)

**Description:** Mengecek apakah setup pertama kali diperlukan. Mengembalikan `needs_setup: true` jika belum ada user di database.

**Success Response (200 OK) - Setup Needed:**
```json
{
  "success": true,
  "data": {
    "needs_setup": true,
    "message": "Belum ada administrator. Silakan buat akun administrator pertama."
  }
}
```

**Success Response (200 OK) - Setup Already Done:**
```json
{
  "success": true,
  "data": {
    "needs_setup": false,
    "message": "Setup sudah selesai. Silakan login."
  }
}
```

**Notes:**
- Endpoint ini selalu mengembalikan 200 OK
- Digunakan oleh frontend untuk menentukan apakah menampilkan Setup Wizard atau Login screen

---

### 17.3 Create First Admin

**Endpoint:** `POST /api/v1/setup/admin`

**Permission:** Public (No authentication required, but only works when no users exist)

**Description:** Membuat akun Administrator pertama. Hanya dapat dipanggil sekali saat database masih kosong.

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123",
  "nama_lengkap": "Administrator Sekolah"
}
```

**Validation Rules:**
- `username`: 5-50 characters, alphanumeric + underscore, required
- `password`: Minimum 8 characters, must contain letters and numbers, required
- `nama_lengkap`: 1-200 characters, required

**Success Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "nama_lengkap": "Administrator Sekolah",
    "role": "Admin",
    "status": "Aktif",
    "dapat_ekspor": true,
    "created_at": "2026-01-12T10:30:00Z"
  },
  "message": "Administrator berhasil dibuat. Silakan login dengan akun yang baru dibuat."
}
```

**Error Response (400 Bad Request) - Validation Error:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Terdapat kesalahan validasi",
    "errors": [
      {
        "field": "password",
        "message": "Password harus minimal 8 karakter dan mengandung huruf dan angka"
      }
    ]
  }
}
```

**Error Response (409 Conflict) - Setup Already Done:**
```json
{
  "success": false,
  "error": {
    "code": "SETUP_ALREADY_DONE",
    "message": "Setup sudah selesai. Tidak dapat membuat admin baru melalui endpoint ini. Gunakan endpoint /api/v1/users untuk menambah user baru."
  }
}
```

**Notes:**
- User yang dibuat otomatis memiliki role "Admin" dan `dapat_ekspor: true`
- Password di-hash dengan bcrypt sebelum disimpan
- Setelah berhasil, endpoint ini akan menolak semua request berikutnya

---

### 17.4 Setup Endpoints Summary

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| GET | /api/v1/setup/status | Public | Check if setup needed |
| POST | /api/v1/setup/admin | Public* | Create first admin |

*Only works when no users exist in database

---

### 17.5 Setup Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION STARTUP                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                ┌───────────────────────┐
                │  GET /api/v1/setup/   │
                │       status          │
                └───────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
    ┌─────────────────┐             ┌─────────────────┐
    │ needs_setup:    │             │ needs_setup:    │
    │     true        │             │     false       │
    └─────────────────┘             └─────────────────┘
              │                               │
              ▼                               ▼
    ┌─────────────────┐             ┌─────────────────┐
    │  Show Setup     │             │  Show Login     │
    │    Wizard       │             │    Screen       │
    └─────────────────┘             └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ POST /api/v1/   │
    │  setup/admin    │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Admin Created   │
    │ → Show Login    │
    └─────────────────┘
```

---

## 18. Changelog

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 6 Januari 2026 | Architecture Engineer | API contract awal berdasarkan analisis RAG 6 dokumen arsitektur |
| 2.0 | 10 Januari 2026 | Kiro AI | Sinkronisasi dengan data_schema.md v2.0: Update KIB B 13 field, fix naming convention (dapat_ekspor), fix kode_barang length (13 char) |
| **2.1** | **12 Januari 2026** | **Kiro AI** | **Tambah Setup Endpoints (Section 17) untuk First-Run Configuration: GET /api/v1/setup/status, POST /api/v1/setup/admin** |

---

*Dokumen ini adalah bagian dari dokumentasi teknis SIMANIS62 V2 dan harus dibaca bersama dengan `data_schema.md`, `tech_stack.md`, dan `STAKEHOLDERS.md`.*

*Terakhir diupdate: 12 Januari 2026*
*Versi: 2.1*
