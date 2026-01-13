/**
 * Text Component - macOS Liquid Glass Style
 * Typography component dengan Apple HIG text styles
 * Updated: Font sizes increased to medium for better readability
 */

import { cn } from '@/lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';
import { HTMLAttributes } from 'react';

const textVariants = cva('', {
  variants: {
    variant: {
      // Titles - Increased sizes
      'large-title': 'text-[32px] font-bold leading-tight tracking-[-0.021em]',
      '3xl': 'text-[32px] font-bold leading-tight tracking-[-0.021em]',
      'title-1': 'text-[28px] font-light leading-tight tracking-[-0.019em]',
      'title-2': 'text-[24px] font-normal leading-snug tracking-[-0.017em]',
      'title-3': 'text-[20px] font-normal leading-snug tracking-[-0.014em]',

      // Body - Increased sizes
      'headline': 'text-[17px] font-semibold leading-normal tracking-[-0.016em]',
      'body': 'text-[16px] font-normal leading-normal tracking-[-0.006em]',
      'callout': 'text-[16px] font-normal leading-normal tracking-[-0.006em]',
      'subhead': 'text-[15px] font-normal leading-normal tracking-normal',

      // Small - Increased sizes
      'footnote': 'text-[14px] font-normal leading-relaxed tracking-normal',
      'caption-1': 'text-[13px] font-normal leading-loose tracking-wide',
      'caption-2': 'text-[12px] font-normal leading-loose tracking-wide',
    },
    color: {
      'primary': 'text-gray-900',
      'secondary': 'text-gray-600',
      'tertiary': 'text-gray-500',
      'quaternary': 'text-gray-400',
      'accent': 'text-[#007AFF]',
      'success': 'text-[#34C759]',
      'warning': 'text-[#FF9500]',
      'danger': 'text-[#FF3B30]',
    },
  },
  defaultVariants: {
    variant: 'body',
    color: 'primary',
  },
});

interface TextProps
  extends Omit<HTMLAttributes<HTMLElement>, 'color'>,
  VariantProps<typeof textVariants> {
  as?: 'p' | 'span' | 'div' | 'label' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
}

export function Text({
  className,
  variant,
  color,
  as: Component = 'p',
  ...props
}: TextProps) {
  return (
    <Component
      className={cn(textVariants({ variant, color }), className)}
      {...props}
    />
  );
}
