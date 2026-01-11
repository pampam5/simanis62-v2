# Panduan Pembuatan UML Diagram untuk Simanis62 V2

| Versi | Tanggal | Penulis | Keterangan |
|-------|---------|---------|------------|
| 1.0 | 8 Januari 2026 | Architecture Engineer | Dokumen panduan UML berdasarkan riset standar |

---

## 1. Ringkasan 7 UML Diagram yang Akan Dibuat

| No | Diagram | Kategori | Tujuan |
|----|---------|----------|--------|
| 1 | Use Case Diagram | Behavioral | Visualisasi interaksi aktor dengan sistem |
| 2 | Class Diagram / ERD | Structural | Struktur data dan relasi antar entitas |
| 3 | State Machine Diagram | Behavioral | Lifecycle status aset |
| 4 | Sequence Diagram - Authentication | Behavioral | Flow login/logout |
| 5 | Sequence Diagram - Mutasi Aset | Behavioral | Flow perpindahan aset |
| 6 | Sequence Diagram - Generate KIB | Behavioral | Flow pembuatan laporan |
| 7 | Component/Deployment Diagram | Structural | Arsitektur sistem |

---

## 2. Use Case Diagram

### 2.1 Elemen Wajib

| Elemen | Shape/Notasi | Keterangan |
|--------|--------------|------------|
| **Actor** | Stick figure (orang) | Representasi pengguna atau sistem eksternal |
| **Use Case** | Oval/Ellipse | Fungsionalitas yang disediakan sistem |
| **System Boundary** | Rectangle | Batas sistem (subject) |
| **Association** | Solid line | Hubungan aktor dengan use case |
| **Include** | Dashed arrow + «include» | Use case yang WAJIB dipanggil |
| **Extend** | Dashed arrow + «extend» | Use case OPSIONAL yang memperluas |
| **Generalization** | Solid line + hollow triangle | Inheritance antar aktor atau use case |

### 2.2 Notasi Arrow

```
Association:     Actor ————————— Use Case (solid line, no arrow)
Include:         Base UC - - - -> Included UC (dashed, open arrow, «include»)
Extend:          Extending UC - - - -> Base UC (dashed, open arrow, «extend»)
Generalization:  Child ——————▷ Parent (solid line, hollow triangle)
```

### 2.3 Best Practices

1. **Nama Actor**: Gunakan role, bukan nama orang (✓ "Admin Sekolah", ✗ "Pak Budi")
2. **Nama Use Case**: Gunakan kata kerja + objek (✓ "Tambah Aset", ✗ "Aset")
3. **System Boundary**: Selalu gambar rectangle untuk menunjukkan scope sistem
4. **Include vs Extend**:
   - Include: Behavior yang SELALU dipanggil (mandatory)
   - Extend: Behavior yang KADANG dipanggil (optional, conditional)
5. **Multiplicity**: Gunakan angka di ujung association jika perlu (1, 0..1, 1..*, *)

### 2.4 Konten untuk Simanis62

**Actors:**
- Admin Sekolah (Primary)
- Guru/Viewer (Primary)
- Kepala Sekolah (Primary)

**Use Cases:**
- Login, Logout
- CRUD Aset (Create, Read, Update, Delete)
- Pencarian Aset
- Generate KIB A-F
- Generate KIR
- Ekspor Excel
- Mutasi Aset
- Soft Delete Aset
- Manajemen User

---

## 3. Class Diagram / ERD

### 3.1 Elemen Wajib

| Elemen | Shape/Notasi | Keterangan |
|--------|--------------|------------|
| **Class/Entity** | Rectangle (3 compartments) | Nama, Atribut, Method |
| **Association** | Solid line | Hubungan antar class |
| **Aggregation** | Solid line + hollow diamond | "Has-a" (part dapat exist sendiri) |
| **Composition** | Solid line + filled diamond | "Owns" (part tidak bisa exist sendiri) |
| **Inheritance** | Solid line + hollow triangle | "Is-a" relationship |
| **Dependency** | Dashed arrow | "Uses" relationship |
| **Realization** | Dashed line + hollow triangle | Implements interface |

### 3.2 Notasi Arrow dan Multiplicity

```
Association:     Class A ————————— Class B
Aggregation:     Whole ◇————————— Part (hollow diamond di whole)
Composition:     Whole ◆————————— Part (filled diamond di whole)
Inheritance:     Child ——————▷ Parent (hollow triangle di parent)
Dependency:      Client - - - -> Supplier (dashed, open arrow)
Realization:     Class - - - -▷ Interface (dashed, hollow triangle)
```

