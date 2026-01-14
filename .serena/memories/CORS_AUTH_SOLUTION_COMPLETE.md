# CORS & Authentication Solution - SIMANIS62 V2

**Tanggal**: 13 Januari 2026
**Status**: RESOLVED ✅

---

## 1. RINGKASAN MASALAH

### Gejala Awal
- Frontend Tauri (Vite) di `http://localhost:1420` tidak bisa berkomunikasi dengan backend FastAPI di `http://127.0.0.1:8000`
- Browser menampilkan error CORS
- Setelah CORS diperbaiki, muncul error 401 Unauthorized

### Root Causes yang Ditemukan
1. **CORS Misconfiguration**: `allow_origins=["*"]` tidak boleh digunakan bersama `allow_credentials=True`
2. **307 Redirect Issue**: FastAPI default `redirect_slashes=True` menyebabkan cookie hilang saat redirect
3. **Missing Auth UI**: Frontend dari v0.dev adalah mockup tanpa implementasi login flow

---

## 2. SOLUSI CORS BACKEND

### File: `backend/app/main.py`

#### Perubahan 1: CORS Origins (KRITIS!)
```python
# SEBELUM (SALAH - menyebabkan CORS error dengan credentials)
if settings.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ❌ TIDAK BOLEH dengan credentials=True
        allow_credentials=True,
        ...
    )

# SESUDAH (BENAR)
allowed_origins = [
    "http://localhost:1420",   # Vite dev server
    "http://127.0.0.1:1420",
    "http://localhost:3000",   # Alternative dev port
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite default port
    "http://127.0.0.1:5173",
    "tauri://localhost",       # Tauri production (Windows/Linux)
    "https://tauri.localhost", # Tauri production (macOS)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ✅ Explicit list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Correlation-ID", "X-Process-Time-Ms"],
)
```

**Alasan**: Browser security policy tidak mengizinkan `Access-Control-Allow-Origin: *` ketika request menggunakan `credentials: 'include'`. Error message:
> "The value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*' when the request's credentials mode is 'include'."

#### Perubahan 2: Disable Redirect Slashes
```python
# SEBELUM
app = FastAPI(
    title="SIMANIS62 V2 API",
    ...
    lifespan=lifespan,
)

# SESUDAH
app = FastAPI(
    title="SIMANIS62 V2 API",
    ...
    lifespan=lifespan,
    redirect_slashes=False,  # ✅ Mencegah 307 redirect
)
```

**Alasan**: FastAPI default melakukan 307 redirect dari `/api/v1/aset` ke `/api/v1/aset/`. Saat redirect terjadi melalui Vite proxy, cookie tidak dikirim ke URL baru karena dianggap cross-origin.

---

## 3. SOLUSI ENDPOINT TRAILING SLASH

### File: `backend/app/api/v1/aset.py`

Karena `redirect_slashes=False`, perlu menambahkan endpoint tanpa trailing slash:

```python
# Tambahkan endpoint tanpa trailing slash
@router.get(
    "",  # ✅ Tanpa trailing slash
    response_model=PaginatedResponse[AsetResponse],
    summary="List assets",
    description="Mengambil list aset dengan pagination dan filtering.",
)
@router.get(
    "/",  # Dengan trailing slash (untuk backward compatibility)
    response_model=PaginatedResponse[AsetResponse],
    include_in_schema=False,  # Hide dari docs
)
async def list_aset(...):
    ...

# Sama untuk POST
@router.post(
    "",
    response_model=SuccessResponse[AsetResponse],
    status_code=status.HTTP_201_CREATED,
    ...
)
@router.post(
    "/",
    response_model=SuccessResponse[AsetResponse],
    include_in_schema=False,
)
async def create_aset(...):
    ...
```

---

## 4. IMPLEMENTASI AUTHENTICATION FRONTEND

### 4.1 AuthContext (`frontend-tauri/src/contexts/AuthContext.tsx`)

```typescript
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '@/services/api';

interface User {
  id: string;
  username: string;
  nama_lengkap: string;
  role: string;
  dapat_ekspor: boolean;
  status: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      setIsLoading(true);
      const response = await api.get<{ success: boolean; data: User }>('/auth/me');
      if (response.success && response.data) {
        setUser(response.data);
      }
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    const response = await api.post<{ success: boolean; data: User }>(
      '/auth/login',
      { username, password }
    );
    if (response.success && response.data) {
      setUser(response.data);
    } else {
      throw new Error('Login gagal');
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, login, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

### 4.2 ProtectedRoute (`frontend-tauri/src/components/ProtectedRoute.tsx`)

```typescript
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          <p className="text-white/70">Memuat...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
```

### 4.3 LoginPage (`frontend-tauri/src/pages/LoginPage.tsx`)

```typescript
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2, Eye, EyeOff, LogIn } from 'lucide-react';

