/**
 * Glass Input Component - macOS Liquid Glass Style
 */

import { cn } from '@/lib/utils';
import { InputHTMLAttributes, forwardRef } from 'react';

interface GlassInputProps extends InputHTMLAttributes<HTMLInputElement> {
  glass?: boolean;
}

export const GlassInput = forwardRef<HTMLInputElement, GlassInputProps>(
  ({ className, glass = true, type = 'text', ...props }, ref) => {
    return (
      <input
        ref={ref}
        type={type}
        className={cn(
          'w-full h-10 px-3 text-[15px]',
          'rounded-lg',
          'transition-all duration-150',
          glass && [
            'bg-white/70',
            'backdrop-blur-lg',
          ],
          !glass && 'bg-white',
          'border border-black/[0.08]',
          'text-gray-900',
          'placeholder:text-gray-400',
          'focus:outline-none focus:ring-2 focus:ring-[#007AFF]/50 focus:border-[#007AFF]',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          className
        )}
        {...props}
      />
    );
  }
);

GlassInput.displayName = 'GlassInput';
