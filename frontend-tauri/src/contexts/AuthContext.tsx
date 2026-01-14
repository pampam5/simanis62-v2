/**
 * Authentication Context untuk SIMANIS62 V2
 * Mengelola state login, user info, dan session
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '@/services/api';

interface User {
    id: string;
    username: string;
    nama_lengkap: string;
    role: string;
    dapat_ekspor: boolean;
    status: string;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (username: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Check auth status on mount
    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            setIsLoading(true);
            const response = await api.get<{ success: boolean; data: User }>('/auth/me');
            if (response.success && response.data) {
                setUser(response.data);
            }
        } catch {
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (username: string, password: string) => {
        const response = await api.post<{ success: boolean; data: User; message: string }>(
            '/auth/login',
            { username, password }
        );
        if (response.success && response.data) {
            setUser(response.data);
        } else {
            throw new Error('Login gagal');
        }
    };

    const logout = async () => {
        try {
            await api.post('/auth/logout');
        } finally {
            setUser(null);
        }
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated: !!user,
                isLoading,
                login,
                logout,
                checkAuth,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