**Multiplicity Notation:**
| Notasi | Arti |
|--------|------|
| `1` | Exactly one |
| `0..1` | Zero or one (optional) |
| `*` atau `0..*` | Zero or more |
| `1..*` | One or more |
| `n..m` | Range (e.g., 2..5) |

### 3.3 Crow's Foot Notation (untuk ERD)

```
One (mandatory):     ——|——
One (optional):      ——○|——
Many (mandatory):    ——<——  atau  ——|<——
Many (optional):     ——○<——

Kombinasi:
One-to-One:          ——|————|——
One-to-Many:         ——|————<——
Many-to-Many:        ——>————<——
```

### 3.4 Visibility Symbols

| Symbol | Visibility |
|--------|------------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package |

### 3.5 Best Practices

1. **Primary Key**: Tandai dengan «PK» atau underline
2. **Foreign Key**: Tandai dengan «FK»
3. **Attribute Format**: `visibility name: type [multiplicity] = default`
4. **Method Format**: `visibility name(params): returnType`
5. **Stereotype**: Gunakan «» untuk menandai tipe khusus (e.g., «entity», «table»)

### 3.6 Konten untuk Simanis62

**Entities (11 tabel):**
- users
- ruangan
- aset (main table)
- aset_kib_a, aset_kib_b, aset_kib_c, aset_kib_d, aset_kib_e, aset_kib_f
- mutasi
- audit_trail

**Relasi Penting:**
- users 1——* aset (created_by)
- ruangan 1——* aset (lokasi)
- aset 1——0..1 aset_kib_x (Single Table Inheritance)
- aset 1——* mutasi (riwayat)

---

## 4. State Machine Diagram

### 4.1 Elemen Wajib

| Elemen | Shape/Notasi | Keterangan |
|--------|--------------|------------|
| **Initial State** | Filled black circle | Titik awal |
| **Final State** | Filled circle inside circle | Titik akhir |
| **State** | Rounded rectangle | Kondisi/status objek |
| **Transition** | Solid arrow | Perpindahan antar state |
| **Guard** | [condition] | Kondisi untuk transisi |
| **Action** | / action | Aksi yang dilakukan saat transisi |
| **Composite State** | Rounded rectangle with sub-states | State yang berisi sub-states |
| **History State** | Circle with H | Kembali ke sub-state terakhir |

### 4.2 Notasi Transition

```
Format: event [guard] / action

Contoh:
- verifikasi [data_valid] / set_status_aktif
- mutasi_dimulai / create_audit_log
- kondisi_berubah [kondisi == "Rusak Berat"]
```

### 4.3 Shape Details

```
Initial State:    ●  (filled circle, diameter ~10px)
Final State:      ◉  (filled circle inside larger circle)
State:            ╭─────────╮
                  │  State  │  (rounded rectangle)
                  ╰─────────╯
Transition:       ————————→  (solid line with filled arrowhead)
```

### 4.4 Best Practices

1. **Nama State**: Gunakan kata sifat atau noun (✓ "Aktif", ✗ "Mengaktifkan")
2. **Guard Condition**: Selalu dalam square brackets [condition]
3. **Action**: Selalu setelah slash /action
4. **Entry/Exit Actions**: Gunakan `entry/` dan `exit/` di dalam state
5. **Do Activity**: Gunakan `do/` untuk aktivitas ongoing

### 4.5 Konten untuk Simanis62

**States:**
- Baru (Initial after creation)
- Aktif
- Mutasi
- Rusak
- Dihapus (Final for soft delete)

**Transitions:**
```
Baru → Aktif: verifikasi [data_lengkap] / set_verified_at
Aktif → Mutasi: mutasi_dimulai / create_mutasi_record
Mutasi → Aktif: mutasi_selesai / update_lokasi
Aktif → Rusak: kondisi_berubah [kondisi != "Baik"]
Rusak → Aktif: diperbaiki [kondisi == "Baik"]
Aktif → Dihapus: soft_delete / set_deleted_at
Rusak → Dihapus: soft_delete / set_deleted_at
```

---

## 5. Sequence Diagram

### 5.1 Elemen Wajib

