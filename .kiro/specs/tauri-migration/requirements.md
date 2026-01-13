# SIMANIS62 V2 - Tauri Frontend Migration

## Overview

Migrasi frontend dari WPF ke Tauri + React + shadcn/ui untuk mendapatkan:
- Bundle size lebih kecil (2-10MB vs 120-150MB)
- Development lebih cepat dengan AI tools (v0.dev)
- Debugging lebih mudah dengan browser DevTools
- Cross-platform support

## User Stories

### US-001: Setup Project dengan tauri-ui Template
**As a** developer
**I want to** setup project Tauri dengan template tauri-ui
**So that** saya bisa mulai development dengan shadcn/ui yang sudah ter-setup

**Acceptance Criteria:**
- [ ] Project dibuat dengan `pnpm create tauri-ui simanis62-frontend --template vite`
- [ ] Dependencies terinstall dengan benar
- [ ] `pnpm tauri dev` berjalan tanpa error
- [ ] Window muncul dengan native controls

### US-002: Main Layout dengan Desktop-Style
**As a** user
**I want to** melihat aplikasi dengan tampilan desktop native
**So that** saya merasa familiar seperti menggunakan aplikasi Windows

**Acceptance Criteria:**
- [ ] Custom title bar dengan logo SIMANIS62
- [ ] Window controls (minimize, maximize, close) berfungsi
- [ ] Collapsible sidebar di kiri
- [ ] Main content area dengan breadcrumb
- [ ] Status bar di bottom

### US-003: Sidebar Navigation
**As a** user
**I want to** navigasi menggunakan sidebar
**So that** saya bisa akses semua fitur dengan mudah

**Acceptance Criteria:**
- [ ] Menu items: Dashboard, Daftar Aset, Laporan KIB, Mutasi, Ruangan, Pengaturan
- [ ] Icons untuk setiap menu
- [ ] Active state highlighting
- [ ] Collapse to icons only mode
- [ ] User profile di bottom dengan logout

### US-004: Login Screen
**As a** user
**I want to** login ke aplikasi
**So that** saya bisa mengakses fitur sesuai role saya

**Acceptance Criteria:**
- [ ] Form login dengan username dan password
- [ ] Validasi input
- [ ] Error message jika login gagal
- [ ] Redirect ke dashboard setelah login sukses
- [ ] Session disimpan

### US-005: Dashboard
**As a** user
**I want to** melihat ringkasan data aset
**So that** saya bisa monitor kondisi aset dengan cepat

**Acceptance Criteria:**
- [ ] Summary cards: Total Aset, Total Nilai, Kondisi Baik, Kondisi Rusak
- [ ] Data dari API backend
- [ ] Recent activity list
- [ ] Quick action buttons

### US-006: Daftar Aset dengan Data Table
**As a** user
**I want to** melihat daftar aset dalam tabel
**So that** saya bisa mencari dan mengelola aset

**Acceptance Criteria:**
- [ ] Data table dengan kolom: No. Register, Nama, Kode, Merk, Tahun, Harga, Kondisi
- [ ] Sorting per kolom
- [ ] Search/filter
- [ ] Pagination
- [ ] Row selection
- [ ] Actions: Edit, Delete

### US-007: Form Tambah/Edit Aset
**As a** Admin
**I want to** menambah atau mengedit data aset
**So that** data aset selalu up-to-date

**Acceptance Criteria:**
- [ ] Modal dialog (bukan full page)
- [ ] Form fields sesuai KIB B (18 kolom)
- [ ] Validasi input
- [ ] Save dan Cancel buttons
- [ ] Success/error notification

### US-008: Export Excel
**As a** Admin atau Kepala Sekolah
**I want to** export data aset ke Excel
**So that** saya bisa membuat laporan

**Acceptance Criteria:**
- [ ] Button Export di toolbar
- [ ] Format sesuai BPAD DKI Jakarta (18 kolom)
- [ ] File tersimpan dengan nama yang benar

### US-009: Dark Mode Support
**As a** user
**I want to** menggunakan dark mode
**So that** mata saya tidak lelah saat bekerja malam

**Acceptance Criteria:**
- [ ] Toggle dark/light mode di settings
- [ ] Semua komponen support dark mode
- [ ] Preference disimpan

### US-010: Keyboard Shortcuts
**As a** power user
**I want to** menggunakan keyboard shortcuts
**So that** saya bisa bekerja lebih cepat

**Acceptance Criteria:**
- [ ] Ctrl+N: Tambah aset baru
- [ ] Ctrl+S: Simpan
- [ ] Ctrl+F: Focus ke search
- [ ] Delete: Hapus selected
- [ ] Escape: Close dialog

## Technical Requirements

### Tech Stack
- Tauri v2
- React 19
- TypeScript 5
- shadcn/ui (latest)
- Tailwind CSS 4
- TanStack Query v5
- TanStack Table v8
- Zustand (state management)
- React Hook Form + Zod

### API Integration
- Backend: FastAPI (port 8000)
- Authentication: Session-based (cookie)
- Endpoints: Sesuai `docs/api_contract.md`

### Bundle Size Target
- Windows installer: < 10MB
- Installed size: < 50MB

## Design References

- v0.dev prompts: `.kiro/steering/design-system.md` section 0.2
- shadcn/ui blocks: sidebar-07, data-table
- Template: tauri-ui by agmmnn

## Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Setup | 1 day | Project structure, dependencies |
| UI Generation | 2 days | Components from v0.dev |
| Customization | 2 days | Desktop styling |
| Integration | 2 days | API connection |
| Testing | 1 day | All features tested |
| **Total** | **~8 days** | |

## Out of Scope (Phase 1)

- Laporan KIB A, C, D, E, F (hanya KIB B untuk MVP)
- Print preview
- Auto-update (Velopack)
- Multi-language support
