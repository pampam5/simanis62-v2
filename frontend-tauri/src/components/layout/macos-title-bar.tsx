/**
 * macOS-Style Title Bar with Traffic Light Buttons
 * 
 * Implements Apple's Liquid Glass design language with:
 * - Traffic light buttons (red/yellow/green) positioned on the left
 * - Centered app title
 * - Glass/vibrancy effect
 * 
 * @see .kiro/steering/design-system.md Section 13.5
 */

import { useState, useEffect } from 'react';
import { getCurrentWindow } from '@tauri-apps/api/window';
import { cn } from '@/lib/utils';
import { Text } from '@/components/ui/text';
// Package removed


interface MacOSTitleBarProps {
    title?: string;
    showAppIcon?: boolean;
    className?: string;
}

export function MacOSTitleBar({
    title = 'SIMANIS62',
    showAppIcon = true,
    className
}: MacOSTitleBarProps) {
    const [isMaximized, setIsMaximized] = useState(false);
    const [isHovered, setIsHovered] = useState(false);
    const [isFocused, setIsFocused] = useState(true);

    useEffect(() => {
        // Safe check for Tauri environment
        let appWindow: any;
        try {
            // Check if running in Tauri
            if (typeof window !== 'undefined' && '__TAURI_INTERNALS__' in window) {
                appWindow = getCurrentWindow();
            }
        } catch (e) {
            console.warn('Tauri window API not available (browser mode)');
        }

        if (!appWindow) return;

        // Listen for window state changes
        const unlistenResize = appWindow.onResized(async () => {
            const maximized = await appWindow.isMaximized();
            setIsMaximized(maximized);
        });

        const unlistenFocus = appWindow.onFocusChanged(({ payload: focused }: any) => {
            setIsFocused(focused);
        });

        // Check initial states
        appWindow.isMaximized().then(setIsMaximized);
        appWindow.isFocused().then(setIsFocused);

        return () => {
            unlistenResize.then((fn: any) => fn());
            unlistenFocus.then((fn: any) => fn());
        };
    }, []);

    const getAppWindow = () => {
        try {
            if (typeof window !== 'undefined' && '__TAURI_INTERNALS__' in window) {
                return getCurrentWindow();
            }
        } catch (e) {
            return null;
        }
        return null;
    };

    const handleClose = () => getAppWindow()?.close();
    const handleMinimize = () => getAppWindow()?.minimize();
    const handleMaximize = () => getAppWindow()?.toggleMaximize();

    return (
        <div
            data-tauri-drag-region
            className={cn(
                // Use new semantic class
                'glass-titlebar',

                // Layout
                'h-[42px] flex items-center justify-between', /* Taller titlebar for modern feel */
                'select-none shrink-0 z-50',

                // Window state
                !isFocused && 'opacity-60 grayscale-[0.5]',

                className
            )}
        >
            {/* Left: Traffic Light Buttons */}
            <div
                className="flex items-center gap-[8px] px-4 h-full"
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
            >
                {/* Close Button (Red) */}
                <WindowControlButton
                    type="close"
                    onClick={handleClose}
                    isFocused={isFocused}
                    isHovered={isHovered}
                />

                {/* Minimize Button (Yellow) */}
                <WindowControlButton
                    type="minimize"
                    onClick={handleMinimize}
                    isFocused={isFocused}
                    isHovered={isHovered}
                />

                {/* Maximize/Fullscreen Button (Green) */}
                <WindowControlButton
                    type="maximize"
                    onClick={handleMaximize}
                    isFocused={isFocused}
                    isHovered={isHovered}
                    isMaximized={isMaximized}
                />
            </div>

            {/* Center: App Title */}
            <div
                data-tauri-drag-region
                className="absolute left-1/2 -translate-x-1/2 flex items-center gap-2"
            >
                {showAppIcon && (
                    <div className="opacity-90 grayscale-[0.2]">
                        {/* Icon placeholder if needed, mostly handled by sidebar now */}
                    </div>
                )}
                <Text
                    variant="caption-1"
                    className={cn(
                        'font-medium tracking-wide text-[13px]',
                        isFocused ? 'text-primary' : 'text-tertiary'
                    )}
                >
                    {title}
                </Text>
            </div>

            {/* Right: Empty space for symmetry or additional controls */}
            <div className="px-4 h-full flex items-center">
                {/* Placeholder for menu or other controls */}
            </div>
        </div>
    );
}

