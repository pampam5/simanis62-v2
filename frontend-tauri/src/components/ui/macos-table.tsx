/**
 * macOS-Style Data Table
 * 
 * Features:
 * - Glass toolbar with search and filters
 * - Sticky header with glass effect
 * - Row hover and selection states
 * - Pagination with glass styling
 * 
 * @see .kiro/steering/design-system.md Section 13.5 PROMPT 3
 */

import { cn } from '@/lib/utils';
import { Text } from '@/components/ui/text';
import { motion } from 'framer-motion';
import {
    Search,
    ChevronLeft,
    ChevronRight,
    ChevronsLeft,
    ChevronsRight,
    ChevronDown,
    Check,
} from 'lucide-react';


/**
 * Table Toolbar with search and actions
 */
interface MacOSTableToolbarProps {
    searchValue?: string;
    onSearchChange?: (value: string) => void;
    searchPlaceholder?: string;
    leftActions?: React.ReactNode;
    rightActions?: React.ReactNode;
    className?: string;
}

export function MacOSTableToolbar({
    searchValue = '',
    onSearchChange,
    searchPlaceholder = 'Search...',
    leftActions,
    rightActions,
    className,
}: MacOSTableToolbarProps) {
    return (
        <div className={cn(
            // Glass effect
            'glass-panel px-4 py-3 rounded-xl mb-4',

            // Remove border definition from here as glass-panel has it, 
            // but maybe adjust opacity if needed
            'border-white/20 dark:border-white/10',

            // Layout
            'flex items-center gap-4 flex-wrap',

            className
        )}>
            {/* Search */}
            <div className="relative flex-1 min-w-[200px] max-w-md">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                    type="text"
                    value={searchValue}
                    onChange={(e) => onSearchChange?.(e.target.value)}
                    placeholder={searchPlaceholder}
                    className={cn(
                        'w-full h-9 pl-9 pr-4 rounded-lg',
                        'text-sm placeholder:text-gray-400',
                        'bg-white/50 dark:bg-zinc-900/50',
                        'border border-black/10 dark:border-white/10',
                        'focus:outline-none focus:ring-2 focus:ring-[#007AFF]/50',
                        'transition-all'
                    )}
                />
            </div>

            {/* Left actions */}
            {leftActions && (
                <div className="flex items-center gap-2">
                    {leftActions}
                </div>
            )}

            {/* Spacer */}
            <div className="flex-1" />

            {/* Right actions */}
            {rightActions && (
                <div className="flex items-center gap-2">
                    {rightActions}
                </div>
            )}
        </div>
    );
}

/**
 * Table container with glass styling
 */
export function MacOSTable({
    children,
    className,
}: {
    children: React.ReactNode;
    className?: string;
}) {
    return (
        <div className={cn(
            // Glass effect
            'glass-panel rounded-xl overflow-hidden',
            // Override standard border if needed, but glass-panel has it
            'shadow-sm dark:shadow-md',

            className
        )}>
            <div className="overflow-x-auto">
                <table className="w-full">
                    {children}
                </table>
            </div>
        </div>
    );
}

/**
 * Table header
 */
export function MacOSTableHeader({
    children,
    className,
}: {
    children: React.ReactNode;
    className?: string;
}) {
    return (
        <thead className={cn(
            // Glass header
            'bg-white/40 dark:bg-zinc-900/40',
            'backdrop-blur-sm',
            'border-b border-black/5 dark:border-white/5',
            'sticky top-0 z-10',

            className
        )}>
            {children}
        </thead>
    );
}

/**
 * Table header cell
 */
interface MacOSTableHeadProps {
    children: React.ReactNode;
    sortable?: boolean;
    sorted?: 'asc' | 'desc' | false;
    onSort?: () => void;
    width?: string | number;
    align?: 'left' | 'center' | 'right';
    className?: string;
}

