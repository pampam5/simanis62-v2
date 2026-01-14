/**
 * Custom hook untuk fetch data dashboard dari backend
 */

import { useState, useEffect, useCallback } from 'react';
import { asetService } from '@/services/aset-service';
import type { AsetStats, RecentAset } from '@/services/types';

interface DashboardData {
    stats: AsetStats | null;
    recentAssets: RecentAset[];
    isLoading: boolean;
    error: string | null;
    refetch: () => Promise<void>;
}

export function useDashboardData(): DashboardData {
    const [stats, setStats] = useState<AsetStats | null>(null);
    const [recentAssets, setRecentAssets] = useState<RecentAset[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        setError(null);

        try {
            // Fetch stats dan recent assets secara parallel
            const [statsResult, recentResult] = await Promise.all([
                asetService.getStats(),
                asetService.getRecent(5),
            ]);

            setStats(statsResult);
            setRecentAssets(recentResult);
        } catch (err) {
            const message = err instanceof Error ? err.message : 'Gagal memuat data dashboard';
            setError(message);
            console.error('Dashboard fetch error:', err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    return {
        stats,
        recentAssets,
        isLoading,
        error,
        refetch: fetchData,
    };
}
