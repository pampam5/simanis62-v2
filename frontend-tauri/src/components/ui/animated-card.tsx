import { motion, HTMLMotionProps } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AnimatedCardProps extends HTMLMotionProps<'div'> {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  hover?: boolean;
}

export function AnimatedCard({
  children,
  className,
  delay = 0,
  hover = true,
  ...props
}: AnimatedCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.4,
        delay,
        ease: [0.25, 0.1, 0.25, 1] // Custom easing
      }}
      whileHover={hover ? {
        y: -4,
        transition: { duration: 0.2 }
      } : undefined}
      className={cn(
        // Glass effect - Light mode optimized
        "bg-white/80",
        "backdrop-blur-xl backdrop-saturate-[180%]",
        "border border-black/[0.06]",
        "rounded-2xl",

        // Shadow
        "shadow-[0_4px_24px_rgba(0,0,0,0.06)]",

        // Transition
        "transition-shadow duration-200",
        hover && "hover:shadow-[0_8px_40px_rgba(0,0,0,0.1)]",

        className
      )}
      {...props}
    >
      {/* Inner highlight */}
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/80 to-transparent rounded-t-2xl" />

      {children}
    </motion.div>
  );
}
