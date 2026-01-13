/**
 * macOS-Style Sidebar Navigation
 * 
 * Features:
 * - Frosted glass background with vibrancy effect
 * - Collapsible design with smooth animations
 * - Apple-style active state with blue accent
 * - SF Symbols-style icons (via Lucide)
 * - User profile section at bottom
 * 
 * @see .kiro/steering/design-system.md Section 13.5 PROMPT 2
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
    LogOut,
    type LucideIcon,
} from 'lucide-react';

export interface NavItem {
    id: string;
    icon: LucideIcon;
    label: string;
    href: string;
    badge?: number;
}

interface MacOSSidebarProps {
    collapsed?: boolean;
    onCollapsedChange?: (collapsed: boolean) => void;
    navigation?: NavItem[];
    activeItem?: string;
    onNavigate?: (href: string) => void;
    user?: {
        name: string;
        role: string;
        avatar?: string;
    };
    className?: string;
}

// Default navigation items for SIMANIS62 - English Menu
const defaultNavigation: NavItem[] = [
    { id: 'dashboard', icon: Home, label: 'Dashboard', href: '/' },
    { id: 'aset', icon: Package, label: 'Assets', href: '/aset' },
    { id: 'kib', icon: FileText, label: 'KIB Reports', href: '/kib' },
    { id: 'mutasi', icon: ArrowLeftRight, label: 'Asset Mutation', href: '/mutasi' },
    { id: 'ruangan', icon: Building, label: 'Rooms', href: '/ruangan' },
];

const settingsNavigation: NavItem[] = [
    { id: 'settings', icon: Settings, label: 'Settings', href: '/settings' },
];

export function MacOSSidebar({
    collapsed = false,
    onCollapsedChange,
    navigation = defaultNavigation,
    activeItem = '/',
    onNavigate,
    user = { name: 'Admin', role: 'Administrator' },
    className,
}: MacOSSidebarProps) {
    const handleNavClick = (href: string) => {
        onNavigate?.(href);
    };

    return (
        <motion.aside
            initial={false}
            animate={{ width: collapsed ? 68 : 260 }} /* Increased width for better spacing */
            transition={{ duration: 0.35, ease: [0.32, 0.72, 0, 1] }} /* Apple Spring-like easing */
            className={cn(
                // Use new semantic sidebar glass class
                'glass-sidebar',
                'bg-opacity-80 dark:bg-opacity-80',

                // Layout
                'h-full flex flex-col',
                'shrink-0 text-sm z-50',

                className
            )}
        >
            {/* Header with improved spacing */}
            <div className={cn(
                'h-[52px] flex items-center justify-between px-4',
                'shrink-0 mb-2'
            )}>
                <AnimatePresence mode="wait">
                    {!collapsed && (
                        <motion.div
                            initial={{ opacity: 0, x: -10, filter: 'blur(5px)' }}
                            animate={{ opacity: 1, x: 0, filter: 'blur(0px)' }}
                            exit={{ opacity: 0, x: -10, filter: 'blur(5px)' }}
                            transition={{ duration: 0.3 }}
                            className="flex items-center gap-2.5"
                        >
                            <div className="w-[26px] h-[26px] rounded-[7px] bg-gradient-to-b from-[#007AFF] to-[#0062CC] dark:from-[#0A84FF] dark:to-[#0056B3] flex items-center justify-center shadow-sm shadow-blue-500/20">
                                <Package className="w-4 h-4 text-white" strokeWidth={2.5} />
                            </div>
                            <Text className="font-bold text-[15px] tracking-tight bg-gradient-to-br from-black to-black/70 dark:from-white dark:to-white/70 bg-clip-text text-transparent">
                                SIMANIS 62
                            </Text>
                        </motion.div>
                    )}
                </AnimatePresence>

                <motion.button
                    whileHover={{ scale: 1.05, backgroundColor: 'var(--color-hover)' }}
                    whileTap={{ scale: 0.96 }}
                    onClick={() => onCollapsedChange?.(!collapsed)}
                    className={cn(
                        'w-7 h-7 rounded-md',
                        'flex items-center justify-center',
                        'text-gray-500 dark:text-gray-400',
                        'transition-all duration-200',
                        collapsed && 'mx-auto'
                    )}
                    aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                >
                    <motion.div
                        animate={{ rotate: collapsed ? 180 : 0 }}
                        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                    >
                        <ChevronLeft className="w-4 h-4" />
                    </motion.div>
                </motion.button>
            </div>

            {/* Navigation Scroller */}
            <nav className="flex-1 overflow-y-auto px-3 pb-4">
                {/* Main Navigation Group */}
                <div className="space-y-[2px]">
                    {navigation.map((item) => (
                        <NavButton
                            key={item.id}
                            item={item}
                            isActive={activeItem === item.href}
                            collapsed={collapsed}
                            onClick={() => handleNavClick(item.href)}
                        />
                    ))}
                </div>

                {/* Separator - now more subtle */}
                <div className="my-4 mx-2 h-px bg-black/5 dark:bg-white/5" />

                {/* Settings Group */}
                <div className="space-y-[2px]">
                    {settingsNavigation.map((item) => (
                        <NavButton
                            key={item.id}
                            item={item}
                            isActive={activeItem === item.href}
                            collapsed={collapsed}
                            onClick={() => handleNavClick(item.href)}
                        />
                    ))}
                </div>
            </nav>

            {/* User Profile - Frosted Card Style */}
            <div className="p-3">
                <div className={cn(
                    'p-2.5 rounded-xl border border-transparent',
                    'hover:bg-white/50 dark:hover:bg-white/5 hover:border-black/5 dark:hover:border-white/5 hover:shadow-sm',
                    'transition-all duration-200 cursor-pointer',
                    'group select-none'
                )}>
                    <div className={cn(
                        'flex items-center gap-3',
                        collapsed && 'justify-center'
                    )}>
                        {/* Avatar */}
                        <div className="relative">
                            <div className={cn(
                                'w-8 h-8 rounded-full',
                                'bg-gradient-to-br from-blue-500 to-indigo-600',
                                'flex items-center justify-center',
                                'shadow-inner'
                            )}>
                                <span className="text-xs font-bold text-white tracking-wide">
                                    {user.name.charAt(0)}
                                </span>
                            </div>
                            <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-green-500 border-[1.5px] border-[#F2F2F7] dark:border-[#1C1C1E] rounded-full" />
                        </div>

                        {/* User info */}
                        <AnimatePresence mode="wait">
                            {!collapsed && (
                                <motion.div
                                    initial={{ opacity: 0, width: 0 }}
                                    animate={{ opacity: 1, width: 'auto' }}
                                    exit={{ opacity: 0, width: 0 }}
                                    className="flex-1 min-w-0"
                                >
                                    <Text className="font-medium truncate text-[13px] leading-tight text-primary">
                                        {user.name}
                                    </Text>
                                    <Text className="truncate text-[11px] text-tertiary">
                                        {user.role}
                                    </Text>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {/* Logout action shows on hover */}
                        <AnimatePresence>
                            {!collapsed && (
                                <motion.button
                                    initial={{ opacity: 0, scale: 0.8 }}
                                    whileHover={{ scale: 1.1, color: 'var(--accent-red)' }}
                                    whileTap={{ scale: 0.9 }}
                                    className={cn(
                                        'opacity-0 group-hover:opacity-100',
                                        'transition-opacity duration-200',
                                        'text-tertiary p-1'
                                    )}
                                    aria-label="Logout"
                                >
                                    <LogOut className="w-3.5 h-3.5" />
                                </motion.button>
                            )}
                        </AnimatePresence>
                    </div>
                </div>
            </div>
        </motion.aside>
    );
}

/**
 * Individual navigation button
 * Implements the "Tinted Button" style for active states
 */
function NavButton({
    item,
    isActive,
    collapsed,
    onClick,
}: {
    item: NavItem;
    isActive: boolean;
    collapsed: boolean;
    onClick: () => void;
}) {
    const Icon = item.icon;

    return (
        <motion.button
            onClick={onClick}
            whileHover={{ backgroundColor: isActive ? undefined : 'var(--color-hover)' }}
            whileTap={{ scale: 0.98 }}
            className={cn(
                'w-full relative group',
                'flex items-center',
                'transition-all duration-200',

                // Sizing
                collapsed ? 'justify-center h-10 px-0 rounded-xl' : 'h-[34px] px-3 rounded-lg gap-3',

                // Active state (Sequoia Tinted Style)
                isActive ? [
                    'bg-blue-500/10 dark:bg-blue-500/15', // Subtle tinted background
                    'text-blue-600 dark:text-blue-400',   // Tinted text
                    'font-medium'
                ] : [
                    'text-gray-500 dark:text-gray-400', // FIXED: Use explicit gray for standard text
                    'hover:text-gray-900 dark:hover:text-gray-100' // High contrast on hover
                ],

                // Collapsed specific styles
                collapsed && isActive && 'bg-transparent text-primary'
            )}
        >
            {/* Active Indicator for Collapsed State */}
            {collapsed && isActive && (
                <motion.div
                    layoutId="activeIndicatorCollapsed"
                    className="absolute inset-0 bg-blue-500/10 dark:bg-blue-500/20 rounded-xl"
                    transition={{ duration: 0.2 }}
                />
            )}

            {/* Icon */}
            <Icon className={cn(
                'shrink-0 transition-colors duration-200',
                collapsed ? 'w-5 h-5' : 'w-[17px] h-[17px]',
                isActive ? 'text-blue-600 dark:text-blue-400' : 'text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-200'
            )} strokeWidth={isActive ? 2.5 : 2} />

            {/* Label */}
            <AnimatePresence mode="wait">
                {!collapsed && (
                    <motion.span
                        initial={{ opacity: 0, x: -5 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -5 }}
                        className="text-[13.5px] whitespace-nowrap tracking-tight"
                    >
                        {item.label}
                    </motion.span>
                )}
            </AnimatePresence>

            {/* Badge */}
            {item.badge && !collapsed && (
                <span className={cn(
                    'ml-auto text-[11px] font-semibold',
                    'px-2 py-0.5 rounded-full',
                    'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400',
                    'min-w-[20px] text-center'
                )}>
                    {item.badge > 99 ? '99+' : item.badge}
                </span>
            )}
        </motion.button>
    );
}
