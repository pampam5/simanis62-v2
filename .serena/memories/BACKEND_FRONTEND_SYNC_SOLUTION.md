# Backend-Frontend Sync Solution - SIMANIS62 V2

**Tanggal**: 13 Januari 2026
**Status**: IMPLEMENTED

---

## 1. RINGKASAN SOLUSI

### Problem Statement
- Manual typing di frontend menyebabkan type mismatch dengan backend
- Perubahan API di backend tidak otomatis ter-reflect di frontend
- Debugging CORS dan type errors memakan waktu banyak

### Solution: Auto-Generated TypeScript Client dari OpenAPI

**Tool**: Hey API (@hey-api/openapi-ts)
- Official FastAPI recommendation
- Simple setup, clean TypeScript output

---

## 2. IMPLEMENTASI

### Installation
```bash
cd frontend-tauri
npm install -D @hey-api/openapi-ts
```

### Package.json Scripts
```json
{
  "scripts": {
    "api:download": "curl -o openapi.json http://127.0.0.1:8000/openapi.json",
    "api:generate": "npx @hey-api/openapi-ts -i ./openapi.json -o ./src/api/generated",
    "api:sync": "npm run api:download && npm run api:generate"
  }
}
```

### Generated Output
```
frontend-tauri/src/api/generated/
├── client/
├── core/
├── client.gen.ts
├── index.ts
├── sdk.gen.ts
└── types.gen.ts
```

---

## 3. WORKFLOW

```
1. Developer modifikasi endpoint di backend (FastAPI)
2. FastAPI auto-generate OpenAPI spec di /openapi.json
3. Run: npm run api:sync
4. TypeScript compiler detect type mismatches
5. Fix errors di frontend code
6. Build & deploy dengan confidence
```

### Commands
```bash
npm run api:download  # Download OpenAPI spec
npm run api:generate  # Generate TypeScript client
npm run api:sync      # Full sync (download + generate)
```

---

## 4. USAGE EXAMPLES

### Import Types
```typescript
import type { AsetCreate, AsetResponse, LoginRequest } from '@/api/generated';
```

### Example: Login
```typescript
import { loginApiV1AuthLoginPost } from '@/api/generated';

const response = await loginApiV1AuthLoginPost({
  body: { username: 'admin', password: 'Admin123!' }
});
```

### Example: List Assets
```typescript
import { listAsetApiV1AsetGet } from '@/api/generated';

const response = await listAsetApiV1AsetGet({
  query: { page: 1, page_size: 20, kategori_kib: 'B' }
});
```

---

## 5. BENEFITS

- Compile-time error detection
- IDE autocomplete untuk semua API calls
- Zero manual typing - types auto-generated
- Single source of truth (OpenAPI spec)
- Breaking changes caught at compile time

---

## 6. BEST PRACTICES

### Backend (FastAPI)
1. Selalu gunakan Pydantic models untuk request/response
2. Tambahkan docstrings - akan muncul di generated types
3. Gunakan tags untuk grouping endpoints

### Frontend (React/TypeScript)
1. Import types dari generated folder
2. Jangan edit generated files - akan di-overwrite
3. Run api:sync setelah backend changes

---

## 7. TROUBLESHOOTING

### Error: Cannot connect to backend
```bash
cd backend && uvicorn app.main:app --reload --port 8000
```

### Error: Type mismatch after sync
```bash
npm run api:generate && npx tsc --noEmit
```

---

## 8. FUTURE IMPROVEMENTS

- Phase 2: Orval + React Query hooks
- Phase 3: MSW mocking untuk testing
- Phase 4: Zod runtime validation

---

## 9. REFERENCES

- https://fastapi.tiangolo.com/advanced/generate-clients/
- https://heyapi.dev/
- https://orval.dev/
