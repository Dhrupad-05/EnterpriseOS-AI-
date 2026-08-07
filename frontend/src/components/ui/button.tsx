import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-colors duration-150 focus-visible:outline-none disabled:pointer-events-none disabled:opacity-40",
  {
    variants: {
      variant: {
        default: "bg-signal text-white hover:bg-signal-strong",
        outline: "border border-border-strong bg-transparent text-ink hover:bg-surface-hover",
        ghost: "text-ink-muted hover:text-ink hover:bg-surface-hover",
        destructive: "bg-crit/90 text-white hover:bg-crit",
        subtle: "bg-surface text-ink hover:bg-surface-hover border border-border",
        gradient: "bg-gradient-to-b from-signal-strong via-signal to-signal text-white shadow-[0_1px_0_0_rgba(255,255,255,0.25)_inset] hover:brightness-110 hover:scale-[1.02] active:scale-[0.98]",
      },
      size: {
        default: "h-10 px-4",
        sm: "h-8 px-3 text-xs",
        lg: "h-12 px-6 text-base",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
