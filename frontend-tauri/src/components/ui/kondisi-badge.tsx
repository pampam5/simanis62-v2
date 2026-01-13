/**
 * KondisiBadge - Badge untuk kondisi aset SIMANIS62
 * 
 * Kondisi: Baik, Rusak Ringan, Rusak Berat
 * 
 * @see .kiro/steering/design-system.md
 */

import { cn } from '@/lib/utils';

type AssetKondisi = 'Baik' | 'Rusak Ringan' | 'Rusak Berat';

interface KondisiBadgeProps {
    kondisi: AssetKondisi;
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

const kondisiConfig: Record<AssetKondisi, { label: string; className: string }> = {
    'Baik': {
        label: 'Baik',
        className: 'badge-kondisi-baik',
    },
    'Rusak Ringan': {
        label: 'Rusak Ringan',
        className: 'badge-kondisi-rusak-ringan',
    },
    'Rusak Berat': {
        label: 'Rusak Berat',
        className: 'badge-kondisi-rusak-berat',
    },
};

export function KondisiBadge({ kondisi, size = 'md', className }: KondisiBadgeProps) {
    const config = kondisiConfig[kondisi];

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

export type { AssetKondisi };
