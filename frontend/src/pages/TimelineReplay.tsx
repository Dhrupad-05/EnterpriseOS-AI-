import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { History, Bot, ShieldCheck, Play, Zap, CheckCircle2 } from "lucide-react"
import { cn } from "@/lib/utils"

const replaySteps = [
  { icon: Zap, label: "Incident detected", detail: "CE-1042 — power outage, Chennai fabrication unit", time: "04:12:03" },
  { icon: Bot, label: "Crisis Agent engaged", detail: "Impact analysis started, alternate suppliers queried", time: "04:12:11" },
  { icon: ShieldCheck, label: "Approval requested", detail: "Overtime authorization routed to Operations Manager", time: "04:14:52" },
  { icon: CheckCircle2, label: "Approved", detail: "Approved by J. Rao, Operations Manager", time: "04:16:30" },
  { icon: CheckCircle2, label: "Executing recovery", detail: "Backup generators engaged, recovery crew dispatched", time: "04:17:05" },
]

export default function TimelineReplay() {
  const [step, setStep] = useState(0)
  const [playing, setPlaying] = useState(false)

  function play() {
    setPlaying(true)
    setStep(0)
    let i = 0
    const tick = () => {
      i++
      setStep(i)
      if (i < replaySteps.length - 1) setTimeout(tick, 900)
      else setPlaying(false)
    }
    setTimeout(tick, 500)
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="flex items-center gap-2 font-display text-xl font-semibold tracking-tight">
            <History className="h-5 w-5 text-signal-strong" /> Timeline Replay
          </h1>
          <p className="text-sm text-ink-faint">Replay any incident like git history — event, agent, approval, execution, completed.</p>
        </div>
        <Button size="sm" onClick={play} disabled={playing}><Play className="h-3.5 w-3.5" /> Replay CE-1042</Button>
      </div>

      <Card>
        <CardContent className="pt-5">
          <div className="space-y-0">
            {replaySteps.map((s, i) => {
              const active = i <= step
              return (
                <div key={i} className="flex gap-4">
                  <div className="flex flex-col items-center">
                    <div className={cn("flex h-8 w-8 shrink-0 items-center justify-center rounded-full border transition-colors", active ? "border-signal/40 bg-signal-soft" : "border-border bg-canvas-raised")}>
                      <s.icon className={cn("h-4 w-4", active ? "text-signal-strong" : "text-ink-faint")} />
                    </div>
                    {i < replaySteps.length - 1 && <div className={cn("w-px flex-1 min-h-[32px] transition-colors", active ? "bg-signal/30" : "bg-border")} />}
                  </div>
                  <div className="pb-7">
                    <div className="flex items-center gap-2.5">
                      <p className={cn("text-sm", active ? "text-ink" : "text-ink-faint")}>{s.label}</p>
                      <span className="font-mono text-[10px] text-ink-faint">{s.time}</span>
                    </div>
                    <p className="mt-0.5 text-xs text-ink-muted">{s.detail}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