export function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as { from?: { pathname: string } })?.from?.pathname || '/';

  if (isAuthenticated) {
    navigate(from, { replace: true });
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(username, password);
      navigate(from, { replace: true });
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Username atau password salah';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    // ... UI implementation dengan glass morphism design
  );
}
```

### 4.4 App.tsx Update (`frontend-tauri/src/App.tsx`)

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { MacOSDashboardPage } from './pages/MacOSDashboardPage';
import { AssetsPage } from './pages/AssetsPage';
// ... other imports

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public route - Login */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <MacOSDesktopShell>
                  <Routes>
                    <Route path="/" element={<MacOSDashboardPage />} />
                    <Route path="/aset" element={<AssetsPage />} />
                    <Route path="/kib" element={<KIBPage />} />
                    <Route path="/mutasi" element={<MutationPage />} />
                    <Route path="/ruangan" element={<RoomsPage />} />
                    <Route path="/settings" element={<SettingsPage />} />
                  </Routes>
                </MacOSDesktopShell>
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
```

---

## 5. VITE PROXY CONFIGURATION

### File: `frontend-tauri/vite.config.ts`

```typescript
export default defineConfig(async () => ({
  // ... other config
  server: {
    port: 1420,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        // Optional: logging untuk debugging
        configure: (proxy, _options) => {
          proxy.on('error', (err) => console.log('[Vite Proxy] Error:', err.message));
          proxy.on('proxyReq', (proxyReq, req) => console.log('[Vite Proxy] Request:', req.method, req.url));
          proxy.on('proxyRes', (proxyRes, req) => console.log('[Vite Proxy] Response:', proxyRes.statusCode, req.url));
        },
      },
    },
  },
}));
```

---

## 6. API CLIENT CONFIGURATION

### File: `frontend-tauri/src/services/api.ts`

```typescript
// Detect environment
const isTauriProduction = window.__TAURI_INTERNALS__ !== undefined &&
  !window.location.hostname.includes('localhost');

// Development: gunakan relative URL (Vite proxy)
// Production: gunakan absolute URL ke sidecar
const API_BASE_URL = isTauriProduction
  ? 'http://127.0.0.1:8000/api/v1'
  : '/api/v1';  // ✅ Relative URL untuk Vite proxy

// Semua request harus include credentials
const response = await fetch(url, {
  method,
  headers: { 'Content-Type': 'application/json', ...headers },
  body: body ? JSON.stringify(body) : undefined,
  credentials: 'include',  // ✅ PENTING untuk session cookie
});
```

---

## 7. AUTHENTICATION FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. User buka app (http://localhost:1420)                      │
│     │                                                           │
│     ▼                                                           │
│  2. AuthProvider.checkAuth() → GET /api/v1/auth/me             │
│     │                                                           │
│     ├─── 401 Unauthorized ──► ProtectedRoute redirect ke /login│
│     │                                                           │
│     ▼                                                           │
│  3. User input credentials di LoginPage                        │
│     │                                                           │
│     ▼                                                           │
│  4. POST /api/v1/auth/login { username, password }             │
│     │                                                           │
│     ├─── 200 OK + Set-Cookie: simanis62_session=xxx            │
│     │                                                           │
│     ▼                                                           │
│  5. AuthContext.setUser(userData)                              │
│     │                                                           │
│     ▼                                                           │
│  6. Navigate ke intended route (atau /)                        │
│     │                                                           │
│     ▼                                                           │
│  7. Semua API request include cookie → Authenticated!          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. TESTING CREDENTIALS

```
Username: admin
Password: Admin123!
Role: ADMIN
```

---

## 9. CHECKLIST TROUBLESHOOTING

### Jika CORS Error Muncul Lagi:
- [ ] Pastikan `allow_origins` BUKAN `["*"]` jika pakai `credentials=True`
- [ ] Pastikan origin frontend ada di list `allowed_origins`
- [ ] Cek browser DevTools → Network → Response Headers untuk `Access-Control-Allow-Origin`

### Jika 401 Unauthorized:
- [ ] Pastikan cookie `simanis62_session` ada di browser (DevTools → Application → Cookies)
- [ ] Pastikan `credentials: 'include'` di semua fetch request
- [ ] Pastikan user sudah login via `/api/v1/auth/login`

### Jika 307 Redirect:
- [ ] Pastikan `redirect_slashes=False` di FastAPI
- [ ] Pastikan endpoint ada versi tanpa trailing slash

### Jika 404 Not Found:
- [ ] Pastikan endpoint path benar (dengan atau tanpa trailing slash)
- [ ] Cek apakah router sudah di-include di `api_router`

---

## 10. FILES YANG DIMODIFIKASI

| File | Perubahan |
|------|-----------|
| `backend/app/main.py` | CORS config, redirect_slashes |
| `backend/app/api/v1/aset.py` | Endpoint tanpa trailing slash |
| `frontend-tauri/src/App.tsx` | AuthProvider, ProtectedRoute |
| `frontend-tauri/src/contexts/AuthContext.tsx` | NEW - Auth state management |
| `frontend-tauri/src/components/ProtectedRoute.tsx` | NEW - Route guard |
| `frontend-tauri/src/pages/LoginPage.tsx` | NEW - Login UI |
| `frontend-tauri/vite.config.ts` | Proxy logging (optional) |

---

## 11. REFERENSI

- [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)
- [Vite Server Proxy](https://vite.dev/config/server-options.html#server-proxy)
- [React Router Protected Routes](https://reactrouter.com/en/main/start/tutorial#protecting-routes)

---

*Memory ini dibuat untuk referensi future development dan troubleshooting.*
