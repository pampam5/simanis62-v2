/**
 * macOS-Style Glass Modal Dialog
 * 
 * Features:
 * - Frosted glass background with strong vibrancy
 * - Centered title with subtle styling
 * - Proper backdrop blur overlay
 * - Smooth scale/fade animations
 * 
 * @see .kiro/steering/design-system.md Section 13.4
 */

import { cn } from '@/lib/utils';
import { Text } from '@/components/ui/text';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { useEffect, useCallback } from 'react';

interface MacOSModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    title?: string;
    description?: string;
    children: React.ReactNode;
    size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
    showCloseButton?: boolean;
    className?: string;
}

const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-[calc(100vw-4rem)] max-h-[calc(100vh-4rem)]',
};

export function MacOSModal({
    open,
    onOpenChange,
    title,
    description,
    children,
    size = 'md',
    showCloseButton = true,
    className,
}: MacOSModalProps) {
    // Handle escape key
    const handleEscape = useCallback((e: KeyboardEvent) => {
        if (e.key === 'Escape') {
            onOpenChange(false);
        }
    }, [onOpenChange]);

    useEffect(() => {
        if (open) {
            document.addEventListener('keydown', handleEscape);
            document.body.style.overflow = 'hidden';
        }
        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = '';
        };
    }, [open, handleEscape]);

    return (
        <AnimatePresence>
            {open && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        onClick={() => onOpenChange(false)}
                        className="absolute inset-0 bg-black/20 backdrop-blur-sm"
                    />

                    {/* Modal */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: 10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: 10 }}
                        transition={{
                            duration: 0.2,
                            ease: [0.4, 0, 0.2, 1]
                        }}
                        className={cn(
                            // Glass effect
                            'glass-modal relative w-full',
                            // Default glass-modal has border and background

                            // Specific rounded corner for modals
                            'rounded-[14px]',

                            // Shadow (stronger for modals)
                            'shadow-2xl dark:shadow-[0_24px_80px_rgba(0,0,0,0.5)]',

                            // Size
                            sizeClasses[size],

                            className
                        )}
                    >
                        {/* Inner highlight */}
                        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/80 dark:via-white/20 to-transparent rounded-t-[14px]" />

                        {/* Header */}
                        {(title || showCloseButton) && (
                            <div className={cn(
                                'flex items-center justify-between',
                                'px-6 pt-5 pb-0'
                            )}>
                                <div className="flex-1">
                                    {title && (
                                        <Text variant="title-2" as="h2" className="font-semibold">
                                            {title}
                                        </Text>
                                    )}
                                    {description && (
                                        <Text variant="body" color="secondary" className="mt-1">
                                            {description}
                                        </Text>
                                    )}
                                </div>

                                {showCloseButton && (
                                    <motion.button
                                        whileHover={{ scale: 1.1 }}
                                        whileTap={{ scale: 0.9 }}
                                        onClick={() => onOpenChange(false)}
                                        className={cn(
                                            'w-7 h-7 rounded-full',
                                            'flex items-center justify-center',
                                            'bg-black/5 dark:bg-white/10',
                                            'hover:bg-black/10 dark:hover:bg-white/20',
                                            'transition-colors'
                                        )}
                                        aria-label="Close"
                                    >
                                        <X className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                                    </motion.button>
                                )}
                            </div>
                        )}

                        {/* Content */}
                        <div className="p-6">
                            {children}
                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
}

/**
 * Modal footer with action buttons
 */
export function MacOSModalFooter({
    children,
    className,
}: {
    children: React.ReactNode;
    className?: string;
}) {
    return (
        <div className={cn(
            'flex items-center justify-end gap-3',
            'pt-4 mt-4',
            'border-t border-black/5 dark:border-white/5',
            className
        )}>
            {children}
        </div>
    );
}

/**
 * Alert dialog variant - used for confirmations
 */
export function MacOSAlert({
    open,
    onOpenChange,
    title,
    message,
    confirmLabel = 'OK',
    cancelLabel = 'Cancel',
    onConfirm,
    destructive = false,
}: {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    title: string;
    message: string;
    confirmLabel?: string;
    cancelLabel?: string;
    onConfirm: () => void;
    destructive?: boolean;
}) {
    return (
        <MacOSModal
            open={open}
            onOpenChange={onOpenChange}
            size="sm"
            showCloseButton={false}
        >
            <div className="text-center">
                <Text variant="headline" as="h2" className="font-semibold mb-2">
                    {title}
                </Text>
                <Text variant="body" color="secondary">
                    {message}
                </Text>
            </div>

            <MacOSModalFooter className="justify-center">
                <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => onOpenChange(false)}
                    className={cn(
                        'px-4 py-2 rounded-lg',
                        'text-sm font-medium',
                        'bg-black/5 dark:bg-white/10',
                        'hover:bg-black/10 dark:hover:bg-white/20',
                        'transition-colors'
                    )}
                >
                    {cancelLabel}
                </motion.button>

                <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => {
                        onConfirm();
                        onOpenChange(false);
                    }}
                    className={cn(
                        'px-4 py-2 rounded-lg',
                        'text-sm font-medium text-white',
                        destructive
                            ? 'bg-[#FF3B30] hover:bg-[#E5352B]'
                            : 'bg-[#007AFF] hover:bg-[#006ADF]',
                        'transition-colors'
                    )}
                >
                    {confirmLabel}
                </motion.button>
            </MacOSModalFooter>
        </MacOSModal>
    );
}
