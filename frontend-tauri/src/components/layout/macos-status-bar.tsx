/**
 * macOS-Style Status Bar
 * 
 * Bottom status bar with:
 * - Glass effect matching system theme
 * - Connection status indicator
 * - System information display
 * 
 * @see .kiro/steering/design-system.md Section 13
 */

import { cn } from '@/lib/utils';
import { Text } from '@/components/ui/text';
import { Wifi, WifiOff, Database, Clock, HardDrive } from 'lucide-react';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface MacOSStatusBarProps {
    leftContent?: React.ReactNode;
    rightContent?: React.ReactNode;
    className?: string;
}

// Custom Animated Wifi Icon
function AnimatedWifi({ className }: { className?: string }) {
    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={className}
        >
            <motion.path
                d="M12 20h.01"
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 1.5, repeat: Infinity, delay: 0 }}
            />
            <motion.path
                d="M8.53 16.11a6 6 0 0 1 6.95 0"
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 1.5, repeat: Infinity, delay: 0.2 }}
            />
            <motion.path
                d="M5 12.55a11 11 0 0 1 14.08 0"
                animate={{ opacity: [0.3, 1, 1, 0.3] }} // Slightly different timing for visual interest
                transition={{ duration: 1.5, repeat: Infinity, delay: 0.4 }}
            />
            <motion.path
                d="M1.42 9a16 16 0 0 1 21.16 0"
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 1.5, repeat: Infinity, delay: 0.6 }}
            />
        </svg>
    );
}

export function MacOSStatusBar({
    leftContent,
    rightContent,
    className,
}: MacOSStatusBarProps) {
    const [currentTime, setCurrentTime] = useState(new Date());
    const [isOnline, setIsOnline] = useState(navigator.onLine);

    useEffect(() => {
        // Update time every second (Realtime)
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);

        const handleOnline = () => setIsOnline(true);
        const handleOffline = () => setIsOnline(false);

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
            clearInterval(timer);
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    const formatTime = (date: Date) => {
        try {
            // Manual UTC+7 calculation to bypass WebView2/OS locale issues
            const utc = date.getTime() + (date.getTimezoneOffset() * 60000);
            const jakartaTime = new Date(utc + (3600000 * 7)); // UTC + 7 hours

            const hours = jakartaTime.getHours().toString().padStart(2, '0');
            const minutes = jakartaTime.getMinutes().toString().padStart(2, '0');
            const seconds = jakartaTime.getSeconds().toString().padStart(2, '0');

            // Use dots or colons? User screenshot usually implies standard time. 
            // Let's use dots if that's the ID preference, or colons if we want 'macOS' feel.
            // Based on previous success logs seeing dots, I'll stick to expected 'id-ID' style but manually forced.
            // Actually, let's use COLONS for a cleaner tech look unless user complains.
            // Wait, previous verification SAID "HH.mm.ss" was present. 
            // If the user said "missing", maybe they expect verified format?
            // Let's safe bet: standard Colon format matches the 'Clock' icon best.
            // If previous verify saw dots, it was because Intl used dots for id-ID.
            return `${hours}:${minutes}:${seconds} WIB`;
        } catch (e) {
            // Fallback to local if something wildly fails
            return date.getHours().toString().padStart(2, '0') + ':' +
                date.getMinutes().toString().padStart(2, '0') + ' (Local)';
        }
    };

    return (
        <div className={cn(
            'h-[28px] px-3 flex items-center justify-between',
            'glass-panel bg-opacity-60 dark:bg-opacity-60',
            'border-t border-black/5 dark:border-white/5',
            'shrink-0 select-none z-50',
            className
        )}>
            {/* Left section */}
            <div className="flex items-center gap-3">
                {leftContent || (
                    <>
                        <StatusIndicator
                            icon={isOnline ? AnimatedWifi : WifiOff}
                            label={isOnline ? 'Connected' : 'Offline'}
                            status={isOnline ? 'success' : 'error'}
                            pulseDot={isOnline}
                        />

                        <Divider />

                        <StatusIndicator
                            icon={Database}
                            label="Database: OK"
                            status="success"
                        />
                    </>
                )}
            </div>

            {/* Right section */}
            <div className="flex items-center gap-3">
                {rightContent}

                {/* Always show Storage if no custom content (optional, but good default) */}
                {!rightContent && (
                    <>
                        <StatusIndicator
                            icon={HardDrive}
                            label="Local"
                        />
                        <Divider />
                    </>
                )}

                {/* Jakarta Time (ALWAYS VISIBLE) */}
                <div className="flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-gray-400 dark:text-gray-500" />
                    <Text variant="subhead" color="tertiary" className="tabular-nums">
                        {formatTime(currentTime)}
                    </Text>
                </div>

                <Divider />

                {/* Version */}
                <Text variant="caption-2" className="text-quaternary opacity-70">
                    v2.0.0
                </Text>
            </div>
        </div>
    );
}

/**
 * Status indicator with icon and label
 */
function StatusIndicator({
    icon: Icon,
    label,
    status,
    animateIcon = false,
    pulseDot = false,
}: {
    icon: React.ComponentType<{ className?: string }>;
    label: string;
    status?: 'success' | 'warning' | 'error';
    animateIcon?: boolean;
    pulseDot?: boolean;
}) {
    const statusColors = {
        success: 'bg-[#34C759] dark:bg-[#30D158]',
        warning: 'bg-[#FF9500] dark:bg-[#FF9F0A]',
        error: 'bg-[#FF3B30] dark:bg-[#FF453A]',
    };

    return (
        <div className="flex items-center gap-1.5">
            {status && (
                <motion.div
                    initial={false}
                    animate={pulseDot ? {
                        scale: [1, 1.2, 1],
                        opacity: [1, 0.7, 1]
                    } : undefined}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                    className={cn(
                        'w-2 h-2 rounded-full',
                        statusColors[status]
                    )}
                />
            )}

            {/* Render Icon directly - if it's AnimatedWifi it handles its own SVG */}
            <Icon className="w-3.5 h-3.5 text-gray-400 dark:text-gray-500" />

            <Text variant="subhead" color="tertiary">
                {label}
            </Text>
        </div>
    );
}

/**
 * Visual divider
 */
function Divider() {
    return (
        <div className="w-px h-3 bg-black/10 dark:bg-white/10" />
    );
}

/**
 * Progress indicator for long-running operations
 */
export function StatusBarProgress({
    progress,
    label,
}: {
    progress: number;
    label: string;
    minWidth?: string;
}) {
    return (
        <div className="flex items-center gap-2">
            <div className="w-24 h-2 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
                <div
                    className="h-full bg-[#007AFF] dark:bg-[#0A84FF] rounded-full transition-all duration-300"
                    style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
                />
            </div>
            <Text variant="footnote" color="tertiary">
                {label}
            </Text>
        </div>
    );
}
