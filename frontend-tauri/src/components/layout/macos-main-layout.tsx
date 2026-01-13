/**
 * macOS Main Layout
 * 
 * Complete application layout using macOS Liquid Glass design
 * with title bar, sidebar, and status bar.
 */

import { useState } from 'react';
import { MacOSDesktopShell } from './macos-desktop-shell';
import {
    Home,
    Package,
    FileText,
    ArrowLeftRight,
    Building,
    Settings,
} from 'lucide-react';
import type { NavItem } from './macos-sidebar';

interface MacOSMainLayoutProps {
    children: React.ReactNode;
    activeRoute?: string;
    onNavigate?: (route: string) => void;
}

// Define navigation items for SIMANIS62
const navigation: NavItem[] = [
    { id: 'dashboard', icon: Home, label: 'Dashboard', href: '/' },
    { id: 'aset', icon: Package, label: 'Daftar Aset', href: '/aset' },
    { id: 'kib', icon: FileText, label: 'Laporan KIB', href: '/kib' },
    { id: 'mutasi', icon: ArrowLeftRight, label: 'Mutasi Aset', href: '/mutasi' },
    { id: 'ruangan', icon: Building, label: 'Ruangan', href: '/ruangan' },
    { id: 'settings', icon: Settings, label: 'Pengaturan', href: '/settings' },
];

export function MacOSMainLayout({
    children,
    activeRoute = '/',
    onNavigate
}: MacOSMainLayoutProps) {
    const [currentRoute, setCurrentRoute] = useState(activeRoute);

    const handleNavigate = (href: string) => {
        setCurrentRoute(href);
        onNavigate?.(href);
    };

    return (
        <MacOSDesktopShell
            title="SIMANIS62"
            navigation={navigation}
            activeNavItem={currentRoute}
            onNavigate={handleNavigate}
        >
            {children}
        </MacOSDesktopShell>
    );
}
