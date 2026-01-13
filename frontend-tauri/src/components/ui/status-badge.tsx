/**
 * StatusBadge - Badge untuk status aset SIMANIS62
 * 
 * Status: Baru, Aktif, Mutasi, Rusak, Dihapus
 * 
 * @see .kiro/steering/design-system.md
 */

import { cn } from '@/lib/utils';

type AssetStatus = 'Baru' | 'Aktif' | 'Mutasi' | 'Rusak' | 'Dihapus';

interface StatusBadgeProps {
    status: AssetStatus;
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

const statusConfig: Record<AssetStatus, { label: string; className: string }> = {
    Baru: {
        label: 'Baru',
        className: 'badge-status-baru',
    },
    Aktif: {
        label: 'Aktif',
        className: 'badge-status-aktif',
    },
    Mutasi: {
        label: 'Mutasi',
        className: 'badge-status-mutasi',
    },
    Rusak: {
        label: 'Rusak',
        className: 'badge-status-rusak',
    },
    Dihapus: {
        label: 'Dihapus',
        className: 'badge-status-dihapus',
    },
};

export function StatusBadge({ status, size = 'md', className }: StatusBadgeProps) {
    const config = statusConfig[status];

    return (
        <span
            className={cn(
                'badge',
                config.className,
                size === 'sm' && 'badge-sm',
                size === 'lg' && 'badge-lg',
                className
            )}
        >
            {config.label}
        </span>
    );
}

export type { AssetStatus };
