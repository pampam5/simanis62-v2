# Design Specs: First-Run Setup Wizard

## Overview

First-Run Setup Wizard adalah fitur OOBE (Out-of-Box Experience) yang memungkinkan client non-technical untuk melakukan konfigurasi awal SIMANIS62 V2 tanpa perlu menjalankan script atau command line.

**Referensi:**
- `requirements.md` - REQ-23 (Data Persistence & First-run configuration)
- `tasks.md` - Phase 8 Tasks 8.1, 8.2, 8.3

---

## User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION START                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  GET /api/v1/setup/   │
                    │       status          │
                    └───────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
            needs_setup=true        needs_setup=false
                    │                       │
                    ▼                       ▼
        ┌───────────────────┐   ┌───────────────────┐
        │  SetupWizardView  │   │    LoginView      │
        └───────────────────┘   └───────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    ┌───────┐   ┌───────┐   ┌───────┐
    │Step 1 │──▶│Step 2 │──▶│Step 3 │
    │Welcome│   │Create │   │Success│
    │       │   │ Admin │   │       │
    └───────┘   └───────┘   └───────┘
                    │           │
                    ▼           ▼
            POST /api/v1/   Navigate to
            setup/admin     LoginView
```

---

## Backend API Design

### Endpoint 1: Check Setup Status

```
GET /api/v1/setup/status
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "needs_setup": true,
    "message": "Aplikasi belum dikonfigurasi. Silakan buat akun administrator."
  }
}
```

**Logic:**
- Query `SELECT COUNT(*) FROM users`
- If count == 0, return `needs_setup: true`
- If count > 0, return `needs_setup: false`

**Notes:**
- Endpoint ini TIDAK memerlukan authentication
- Dapat dipanggil kapan saja untuk check status

---

### Endpoint 2: Create First Admin

```
POST /api/v1/setup/admin
```

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123",
  "nama_lengkap": "Administrator Sekolah"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "nama_lengkap": "Administrator Sekolah",
    "role": "Admin",
    "status": "Aktif",
    "dapat_ekspor": true
  },
  "message": "Administrator berhasil dibuat. Silakan login."
}
```

**Response (400 Bad Request - Setup Already Done):**
```json
{
  "success": false,
  "error": {
    "code": "SETUP_ALREADY_DONE",
    "message": "Setup sudah selesai. Tidak dapat membuat admin baru melalui endpoint ini."
  }
}
```

**Validation:**
- `username`: 5-50 karakter, alphanumeric + underscore
- `password`: min 8 karakter
- `nama_lengkap`: 3-100 karakter

**Logic:**
1. Check if users table is empty
2. If not empty, return 400 error
3. Create user with role=Admin, status=Aktif, dapat_ekspor=true
4. Hash password dengan bcrypt
5. Return created user (tanpa password)

**Notes:**
- Endpoint ini TIDAK memerlukan authentication
- Hanya bisa dipanggil SEKALI (saat users table kosong)
- Setelah admin dibuat, endpoint akan selalu return error

---

## Frontend UI Design

### Step 1: Selamat Datang (Welcome)

```
┌─────────────────────────────────────────────────────────────────┐
│                         Step 1 of 3                              │
│  ●───────○───────○                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                         🏫                                       │
│                                                                  │
│                    SIMANIS62 V2                                  │
│           Sistem Manajemen Aset Sekolah                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Selamat datang di SIMANIS62!                                   │
│                                                                  │
│  Aplikasi ini akan membantu Anda mengelola aset sekolah         │
│  sesuai dengan format BPAD DKI Jakarta dan regulasi             │
│  Permendagri 19/2016.                                           │
│                                                                  │
│  Untuk memulai, Anda perlu membuat akun Administrator           │
│  yang akan digunakan untuk mengelola aplikasi.                  │
│                                                                  │
│                                                                  │
│                    ┌─────────────────────┐                      │
│                    │      LANJUTKAN      │                      │
│                    └─────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- MaterialDesign `PackIcon` Kind="School" (64x64)
- Title: "SIMANIS62 V2" (28pt, Bold, Primary color)
- Subtitle: "Sistem Manajemen Aset Sekolah" (14pt, Gray)
- Description text (14pt, centered)
- Primary button "LANJUTKAN"

---

### Step 2: Buat Administrator (Create Admin)

```
┌─────────────────────────────────────────────────────────────────┐
│                         Step 2 of 3                              │
│  ●───────●───────○                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    👤 Buat Administrator                         │
│                                                                  │
│  Buat akun administrator untuk mengelola aplikasi.              │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Username                                                │   │
│  │  ┌─────────────────────────────────────────────────────┐│   │
│  │  │ admin                                               ││   │
│  │  └─────────────────────────────────────────────────────┘│   │
│  │  Min 5 karakter, huruf, angka, underscore               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Password                                                │   │
│  │  ┌─────────────────────────────────────────────────────┐│   │
│  │  │ ••••••••                                     👁     ││   │
│  │  └─────────────────────────────────────────────────────┘│   │
│  │  Min 8 karakter                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Konfirmasi Password                                     │   │
│  │  ┌─────────────────────────────────────────────────────┐│   │
│  │  │ ••••••••                                     👁     ││   │
│  │  └─────────────────────────────────────────────────────┘│   │
│  │  Password harus sama                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Nama Lengkap                                            │   │
│  │  ┌─────────────────────────────────────────────────────┐│   │
│  │  │ Administrator Sekolah                               ││   │
│  │  └─────────────────────────────────────────────────────┘│   │
│  │  Nama yang akan ditampilkan di aplikasi                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│       ┌──────────────┐              ┌─────────────────────┐    │
│       │    KEMBALI   │              │   BUAT ADMINISTRATOR │    │
│       └──────────────┘              └─────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- MaterialDesign `PackIcon` Kind="AccountPlus" (48x48)
- Title: "Buat Administrator" (24pt, Bold)
- 4 input fields dengan MaterialDesign OutlinedTextBox style
- Password fields dengan toggle visibility
- Helper text di bawah setiap field
- Secondary button "KEMBALI" (outline style)
- Primary button "BUAT ADMINISTRATOR"

