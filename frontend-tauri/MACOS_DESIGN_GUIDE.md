# macOS Liquid Glass (Sequoia 2025) - Design Guide

## 1. Design Philosophy: "Liquid Glass"
Apple's latest design language for macOS Sequoia (15.x+) and upcoming 2025 updates focuses on **Liquid Glass**—a functional layer that floats above content, providing structure without stealing focus.

### Key Heuristics
- **Separation**: Primary content vs. Functional UI vs. Background.
- **Dimming**: When a sheet/modal appears, the background dims, focusing attention on the "Liquid Glass" layer.
- **Tinted Actions**: Primary actions (like "Done" or "Save") are **tinted** (often blue/accent color text on a light tinted background) rather than solid filled buttons in many contexts, or solid text buttons for high emphasis.

---

## 2. Design Tokens (src/styles/glass.css)

### Materials (Backdrops)
We define specific material types based on their "thickness" and purpose.

| Material | Class | CSS Properties | Usage |
|----------|-------|----------------|-------|
| **Base** | `.glass-base` | `bg-white/72 backdrop-blur(20px) saturate(180%)` | Window background, Sidebar (Base) |
| **Thick** | `.glass-thick` | `bg-white/85 backdrop-blur(50px) saturate(200%)` | Popovers, Menus, Modals, HUDs |
| **Thin** | `.glass-thin` | `bg-white/50 backdrop-blur(10px) saturate(150%)` | Overlays, Toast notifications |
| **Chrome** | `.glass-chrome` | `bg-white/60 backdrop-blur(30px) saturate(180%)` | Toolbars, Title Bars |

### Shadows & Depth
macOS 2025 reduces heavy drop shadows in favor of **rim highlights** and **ambient occlusion**.

```css
/* Rim Highlight (Inner top border) */
--glass-rim: inset 0 1px 0 0 rgba(255, 255, 255, 0.4);

/* Ambient Shadow (Deep, soft) */
--glass-shadow: 0 4px 20px rgba(0, 0, 0, 0.12), 0 0 1px rgba(0, 0, 0, 0.1);
```

### Typography (San Francisco / SF Pro)
If `SF Pro` is available, use it. Otherwise fallback to `-apple-system`.

```css
font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
```

---

## 3. Component Updates

### Tinted Buttons
Primary actions should use the **Tinted** style.

- **Light Mode**: Text is Accent Color. Background is Accent Color (opacity 10-15%).
- **Dark Mode**: Text is Light Accent. Background is Accent Color (opacity 20-25%).
- **Hover**: Increase background opacity and scale subtlely (1.02x).

**Example:**
```tsx
<button className="bg-[#007AFF]/10 text-[#007AFF] hover:bg-[#007AFF]/20 transition-all rounded-[6px] px-3 py-1 text-[13px] font-medium">
  Save Changes
</button>
```

### Sidebar (Navigation)
- **Selection State**: Rounded rectangle, **not** touching screen edges.
- **Icon**: Tinted Blue (or Accent) when active. Gray when inactive.
- **Text**: Semibold black when active. Regular gray when inactive.
- **Hover**: Subtle gray background `rgba(0,0,0,0.05)`.

### Cards (Dashboard)
- Remove heavy borders inside grids. Use **spacing** and **subtle background variation**.
- Use `.glass-card` for container.
- Content inside cards should be clean, using `SF Symbols` (Lucide equivalents) with **gradient circles** as backgrounds for icons.

---

## 4. Implementation Checklist

1. [ ] **Update `glass.css`**: Add `.glass-base`, `.glass-thick`, `.glass-chrome` utilities.
2. [ ] **Refactor `MacOSSidebar.tsx`**: Implement the new selection state and glass material.
3. [ ] **Create `MacOSTintedButton.tsx`**: Reusable component for the specific Sequoia button style.
4. [ ] **Update `MacOSStatsGrid`**: Use new card styling with reduced visual noise.

---
*Verified against WWDC25 "Liquid Glass" heuristics.*