export function MacOSTableHead({
    children,
    sortable,
    sorted,
    onSort,
    width,
    align = 'left',
    className,
}: MacOSTableHeadProps) {
    const alignClasses = {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right',
    };

    return (
        <th
            onClick={sortable ? onSort : undefined}
            style={{ width }}
            className={cn(
                'px-4 py-3',
                'text-[11px] font-semibold uppercase tracking-wider',
                'text-gray-500 dark:text-gray-400',
                alignClasses[align],
                sortable && 'cursor-pointer hover:text-gray-700 dark:hover:text-gray-200 transition-colors',
                className
            )}
        >
            <div className={cn(
                'flex items-center gap-1',
                align === 'center' && 'justify-center',
                align === 'right' && 'justify-end'
            )}>
                {children}
                {sortable && sorted && (
                    <ChevronDown className={cn(
                        'w-3 h-3',
                        sorted === 'asc' && 'rotate-180'
                    )} />
                )}
            </div>
        </th>
    );
}

/**
 * Table body
 */
export function MacOSTableBody({
    children,
    className,
}: {
    children: React.ReactNode;
    className?: string;
}) {
    return (
        <tbody className={cn('divide-y divide-black/5 dark:divide-white/5', className)}>
            {children}
        </tbody>
    );
}

/**
 * Table row
 */
interface MacOSTableRowProps {
    children: React.ReactNode;
    selected?: boolean;
    onClick?: () => void;
    className?: string;
}

export function MacOSTableRow({
    children,
    selected,
    onClick,
    className,
}: MacOSTableRowProps) {
    return (
        <motion.tr
            whileHover={{ backgroundColor: 'rgba(0, 122, 255, 0.04)' }}
            onClick={onClick}
            className={cn(
                'h-10 transition-colors',
                selected && 'bg-[#007AFF]/8 dark:bg-[#0A84FF]/10',
                onClick && 'cursor-pointer',
                className
            )}
        >
            {children}
        </motion.tr>
    );
}

/**
 * Table cell
 */
interface MacOSTableCellProps {
    children: React.ReactNode;
    align?: 'left' | 'center' | 'right';
    mono?: boolean;
    className?: string;
}

export function MacOSTableCell({
    children,
    align = 'left',
    mono,
    className,
}: MacOSTableCellProps) {
    const alignClasses = {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right',
    };

    return (
        <td className={cn(
            'px-4 py-2',
            'text-[13px]',
            mono && 'font-mono tabular-nums',
            alignClasses[align],
            className
        )}>
            {children}
        </td>
    );
}

/**
 * Table checkbox
 */
export function MacOSTableCheckbox({
    checked,
    onChange,
    indeterminate,
}: {
    checked: boolean;
    onChange: (checked: boolean) => void;
    indeterminate?: boolean;
}) {
    return (
        <button
            onClick={(e) => {
                e.stopPropagation();
                onChange(!checked);
            }}
            className={cn(
                'w-4 h-4 rounded',
                'border transition-all',
                checked || indeterminate
                    ? 'bg-[#007AFF] border-[#007AFF]'
                    : 'bg-white dark:bg-zinc-800 border-gray-300 dark:border-gray-600',
                'flex items-center justify-center'
            )}
        >
            {checked && <Check className="w-3 h-3 text-white" />}
            {indeterminate && <div className="w-2 h-0.5 bg-white rounded" />}
        </button>
    );
}

/**
 * Status badge for table cells
 */
