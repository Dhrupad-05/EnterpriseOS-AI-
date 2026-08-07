import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Flame, Wifi, ShieldAlert, Building2, Cog, Zap,
  CheckCircle2, Loader2, TrendingDown, Users, FileText, ShieldCheck,
} from "lucide-react"
import { cn } from "@/lib/utils"

const scenarios = [
  { id: "fire", label: "Factory fire", icon: Flame },
  { id: "outage", label: "Internet outage", icon: Wifi },
  { id: "cyber", label: "Cyber attack", icon: ShieldAlert },
  { id: "bankruptcy", label: "Supplier bankruptcy", icon: Building2 },
  { id: "machine", label: "Machine failure", icon: Cog },
  { id: "power", label: "Power outage", icon: Zap },
]

const steps = [
  { id: "impact", label: "Impact analysis", icon: TrendingDown, detail: "Assessing affected lines, orders, and downstream dependencies." },
  { id: "supplier", label: "Alternative supplier", icon: Building2, detail: "Vendor Intelligence scored 3 alternates on lead time and cost." },
  { id: "notify", label: "Notify employees", icon: Users, detail: "Drafted alerts for 34 affected staff across 2 shifts." },
  { id: "plan", label: "Generate action plan", icon: FileText, detail: "Crisis Agent compiled a 4-step recovery workflow." },
  { id: "loss", label: "Estimate business loss", icon: TrendingDown, detail: "Projected exposure: $42,000 if unresolved within 24h." },
  { id: "recovery", label: "Recovery workflow", icon: Cog, detail: "Workflow staged in the Business Event Engine, ready to execute." },
  { id: "approval", label: "Executive approval", icon: ShieldCheck, detail: "Routed to CEO Dashboard — awaiting sign-off to execute." },
]

export default function CrisisCenter() {
  const [active, setActive] = useState<string | null>(null)
  const [stepIndex, setStepIndex] = useState(-1)
  const [running, setRunning] = useState(false)

  function simulate(id: string) {
    setActive(id)
    setStepIndex(-1)
    setRunning(true)
    let i = 0
    const tick = () => {
      setStepIndex(i)
      i++
      if (i < steps.length) setTimeout(tick, 750)
      else setRunning(false)
    }
    setTimeout(tick, 300)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 font-display text-xl font-semibold tracking-tight">
          <Flame className="h-5 w-5 text-crit" /> Crisis Center
        </h1>
        <p className="text-sm text-ink-faint">Simulate a disruption. The Crisis Agent builds a recovery workflow automatically — execution still waits on your approval.</p>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-6">
        {scenarios.map((s) => (
          <button
            key={s.id}
            onClick={() => simulate(s.id)}
            disabled={running}
            className={cn(
              "flex flex-col items-center gap-2.5 rounded-xl border p-4 text-center transition-colors disabled:opacity-50",
              active === s.id ? "border-crit/40 bg-crit-soft" : "border-border bg-surface hover:border-crit/30 hover:bg-surface-hover"
            )}
          >
            <s.icon className={cn("h-5 w-5", active === s.id ? "text-crit" : "text-ink-muted")} />
            <span className="text-xs">{s.label}</span>
          </button>
        ))}
      </div>

      {active && (
        <Card>
          <CardContent className="pt-5">
            <div className="mb-5 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <Badge variant="crit">Simulating</Badge>
                <span className="text-sm text-ink-muted">{scenarios.find((s) => s.id === active)?.label}</span>
              </div>
              {!running && stepIndex === steps.length - 1 && (
                <Button size="sm">Approve recovery workflow</Button>
              )}
            </div>

            <div className="space-y-0">
              {steps.map((step, i) => {
                const state = i < stepIndex ? "done" : i === stepIndex ? "active" : "pending"
                return (
                  <div key={step.id} className="flex gap-4">
                    <div className="flex flex-col items-center">
                      <div className={cn(
                        "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border",
                        state === "done" && "border-good/40 bg-good-soft",
                        state === "active" && "border-signal/40 bg-signal-soft",
                        state === "pending" && "border-border bg-canvas-raised"
                      )}>
                        {state === "done" && <CheckCircle2 className="h-4 w-4 text-good" />}
                        {state === "active" && <Loader2 className="h-4 w-4 animate-spin text-signal-strong" />}
                        {state === "pending" && <step.icon className="h-3.5 w-3.5 text-ink-faint" />}
                      </div>
                      {i < steps.length - 1 && <div className={cn("w-px flex-1 min-h-[28px]", state === "done" ? "bg-good/40" : "bg-border")} />}
                    </div>
                    <div className="pb-6">
                      <p className={cn("text-sm", state === "pending" ? "text-ink-faint" : "text-ink")}>{step.label}</p>
                      <AnimatePresence>
                        {state !== "pending" && (
                          <motion.p
                            initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}
                            className="mt-1 text-xs text-ink-muted"
                          >
                            {step.detail}
                          </motion.p>
                        )}
                      </AnimatePresence>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {!active && (
        <div className="rounded-xl border border-dashed border-border p-12 text-center text-sm text-ink-faint">
          Select a scenario above to run a crisis simulation.
        </div>
      )}
    </div>
  )
}
