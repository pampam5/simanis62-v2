# SIMANIS62 Frontend - macOS Liquid Glass Style

Frontend aplikasi SIMANIS62 dengan **macOS Liquid Glass Design Language 2025**.

## Tech Stack

- **Tauri v2** - Desktop runtime
- **React 19** - UI framework
- **TypeScript 5** - Type safety
- **Tailwind CSS 4** - Styling
- **Bun** - Package manager
- **Lucide React** - Icons
- **class-variance-authority** - Component variants

## Design System

Menggunakan **Apple Liquid Glass Design Language** dengan karakteristik:
- Glassmorphism effects (backdrop blur, transparency)
- Apple-style typography (Inter font, SF Pro alternative)
- macOS color palette (vibrant accents)
- Smooth animations dan microinteractions
- Dark mode support

## Project Structure

```
src/
├── components/
│   ├── ui/                    # Glass UI components
│   │   ├── glass-button.tsx
│   │   ├── glass-card.tsx
│   │   ├── glass-input.tsx
│   │   └── text.tsx
│   └── layout/                # Layout components
│       ├── Sidebar.tsx
│       └── MainLayout.tsx
├── pages/                     # Page components
│   └── DashboardPage.tsx
├── styles/
│   └── glass.css             # Glass effects CSS
└── lib/
    └── utils.ts              # Utilities (cn helper)
```

## Components

### Glass UI Components

#### GlassButton
Button dengan glassmorphism effect dan 4 variants:
- `primary` - Blue filled button
- `secondary` - Glass button dengan border
- `ghost` - Transparent button
- `danger` - Red filled button

```tsx
import { GlassButton } from '@/components/ui/glass-button';

<GlassButton variant="primary" size="md">
  Simpan
</GlassButton>
```

#### GlassCard
Card dengan glass effect dan hover animation:

```tsx
import { GlassCard } from '@/components/ui/glass-card';

<GlassCard className="p-6">
  <h2>Card Title</h2>
  <p>Card content...</p>
</GlassCard>
```

#### GlassInput
Input field dengan glass background:

```tsx
import { GlassInput } from '@/components/ui/glass-input';

<GlassInput 
  placeholder="Cari aset..." 
  glass={true}
/>
```

#### Text
Typography component dengan Apple HIG text styles:

```tsx
import { Text } from '@/components/ui/text';

<Text variant="large-title" as="h1">Dashboard</Text>
<Text variant="body" color="secondary">Description text</Text>
<Text variant="caption-1" color="tertiary">Small text</Text>
```

**Text Variants:**
- `large-title` (28px, bold)
- `title-1` (24px, light)
- `title-2` (20px, regular)
- `title-3` (18px, regular)
- `headline` (15px, semibold)
- `body` (14px, regular)
- `callout` (14px, regular)
- `subhead` (13px, regular)
- `footnote` (12px, regular)
- `caption-1` (11px, regular)
- `caption-2` (11px, regular)

**Text Colors:**
- `primary` - Main text color
- `secondary` - Secondary text
- `tertiary` - Tertiary text
- `quaternary` - Quaternary text
- `accent` - Blue accent
- `success` - Green
- `warning` - Orange
- `danger` - Red

### Layout Components

#### Sidebar
Collapsible sidebar dengan glass effect:
- Logo dan app name
- Navigation menu dengan icons
- Active state highlighting
- User profile section
- Collapse to icons only mode

#### MainLayout
Main layout wrapper dengan:
- Sidebar
- Content area
- Status bar

## Development

### Install Dependencies

```bash
# Install dengan Bun (recommended)
bun install

# Atau dengan npm
npm install
```

### Run Development Server

```bash
# Tauri dev mode
bun run tauri dev

# Atau hanya frontend
bun run dev
```

### Build

```bash
# Build untuk production
bun run tauri build
```

## Typography System

Font stack: **Inter** (closest to SF Pro)

### Font Sizes (Desktop Optimized)

| Style | Size | Weight | Use Case |
|-------|------|--------|----------|
| Large Title | 28px | Bold | Page headers |
| Title 1 | 24px | Light | Section titles |
| Title 2 | 20px | Regular | Card headers |
| Body | 14px | Regular | Main content |
| Caption | 11px | Regular | Small text |

### Character Spacing (Tracking)

- Body text (14-17px): **-0.006em** (negative)
- Small text (11-12px): **0 to +0.006em** (positive)
- Large titles (20px+): **+0.011em** (positive)

## Color Palette

### Accent Colors (Apple-style)

```css
--accent-blue: #007AFF;      /* Primary action */
--accent-green: #34C759;     /* Success */
--accent-orange: #FF9500;    /* Warning */
--accent-red: #FF3B30;       /* Danger */
--accent-purple: #AF52DE;    /* Secondary */
--accent-pink: #FF2D55;      /* Alerts */
--accent-teal: #5AC8FA;      /* Info */
```

### Dark Mode

Otomatis menggunakan dark variants:
```css
.dark --accent-blue: #0A84FF;
.dark --accent-green: #30D158;
```

## Glass Effects

### CSS Classes

```css
.glass-panel      /* Standard glass panel */
.glass-sidebar    /* Sidebar dengan blur 40px */
.glass-card       /* Card dengan hover effect */
.glass-modal      /* Modal dengan blur tinggi */
.glass-button     /* Button glass */
.glass-input      /* Input glass */
```

### Custom Glass Effect

```tsx
<div className="bg-white/60 dark:bg-zinc-800/60 backdrop-blur-xl backdrop-saturate-[180%] border border-white/20 rounded-2xl">
  Content
</div>
```

## Animations

Built-in animations:
- `animate-fade-in` - Fade in effect
- `animate-slide-up` - Slide up from bottom
- `animate-scale-in` - Scale in effect
- `animate-blur-in` - Blur in effect

## Accessibility

- Support `prefers-reduced-motion`
- Support `prefers-contrast: high`
- Keyboard navigation
- Focus rings
- ARIA labels

## References

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Liquid Glass Design Language](https://developer.apple.com/design/whats-new/)
- [Inter Font](https://rsms.me/inter/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)

## Design System Documentation

Lihat dokumentasi lengkap di:
- `.kiro/steering/design-system.md` - Section 13 & 14
- `src/styles/glass.css` - CSS implementation

---

**Version:** 2.0.0  
**Last Updated:** 12 Januari 2026  
**Design Language:** macOS Liquid Glass 2025