// Helper component for window controls
function WindowControlButton({
    type,
    onClick,
    isFocused,
    isHovered,
    isMaximized
}: {
    type: 'close' | 'minimize' | 'maximize';
    onClick: () => void;
    isFocused: boolean;
    isHovered: boolean;
    isMaximized?: boolean;
}) {
    const colors = {
        close: { bg: '#FF5F57', border: '#E0443E', icon: '#4D0000' },
        minimize: { bg: '#FEBC2E', border: '#D09A22', icon: '#995700' },
        maximize: { bg: '#28C840', border: '#1AAB29', icon: '#006500' },
    };

    const config = colors[type];

    return (
        <button
            onClick={onClick}
            className={cn(
                'w-3 h-3 rounded-full',
                'flex items-center justify-center',
                'transition-all duration-100',
                'border-[0.5px]',
                isFocused
                    ? `bg-[${config.bg}] border-[${config.border}]`
                    : 'bg-[#DFDFDF] border-[#D0D0D0] dark:bg-[#3D3D3D] dark:border-[#4B4B4B]',
            )}
            style={isFocused ? { backgroundColor: config.bg, borderColor: config.border } : undefined}
            aria-label={type}
        >
            {isHovered && isFocused && (
                <div className="opacity-60">
                    {type === 'close' && (
                        <svg width="6" height="6" viewBox="0 0 6 6">
                            <path d="M0.5 0.5L5.5 5.5M5.5 0.5L0.5 5.5" stroke={config.icon} strokeWidth="1.2" strokeLinecap="round" />
                        </svg>
                    )}
                    {type === 'minimize' && (
                        <svg width="8" height="2" viewBox="0 0 8 2">
                            <path d="M1 1H7" stroke={config.icon} strokeWidth="1.2" strokeLinecap="round" />
                        </svg>
                    )}
                    {type === 'maximize' && (
                        <svg width="6" height="6" viewBox="0 0 6 6">
                            {isMaximized ? (
                                <path d="M5.5 0.5L3.5 2.5M0.5 5.5L2.5 3.5M5.5 5.5L3.5 3.5M0.5 0.5L2.5 2.5" stroke={config.icon} strokeWidth="1.2" strokeLinecap="round" />
                            ) : (
                                <path d="M0.5 0.5L2.5 0.5M0.5 0.5L0.5 2.5M5.5 0.5L3.5 0.5M5.5 0.5L5.5 2.5M0.5 5.5L2.5 5.5M0.5 5.5L0.5 3.5M5.5 5.5L3.5 5.5M5.5 5.5L5.5 3.5" stroke={config.icon} strokeWidth="1" strokeLinecap="round" />
                            )}
                        </svg>
                    )}
                </div>
            )}
        </button>
    );
}

/**
 * Compact variant for use in dialogs or secondary windows
 */
export function MacOSTitleBarCompact({
    title,
    onClose
}: {
    title?: string;
    onClose?: () => void;
}) {
    return (
        <div className={cn(
            'h-8 px-3 flex items-center justify-between',
            'bg-white/60 dark:bg-zinc-900/60',
            'backdrop-blur-xl',
            'border-b border-black/5 dark:border-white/5',
            'rounded-t-[14px]'
        )}>
            <button
                onClick={onClose}
                className={cn(
                    'w-3 h-3 rounded-full',
                    'bg-[#FF5F57] hover:bg-[#E5453C]',
                    'transition-colors'
                )}
                aria-label="Close"
            />

            {title && (
                <Text variant="caption-1" color="secondary" className="font-medium">
                    {title}
                </Text>
            )}

            <div className="w-3" /> {/* Spacer for alignment */}
        </div>
    );
}
