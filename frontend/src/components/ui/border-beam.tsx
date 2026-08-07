import * as React from "react"
import { cn } from "@/lib/utils"

interface BorderBeamProps extends React.HTMLAttributes<HTMLDivElement> {
  active?: boolean
  children: React.ReactNode
}

/**
 * Wraps children in a card that grows an animated light traveling
 * around its border on hover (always-on if `active` is true).
 * Pure CSS conic-gradient — no per-frame JS.
 */
const BorderBeam = React.forwardRef<HTMLDivElement, BorderBeamProps>(
  ({ className, active = false, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn("group relative rounded-xl", active && "border-beam", className)}
        {...props}
      >
        {!active && (
          <div className="border-beam pointer-events-none absolute inset-0 rounded-xl opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
        )}
        {children}
      </div>
    )
  }
)
BorderBeam.displayName = "BorderBeam"

export { BorderBeam }
