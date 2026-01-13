/**
 * macOS-Style Dashboard Cards
 * 
 * Features:
 * - Frosted glass effect with vibrancy
 * - Colored icon circles with gradients
 * - Trend indicators with arrows
 * - Hover lift effect
 * 
 * @see .kiro/steering/design-system.md Section 13.5 PROMPT 4
 */

import { cn } from '@/lib/utils';
import { Text } from '@/components/ui/text';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, type LucideIcon } from 'lucide-react';

interface MacOSStatCardProps {
    label: string;
    value: string | number;
    icon: LucideIcon;
    iconColor?: string;
    iconBgColor?: string;
    trend?: {
        value: number;
        label?: string;
    };
    onClick?: () => void;
    className?: string;
    delay?: number;
}

export function MacOSStatCard({
    label,
    value,
    icon: Icon,
    iconColor = 'text-[#007AFF]',
    iconBgColor = 'bg-[#007AFF]/10',
    trend,
    onClick,
    className,
    delay = 0,
}: MacOSStatCardProps) {
    const isPositiveTrend = trend && trend.value >= 0;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay, ease: [0.4, 0, 0.2, 1] }}
            whileHover={{ y: -2, transition: { duration: 0.2 } }}
            onClick={onClick}
            className={cn(
                // Glass effect
                'relative p-5 rounded-2xl',
                'bg-white/60 dark:bg-zinc-800/60',
                'backdrop-blur-xl backdrop-saturate-[180%]',
                'border border-white/20 dark:border-white/6',

                // Shadow
                'shadow-[0_4px_24px_rgba(0,0,0,0.06)]',
                'dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)]',

                // Hover
                'transition-shadow duration-200',
                'hover:shadow-[0_8px_40px_rgba(0,0,0,0.12)]',
                'dark:hover:shadow-[0_8px_40px_rgba(0,0,0,0.3)]',

                onClick && 'cursor-pointer',

                className
            )}
        >
            {/* Inner highlight */}
            <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/60 dark:via-white/10 to-transparent rounded-t-2xl" />

            <div className="flex items-start justify-between">
                {/* Icon */}
                <div className={cn(
                    'w-10 h-10 rounded-xl',
                    'flex items-center justify-center',
                    iconBgColor
                )}>
                    <Icon className={cn('w-5 h-5', iconColor)} />
                </div>

                {/* Trend indicator - Apple HIG colors */}
                {trend && (
                    <div className={cn(
                        'flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium',
                        isPositiveTrend
                            ? 'bg-[#34C759]/10 text-[#248A3D] dark:bg-[#30D158]/15 dark:text-[#30D158]'
                            : 'bg-[#FF3B30]/10 text-[#D70015] dark:bg-[#FF453A]/15 dark:text-[#FF453A]'
                    )}>
                        {isPositiveTrend ? (
                            <TrendingUp className="w-3 h-3" />
                        ) : (
                            <TrendingDown className="w-3 h-3" />
                        )}
                        <span>{Math.abs(trend.value)}%</span>
                    </div>
                )}
            </div>

            {/* Content */}
            <div className="mt-4">
                <Text variant="caption-1" color="tertiary" className="uppercase tracking-wider">
                    {label}
                </Text>
                <Text variant="3xl" className="font-bold mt-1 tabular-nums">
                    {value}
                </Text>
                {trend?.label && (
                    <Text variant="caption-1" color="tertiary" className="mt-1">
                        {trend.label}
                    </Text>
                )}
            </div>
        </motion.div>
    );
}

/**
 * Stats grid container
 */
export function MacOSStatsGrid({
    children,
    columns = 4,
    className,
}: {
    children: React.ReactNode;
    columns?: 2 | 3 | 4;
    className?: string;
}) {
    const gridCols = {
        2: 'grid-cols-1 sm:grid-cols-2',
        3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
        4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
    };

    return (
        <div className={cn(
            'grid gap-4',
            gridCols[columns],
            className
        )}>
            {children}
        </div>
    );
}

/**
 * Section card for grouping content
 */
export function MacOSSectionCard({
    title,
    subtitle,
    action,
    children,
    className,
    delay = 0,
}: {
    title: string;
    subtitle?: string;
    action?: React.ReactNode;
    children: React.ReactNode;
    className?: string;
    delay?: number;
}) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay, ease: [0.4, 0, 0.2, 1] }}
            className={cn(
                // Glass effect
                'relative p-6 rounded-2xl',
                'bg-white/60 dark:bg-zinc-800/60',
                'backdrop-blur-xl backdrop-saturate-[180%]',
                'border border-white/20 dark:border-white/6',

                // Shadow
                'shadow-[0_4px_24px_rgba(0,0,0,0.06)]',
                'dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)]',

                className
            )}
        >
            {/* Inner highlight */}
            <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/60 dark:via-white/10 to-transparent rounded-t-2xl" />

            {/* Header */}
            <div className="flex items-center justify-between mb-5">
                <div>
                    <Text variant="title-2" as="h2" className="font-semibold">
                        {title}
                    </Text>
                    {subtitle && (
                        <Text variant="body" color="secondary" className="mt-0.5">
                            {subtitle}
                        </Text>
                    )}
                </div>
                {action}
            </div>

            {/* Content */}
            {children}
        </motion.div>
    );
}

/**
 * Activity list item
 */
export function MacOSActivityItem({
    avatar,
    title,
    description,
    time,
    onClick,
}: {
    avatar?: React.ReactNode;
    title: string;
    description?: string;
    time: string;
    onClick?: () => void;
}) {
    return (
        <motion.div
            whileHover={{ backgroundColor: 'rgba(0, 0, 0, 0.02)' }}
            onClick={onClick}
            className={cn(
                'flex items-center gap-3 p-3 -mx-3 rounded-lg',
                'transition-colors',
                onClick && 'cursor-pointer'
            )}
        >
            {/* Avatar */}
            {avatar || (
                <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#007AFF]/20 to-[#5856D6]/20 flex items-center justify-center shrink-0">
                    <span className="text-sm font-medium text-[#007AFF]">
                        {title.charAt(0).toUpperCase()}
                    </span>
                </div>
            )}

            {/* Content */}
            <div className="flex-1 min-w-0">
                <Text variant="body" className="truncate">
                    {title}
                </Text>
                {description && (
                    <Text variant="caption-1" color="tertiary" className="truncate">
                        {description}
                    </Text>
                )}
            </div>

            {/* Time */}
            <Text variant="caption-1" color="quaternary" className="shrink-0">
                {time}
            </Text>
        </motion.div>
    );
}
