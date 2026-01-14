/**
 * Protected Route Component
 * Redirect ke login jika user belum authenticated
 */

import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
    const { isAuthenticated, isLoading } = useAuth();
    const location = useLocation();

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
                <div className="flex flex-col items-center gap-4">
                    <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
                    <p className="text-white/70">Memuat...</p>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) {
        // Redirect ke login, simpan intended location
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return <>{children}</>;
}
