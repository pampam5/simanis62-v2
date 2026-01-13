# Design System Rules - SIMANIS62 V2

## Overview

Design system untuk SIMANIS62 V2 menggunakan **Tauri + React + TypeScript + shadcn/ui + Tailwind CSS**.

**PENTING**: UI harus terlihat seperti **aplikasi desktop native** (Windows/Mac style), BUKAN seperti web app biasa.

---

## 0. Desktop-Style UI Principles

### Kenapa Desktop-Style?

SIMANIS62 adalah aplikasi desktop untuk sekolah. User terbiasa dengan:
- Windows Explorer, Microsoft Office, VS Code
- Bukan web app seperti Gmail atau Twitter

### Karakteristik Desktop App vs Web App

| Aspek | Desktop App ✅ | Web App ❌ |
|-------|---------------|-----------|
| Window | Custom title bar dengan min/max/close | Browser chrome |
| Navigation | Sidebar (collapsible) | Top navbar |
| Layout | Dense, banyak info per screen | Spacious, banyak whitespace |
| Tables | Dense rows, resizable columns | Card-based atau simple tables |
| Forms | Modal dialog | Full page navigation |
| Corners | Sharp edges pada window | Rounded corners everywhere |
| Font size | Smaller (12-14px) | Larger (16px+) |
| Actions | Toolbar dengan icons | Buttons scattered |

### Key Design Elements

1. **Custom Window Chrome**
   - Title bar dengan logo + app name
   - Native window controls (minimize, maximize, close)
   - Gunakan `tauri-controls` library

2. **Collapsible Sidebar**
   - Icons + labels
   - Collapse to icons only mode
   - Grouped menu sections
   - User profile di bottom

3. **Dense Data Tables**
   - Smaller row height (32-40px)
   - Column sorting indicators
   - Right-click context menu
   - Toolbar di atas table

4. **Modal Dialogs**
   - Fixed width (tidak full screen)
   - Form dalam dialog
   - Save/Cancel di bottom right

5. **Status Bar**
   - Di bottom window
   - Show: user info, connection status, version

6. **Keyboard Shortcuts**
   - Ctrl+N: New
   - Ctrl+S: Save
   - Ctrl+F: Search
   - Delete: Delete selected

---

## 0.1 Quick Start dengan tauri-ui

### Package Manager: Bun 🚀

Proyek ini menggunakan **Bun** untuk kecepatan maksimal:
- Install dependencies: ~3x lebih cepat dari npm
- Script execution: ~4x lebih cepat
- Built-in TypeScript support

### Install Bun (Windows)

```powershell
# Via PowerShell
powershell -c "irm bun.sh/install.ps1 | iex"

# Atau via npm (jika sudah ada Node.js)
npm install -g bun
```

### Recommended Template

```bash
# Create new project dengan tauri-ui template
bun create tauri-ui simanis62-frontend --template vite

# Atau dengan bunx (seperti npx)
bunx create-tauri-ui simanis62-frontend --template vite
```

### Kenapa tauri-ui?

| Feature | Benefit |
|---------|---------|
| 1.8k GitHub stars | Active community |
| Bundle size: 2.5MB | Perfect untuk flashdisk |
| Native window controls | Windows/Mac look |
| shadcn/ui included | No setup needed |
| Dark/light mode | Built-in |
| Cross-platform CI | GitHub Actions ready |

### After Setup

```bash
cd simanis62-frontend
bun install
bun run tauri dev
```

### Bun Commands Reference

| Task | Command |
|------|---------|
| Install deps | `bun install` |
| Dev server | `bun run dev` |
| Tauri dev | `bun run tauri dev` |
| Build | `bun run build` |
| Tauri build | `bun run tauri build` |
| Add package | `bun add <package>` |
| Add dev dep | `bun add -d <package>` |

---

## 0.2 v0.dev Prompts untuk SIMANIS62

