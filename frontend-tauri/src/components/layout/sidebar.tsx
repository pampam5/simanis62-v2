/**
 * Sidebar Component - macOS Liquid Glass Style with Responsive Design
 */

import { cn } from '@/lib/utils';
import { Text } from '@/components/ui/text';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Home,
  Package,
  FileText,
  ArrowLeftRight,
  Building,
  Settings,
  ChevronLeft,
  User,
  Menu,
  X
} from 'lucide-react';
import { useState } from 'react';

interface SidebarProps {
  className?: string;
  collapsed?: boolean;
  onCollapsedChange?: (collapsed: boolean) => void;
}

const menuItems = [
  { icon: Home, label: 'Dashboard', href: '/' },
  { icon: Package, label: 'Daftar Aset', href: '/aset' },
  { icon: FileText, label: 'Laporan KIB', href: '/kib' },
  { icon: ArrowLeftRight, label: 'Mutasi Aset', href: '/mutasi' },
  { icon: Building, label: 'Ruangan', href: '/ruangan' },
];

const settingsItems = [
  { icon: Settings, label: 'Pengaturan', href: '/settings' },
];

export function Sidebar({ className, collapsed: controlledCollapsed, onCollapsedChange }: SidebarProps) {
  const [internalCollapsed, setInternalCollapsed] = useState(false);

  const collapsed = controlledCollapsed ?? internalCollapsed;
  const setCollapsed = (value: boolean) => {
    setInternalCollapsed(value);
    onCollapsedChange?.(value);
  };

  const [mobileOpen, setMobileOpen] = useState(false);
  const [activeItem, setActiveItem] = useState('/');

  return (
    <>
      {/* Mobile Menu Button */}
      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        onClick={() => setMobileOpen(!mobileOpen)}
        className={cn(
          'lg:hidden fixed top-4 left-4 z-50',
          'p-2 rounded-lg',
          'bg-white/90',
          'backdrop-blur-xl',
          'border border-black/[0.06]',
          'shadow-lg'
        )}
      >
        {mobileOpen ? (
          <X className="h-5 w-5" />
        ) : (
          <Menu className="h-5 w-5" />
        )}
      </motion.button>

      {/* Mobile Overlay */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setMobileOpen(false)}
            className="lg:hidden fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <aside
        className={cn(
          // Glass effect - Light mode optimized
          'bg-white/90',
          'backdrop-blur-2xl backdrop-saturate-[180%]',
          'border-r border-black/[0.06]',

          // Layout
          'h-screen flex flex-col',
          'transition-all duration-300 ease-out',

          // Width - Responsive
          'fixed lg:relative z-40',
          collapsed ? 'w-16' : 'w-64',

          // Mobile: slide from left
          'lg:translate-x-0',
          mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',

          className
        )}
      >
        {/* Logo Section */}
        <div className="h-14 flex items-center justify-between px-4 border-b border-black/[0.04]">
          <AnimatePresence mode="wait">
            {!collapsed && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.2 }}
                className="flex items-center gap-3"
              >
                <Package className="h-6 w-6 text-[#007AFF]" />
                <Text variant="headline" className="font-semibold">
                  SIMANIS62
                </Text>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Collapse Button - Desktop only */}
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setCollapsed(!collapsed)}
            className={cn(
              'hidden lg:flex p-1.5 rounded-lg',
              'hover:bg-black/[0.04]',
              'transition-colors',
              collapsed && 'mx-auto'
            )}
          >
            <ChevronLeft
              className={cn(
                'h-4 w-4 transition-transform',
                collapsed && 'rotate-180'
              )}
            />
          </motion.button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 overflow-y-auto">
          {/* Main Menu */}
          <div className="px-3 mb-6">
            <AnimatePresence mode="wait">
              {!collapsed && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <Text
                    variant="subhead"
                    color="tertiary"
                    className="px-3 mb-2 uppercase tracking-wider"
                  >
                    Menu Utama
                  </Text>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="space-y-1">
              {menuItems.map((item, index) => (
                <motion.button
                  key={item.href}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    setActiveItem(item.href);
                    setMobileOpen(false);
                  }}
                  className={cn(
                    'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg',
                    'transition-all duration-200',
                    'group relative',
                    activeItem === item.href
                      ? 'bg-[#007AFF]/10 text-[#007AFF]'
                      : 'hover:bg-black/[0.04] text-gray-700'
                  )}
                >
                  {/* Active Indicator */}
                  {activeItem === item.href && (
                    <motion.div
                      layoutId="activeIndicator"
                      className="absolute left-0 w-1 h-6 bg-[#007AFF] rounded-r-full"
                      transition={{ type: 'spring', damping: 30, stiffness: 300 }}
                    />
                  )}

                  <item.icon className={cn(
                    'h-5 w-5 flex-shrink-0',
                    collapsed && 'mx-auto'
                  )} />

                  <AnimatePresence mode="wait">
                    {!collapsed && (
                      <motion.span
                        initial={{ opacity: 0, width: 0 }}
                        animate={{ opacity: 1, width: 'auto' }}
                        exit={{ opacity: 0, width: 0 }}
                        transition={{ duration: 0.2 }}
                      >
                        <Text variant="body" className="whitespace-nowrap">
                          {item.label}
                        </Text>
                      </motion.span>
                    )}
                  </AnimatePresence>
                </motion.button>
              ))}
            </div>
          </div>

          {/* Settings */}
          <div className="px-3">
            <AnimatePresence mode="wait">
              {!collapsed && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <Text
                    variant="subhead"
                    color="tertiary"
                    className="px-3 mb-2 uppercase tracking-wider"
                  >
                    Pengaturan
                  </Text>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="space-y-1">
              {settingsItems.map((item) => (
                <motion.button
                  key={item.href}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    setActiveItem(item.href);
                    setMobileOpen(false);
                  }}
                  className={cn(
                    'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg',
                    'transition-all duration-200',
                    activeItem === item.href
                      ? 'bg-[#007AFF]/10 text-[#007AFF]'
                      : 'hover:bg-black/[0.04] text-gray-700'
                  )}
                >
                  <item.icon className={cn(
                    'h-5 w-5 flex-shrink-0',
                    collapsed && 'mx-auto'
                  )} />

                  <AnimatePresence mode="wait">
                    {!collapsed && (
                      <motion.span
                        initial={{ opacity: 0, width: 0 }}
                        animate={{ opacity: 1, width: 'auto' }}
                        exit={{ opacity: 0, width: 0 }}
                        transition={{ duration: 0.2 }}
                      >
                        <Text variant="body" className="whitespace-nowrap">
                          {item.label}
                        </Text>
                      </motion.span>
                    )}
                  </AnimatePresence>
                </motion.button>
              ))}
            </div>
          </div>
        </nav>

        {/* User Profile */}
        <motion.div
          whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.03)' }}
          className={cn(
            'p-3 border-t border-black/[0.04]',
            'cursor-pointer transition-colors'
          )}
        >
          <div className={cn(
            'flex items-center gap-3',
            collapsed && 'justify-center'
          )}>
            <div className="w-10 h-10 rounded-full bg-[#007AFF]/20 flex items-center justify-center flex-shrink-0">
              <User className="h-5 w-5 text-[#007AFF]" />
            </div>

            <AnimatePresence mode="wait">
              {!collapsed && (
                <motion.div
                  initial={{ opacity: 0, width: 0 }}
                  animate={{ opacity: 1, width: 'auto' }}
                  exit={{ opacity: 0, width: 0 }}
                  transition={{ duration: 0.2 }}
                  className="flex-1 min-w-0"
                >
                  <Text variant="body" className="font-medium truncate text-[15px]">
                    Admin
                  </Text>
                  <Text variant="subhead" color="tertiary" className="truncate">
                    Administrator
                  </Text>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </aside>
    </>
  );
}