| Elemen | Shape/Notasi | Keterangan |
|--------|--------------|------------|
| **Lifeline** | Rectangle + dashed vertical line | Objek/participant |
| **Activation** | Thin rectangle on lifeline | Periode eksekusi |
| **Synchronous Message** | Solid line + filled arrowhead | Call yang menunggu response |
| **Asynchronous Message** | Solid line + open arrowhead | Call tanpa menunggu |
| **Return Message** | Dashed line + open arrowhead | Response dari call |
| **Self Message** | Arrow looping back | Call ke diri sendiri |
| **Create Message** | Dashed arrow + «create» | Membuat objek baru |
| **Destroy** | X at end of lifeline | Menghancurkan objek |

### 5.2 Notasi Arrow

```
Synchronous:     ——————————▶  (solid line, filled arrowhead)
Asynchronous:    ——————————>  (solid line, open arrowhead)
Return:          - - - - - ->  (dashed line, open arrowhead)
Create:          - - - - - -▶  (dashed line, filled arrowhead, «create»)
```

### 5.3 Combined Fragments

| Fragment | Keyword | Keterangan |
|----------|---------|------------|
| **Alternative** | `alt` | If-else condition |
| **Option** | `opt` | Optional (if only) |
| **Loop** | `loop` | Iteration |
| **Break** | `break` | Exit from loop |
| **Parallel** | `par` | Concurrent execution |
| **Critical** | `critical` | Atomic region |
| **Reference** | `ref` | Reference to another diagram |

### 5.4 Best Practices

1. **Lifeline Order**: Dari kiri ke kanan sesuai urutan interaksi
2. **Message Label**: Gunakan format `methodName(params): returnType`
3. **Activation Bar**: Tunjukkan kapan objek aktif memproses
4. **Guard Condition**: Gunakan [condition] untuk conditional messages
5. **Numbering**: Opsional, gunakan 1, 1.1, 1.2, 2, dst untuk nested calls

### 5.5 Konten untuk Simanis62

**Sequence Diagram 1: Authentication Flow**
```
Participants: User, WPF Client, FastAPI Server, SQLite DB
Messages:
1. User → WPF: input credentials
2. WPF → FastAPI: POST /auth/login
3. FastAPI → SQLite: SELECT user
4. SQLite → FastAPI: user data
5. FastAPI → FastAPI: validate password
6. alt [valid]
   FastAPI → SQLite: CREATE session
   FastAPI → WPF: 200 OK + Set-Cookie
7. else [invalid]
   FastAPI → WPF: 401 Unauthorized
```

**Sequence Diagram 2: Mutasi Aset Flow**
```
Participants: Admin, WPF Client, FastAPI Server, SQLite DB
Messages:
1. Admin → WPF: select aset, select ruangan_tujuan
2. WPF → FastAPI: POST /mutasi
3. FastAPI → SQLite: BEGIN TRANSACTION
4. FastAPI → SQLite: UPDATE aset SET ruangan_id
5. FastAPI → SQLite: INSERT mutasi record
6. FastAPI → SQLite: INSERT audit_trail
7. FastAPI → SQLite: COMMIT
8. FastAPI → WPF: 201 Created
9. WPF → Admin: success notification
```

**Sequence Diagram 3: Generate KIB Flow**
```
Participants: Admin, WPF Client, FastAPI Server, SQLite DB, Excel Generator
Messages:
1. Admin → WPF: select KIB type, filters
2. WPF → FastAPI: GET /reports/kib/{type}
3. FastAPI → SQLite: SELECT aset JOIN kib_x
4. SQLite → FastAPI: aset data
5. FastAPI → Excel Generator: create workbook
6. Excel Generator → FastAPI: Excel file bytes
7. FastAPI → WPF: 200 OK + file
8. WPF → Admin: download dialog
```

---

## 6. Component Diagram

### 6.1 Elemen Wajib

| Elemen | Shape/Notasi | Keterangan |
|--------|--------------|------------|
| **Component** | Rectangle + «component» atau icon | Unit deployable |
| **Provided Interface** | Lollipop (circle on stick) | Interface yang disediakan |
| **Required Interface** | Socket (half circle) | Interface yang dibutuhkan |
| **Port** | Small square on component edge | Interaction point |
| **Dependency** | Dashed arrow | Ketergantungan |
| **Assembly Connector** | Ball-and-socket | Koneksi provided-required |

### 6.2 Notasi

```
Component:           ┌──────────────┐
                     │ «component»  │
                     │  ComponentA  │
                     └──────────────┘

Provided Interface:  ○——— Component (lollipop)
Required Interface:  ◠——— Component (socket/half circle)
Assembly:            Component1 ○——◠ Component2
```

