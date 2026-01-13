/**
 * Glass Card Component - macOS Liquid Glass Style
 * Card dengan glassmorphism effect dan hover animation
 */

import { cn } from '@/lib/utils';
import { HTMLAttributes, forwardRef } from 'react';

interface GlassCardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  glass?: boolean;
}

export const GlassCard = forwardRef<HTMLDivElement, GlassCardProps>(
  ({ className, hover = true, glass = true, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'relative rounded-2xl',
          glass && [
            // Glass effect - Light mode optimized
            'bg-white/80',
            'backdrop-blur-xl backdrop-saturate-[180%]',
            'border border-black/[0.06]',
            // Shadow
            'shadow-[0_4px_24px_rgba(0,0,0,0.06)]',
          ],
          !glass && 'bg-white border border-gray-200',
          // Hover effect
          hover && [
            'transition-all duration-200 ease-out',
            'hover:bg-white/90',
            'hover:shadow-[0_8px_40px_rgba(0,0,0,0.1)]',
            'hover:-translate-y-0.5',
          ],
          className
        )}
        {...props}
      >
        {/* Inner highlight */}
        {glass && (
          <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/80 to-transparent rounded-t-2xl" />
        )}

        {children}
      </div>
    );
  }
);

GlassCard.displayName = 'GlassCard';