export function MacOSTableBadge({
    children,
    variant = 'default',
}: {
    children: React.ReactNode;
    variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
}) {
    // Apple HIG color values for light and dark modes
    const variants = {
        default: 'bg-[#8E8E93]/15 text-[#636366] dark:bg-[#636366]/20 dark:text-[#8E8E93]',
        success: 'bg-[#34C759]/15 text-[#248A3D] dark:bg-[#30D158]/20 dark:text-[#30D158]',
        warning: 'bg-[#FF9500]/15 text-[#C77800] dark:bg-[#FF9F0A]/20 dark:text-[#FF9F0A]',
        error: 'bg-[#FF3B30]/15 text-[#D70015] dark:bg-[#FF453A]/20 dark:text-[#FF453A]',
        info: 'bg-[#007AFF]/15 text-[#0056B3] dark:bg-[#0A84FF]/20 dark:text-[#0A84FF]',
    };

    return (
        <span className={cn(
            'inline-flex items-center px-2 py-0.5 rounded-full',
            'text-[11px] font-medium',
            variants[variant]
        )}>
            {children}
        </span>
    );
}

/**
 * Table pagination
 */
interface MacOSTablePaginationProps {
    currentPage: number;
    totalPages: number;
    pageSize: number;
    totalItems: number;
    onPageChange: (page: number) => void;
    onPageSizeChange?: (size: number) => void;
    pageSizeOptions?: number[];
    className?: string;
}

export function MacOSTablePagination({
    currentPage,
    totalPages,
    pageSize,
    totalItems,
    onPageChange,
    onPageSizeChange,
    pageSizeOptions = [10, 25, 50, 100],
    className,
}: MacOSTablePaginationProps) {
    const startItem = (currentPage - 1) * pageSize + 1;
    const endItem = Math.min(currentPage * pageSize, totalItems);

    return (
        <div className={cn(
            // Glass effect
            'glass-panel px-4 py-3 rounded-xl mt-4',
            // Default glass-panel style is sufficient


            // Layout
            'flex items-center justify-between flex-wrap gap-4',

            className
        )}>
            {/* Items info */}
            <Text variant="caption-1" color="secondary">
                Showing {startItem}-{endItem} of {totalItems}
            </Text>

            {/* Page size selector */}
            {onPageSizeChange && (
                <div className="flex items-center gap-2">
                    <Text variant="caption-1" color="tertiary">
                        Per page:
                    </Text>
                    <select
                        value={pageSize}
                        onChange={(e) => onPageSizeChange(Number(e.target.value))}
                        className={cn(
                            'h-7 px-2 rounded-md',
                            'text-xs',
                            'bg-white/50 dark:bg-zinc-900/50',
                            'border border-black/10 dark:border-white/10',
                            'focus:outline-none focus:ring-2 focus:ring-[#007AFF]/50'
                        )}
                    >
                        {pageSizeOptions.map((size) => (
                            <option key={size} value={size}>
                                {size}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            {/* Navigation */}
            <div className="flex items-center gap-1">
                <PaginationButton
                    onClick={() => onPageChange(1)}
                    disabled={currentPage === 1}
                >
                    <ChevronsLeft className="w-4 h-4" />
                </PaginationButton>

                <PaginationButton
                    onClick={() => onPageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                >
                    <ChevronLeft className="w-4 h-4" />
                </PaginationButton>

                <div className="px-3">
                    <Text variant="caption-1" color="secondary">
                        Page {currentPage} of {totalPages}
                    </Text>
                </div>

                <PaginationButton
                    onClick={() => onPageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                >
                    <ChevronRight className="w-4 h-4" />
                </PaginationButton>

                <PaginationButton
                    onClick={() => onPageChange(totalPages)}
                    disabled={currentPage === totalPages}
                >
                    <ChevronsRight className="w-4 h-4" />
                </PaginationButton>
            </div>
        </div>
    );
}

function PaginationButton({
    children,
    onClick,
    disabled,
}: {
    children: React.ReactNode;
    onClick: () => void;
    disabled: boolean;
}) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={cn(
                'w-7 h-7 rounded-md',
                'flex items-center justify-center',
                'transition-colors',
                disabled
                    ? 'text-gray-300 dark:text-gray-600 cursor-not-allowed'
                    : 'text-gray-600 dark:text-gray-300 hover:bg-black/5 dark:hover:bg-white/10'
            )}
        >
            {children}
        </button>
    );
}