### 6.3 Best Practices

1. **Stereotype**: Gunakan «component», «service», «library»
2. **Interface Naming**: Gunakan prefix "I" (e.g., IAuthService)
3. **Layering**: Susun komponen berdasarkan layer (UI, Business, Data)
4. **Dependencies**: Panah mengarah ke komponen yang dibutuhkan

### 6.4 Konten untuk Simanis62

**Components:**
- WPF Client (UI Layer)
  - Provided: User Interface
  - Required: IApiService
- FastAPI Server (Business Layer)
  - Provided: IApiService, IAuthService
  - Required: IDataAccess
- SQLite Database (Data Layer)
  - Provided: IDataAccess
- Excel Generator (Utility)
  - Provided: IExcelExport

---

## 7. Deployment Diagram

### 7.1 Elemen Wajib

| Elemen | Shape/Notasi | Keterangan |
|--------|--------------|------------|
| **Node** | 3D box | Hardware atau execution environment |
| **Device** | 3D box + «device» | Physical hardware |
| **Execution Environment** | 3D box + «executionEnvironment» | Software container |
| **Artifact** | Rectangle + «artifact» atau document icon | Deployable file |
| **Communication Path** | Solid line | Koneksi antar node |
| **Deployment** | Dashed arrow + «deploy» | Artifact deployed ke node |

### 7.2 Notasi

```
Node:                ┌─────────────────┐
                    ╱                 ╱│
                   ┌─────────────────┐ │
                   │   «device»      │ │
                   │   Server        │╱
                   └─────────────────┘

Artifact:           ┌─────────────────┐
                    │ «artifact»      │
                    │ app.exe         │
                    └─────────────────┘

Communication:      Node1 ═══════════ Node2 (solid line)
```

### 7.3 Best Practices

1. **Node Stereotype**: Gunakan «device», «executionEnvironment»
2. **Artifact Stereotype**: Gunakan «artifact», «executable», «library»
3. **Protocol**: Label communication path dengan protocol (HTTP, TCP)
4. **Multiplicity**: Tunjukkan jumlah instance jika perlu

### 7.4 Konten untuk Simanis62

**Nodes:**
- Client PC «device»
  - Windows 10+ «executionEnvironment»
    - Simanis62.exe «artifact»
- Server PC «device» (optional, untuk multi-user)
  - Python Runtime «executionEnvironment»
    - FastAPI Server «artifact»
    - simanis62.db «artifact»

**Communication:**
- Client PC ——HTTP/REST—— Server PC (port 8000)
- Atau: Single PC deployment (all-in-one)

---

## 8. Tools yang Direkomendasikan

| Tool | Kelebihan | Gratis? |
|------|-----------|---------|
| **Draw.io / diagrams.net** | Web-based, mudah, export PNG/SVG | Ya |
| **PlantUML** | Text-based, version control friendly | Ya |
| **Visual Paradigm** | Lengkap, professional | Free Community Edition |
| **Lucidchart** | Collaborative, cloud-based | Freemium |
| **StarUML** | Desktop app, lengkap | Freemium |

---

## 9. Checklist Sebelum Finalisasi

### Use Case Diagram
- [ ] Semua aktor terdefinisi dengan jelas
- [ ] System boundary tergambar
- [ ] Include/Extend relationship benar
- [ ] Tidak ada use case yang "mengambang" tanpa aktor

### Class Diagram / ERD
- [ ] Primary key dan foreign key ditandai
- [ ] Multiplicity di semua relasi
- [ ] Attribute types terdefinisi
- [ ] Tidak ada relasi many-to-many tanpa junction table

### State Machine Diagram
- [ ] Initial state ada
- [ ] Semua transisi memiliki trigger/event
- [ ] Guard conditions jelas
- [ ] Tidak ada dead state (state tanpa exit)

### Sequence Diagram
- [ ] Lifeline order logis (kiri ke kanan)
- [ ] Return message untuk synchronous call
- [ ] Combined fragments untuk kondisi/loop
- [ ] Activation bars konsisten

### Component/Deployment Diagram
- [ ] Semua komponen utama tergambar
- [ ] Interface provided/required jelas
- [ ] Communication path dengan protocol
- [ ] Artifact deployment ke node benar

---

*Dokumen ini disusun berdasarkan standar UML 2.x dan best practices dari berbagai sumber.*
*Referensi: Visual Paradigm, UML-Diagrams.org, Creately, ArchiMetric*