**Validation:**
- Username: 5-50 chars, alphanumeric + underscore, real-time validation
- Password: min 8 chars, strength indicator optional
- Confirm Password: must match password
- Nama Lengkap: 3-100 chars

---

### Step 3: Selesai (Success)

```
┌─────────────────────────────────────────────────────────────────┐
│                         Step 3 of 3                              │
│  ●───────●───────●                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                         ✅                                       │
│                                                                  │
│                    Setup Berhasil!                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Akun administrator telah berhasil dibuat.                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Username: admin                                         │   │
│  │  Nama: Administrator Sekolah                             │   │
│  │  Role: Administrator                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Anda sekarang dapat login menggunakan akun ini untuk          │
│  mulai mengelola aset sekolah.                                  │
│                                                                  │
│                                                                  │
│                    ┌─────────────────────┐                      │
│                    │    MULAI SEKARANG   │                      │
│                    └─────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Components:**
- MaterialDesign `PackIcon` Kind="CheckCircle" (64x64, Success color)
- Title: "Setup Berhasil!" (28pt, Bold, Success color)
- Summary card dengan info admin yang dibuat
- Primary button "MULAI SEKARANG"
- Optional: Lottie animation untuk success

**Behavior:**
- No back button (cannot go back from success)
- "MULAI SEKARANG" navigates to LoginView

---

## Pydantic Schemas

### SetupStatusResponse

```python
class SetupStatusResponse(BaseModel):
    needs_setup: bool = Field(..., description="True jika setup diperlukan")
    message: str = Field(..., description="Pesan untuk user")
```

### CreateAdminRequest

```python
class CreateAdminRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Username untuk admin"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 karakter)"
    )
    nama_lengkap: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nama lengkap admin"
    )
```

### CreateAdminResponse

```python
class CreateAdminResponse(BaseModel):
    id: str
    username: str
    nama_lengkap: str
    role: str
    status: str
    dapat_ekspor: bool
```

---

## Implementation Notes

### Backend

1. **Router Registration:**
   - Setup router harus didaftarkan di `main.py`
   - Prefix: `/api/v1/setup`
   - Tags: `["Setup"]`

2. **No Authentication:**
   - Setup endpoints TIDAK menggunakan `Depends(get_current_user)`
   - Ini karena belum ada user saat pertama kali

3. **Security:**
   - Endpoint `POST /setup/admin` hanya bisa dipanggil sekali
   - Setelah ada user, endpoint akan return 400 error
   - Ini mencegah pembuatan admin baru tanpa authorization

### Frontend

1. **App Startup Flow:**
   ```csharp
   // App.xaml.cs
   protected override async void OnStartup(StartupEventArgs e)
   {
       var setupService = _serviceProvider.GetRequiredService<ISetupService>();
       var needsSetup = await setupService.CheckSetupStatusAsync();
       
       if (needsSetup)
       {
           _navigationService.NavigateTo("SetupWizard");
       }
       else
       {
           _navigationService.NavigateTo("Login");
       }
   }
   ```

2. **ViewModel State:**
   ```csharp
   public partial class SetupWizardViewModel : ViewModelBase
   {
       [ObservableProperty]
       private int _currentStep = 1;
       
       [ObservableProperty]
       private string _username = string.Empty;
       
       [ObservableProperty]
       private string _password = string.Empty;
       
       [ObservableProperty]
       private string _confirmPassword = string.Empty;
       
       [ObservableProperty]
       private string _namaLengkap = string.Empty;
       
       [ObservableProperty]
       private CreateAdminResponse? _createdAdmin;
   }
   ```

3. **Validation:**
   - Real-time validation saat user mengetik
   - Button disabled sampai semua validation pass
   - Error message ditampilkan di bawah field

---

## Testing Checklist

### Backend Tests
- [ ] `GET /setup/status` returns `needs_setup: true` when users table empty
- [ ] `GET /setup/status` returns `needs_setup: false` when users exist
- [ ] `POST /setup/admin` creates admin successfully when no users
- [ ] `POST /setup/admin` returns 400 when users already exist
- [ ] `POST /setup/admin` validates username format
- [ ] `POST /setup/admin` validates password length
- [ ] `POST /setup/admin` validates nama_lengkap length
- [ ] Created admin has role=Admin, status=Aktif, dapat_ekspor=true

### Frontend Tests
- [ ] SetupWizardView shows when needs_setup=true
- [ ] LoginView shows when needs_setup=false
- [ ] Step navigation works correctly
- [ ] Back button works on Step 2
- [ ] Validation errors display correctly
- [ ] Success step shows created admin info
- [ ] "MULAI SEKARANG" navigates to LoginView

---

## References

- [Nielsen Norman Group - Wizard Pattern](https://www.nngroup.com/articles/wizards/)
- [Microsoft OOBE Design](https://docs.microsoft.com/en-us/windows-hardware/customize/desktop/customize-oobe)
- [MaterialDesignInXAML Documentation](https://materialdesigninxaml.net/)
- [Eleken UX - Stepper Design](https://www.eleken.co/blog-posts/stepper-design)

---

*Dokumen ini adalah bagian dari `.kiro/specs/simanis62-v2/`*
*Terakhir diupdate: 12 Januari 2026*
*Versi: 1.0*
