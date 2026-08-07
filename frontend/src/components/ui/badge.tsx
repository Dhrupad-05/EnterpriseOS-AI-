import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-[11px] font-mono font-medium tracking-wide uppercase",
  {
    variants: {
      variant: {
        default: "border-border-strong text-ink-muted bg-surface",
        signal: "border-signal/30 text-signal-strong bg-signal-soft",
        good: "border-good/30 text-good bg-good-soft",
        warn: "border-warn/30 text-warn bg-warn-soft",
        crit: "border-crit/30 text-crit bg-crit-soft",
        violet: "border-violet/30 text-violet bg-violet/10",
      },
    },
    defaultVariants: { variant: "default" },
  }
)

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
