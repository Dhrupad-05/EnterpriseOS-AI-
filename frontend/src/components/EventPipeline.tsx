import { motion } from "framer-motion"
import { cn } from "@/lib/utils"

const stages = ["Event", "Classify", "Plan", "Approve", "Execute", "Audit"]

export function EventPipeline({ compact = false }: { compact?: boolean }) {
  return (
    <div className={cn("flex items-center", compact ? "gap-1" : "gap-2 md:gap-3")}>
      {stages.map((s, i) => (
        <div key={s} className="flex items-center">
          <div className="flex flex-col items-center gap-2">
            <motion.div
              initial={{ opacity: 0.3, scale: 0.9 }}
              animate={{ opacity: [0.5, 1, 0.5], scale: [0.96, 1.04, 0.96] }}
              transition={{ duration: 2.4, repeat: Infinity, delay: i * 0.35, ease: "easeInOut" }}
              className={cn(
                "flex items-center justify-center rounded-lg border font-mono uppercase tracking-wide",
                compact ? "h-8 px-2 text-[9px]" : "h-11 px-3.5 text-[11px]",
                "border-signal/30 bg-signal-soft text-signal-strong"
              )}
            >
              {s}
            </motion.div>
          </div>
          {i < stages.length - 1 && (
            <motion.div
              initial={{ opacity: 0.2 }}
              animate={{ opacity: [0.2, 0.8, 0.2] }}
              transition={{ duration: 2.4, repeat: Infinity, delay: i * 0.35, ease: "easeInOut" }}
              className={cn("bg-gradient-to-r from-signal/60 to-signal/10", compact ? "h-px w-3" : "h-px w-5 md:w-8")}
            />
          )}
        </div>
      ))}
    </div>
  )
}
