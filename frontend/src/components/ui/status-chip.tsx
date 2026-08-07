import { cn } from "@/lib/utils"
import type { EventStage } from "@/data/mockData"

const stageMeta: Record<EventStage, { label: string; className: string }> = {
  pending: { label: "Pending", className: "text-ink-faint bg-surface border-border-strong" },
  planning: { label: "Planning", className: "text-violet bg-violet/10 border-violet/30" },
  approval: { label: "Approval", className: "text-warn bg-warn-soft border-warn/30" },
  executing: { label: "Executing", className: "text-signal-strong bg-signal-soft border-signal/30" },
  completed: { label: "Completed", className: "text-good bg-good-soft border-good/30" },
  archived: { label: "Archived", className: "text-ink-faint bg-transparent border-border" },
}

export function StatusChip({ stage }: { stage: EventStage }) {
  const meta = stageMeta[stage]
  return (
    <span className={cn("inline-flex items-center rounded-full border px-2 py-0.5 font-mono text-[10px] uppercase tracking-wide", meta.className)}>
      {meta.label}
    </span>
  )
}

export const severityColor: Record<string, string> = {
  low: "text-ink-faint",
  medium: "text-warn",
  high: "text-crit",
  critical: "text-crit",
}
