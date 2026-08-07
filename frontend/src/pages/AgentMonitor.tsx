import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { agents, type AgentStatus } from "@/data/mockData"
import { Bot, Activity, Zap, Hash, Gauge } from "lucide-react"
import { cn } from "@/lib/utils"

const statusMeta: Record<AgentStatus, { label: string; className: string }> = {
  working: { label: "Working", className: "text-signal-strong bg-signal-soft border-signal/30" },
  completed: { label: "Completed", className: "text-good bg-good-soft border-good/30" },
  waiting: { label: "Waiting", className: "text-warn bg-warn-soft border-warn/30" },
  idle: { label: "Idle", className: "text-ink-faint bg-surface border-border-strong" },
  error: { label: "Error", className: "text-crit bg-crit-soft border-crit/30" },
}

export default function AgentMonitor() {
  const [selected, setSelected] = useState(agents[0])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 font-display text-xl font-semibold tracking-tight">
          <Bot className="h-5 w-5 text-signal-strong" /> Agent Monitor
        </h1>
        <p className="text-sm text-ink-faint">Live view of every agent — prompt, reasoning, confidence, latency, and token usage.</p>
      </div>

      <div className="grid gap-5 lg:grid-cols-5">
        <div className="lg:col-span-3 space-y-2.5">
          {agents.map((a) => (
            <button
              key={a.id}
              onClick={() => setSelected(a)}
              className={cn(
                "w-full rounded-xl border p-4 text-left transition-colors",
                selected.id === a.id ? "border-signal/40 bg-signal-soft/30" : "border-border bg-surface hover:bg-surface-hover"
              )}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium">{a.name}</p>
                  <p className="text-[11px] text-ink-faint">{a.role}</p>
                </div>
                <span className={cn("rounded-full border px-2 py-0.5 font-mono text-[10px] uppercase", statusMeta[a.status].className)}>
                  {statusMeta[a.status].label}
                </span>
              </div>
              <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-canvas-raised">
                <div
                  className={cn("h-full rounded-full transition-all duration-500", a.status === "error" ? "bg-crit" : "bg-signal")}
                  style={{ width: `${a.progress}%` }}
                />
              </div>
              <p className="mt-2.5 truncate text-xs text-ink-muted">{a.lastAction}</p>
            </button>
          ))}
        </div>

        <Card className="lg:col-span-2 h-fit">
          <CardContent className="space-y-5 pt-5">
            <div>
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium">{selected.name}</h3>
                <Badge variant="signal">{selected.role}</Badge>
              </div>
              <p className="mt-2 text-xs text-ink-muted">{selected.lastAction}</p>
            </div>

            <div className="grid grid-cols-3 gap-3 border-t border-border pt-4">
              <div>
                <p className="flex items-center gap-1 font-mono text-[10px] uppercase text-ink-faint"><Gauge className="h-3 w-3" /> Confidence</p>
                <p className="mt-1 font-mono text-sm">{selected.confidence ? `${Math.round(selected.confidence * 100)}%` : "—"}</p>
              </div>
              <div>
                <p className="flex items-center gap-1 font-mono text-[10px] uppercase text-ink-faint"><Zap className="h-3 w-3" /> Latency</p>
                <p className="mt-1 font-mono text-sm">{selected.latencyMs ? `${selected.latencyMs}ms` : "—"}</p>
              </div>
              <div>
                <p className="flex items-center gap-1 font-mono text-[10px] uppercase text-ink-faint"><Hash className="h-3 w-3" /> Tokens</p>
                <p className="mt-1 font-mono text-sm">{selected.tokens || "—"}</p>
              </div>
            </div>

            <div className="border-t border-border pt-4">
              <p className="flex items-center gap-1.5 font-mono text-[10px] uppercase text-ink-faint"><Activity className="h-3 w-3" /> Reasoning summary</p>
              <div className="mt-2 rounded-lg border border-border bg-canvas-raised p-3 font-mono text-xs leading-relaxed text-ink-muted">
                {selected.status === "waiting"
                  ? "Idle — queued behind a dependency. Will resume once the upstream agent reports back."
                  : `Evaluated available context, cross-checked policy constraints, and ${selected.status === "completed" ? "produced a final recommendation for human review." : "is drafting the next step in the workflow."}`}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
