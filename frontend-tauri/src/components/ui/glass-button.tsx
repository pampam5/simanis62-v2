/**
 * Glass Button Component - macOS Liquid Glass Style
 * Button dengan glassmorphism effect
 */

import { cn } from '@/lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';
import { ButtonHTMLAttributes, forwardRef } from 'react';

const glassButtonVariants = cva(
  'inline-flex items-center justify-center gap-2 font-medium transition-all duration-200 ease-out focus:outline-none focus:ring-2 focus:ring-[#007AFF]/50 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        primary: [
          'bg-[#007AFF] text-white',
          'hover:bg-[#007AFF]/90',
          'active:bg-[#007AFF]/80',
          'shadow-sm hover:shadow-md',
        ],
        secondary: [
          'bg-white/70',
          'backdrop-blur-lg',
          'border border-black/[0.08]',
          'text-gray-900',
          'hover:bg-white/90',
          'active:bg-white',
        ],
        ghost: [
          'bg-transparent',
          'text-gray-600',
          'hover:bg-black/[0.04]',
          'active:bg-black/[0.08]',
        ],
        danger: [
          'bg-[#FF3B30] text-white',
          'hover:bg-[#FF3B30]/90',
          'active:bg-[#FF3B30]/80',
          'shadow-sm hover:shadow-md',
        ],
      },
      size: {
        sm: 'h-9 px-3 text-[13px] rounded-lg',
        md: 'h-10 px-4 text-[14px] rounded-[10px]',
        lg: 'h-12 px-6 text-[16px] rounded-xl',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface GlassButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof glassButtonVariants> { }

export const GlassButton = forwardRef<HTMLButtonElement, GlassButtonProps>(
  ({ className, variant, size, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(glassButtonVariants({ variant, size }), className)}
        {...props}
      >
        {children}
      </button>
    );
  }
);

GlassButton.displayName = 'GlassButton';
