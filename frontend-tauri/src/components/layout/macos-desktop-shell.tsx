/**
 * macOS-Style Desktop Shell
 * 
 * Complete application shell with:
 * - macOS traffic light title bar
 * - Glass sidebar with navigation
 * - Main content area
 * - Status bar at bottom
 * 
 * This is the main layout container for the SIMANIS62 desktop app
 * implementing Apple's Liquid Glass design language.
 * 
 * @see .kiro/steering/design-system.md Section 13
 */

import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { MacOSTitleBar } from './macos-title-bar';
import { MacOSSidebar, type NavItem } from './macos-sidebar';
import { MacOSStatusBar } from './macos-status-bar';
import { Home, Package, FileText, ArrowLeftRight, Building } from 'lucide-react'; // Import icons

interface MacOSDesktopShellProps {
    children: React.ReactNode;
    title?: string;
    navigation?: NavItem[];
    // activeNavItem removed as it's now derived from useLocation
    // onNavigate removed as it's now handled by useNavigate
    statusItems?: {
        left?: React.ReactNode;
        right?: React.ReactNode;
    };
    className?: string;
}

export function MacOSDesktopShell({
    children,
    title = 'SIMANIS62',
    navigation = [ // Default navigation array with English labels
        { id: 'dashboard', icon: Home, label: 'Dashboard', href: '/' },
        { id: 'aset', icon: Package, label: 'Assets', href: '/aset' },
        { id: 'kib', icon: FileText, label: 'KIB Reports', href: '/kib' },
        { id: 'mutasi', icon: ArrowLeftRight, label: 'Asset Mutation', href: '/mutasi' },
        { id: 'ruangan', icon: Building, label: 'Rooms', href: '/ruangan' },
    ],
    // Removed activeNavItem & onNavigate props
    statusItems,
    className,
}: MacOSDesktopShellProps) {
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();

    const handleNavigate = (href: string) => {
        navigate(href);
    };

    return (
        <div className={cn(
            'h-screen w-screen flex flex-col overflow-hidden',
            // Sequoia-like background (very subtle gray/black)
            'bg-[#F5F5F7] dark:bg-[#000000]',
            className
        )}>
            {/* Title Bar */}
            <MacOSTitleBar title={title} />

            {/* Main Content Area */}
            <div className="flex-1 flex overflow-hidden min-h-0 relative">
                {/* Sidebar */}
                <MacOSSidebar
                    collapsed={sidebarCollapsed}
                    onCollapsedChange={setSidebarCollapsed}
                    navigation={navigation}
                    activeItem={location.pathname}
                    onNavigate={handleNavigate}
                />

                {/* Content */}
                <main className={cn(
                    'flex-1 min-h-0 min-w-0 overflow-y-auto overflow-x-hidden',
                    'bg-[#F5F5F7] dark:bg-[#000000]', // Match shell background
                    'relative z-0'
                )}>
                    {children}
                </main>
            </div>

            {/* Status Bar */}
            <MacOSStatusBar
                leftContent={statusItems?.left}
                rightContent={statusItems?.right}
            />
        </div>
    );
}

/**
 * Simpler shell variant without sidebar
 * Useful for modal windows or single-page views
 */
export function MacOSWindowShell({
    children,
    title,
    className,
}: {
    children: React.ReactNode;
    title?: string;
    className?: string;
}) {
    return (
        <div className={cn(
            'h-screen w-screen flex flex-col overflow-hidden',
            'bg-[#F5F5F7] dark:bg-[#1C1C1E]',
            className
        )}>
            <MacOSTitleBar title={title} showAppIcon={false} />
            <main className="flex-1 overflow-y-auto">
                {children}
            </main>
        </div>
    );
}
