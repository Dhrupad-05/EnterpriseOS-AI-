import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { StatusChip, severityColor } from "@/components/ui/status-chip"
import { businessEvents, type EventKind } from "@/data/mockData"
import { ShoppingCart, Boxes, Truck, Flame, MessageCircle, Cog, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"

const kindMeta: Record<EventKind, { icon: typeof Flame; label: string }> = {
  purchase: { icon: ShoppingCart, label: "Purchase" },
  inventory: { icon: Boxes, label: "Inventory" },
  vendor: { icon: Truck, label: "Vendor" },
  incident: { icon: Flame, label: "Incident" },
  complaint: { icon: MessageCircle, label: "Complaint" },
  machine: { icon: Cog, label: "Machine" },
}

const filters: ("all" | EventKind)[] = ["all", "purchase", "inventory", "vendor", "incident", "complaint", "machine"]

export default function OperationsCenter() {
  const [filter, setFilter] = useState<"all" | EventKind>("all")
  const [selected, setSelected] = useState(businessEvents[0])
  const filtered = filter === "all" ? businessEvents : businessEvents.filter((e) => e.kind === filter)

  return (
    <div className="space-y-5">
      <div>
        <h1 className="font-display text-xl font-semibold tracking-tight">Operations Center</h1>
        <p className="text-sm text-ink-faint">Every business event — purchase, inventory, vendor, incident, complaint, machine — in one feed.</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {filters.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={cn(
              "rounded-full border px-3 py-1.5 text-xs capitalize transition-colors",
              filter === f ? "border-signal/40 bg-signal-soft text-signal-strong" : "border-border text-ink-faint hover:text-ink-muted"
            )}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="grid gap-5 lg:grid-cols-5">
        <div className="lg:col-span-3 space-y-2.5">
          {filtered.map((e) => {
            const Icon = kindMeta[e.kind].icon
            return (
              <button
                key={e.id}
                onClick={() => setSelected(e)}
                className={cn(
                  "flex w-full items-center gap-4 rounded-xl border p-4 text-left transition-colors",
                  selected.id === e.id ? "border-signal/40 bg-signal-soft/40" : "border-border bg-surface hover:bg-surface-hover"
                )}
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-canvas-raised">
                  <Icon className={cn("h-4 w-4", severityColor[e.severity])} />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <p className="truncate text-sm">{e.title}</p>
                  </div>
                  <p className="text-[11px] text-ink-faint">{e.id} · {e.owner} · {e.time}</p>
                </div>
                <StatusChip stage={e.stage} />
                <ChevronRight className="h-4 w-4 shrink-0 text-ink-faint" />
              </button>
            )
          })}
        </div>

        <Card className="lg:col-span-2 h-fit">
          <CardContent className="pt-5 space-y-4">
            <div className="flex items-center justify-between">
              <Badge variant="signal">{selected.id}</Badge>
              <StatusChip stage={selected.stage} />
            </div>
            <div>
              <h3 className="text-sm font-medium">{selected.title}</h3>
              <p className="mt-1.5 text-sm text-ink-muted">{selected.summary}</p>
            </div>

            <div className="space-y-2 border-t border-border pt-4">
              <p className="font-mono text-[10px] uppercase tracking-wide text-ink-faint">Timeline</p>
              {["Detected", "Classified", "Agent assigned", "In progress"].map((step, i) => (
                <div key={step} className="flex items-center gap-2.5 text-xs text-ink-muted">
                  <span className={cn("h-1.5 w-1.5 rounded-full", i <= 2 ? "bg-good" : "bg-signal animate-pulse")} />
                  {step}
                </div>
              ))}
            </div>

            <div className="space-y-1.5 border-t border-border pt-4">
              <p className="font-mono text-[10px] uppercase tracking-wide text-ink-faint">AI reasoning</p>
              <p className="text-xs text-ink-muted">Owned by {selected.owner}. Severity assessed as {selected.severity} based on operational impact and affected downstream systems.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
