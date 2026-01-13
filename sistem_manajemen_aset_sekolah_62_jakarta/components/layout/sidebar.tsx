"use client"

import type React from "react"

import { useState } from "react"
import {
  LayoutDashboard,
  Package,
  FileText,
  Users,
  Settings,
  ChevronLeft,
  ChevronRight,
  Building2,
  FolderTree,
  BarChart3,
  HelpCircle,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface NavItem {
  id: string
  label: string
  icon: React.ElementType
  href?: string
  badge?: number
  children?: { id: string; label: string; href: string }[]
}

const navItems: NavItem[] = [
  {
    id: "dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
    href: "/dashboard",
  },
  {
    id: "aset",
    label: "Daftar Aset",
    icon: Package,
    children: [
      { id: "kib-a", label: "KIB A - Tanah", href: "/aset/kib-a" },
      { id: "kib-b", label: "KIB B - Peralatan & Mesin", href: "/aset/kib-b" },
      { id: "kib-c", label: "KIB C - Gedung & Bangunan", href: "/aset/kib-c" },
      { id: "kib-d", label: "KIB D - Jalan, Irigasi, Jaringan", href: "/aset/kib-d" },
      { id: "kib-e", label: "KIB E - Aset Tetap Lainnya", href: "/aset/kib-e" },
      { id: "kib-f", label: "KIB F - Konstruksi Dalam Pengerjaan", href: "/aset/kib-f" },
    ],
  },
  {
    id: "ruangan",
    label: "Ruangan",
    icon: Building2,
    href: "/ruangan",
  },
  {
    id: "kategori",
    label: "Kategori",
    icon: FolderTree,
    href: "/kategori",
  },
  {
    id: "laporan",
    label: "Laporan",
    icon: FileText,
    children: [
      { id: "rekap", label: "Rekap Aset", href: "/laporan/rekap" },
      { id: "mutasi", label: "Laporan Mutasi", href: "/laporan/mutasi" },
      { id: "kondisi", label: "Laporan Kondisi", href: "/laporan/kondisi" },
    ],
  },
  {
    id: "statistik",
    label: "Statistik",
    icon: BarChart3,
    href: "/statistik",
  },
  {
    id: "pengguna",
    label: "Pengguna",
    icon: Users,
    href: "/pengguna",
  },
]

const bottomNavItems: NavItem[] = [
  {
    id: "pengaturan",
    label: "Pengaturan",
    icon: Settings,
    href: "/pengaturan",
  },
  {
    id: "bantuan",
    label: "Bantuan",
    icon: HelpCircle,
    href: "/bantuan",
  },
]

interface SidebarProps {
  collapsed?: boolean
  onCollapsedChange?: (collapsed: boolean) => void
}

export function Sidebar({ collapsed = false, onCollapsedChange }: SidebarProps) {
  const [expandedItems, setExpandedItems] = useState<string[]>(["aset"])
  const [activeItem, setActiveItem] = useState("dashboard")

  const toggleExpanded = (id: string) => {
    setExpandedItems((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]))
  }

  const NavItemComponent = ({ item, isBottom = false }: { item: NavItem; isBottom?: boolean }) => {
    const Icon = item.icon
    const isExpanded = expandedItems.includes(item.id)
    const isActive = activeItem === item.id
    const hasChildren = item.children && item.children.length > 0

    const content = (
      <div>
        <button
          onClick={() => {
            if (hasChildren) {
              toggleExpanded(item.id)
            } else {
              setActiveItem(item.id)
            }
          }}
          className={cn(
            "w-full flex items-center gap-2 px-2 py-1.5 text-xs rounded-sm transition-colors",
            isActive && !hasChildren
              ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
              : "text-sidebar-foreground/80 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground",
          )}
        >
          <Icon className="w-4 h-4 shrink-0" />
          {!collapsed && (
            <>
              <span className="flex-1 text-left truncate">{item.label}</span>
              {hasChildren && (
                <ChevronRight className={cn("w-3 h-3 transition-transform", isExpanded && "rotate-90")} />
              )}
              {item.badge && (
                <span className="px-1.5 py-0.5 text-[10px] bg-primary text-primary-foreground rounded-sm">
                  {item.badge}
                </span>
              )}
            </>
          )}
        </button>

        {/* Children */}
        {hasChildren && isExpanded && !collapsed && (
          <div className="ml-4 mt-0.5 space-y-0.5 border-l border-border pl-2">
            {item.children!.map((child) => (
              <button
                key={child.id}
                onClick={() => setActiveItem(child.id)}
                className={cn(
                  "w-full flex items-center px-2 py-1 text-xs rounded-sm transition-colors",
                  activeItem === child.id
                    ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                    : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground",
                )}
              >
                <span className="truncate">{child.label}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    )

    if (collapsed) {
      return (
        <Tooltip delayDuration={0}>
          <TooltipTrigger asChild>{content}</TooltipTrigger>
          <TooltipContent side="right" className="text-xs">
            {item.label}
          </TooltipContent>
        </Tooltip>
      )
    }

    return content
  }

  return (
    <TooltipProvider>
      <div
        className={cn(
          "h-full bg-sidebar border-r border-sidebar-border flex flex-col transition-all duration-200",
          collapsed ? "w-12" : "w-52",
        )}
      >
        {/* Logo Section */}
        <div className="h-10 flex items-center justify-between px-2 border-b border-sidebar-border shrink-0">
          {!collapsed && (
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-primary rounded-sm flex items-center justify-center">
                <span className="text-xs font-bold text-primary-foreground">S</span>
              </div>
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-sidebar-foreground leading-tight">SIMANIS62</span>
                <span className="text-[10px] text-sidebar-foreground/60 leading-tight">v2.0.0</span>
              </div>
            </div>
          )}
          <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => onCollapsedChange?.(!collapsed)}>
            {collapsed ? <ChevronRight className="w-3.5 h-3.5" /> : <ChevronLeft className="w-3.5 h-3.5" />}
          </Button>
        </div>

        {/* Main Navigation */}
        <nav className="flex-1 overflow-y-auto py-2 px-1.5 space-y-0.5">
          {navItems.map((item) => (
            <NavItemComponent key={item.id} item={item} />
          ))}
        </nav>

        {/* Bottom Navigation */}
        <div className="border-t border-sidebar-border py-2 px-1.5 space-y-0.5 shrink-0">
          {bottomNavItems.map((item) => (
            <NavItemComponent key={item.id} item={item} isBottom />
          ))}
        </div>
      </div>
    </TooltipProvider>
  )
}