Gunakan prompts ini di [v0.dev](https://v0.dev) untuk generate komponen:

### PROMPT 1: Main Layout (Desktop Shell)

```
Create a desktop application layout with:
- Custom title bar with app logo "SIMANIS62", window title, and minimize/maximize/close buttons (Windows style)
- Collapsible sidebar on the left that can collapse to icons only
- Main content area with breadcrumb navigation at top
- Status bar at the bottom showing "User: Admin | Connected | v2.0.0"
- Use shadcn/ui components
- Dark mode support
- Dense, professional look like VS Code or Windows File Explorer
- Sharp edges on outer window (no rounded corners)
- Use Inter font, 14px base size
```

### PROMPT 2: Sidebar Navigation

```
Create a desktop-style sidebar navigation for asset management app with:
- App logo "SIMANIS62" at top with collapse button
- Menu items with icons:
  - Dashboard (Home icon)
  - Daftar Aset (Package icon)
  - Laporan KIB (FileText icon)
  - Mutasi Aset (ArrowLeftRight icon)
  - Ruangan (Building icon)
  - Pengaturan (Settings icon)
- Grouped sections: "Menu Utama" and "Pengaturan"
- Active state with blue highlight
- Collapse to icons only mode (like VS Code)
- User profile section at bottom with avatar, name "Admin", and logout button
- Use shadcn/ui Sidebar component
- Dense spacing, 14px font
```

### PROMPT 3: Data Table untuk Daftar Aset

```
Create a desktop-style data table for asset management with:
- Dense rows (36px height, smaller than typical web tables)
- Toolbar above table with:
  - Search input with icon
  - Filter dropdown (Semua, Aktif, Rusak, Dihapus)
  - "Tambah Aset" button with Plus icon
  - "Export Excel" button with Download icon
- Column headers with sort indicators, columns:
  - Checkbox for selection
  - No. Register
  - Nama Barang
  - Kode Barang
  - Merk/Type
  - Tahun Perolehan
  - Harga (formatted as Rupiah)
  - Kondisi (badge: Baik=green, Rusak Ringan=yellow, Rusak Berat=red)
  - Actions (Edit, Delete icons)
- Row hover state
- Right-click context menu with: Lihat Detail, Edit, Hapus, Mutasi
- Pagination at bottom: "Showing 1-10 of 150" with page size selector
- Use shadcn/ui DataTable with TanStack Table
- Professional look like Excel or database admin tools
```

### PROMPT 4: Form Dialog untuk Tambah/Edit Aset

```
Create a desktop-style modal dialog for asset form with:
- Dialog width: 600px (not full screen)
- Title: "Tambah Aset Baru" or "Edit Aset"
- Form with 2 columns layout:
  Left column:
  - Nama Barang (text input, required)
  - Kode Barang (text input with pattern XX.XX.XX.XXXX)
  - Merk/Type (text input)
  - Ukuran (text input)
  - Bahan (text input)
  Right column:
  - Tahun Perolehan (number input, 4 digits)
  - Harga (number input, formatted as Rupiah)
  - Kondisi (select: Baik, Rusak Ringan, Rusak Berat)
  - Ruangan (select dropdown)
  - Keterangan (textarea)
- Validation error messages inline below inputs
- Footer with "Batal" (secondary) and "Simpan" (primary) buttons aligned right
- Use shadcn/ui Dialog, Form, Input, Select components
- Dense form layout with labels above inputs
- 14px font size
```

### PROMPT 5: Dashboard

```
Create a desktop-style dashboard for asset management with:
- 4 summary cards in a row:
  - Total Aset (number with Package icon)
  - Total Nilai (Rupiah formatted with DollarSign icon)
  - Kondisi Baik (number with CheckCircle icon, green)
  - Kondisi Rusak (number with AlertCircle icon, red)
- Recent Activity section below cards:
  - List of recent actions with timestamp
  - "Admin menambah aset Laptop Dell" - 5 menit lalu
  - "Admin mengubah status aset" - 1 jam lalu
- Quick Actions toolbar:
  - "Tambah Aset" button
  - "Export Laporan" button
  - "Backup Database" button
- Dense layout, minimal whitespace
- Use shadcn/ui Card components
- Professional, data-focused design
```

### PROMPT 6: Login Screen

```
Create a desktop application login screen with:
- Centered card (400px width) with subtle shadow
- App logo "SIMANIS62" at top with subtitle "Sistem Manajemen Aset Sekolah"
- Form fields:
  - Username (text input with User icon)
  - Password (password input with Lock icon)
  - "Ingat saya" checkbox
- "Masuk" button (full width, primary blue)
- Simple, clean design with no social login buttons
- Footer text: "© 2026 SIMANIS62 v2.0.0"
- Use shadcn/ui Card, Form, Input, Button, Checkbox
- Professional government/institutional look
```

### PROMPT 7: Settings Page dengan Tabs

```
Create a desktop-style settings page with:
- Tabs navigation: Umum, Pengguna, Database, Tentang
- Tab "Umum":
  - Theme selector (Light/Dark/System)
  - Language selector (Indonesia)
  - Auto-backup toggle
- Tab "Pengguna":
  - User list table with columns: Username, Role, Status, Actions
  - "Tambah Pengguna" button
- Tab "Database":
  - Database path display
  - "Backup Sekarang" button
  - "Restore dari Backup" button
  - Last backup info
- Tab "Tentang":
  - App version, build date
  - Developer info
  - License info
- Use shadcn/ui Tabs, Form, Switch, Button
- Dense layout like Windows Settings
```

---

## 0.3 shadcn/ui Blocks yang Direkomendasikan

Gunakan blocks dari [ui.shadcn.com/blocks](https://ui.shadcn.com/blocks):

| Block | Use Case | URL |
|-------|----------|-----|
| sidebar-07 | Collapsible to icons | ui.shadcn.com/blocks/sidebar |
| sidebar-11 | File tree navigation | ui.shadcn.com/blocks/sidebar |
| dashboard-01 | Summary cards | ui.shadcn.com/blocks |
| data-table | Asset list | ui.shadcn.com/docs/components/data-table |
| dialog | Forms | ui.shadcn.com/docs/components/dialog |

### Sidebar-07 Pattern (Recommended)

```tsx
// Sidebar yang collapse ke icons saja
<Sidebar collapsible="icon">
  <SidebarHeader>
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton size="lg">
          <Package className="h-6 w-6" />
          <span>SIMANIS62</span>
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  </SidebarHeader>
  <SidebarContent>
    <SidebarGroup>
      <SidebarGroupLabel>Menu Utama</SidebarGroupLabel>
      <SidebarGroupContent>
        <SidebarMenu>
          {menuItems.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton asChild>
                <a href={item.url}>
                  <item.icon />
                  <span>{item.title}</span>
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  </SidebarContent>
  <SidebarFooter>
    {/* User profile */}
  </SidebarFooter>
</Sidebar>
```

---

## 1. Token Definitions

### Colors (Tailwind CSS)

```typescript
// tailwind.config.ts
const colors = {
  // Primary - Blue (Government/Professional)
  primary: {
    50: '#eff6ff',
    100: '#dbeafe',
    500: '#3b82f6',
    600: '#2563eb',
    700: '#1d4ed8',
  },
  // Secondary - Slate (Neutral)
  secondary: {
    50: '#f8fafc',
    100: '#f1f5f9',
    500: '#64748b',
    600: '#475569',
    700: '#334155',
  },
  // Success - Green
  success: {
    500: '#22c55e',
    600: '#16a34a',
  },
  // Warning - Amber
  warning: {
    500: '#f59e0b',
    600: '#d97706',
  },
  // Danger - Red
  danger: {
    500: '#ef4444',
    600: '#dc2626',
  },
  // Status Colors (Asset Status)
  status: {
    baru: '#3b82f6',      // Blue
    aktif: '#22c55e',     // Green
    mutasi: '#f59e0b',    // Amber
    rusak: '#ef4444',     // Red
    dihapus: '#6b7280',   // Gray
  },
  // Kondisi Colors
  kondisi: {
    baik: '#22c55e',           // Green
    rusakRingan: '#f59e0b',    // Amber
    rusakBerat: '#ef4444',     // Red
  },
}
```

### Typography

```typescript
// Font Family
fontFamily: {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  mono: ['JetBrains Mono', 'monospace'],
}

// Font Sizes
fontSize: {
  xs: '0.75rem',    // 12px - Labels, captions
  sm: '0.875rem',   // 14px - Body small
  base: '1rem',     // 16px - Body
  lg: '1.125rem',   // 18px - Subheading
  xl: '1.25rem',    // 20px - Heading
  '2xl': '1.5rem',  // 24px - Page title
}
```

### Spacing

```typescript
// Base unit: 4px
spacing: {
  0: '0',
  1: '0.25rem',   // 4px
  2: '0.5rem',    // 8px
  3: '0.75rem',   // 12px
  4: '1rem',      // 16px
  5: '1.25rem',   // 20px
  6: '1.5rem',    // 24px
  8: '2rem',      // 32px
  10: '2.5rem',   // 40px
  12: '3rem',     // 48px
}
```

---

## 2. Component Library

### Location
```
frontend-tauri/src/components/
├── ui/                    # shadcn/ui components
│   ├── button.tsx
│   ├── input.tsx
│   ├── table.tsx
│   ├── dialog.tsx
│   ├── select.tsx
│   ├── badge.tsx
│   └── ...
├── layout/                # Layout components
│   ├── Sidebar.tsx
│   ├── Header.tsx
│   └── MainLayout.tsx
├── features/              # Feature-specific components
│   ├── aset/
│   │   ├── AsetTable.tsx
│   │   ├── AsetForm.tsx
│   │   └── AsetCard.tsx
│   ├── kib/
│   │   ├── KibBForm.tsx
│   │   └── KibReport.tsx
│   └── mutasi/
│       └── MutasiForm.tsx
└── shared/                # Shared components
    ├── StatusBadge.tsx
    ├── KondisiBadge.tsx
    └── SearchInput.tsx
```

### Component Architecture
- **Atomic Design**: atoms → molecules → organisms → templates → pages
- **Composition over inheritance**
- **Props interface dengan TypeScript**
- **Controlled components untuk forms**

---

## 3. Frameworks & Libraries

| Category | Library | Version |
|----------|---------|---------|
| Desktop Runtime | Tauri | v2.x |
| UI Framework | React | 19.x |
| Language | TypeScript | 5.x |
| Styling | Tailwind CSS | 4.x |
| Components | shadcn/ui | Latest |
| State Management | Zustand | Latest |
| Data Fetching | TanStack Query | v5 |
| Forms | React Hook Form + Zod | Latest |
| Icons | Lucide React | Latest |
| Tables | TanStack Table | v8 |

---

## 4. Asset Management

### Location
```
frontend-tauri/src/assets/
├── images/
│   ├── logo.svg
│   └── placeholder.png
├── fonts/
│   └── Inter-*.woff2
└── icons/
    └── (use Lucide React instead)
```

### Usage
```tsx
// Images
import logo from '@/assets/images/logo.svg';

// Icons (Lucide)
import { Package, Building, FileText } from 'lucide-react';
```

---

## 5. Icon System

### Library: Lucide React

```tsx
import {
  // Navigation
  Home, Menu, ChevronRight, ChevronDown,
  
  // Actions
  Plus, Edit, Trash2, Search, Download, Upload,
  
  // Assets
  Package, Building, FileText, Folder,
  
  // Status
  CheckCircle, AlertCircle, XCircle, Clock,
  
  // Users
  User, Users, Shield,
} from 'lucide-react';

// Usage
<Package className="h-5 w-5 text-primary-500" />
```

### Icon Sizes
- `h-4 w-4` - Small (buttons, badges)
- `h-5 w-5` - Default (navigation, actions)
- `h-6 w-6` - Large (headers, empty states)
- `h-8 w-8` - Extra large (hero sections)

---

## 6. Styling Approach

### Tailwind CSS + shadcn/ui

```tsx
// Component with Tailwind
export function StatusBadge({ status }: { status: string }) {
  const variants = {
    Baru: 'bg-blue-100 text-blue-800',
    Aktif: 'bg-green-100 text-green-800',
    Mutasi: 'bg-amber-100 text-amber-800',
    Rusak: 'bg-red-100 text-red-800',
    Dihapus: 'bg-gray-100 text-gray-800',
  };
  
  return (
    <span className={cn(
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
      variants[status]
    )}>
      {status}
    </span>
  );
}
```

### Global Styles
```css
/* src/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    /* ... shadcn/ui CSS variables */
  }
}
```

### Responsive Design
```tsx
// Mobile-first approach
<div className="
  grid 
  grid-cols-1 
  md:grid-cols-2 
  lg:grid-cols-3 
  gap-4
">
  {/* Cards */}
</div>
```

---

## 7. Project Structure

```
frontend-tauri/
├── src/
│   ├── components/        # UI Components
│   │   ├── ui/           # shadcn/ui
│   │   ├── layout/       # Layout components
│   │   ├── features/     # Feature components
│   │   └── shared/       # Shared components
│   ├── pages/            # Page components
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── AsetPage.tsx
│   │   ├── KibPage.tsx
│   │   └── MutasiPage.tsx
│   ├── hooks/            # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useAset.ts
│   │   └── useApi.ts
│   ├── services/         # API services
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── aset.ts
│   ├── stores/           # Zustand stores
│   │   ├── authStore.ts
│   │   └── uiStore.ts
│   ├── types/            # TypeScript types
│   │   ├── api.ts
│   │   ├── aset.ts
│   │   └── user.ts
│   ├── lib/              # Utilities
│   │   ├── utils.ts
│   │   └── cn.ts
│   ├── styles/           # Global styles
│   │   └── globals.css
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/            # Tauri backend (Rust)
│   ├── src/
│   │   └── main.rs
│   ├── Cargo.toml
│   └── tauri.conf.json
├── public/
├── index.html
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── vite.config.ts
```

---

## 8. Figma to Code Mapping

### Component Mapping

| Figma Component | Code Component | Location |
|-----------------|----------------|----------|
| Button/Primary | `<Button>` | `components/ui/button.tsx` |
| Button/Secondary | `<Button variant="secondary">` | `components/ui/button.tsx` |
| Input/Text | `<Input>` | `components/ui/input.tsx` |
| Select/Dropdown | `<Select>` | `components/ui/select.tsx` |
| Table | `<DataTable>` | `components/ui/data-table.tsx` |
| Card | `<Card>` | `components/ui/card.tsx` |
| Dialog/Modal | `<Dialog>` | `components/ui/dialog.tsx` |
| Badge/Status | `<StatusBadge>` | `components/shared/StatusBadge.tsx` |
| Sidebar | `<Sidebar>` | `components/layout/Sidebar.tsx` |

### Auto-props from Figma

```tsx
// Figma node with variant="primary" size="lg"
// Maps to:
<Button variant="primary" size="lg">
  {children}
</Button>
```

---

## 9. SIMANIS62 Specific Components

### StatusBadge
```tsx
// Status aset: Baru, Aktif, Mutasi, Rusak, Dihapus
<StatusBadge status="Aktif" />
```

### KondisiBadge
```tsx
// Kondisi: Baik, Rusak Ringan, Rusak Berat
<KondisiBadge kondisi="Baik" />
```

### KibCategoryBadge
```tsx
// KIB: A, B, C, D, E, F
<KibCategoryBadge category="B" />
```

### AsetTable
```tsx
// Table dengan sorting, filtering, pagination
<AsetTable 
  data={asetList}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

### KibBForm
```tsx
// Form untuk KIB B (18 kolom BPAD DKI Jakarta)
<KibBForm 
  onSubmit={handleSubmit}
  defaultValues={existingAset}
/>
```

---

## 10. API Integration Pattern

### TanStack Query + Fetch

```tsx
// services/aset.ts
export const asetApi = {
  getAll: async (params: AsetSearchParams) => {
    const response = await fetch(`${API_URL}/aset?${new URLSearchParams(params)}`);
    return response.json();
  },
  
  create: async (data: AsetCreate) => {
    const response = await fetch(`${API_URL}/aset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      credentials: 'include', // For session cookie
    });
    return response.json();
  },
};

// hooks/useAset.ts
export function useAsetList(params: AsetSearchParams) {
  return useQuery({
    queryKey: ['aset', params],
    queryFn: () => asetApi.getAll(params),
  });
}
```

---

## References

- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [shadcn/ui Blocks](https://ui.shadcn.com/blocks/sidebar)
- [Tailwind CSS](https://tailwindcss.com/)
- [Tauri v2 Documentation](https://v2.tauri.app/)
- [tauri-ui Template](https://github.com/agmmnn/tauri-ui)
- [tauri-controls](https://github.com/agmmnn/tauri-controls)
- [TanStack Query](https://tanstack.com/query)
- [TanStack Table](https://tanstack.com/table)
- [Lucide Icons](https://lucide.dev/)
- [v0.dev](https://v0.dev) - AI UI Generator

---

## 11. Development Workflow dengan v0.dev

### Step-by-Step

1. **Install Bun** (jika belum)
   ```powershell
   powershell -c "irm bun.sh/install.ps1 | iex"
   ```

2. **Setup Project**
   ```bash
   bun create tauri-ui simanis62-frontend --template vite
   cd simanis62-frontend
   bun install
   ```

3. **Generate Components di v0.dev**
   - Buka [v0.dev](https://v0.dev)
   - Paste prompt dari section 0.2
   - Iterate sampai sesuai
   - Copy code ke project

4. **Customize untuk Desktop Look**
   - Kurangi padding/margin
   - Gunakan font size lebih kecil (14px)
   - Tambahkan keyboard shortcuts
   - Tambahkan right-click menus

5. **Integrate dengan Backend**
   - Setup TanStack Query
   - Connect ke FastAPI (port 8000)
   - Handle authentication

6. **Test dengan Tauri**
   ```bash
   bun run tauri dev
   ```

7. **Build untuk Production**
   ```bash
   bun run tauri build
   ```

### Estimated Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Setup | 1 day | Create project, install deps |
| UI Generation | 2 days | Generate components with v0.dev |
| Customization | 2 days | Desktop styling, keyboard shortcuts |
| Integration | 2 days | Connect to FastAPI backend |
| Testing | 1 day | Test all features |
| **Total** | **~1 week** | |

---

## 12. Comparison: WPF vs Tauri + shadcn/ui

| Aspect | WPF | Tauri + shadcn/ui |
|--------|-----|-------------------|
| Look | Native Windows | Can look native with tauri-controls |
| Bundle size | 120-150MB | 2-10MB ✅ |
| Development speed | Slower (XAML) | Faster (React + AI tools) ✅ |
| MCP debugging | Custom MCP needed | Browser DevTools + Tauri MCP ✅ |
| Cross-platform | Windows only | Windows, Mac, Linux ✅ |
| Learning curve | C#/XAML | React/TypeScript (more common) ✅ |
| AI assistance | Limited | v0.dev, Copilot, etc. ✅ |
| Community | Declining | Growing ✅ |

**Conclusion**: Tauri + shadcn/ui adalah pilihan terbaik untuk SIMANIS62 V2 karena:
- Bundle size kecil (penting untuk distribusi flashdisk)
- Development lebih cepat dengan AI tools
- Debugging lebih mudah dengan browser DevTools
- Cross-platform support

#[[file:docs/api_contract.md]]
#[[file:docs/data_schema.md]]


---

## 13. macOS Liquid Glass Style 2025

### 13.1 Overview & Philosophy

**Liquid Glass** adalah design language terbaru Apple yang diperkenalkan di iOS 26, iPadOS 26, macOS Tahoe 26 (2025-2026). Style ini sangat cocok untuk SIMANIS62 karena memberikan kesan:
- **Professional** - Tampilan bersih dan modern
- **Premium** - Efek glass memberikan kesan high-quality
- **Familiar** - User sudah terbiasa dengan macOS/iOS style

#### Prinsip Utama Apple Design

| Prinsip | Deskripsi | Implementasi di SIMANIS62 |
|---------|-----------|---------------------------|
| **Hierarchy** | Visual hierarchy yang jelas | Sidebar → Content → Actions |
| **Harmony** | Konsistensi visual language | Warna, spacing, typography seragam |
| **Consistency** | Interaksi yang predictable | Button, form, navigation konsisten |
| **Concentricity** | Shapes align dengan hardware | Rounded corners yang proporsional |

#### Karakteristik Liquid Glass

```
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────┐   │
│  │  TRANSLUCENT LAYER                                   │   │
│  │  - Background blur (20-40px)                         │   │
│  │  - Saturation boost (180%)                           │   │
│  │  - Subtle border (1px white/10%)                     │   │
│  │  - Inner highlight (top edge)                        │   │
│  │  - Soft shadow (8-32px)                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  BACKGROUND CONTENT (visible through glass)                 │
└─────────────────────────────────────────────────────────────┘
```

---

### 13.2 Color Palette - macOS Style (Updated January 2026)

> **Research Sources:**
> - Apple Human Interface Guidelines (iOS/macOS 2025)
> - Apple System Colors CSS (GitHub: lithammer/apple.css)
> - UI/UX Color Trends 2025-2026 (webosmotic.com, scrumlaunch.com)
> - Liquid Glass Design Language (WWDC 2025)

#### Key Insights dari Research

1. **81.9% smartphone users prefer dark mode** - Dark mode bukan optional lagi
2. **Contrast ratio minimum**: 4.5:1 untuk normal text, 3:1 untuk large text (WCAG)
3. **Apple menggunakan RGB values** bukan hex untuk precision
4. **Dark mode colors berbeda** - Bukan sekadar invert, tapi adjusted untuk legibility

#### Apple System Colors (Official - Light Mode)

| Color | RGB Value | Hex | Use Case |
|-------|-----------|-----|----------|
| Blue | rgb(0, 122, 255) | #007AFF | Primary actions, links |
| Green | rgb(52, 199, 89) | #34C759 | Success, positive |
| Indigo | rgb(88, 86, 214) | #5856D6 | Alternative primary |
| Orange | rgb(255, 149, 0) | #FF9500 | Warnings |
| Pink | rgb(255, 45, 85) | #FF2D55 | Alerts, notifications |
| Purple | rgb(175, 82, 222) | #AF52DE | Secondary accent |
| Red | rgb(255, 59, 48) | #FF3B30 | Danger, errors |
| Teal | rgb(90, 200, 250) | #5AC8FA | Info, highlights |
| Yellow | rgb(255, 204, 0) | #FFCC00 | Caution |

#### Apple System Colors (Official - Dark Mode)

| Color | RGB Value | Hex | Notes |
|-------|-----------|-----|-------|
| Blue | rgb(10, 132, 255) | #0A84FF | Brighter for dark bg |
| Green | rgb(48, 209, 88) | #30D158 | Slightly adjusted |
| Indigo | rgb(94, 92, 230) | #5E5CE6 | Brighter |
| Orange | rgb(255, 159, 10) | #FF9F0A | Warmer |
| Pink | rgb(255, 55, 95) | #FF375F | Adjusted |
| Purple | rgb(191, 90, 242) | #BF5AF2 | Brighter |
| Red | rgb(255, 69, 58) | #FF453A | Slightly adjusted |
| Teal | rgb(100, 210, 255) | #64D2FF | Brighter |
| Yellow | rgb(255, 214, 10) | #FFD60A | Warmer |

#### Apple System Gray Scale

**Light Mode:**
| Gray | RGB Value | Hex | Use Case |
|------|-----------|-----|----------|
| Gray 1 | rgb(142, 142, 147) | #8E8E93 | Secondary text |
| Gray 2 | rgb(174, 174, 178) | #AEAEB2 | Tertiary text |
| Gray 3 | rgb(199, 199, 204) | #C7C7CC | Borders |
| Gray 4 | rgb(209, 209, 214) | #D1D1D6 | Dividers |
| Gray 5 | rgb(229, 229, 234) | #E5E5EA | Backgrounds |
| Gray 6 | rgb(242, 242, 247) | #F2F2F7 | Page background |

**Dark Mode:**
| Gray | RGB Value | Hex | Use Case |
|------|-----------|-----|----------|
| Gray 1 | rgb(142, 142, 147) | #8E8E93 | Same as light |
| Gray 2 | rgb(99, 99, 102) | #636366 | Darker |
| Gray 3 | rgb(72, 72, 74) | #48484A | Borders |
| Gray 4 | rgb(58, 58, 60) | #3A3A3C | Dividers |
| Gray 5 | rgb(44, 44, 46) | #2C2C2E | Elevated bg |
| Gray 6 | rgb(28, 28, 30) | #1C1C1E | Page background |

#### SIMANIS62 Semantic Color Mapping

```typescript
// Semantic colors untuk SIMANIS62
const semanticColors = {
  // Status Aset
  status: {
    baru: 'var(--accent-blue)',      // Aset baru ditambahkan
    aktif: 'var(--accent-green)',    // Aset aktif/baik
    mutasi: 'var(--accent-orange)',  // Sedang proses mutasi
    rusak: 'var(--accent-red)',      // Rusak/bermasalah
    dihapus: 'var(--gray-1)',        // Sudah dihapus
  },
  
  // Kondisi Aset
  kondisi: {
    baik: 'var(--accent-green)',
    rusakRingan: 'var(--accent-orange)',
    rusakBerat: 'var(--accent-red)',
  },
  
  // UI States
  interactive: {
    hover: 'rgba(0, 0, 0, 0.04)',      // Light mode
    hoverDark: 'rgba(255, 255, 255, 0.06)', // Dark mode
    active: 'rgba(0, 0, 0, 0.08)',
    selected: 'rgba(0, 122, 255, 0.12)',
    focusRing: 'rgba(0, 122, 255, 0.4)',
  },
};
```

#### Tailwind Config - Complete Colors

```typescript
// tailwind.config.ts - Extended colors
const colors = {
  // Apple System Colors (Light Mode defaults, dark mode via CSS vars)
  accent: {
    blue: 'rgb(var(--accent-blue) / <alpha-value>)',
    green: 'rgb(var(--accent-green) / <alpha-value>)',
    indigo: 'rgb(var(--accent-indigo) / <alpha-value>)',
    orange: 'rgb(var(--accent-orange) / <alpha-value>)',
    pink: 'rgb(var(--accent-pink) / <alpha-value>)',
    purple: 'rgb(var(--accent-purple) / <alpha-value>)',
    red: 'rgb(var(--accent-red) / <alpha-value>)',
    teal: 'rgb(var(--accent-teal) / <alpha-value>)',
    yellow: 'rgb(var(--accent-yellow) / <alpha-value>)',
  },
  
  // Glass Background Colors
  glass: {
    white: 'rgba(255, 255, 255, 0.72)',
    light: 'rgba(246, 246, 246, 0.8)',
    dark: 'rgba(30, 30, 30, 0.72)',
    darker: 'rgba(20, 20, 20, 0.85)',
  },
  
  // macOS-style Grays (using CSS vars for dark mode support)
  macos: {
    gray1: 'var(--gray-1)',
    gray2: 'var(--gray-2)',
    gray3: 'var(--gray-3)',
    gray4: 'var(--gray-4)',
    gray5: 'var(--gray-5)',
    gray6: 'var(--gray-6)',
    separator: 'var(--separator)',
  },
  
  // Semantic Colors
  success: 'var(--color-success)',
  warning: 'var(--color-warning)',
  error: 'var(--color-error)',
  info: 'var(--color-info)',
}
```

#### CSS Custom Properties (Complete)

Lihat `frontend-tauri/src/styles/glass.css` untuk implementasi lengkap dengan:
- Light mode colors
- Dark mode colors (auto-switch)
- Semantic colors (success, warning, error, info)
- SIMANIS62 specific colors (status aset, kondisi)
- Interactive states (hover, active, selected)
- Colored shadows untuk accent buttons

---

### 13.3 Glassmorphism Effects

#### Base Glass Classes

```css
/* src/styles/glass.css */

/* Standard Glass Panel */
.glass-panel {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 12px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
}

/* Sidebar Glass */
.glass-sidebar {
  background: rgba(246, 246, 246, 0.8);
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
}

/* Card Glass */
.glass-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 
    0 4px 24px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

/* Modal Glass */
.glass-modal {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(40px) saturate(200%);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 14px;
  box-shadow: 
    0 24px 80px rgba(0, 0, 0, 0.15),
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

/* Button Glass */
.glass-button {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  transition: all 0.2s ease;
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

/* Dark Mode Variants */
.dark .glass-panel {
  background: rgba(30, 30, 30, 0.72);
  border-color: rgba(255, 255, 255, 0.08);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.dark .glass-sidebar {
  background: rgba(28, 28, 30, 0.8);
  border-right-color: rgba(255, 255, 255, 0.08);
}

.dark .glass-card {
  background: rgba(44, 44, 46, 0.6);
  border-color: rgba(255, 255, 255, 0.06);
}
```

#### Tailwind Config Extensions

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      // Backdrop Blur
      backdropBlur: {
        xs: '2px',
        '2xl': '40px',
        '3xl': '64px',
      },
      
      // Background Opacity
      backgroundOpacity: {
        '72': '0.72',
        '85': '0.85',
      },
      
      // Border Radius (macOS-style)
      borderRadius: {
        'macos-sm': '6px',
        'macos': '10px',
        'macos-lg': '14px',
        'macos-xl': '20px',
      },
      
      // Box Shadow (Liquid Glass)
      boxShadow: {
        'glass': '0 8px 32px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.5)',
        'glass-lg': '0 24px 80px rgba(0, 0, 0, 0.15), 0 8px 32px rgba(0, 0, 0, 0.1)',
        'glass-dark': '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
        'button-hover': '0 4px 16px rgba(0, 0, 0, 0.1)',
        'card-hover': '0 8px 40px rgba(0, 0, 0, 0.12)',
      },
      
      // Animation
      animation: {
        'fade-in': 'fadeIn 0.2s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'blur-in': 'blurIn 0.3s ease-out',
      },
      
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        blurIn: {
          '0%': { opacity: '0', filter: 'blur(10px)' },
          '100%': { opacity: '1', filter: 'blur(0)' },
        },
      },
    },
  },
}
```

---

### 13.4 Component Updates - macOS Style

#### Sidebar dengan Liquid Glass

```tsx
// components/layout/Sidebar.tsx
import { cn } from '@/lib/utils';

export function Sidebar({ children, collapsed }: SidebarProps) {
  return (
    <aside
      className={cn(
        // Glass effect
        "bg-white/80 dark:bg-zinc-900/80",
        "backdrop-blur-2xl backdrop-saturate-[180%]",
        "border-r border-black/10 dark:border-white/8",
        
        // Layout
        "h-screen flex flex-col",
        "transition-all duration-300 ease-out",
        
        // Width
        collapsed ? "w-16" : "w-64",
      )}
    >
      {/* Logo Section */}
      <div className="h-14 flex items-center px-4 border-b border-black/5 dark:border-white/5">
        <Package className="h-6 w-6 text-accent-blue" />
        {!collapsed && (
          <span className="ml-3 font-semibold text-sm">SIMANIS62</span>
        )}
      </div>
      
      {/* Navigation */}
      <nav className="flex-1 py-2 overflow-y-auto">
        {children}
      </nav>
      
      {/* User Profile */}
      <div className="p-3 border-t border-black/5 dark:border-white/5">
        <UserProfile collapsed={collapsed} />
      </div>
    </aside>
  );
}
```

#### Card dengan Glassmorphism

```tsx
// components/ui/glass-card.tsx
import { cn } from '@/lib/utils';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

export function GlassCard({ children, className, hover = true }: GlassCardProps) {
  return (
    <div
      className={cn(
        // Glass effect
        "bg-white/60 dark:bg-zinc-800/60",
        "backdrop-blur-xl backdrop-saturate-[180%]",
        "border border-white/20 dark:border-white/6",
        "rounded-2xl",
        
        // Shadow
        "shadow-glass dark:shadow-glass-dark",
        
        // Hover effect
        hover && [
          "transition-all duration-200 ease-out",
          "hover:bg-white/70 dark:hover:bg-zinc-800/70",
          "hover:shadow-card-hover",
          "hover:-translate-y-0.5",
        ],
        
        className
      )}
    >
      {/* Inner highlight */}
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/60 to-transparent" />
      
      {children}
    </div>
  );
}
```

#### Button dengan Subtle Gradient

```tsx
// components/ui/glass-button.tsx
import { cn } from '@/lib/utils';
import { ButtonHTMLAttributes, forwardRef } from 'react';

interface GlassButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

export const GlassButton = forwardRef<HTMLButtonElement, GlassButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          // Base
          "inline-flex items-center justify-center font-medium",
          "transition-all duration-200 ease-out",
          "focus:outline-none focus:ring-2 focus:ring-accent-blue/50",
          
          // Size
          size === 'sm' && "h-8 px-3 text-xs rounded-lg",
          size === 'md' && "h-10 px-4 text-sm rounded-[10px]",
          size === 'lg' && "h-12 px-6 text-base rounded-xl",
          
          // Variants
          variant === 'primary' && [
            "bg-accent-blue text-white",
            "hover:bg-accent-blue/90",
            "active:bg-accent-blue/80",
            "shadow-sm hover:shadow-md",
          ],
          
          variant === 'secondary' && [
            "bg-white/50 dark:bg-white/10",
            "backdrop-blur-lg",
            "border border-black/10 dark:border-white/10",
            "text-gray-900 dark:text-white",
            "hover:bg-white/70 dark:hover:bg-white/15",
            "active:bg-white/80 dark:active:bg-white/20",
          ],
          
          variant === 'ghost' && [
            "bg-transparent",
            "text-gray-600 dark:text-gray-300",
            "hover:bg-black/5 dark:hover:bg-white/10",
            "active:bg-black/10 dark:active:bg-white/15",
          ],
          
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);
```

#### Modal dengan Backdrop Blur

```tsx
// components/ui/glass-modal.tsx
import { cn } from '@/lib/utils';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';

interface GlassModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export function GlassModal({ open, onOpenChange, title, children, size = 'md' }: GlassModalProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      {/* Backdrop with blur */}
      <div className="fixed inset-0 bg-black/20 backdrop-blur-sm" />
      
      <DialogContent
        className={cn(
          // Glass effect
          "bg-white/85 dark:bg-zinc-900/85",
          "backdrop-blur-2xl backdrop-saturate-[200%]",
          "border border-white/30 dark:border-white/10",
          "rounded-[14px]",
          
          // Shadow
          "shadow-glass-lg",
          
          // Animation
          "animate-scale-in",
          
          // Size
          size === 'sm' && "max-w-sm",
          size === 'md' && "max-w-lg",
          size === 'lg' && "max-w-2xl",
          size === 'xl' && "max-w-4xl",
        )}
      >
        {/* Inner highlight */}
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/80 to-transparent rounded-t-[14px]" />
        
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold">{title}</DialogTitle>
        </DialogHeader>
        
        {children}
      </DialogContent>
    </Dialog>
  );
}
```

---

### 13.5 v0.dev Prompts - macOS Liquid Glass Style

#### PROMPT 1: Main Layout (macOS Style)

```
Create a macOS-style desktop application layout with Liquid Glass aesthetics:

- Custom title bar with traffic light buttons (red/yellow/green) on the left
- App title "SIMANIS62" centered in title bar
- Translucent sidebar (240px) with frosted glass effect:
  - Background: rgba(246, 246, 246, 0.8) with backdrop-blur-2xl
  - Border-right: 1px solid rgba(0, 0, 0, 0.1)
- Main content area with subtle gray background (#F5F5F7)
- Status bar at bottom with glass effect

Design requirements:
- Use Apple's SF Pro font or Inter as fallback
- Vibrant blue accent color (#007AFF)
- Rounded corners: 10px for panels, 8px for buttons
- Subtle shadows with colored tints
- Support dark mode with deep blacks (#1C1C1E)
- Use shadcn/ui components with custom styling
- Dense, professional look suitable for asset management
```

#### PROMPT 2: Sidebar Navigation (macOS Style)

```
Create a macOS-style sidebar navigation with Liquid Glass effect:

- Frosted glass background with 80% opacity
- Backdrop blur: 40px with saturation boost
- App logo "SIMANIS62" at top with blue accent icon
- Collapse button (chevron) that shrinks sidebar to 64px

Menu items with SF Symbols style icons:
- Dashboard (square.grid.2x2)
- Daftar Aset (cube.box)
- Laporan KIB (doc.text)
- Mutasi Aset (arrow.left.arrow.right)
- Ruangan (building.2)
- Pengaturan (gear)

Active state:
- Background: rgba(0, 122, 255, 0.12)
- Text color: #007AFF
- Left border: 3px solid #007AFF

Hover state:
- Background: rgba(0, 0, 0, 0.04)
- Smooth transition: 150ms ease

User profile at bottom:
- Avatar with initials
- Name and role
- Logout button (ghost style)

Use Lucide React icons, shadcn/ui Sidebar component
```

#### PROMPT 3: Data Table (macOS Style)

```
Create a macOS-style data table for asset management with glass effects:

Toolbar (glass panel):
- Search input with magnifying glass icon
- Filter dropdown with chevron
- "Tambah Aset" button (blue, filled)
- "Export" button (secondary, glass style)
- Background: white/60 with backdrop-blur

Table styling:
- Header: sticky, glass background, uppercase labels, 12px font
- Rows: 40px height, alternating subtle backgrounds
- Hover: light blue tint (rgba(0, 122, 255, 0.04))
- Selected: blue tint (rgba(0, 122, 255, 0.08))
- Borders: 1px solid rgba(0, 0, 0, 0.06)

Columns:
- Checkbox (rounded)
- No. Register
- Nama Barang
- Kode Barang
- Merk/Type
- Tahun
- Harga (Rp format)
- Kondisi (pill badge: green/yellow/red)
- Actions (icon buttons)

Pagination:
- Glass panel at bottom
- "1-10 dari 150" text
- Page size selector
- Navigation arrows

Use TanStack Table with shadcn/ui styling
```

#### PROMPT 4: Dashboard Cards (macOS Style)

```
Create macOS-style dashboard with glass cards:

4 summary cards in a row:
- Total Aset (cube icon, blue)
- Total Nilai (banknote icon, green)
- Kondisi Baik (checkmark.circle icon, green)
- Kondisi Rusak (exclamationmark.triangle icon, red)

Card styling:
- Glass background: white/60 with backdrop-blur-xl
- Border: 1px solid white/20
- Border-radius: 16px
- Inner highlight: gradient line at top
- Shadow: 0 4px 24px rgba(0,0,0,0.06)
- Hover: lift effect (-2px translateY)

Card content:
- Icon in colored circle (40px)
- Label: 12px, gray, uppercase
- Value: 28px, bold, dark
- Trend indicator: +5% with arrow

Recent Activity section:
- Glass card below summary
- List of activities with avatars
- Timestamp in relative format
- "Lihat Semua" link

Use shadcn/ui Card with custom glass styling
```

#### PROMPT 5: Form Dialog (macOS Style)

```
Create a macOS-style form dialog with Liquid Glass effect:

Dialog styling:
- Width: 560px
- Glass background: white/85 with backdrop-blur-2xl
- Border-radius: 14px
- Shadow: layered (24px + 8px)
- Inner highlight at top edge

Header:
- Title: "Tambah Aset Baru" (18px, semibold)
- Close button (X) with hover effect
- Subtle separator line

Form layout (2 columns):
Left:
- Nama Barang (required)
- Kode Barang (pattern input)
- Merk/Type
- Ukuran
- Bahan

Right:
- Tahun Perolehan
- Harga (Rupiah format)
- Kondisi (select)
- Ruangan (select)
- Keterangan (textarea)

Input styling:
- Height: 36px
- Border-radius: 8px
- Border: 1px solid rgba(0,0,0,0.1)
- Focus: blue ring (2px)
- Background: white/50

Footer:
- "Batal" button (secondary, glass)
- "Simpan" button (primary, blue)
- Aligned right with 12px gap

Use React Hook Form + Zod, shadcn/ui Form components
```

---

### 13.6 Animation & Microinteractions

#### Transition Timing

```css
/* Standard transitions */
:root {
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease;
  --transition-slow: 300ms ease;
  --transition-spring: 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

#### Hover Effects

```tsx
// Subtle lift on hover
const hoverLift = "transition-transform duration-200 hover:-translate-y-0.5";

// Scale on press
const pressScale = "active:scale-[0.98] transition-transform duration-100";

// Glow effect
const hoverGlow = "hover:shadow-[0_0_20px_rgba(0,122,255,0.3)]";
```

#### Page Transitions

```tsx
// components/layout/PageTransition.tsx
import { motion, AnimatePresence } from 'framer-motion';

export function PageTransition({ children }: { children: React.ReactNode }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

#### Loading States

```tsx
// Skeleton with shimmer
const skeletonShimmer = `
  relative overflow-hidden
  before:absolute before:inset-0
  before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent
  before:animate-[shimmer_1.5s_infinite]
`;

// Pulse animation
const pulse = "animate-pulse bg-gray-200 dark:bg-gray-700 rounded";
```

---

### 13.7 Implementation Checklist

#### Setup Steps

1. **Update Tailwind Config**
   ```bash
   # Add glass utilities to tailwind.config.ts
   # See section 13.3 for full config
   ```

2. **Add Glass CSS**
   ```bash
   # Create src/styles/glass.css
   # Import in main.tsx
   ```

3. **Install Dependencies**
   ```bash
   bun add framer-motion
   bun add @radix-ui/react-dialog
   ```

4. **Update shadcn/ui Components**
   - Modify button.tsx with glass variants
   - Modify card.tsx with glass effect
   - Modify dialog.tsx with backdrop blur

#### Component Migration

| Component | Status | Notes |
|-----------|--------|-------|
| Sidebar | 🔄 Update | Add glass effect |
| Card | 🔄 Update | Add glassmorphism |
| Button | 🔄 Update | Add glass variant |
| Dialog | 🔄 Update | Add backdrop blur |
| Table | 🔄 Update | Add glass toolbar |
| Input | 🔄 Update | Subtle glass background |

#### Testing Checklist

- [ ] Glass effects render correctly
- [ ] Dark mode transitions smoothly
- [ ] Animations are smooth (60fps)
- [ ] Backdrop blur works in Tauri
- [ ] No performance issues with blur
- [ ] Accessible contrast ratios maintained

---

### 13.8 Performance Considerations

#### Backdrop Blur Optimization

```css
/* Use will-change for animated glass elements */
.glass-animated {
  will-change: transform, opacity;
}

/* Reduce blur on low-end devices */
@media (prefers-reduced-motion: reduce) {
  .glass-panel {
    backdrop-filter: none;
    background: rgba(255, 255, 255, 0.95);
  }
}
```

#### Tauri-Specific Notes

```rust
// src-tauri/src/main.rs
// Enable transparent window for glass effects
fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let window = app.get_window("main").unwrap();
            // Enable transparency
            window.set_decorations(false)?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

### 13.9 References

- [Apple Human Interface Guidelines - Liquid Glass](https://developer.apple.com/design/human-interface-guidelines/)
- [Apple Design Resources](https://developer.apple.com/design/resources/)
- [Glassmorphism CSS Generator](https://glassmorphism.com/)
- [Tailwind CSS Backdrop Filter](https://tailwindcss.com/docs/backdrop-blur)
- [Framer Motion](https://www.framer.com/motion/)
- [SF Symbols](https://developer.apple.com/sf-symbols/)

---

*Section ini ditambahkan: 12 Januari 2026*
*Berdasarkan research UI/UX Trends 2025 dan Apple Liquid Glass Design Language*


---

## 14. Typography System - macOS Liquid Glass Style 2025

### 14.1 Font Stack

#### Primary Font: Inter (Web) / SF Pro (Native)

```css
/* Font Stack untuk SIMANIS62 */
:root {
  /* Primary - Inter (closest to SF Pro, open-source) */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 
               'SF Pro Text', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  
  /* Monospace - untuk kode dan data */
  --font-mono: 'SF Mono', 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 
               Consolas, 'Liberation Mono', Menlo, monospace;
  
  /* Display - untuk headlines besar */
  --font-display: 'Inter Display', 'SF Pro Display', var(--font-sans);
}
```

#### Font Variants

| Font | Use Case | Size Range |
|------|----------|------------|
| **Inter** | Body text, UI elements | 11-19px |
| **Inter Display** | Headlines, titles | 20px+ |
| **SF Mono / JetBrains Mono** | Code, data tables, numbers | All sizes |

#### Install Inter (Variable Font)

```bash
# Via Bun
bun add @fontsource-variable/inter

# Import di main.tsx
import '@fontsource-variable/inter';
```

```css
/* Atau via Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=swap');
```

---

### 14.2 Text Styles - Apple HIG Mapping

#### macOS/iOS Text Styles → SIMANIS62

| Apple Style | Size | Weight | Line Height | SIMANIS62 Use Case |
|-------------|------|--------|-------------|-------------------|
| **Large Title** | 34px | Bold | 41px | Page headers (Dashboard) |
| **Title 1** | 28px | Light | 34px | Section titles |
| **Title 2** | 22px | Regular | 28px | Card headers |
| **Title 3** | 20px | Regular | 24px | Subsection titles |
| **Headline** | 17px | Semibold | 22px | Table headers, labels |
| **Body** | 17px | Regular | 22px | Main content |
| **Callout** | 16px | Regular | 21px | Highlighted info |
| **Subhead** | 15px | Regular | 20px | Secondary labels |
| **Footnote** | 13px | Regular | 18px | Help text, timestamps |
| **Caption 1** | 12px | Regular | 16px | Table cells, badges |
| **Caption 2** | 11px | Regular | 13px | Smallest text, status |

#### Optimized untuk Desktop App (Interaction-Heavy)

Karena SIMANIS62 adalah **interaction-heavy desktop app** (bukan text-heavy), ukuran font di-scale down:

| Style | Original | SIMANIS62 | Tailwind Class |
|-------|----------|-----------|----------------|
| Large Title | 34px | 28px | `text-2xl` |
| Title 1 | 28px | 24px | `text-xl` |
| Title 2 | 22px | 20px | `text-lg` |
| Title 3 | 20px | 18px | `text-base` |
| Headline | 17px | 15px | `text-sm font-semibold` |
| Body | 17px | 14px | `text-sm` |
| Callout | 16px | 14px | `text-sm` |
| Subhead | 15px | 13px | `text-xs` |
| Footnote | 13px | 12px | `text-xs` |
| Caption | 12px | 11px | `text-[11px]` |

---

### 14.3 Font Sizes - Tailwind Configuration

```typescript
// tailwind.config.ts
export default {
  theme: {
    fontSize: {
      // macOS-style sizes (optimized for desktop)
      'xs': ['12px', { lineHeight: '16px', letterSpacing: '0' }],
      'sm': ['14px', { lineHeight: '20px', letterSpacing: '-0.006em' }],
      'base': ['16px', { lineHeight: '24px', letterSpacing: '-0.011em' }],
      'lg': ['18px', { lineHeight: '28px', letterSpacing: '-0.014em' }],
      'xl': ['20px', { lineHeight: '28px', letterSpacing: '-0.017em' }],
      '2xl': ['24px', { lineHeight: '32px', letterSpacing: '-0.019em' }],
      '3xl': ['28px', { lineHeight: '36px', letterSpacing: '-0.021em' }],
      '4xl': ['34px', { lineHeight: '40px', letterSpacing: '-0.022em' }],
      '5xl': ['42px', { lineHeight: '48px', letterSpacing: '-0.022em' }],
      
      // Custom sizes untuk dense UI
      '2xs': ['11px', { lineHeight: '14px', letterSpacing: '0.006em' }],
      '3xs': ['10px', { lineHeight: '12px', letterSpacing: '0.012em' }],
    },
  },
}
```

---

### 14.4 Character Spacing (Tracking)

Apple menggunakan **negative tracking** untuk ukuran besar dan **positive tracking** untuk ukuran kecil:

```typescript
// tailwind.config.ts
export default {
  theme: {
    letterSpacing: {
      // Apple-style tracking
      'tighter': '-0.025em',   // -2.5% untuk body (17pt)
      'tight': '-0.016em',     // -1.6% untuk secondary (15pt)
      'normal': '0',           // 0% untuk footnote (12pt)
      'wide': '0.006em',       // +0.6% untuk caption (11pt)
      'wider': '0.011em',      // +1.1% untuk bold title
      'widest': '0.012em',     // +1.2% untuk smallest (10pt)
    },
  },
}
```

#### Tracking by Size (SF Pro / Inter)

| Size | Tracking (px) | Tracking (%) | CSS Value |
|------|---------------|--------------|-----------|
| 10px | +0.12 | +1.2% | `0.012em` |
| 11px | +0.06 | +0.5% | `0.006em` |
| 12px | 0 | 0% | `0` |
| 13px | -0.08 | -0.6% | `-0.006em` |
| 14px | -0.15 | -1.1% | `-0.011em` |
| 15px | -0.24 | -1.6% | `-0.016em` |
| 16px | -0.32 | -2.0% | `-0.020em` |
| 17px | -0.43 | -2.5% | `-0.025em` |
| 18px+ | -0.43 | -2.5% | `-0.025em` |
| 20px+ | +0.19 | +1.0% | `0.019em` |
| 28px+ | +0.13 | +0.5% | `0.013em` |
| 34px+ | +0.40 | +1.1% | `0.011em` |

---

### 14.5 Line Heights (Leading)

```typescript
// tailwind.config.ts
export default {
  theme: {
    lineHeight: {
      // Apple-style leading
      'none': '1',
      'tight': '1.15',      // Headlines
      'snug': '1.25',       // Subheadings
      'normal': '1.4',      // Body text
      'relaxed': '1.5',     // Long-form text
      'loose': '1.625',     // Captions, small text
      
      // Fixed values (untuk precise control)
      '3': '12px',
      '4': '16px',
      '5': '20px',
      '6': '24px',
      '7': '28px',
      '8': '32px',
      '9': '36px',
      '10': '40px',
    },
  },
}
```

---

### 14.6 Font Weights

Inter dan SF Pro memiliki 9 weights yang sama:

```typescript
// tailwind.config.ts
export default {
  theme: {
    fontWeight: {
      'thin': '100',        // Ultralight
      'extralight': '200',  // Thin
      'light': '300',       // Light
      'normal': '400',      // Regular
      'medium': '500',      // Medium
      'semibold': '600',    // Semibold
      'bold': '700',        // Bold
      'extrabold': '800',   // Heavy
      'black': '900',       // Black
    },
  },
}
```

#### Weight Usage Guidelines

| Weight | Value | Use Case |
|--------|-------|----------|
| Light | 300 | Large titles (28px+) |
| Regular | 400 | Body text, labels |
| Medium | 500 | Emphasized body, buttons |
| Semibold | 600 | Headlines, table headers |
| Bold | 700 | Important actions, alerts |

---

### 14.7 CSS Custom Properties

```css
/* src/styles/typography.css */

:root {
  /* Font Family */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 
               'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', 'JetBrains Mono', Consolas, monospace;
  
  /* Base Size */
  --text-base-size: 14px;
  
  /* Type Scale (1.25 ratio - Major Third) */
  --text-scale-ratio: 1.25;
  
  /* Computed Sizes */
  --text-xs: calc(var(--text-base-size) / var(--text-scale-ratio));     /* 11.2px */
  --text-sm: var(--text-base-size);                                      /* 14px */
  --text-md: calc(var(--text-base-size) * var(--text-scale-ratio));     /* 17.5px */
  --text-lg: calc(var(--text-md) * var(--text-scale-ratio));            /* 21.9px */
  --text-xl: calc(var(--text-lg) * var(--text-scale-ratio));            /* 27.3px */
  --text-2xl: calc(var(--text-xl) * var(--text-scale-ratio));           /* 34.2px */
  
  /* Line Heights */
  --leading-tight: 1.15;
  --leading-snug: 1.25;
  --leading-normal: 1.4;
  --leading-relaxed: 1.5;
  
  /* Letter Spacing */
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.006em;
}

/* Dark Mode Adjustments */
.dark {
  /* Slightly increase font weight in dark mode for better legibility */
  --font-weight-body: 400;
  --font-weight-heading: 600;
}
```

---

### 14.8 Typography Components

#### Text Styles Component

```tsx
// components/ui/text.tsx
import { cn } from '@/lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';

const textVariants = cva('', {
  variants: {
    variant: {
      // Titles
      'large-title': 'text-[28px] font-bold leading-tight tracking-[-0.021em]',
      'title-1': 'text-2xl font-light leading-tight tracking-[-0.019em]',
      'title-2': 'text-xl font-normal leading-snug tracking-[-0.017em]',
      'title-3': 'text-lg font-normal leading-snug tracking-[-0.014em]',
      
      // Body
      'headline': 'text-[15px] font-semibold leading-normal tracking-[-0.016em]',
      'body': 'text-sm font-normal leading-normal tracking-[-0.006em]',
      'callout': 'text-sm font-normal leading-normal tracking-[-0.006em]',
      'subhead': 'text-[13px] font-normal leading-normal tracking-normal',
      
      // Small
      'footnote': 'text-xs font-normal leading-relaxed tracking-normal',
      'caption-1': 'text-[11px] font-normal leading-loose tracking-wide',
      'caption-2': 'text-[11px] font-normal leading-loose tracking-wide',
    },
    color: {
      'primary': 'text-gray-900 dark:text-white',
      'secondary': 'text-gray-600 dark:text-gray-300',
      'tertiary': 'text-gray-500 dark:text-gray-400',
      'quaternary': 'text-gray-400 dark:text-gray-500',
      'accent': 'text-accent-blue',
      'success': 'text-accent-green',
      'warning': 'text-accent-orange',
      'danger': 'text-accent-red',
    },
  },
  defaultVariants: {
    variant: 'body',
    color: 'primary',
  },
});

interface TextProps
  extends React.HTMLAttributes<HTMLParagraphElement>,
    VariantProps<typeof textVariants> {
  as?: 'p' | 'span' | 'div' | 'label' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
}

export function Text({
  className,
  variant,
  color,
  as: Component = 'p',
  ...props
}: TextProps) {
  return (
    <Component
      className={cn(textVariants({ variant, color }), className)}
      {...props}
    />
  );
}
```

#### Usage Examples

```tsx
// Page title
<Text variant="large-title" as="h1">Dashboard</Text>

// Section title
<Text variant="title-2" as="h2">Daftar Aset</Text>

// Table header
<Text variant="headline" color="secondary">Nama Barang</Text>

// Body text
<Text variant="body">Laptop Dell Latitude 5520</Text>

// Caption
<Text variant="caption-1" color="tertiary">Terakhir diupdate: 5 menit lalu</Text>

// Footnote
<Text variant="footnote" color="quaternary">* Harga dalam Rupiah</Text>
```

---

### 14.9 Typography for Data Tables

Untuk dense data tables di SIMANIS62:

```tsx
// components/features/aset/AsetTable.tsx

// Table header
<th className="text-[11px] font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
  Nama Barang
</th>

// Table cell - primary
<td className="text-[13px] font-normal text-gray-900 dark:text-white">
  Laptop Dell Latitude 5520
</td>

// Table cell - secondary
<td className="text-[13px] font-normal text-gray-600 dark:text-gray-300">
  02.06.01.0001
</td>

// Table cell - number (monospace)
<td className="text-[13px] font-mono tabular-nums text-gray-900 dark:text-white">
  Rp 15.000.000
</td>

// Table cell - badge
<span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-green-100 text-green-800">
  Baik
</span>
```

#### Table Typography Specs

| Element | Size | Weight | Font | Tracking |
|---------|------|--------|------|----------|
| Header | 11px | Semibold | Sans | +0.05em (uppercase) |
| Cell Primary | 13px | Normal | Sans | 0 |
| Cell Secondary | 13px | Normal | Sans | 0 |
| Cell Number | 13px | Normal | Mono | 0 |
| Badge | 11px | Medium | Sans | 0 |
| Pagination | 12px | Normal | Sans | 0 |

---

### 14.10 Typography Best Practices

#### ✅ DO

1. **Use Inter as primary font** - Closest to SF Pro, open-source
2. **Use variable font** - Better performance, smoother scaling
3. **Apply negative tracking** - For body text (14-17px)
4. **Use monospace for numbers** - Better alignment in tables
5. **Maintain hierarchy** - Max 4-5 font sizes per page
6. **Test on actual device** - Rendering differs across OS/browser

#### ❌ DON'T

1. **Don't use too many font sizes** - Stick to the type scale
2. **Don't use light weights below 14px** - Poor legibility
3. **Don't ignore tracking** - SF Pro/Inter need adjusted spacing
4. **Don't mix too many fonts** - Max 2 font families
5. **Don't use pure black (#000)** - Use dark gray (#1C1C1E) instead

---

### 14.11 Accessibility Considerations

```css
/* Minimum font sizes for accessibility */
:root {
  /* WCAG 2.0 recommends minimum 18pt (24px) or 14pt bold (18.67px) */
  --min-readable-size: 12px;
  --min-body-size: 14px;
  --min-touch-target: 44px;
}

/* Support user font size preferences */
@media (prefers-reduced-motion: no-preference) {
  html {
    font-size: 100%; /* Respect browser default (usually 16px) */
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  :root {
    --text-primary: #000000;
    --text-secondary: #1C1C1E;
  }
  
  .dark {
    --text-primary: #FFFFFF;
    --text-secondary: #F5F5F7;
  }
}
```

---

### 14.12 Font Loading Strategy

```tsx
// main.tsx - Optimal font loading

// 1. Preload critical fonts
<link
  rel="preload"
  href="/fonts/Inter-Variable.woff2"
  as="font"
  type="font/woff2"
  crossOrigin="anonymous"
/>

// 2. Use font-display: swap for fast initial render
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

// 3. Subset fonts for smaller file size
// Use tools like glyphhanger or fonttools to subset
```

#### Font File Sizes

| Font | Full | Subset (Latin) |
|------|------|----------------|
| Inter Variable | ~300KB | ~100KB |
| SF Mono | ~200KB | ~80KB |

---

*Section ini ditambahkan: 12 Januari 2026*
*Berdasarkan Apple Human Interface Guidelines Typography dan research font best practices 2025*
*Sources: Apple HIG, learnui.design, pangrampangram.com, scopedesign.com*
