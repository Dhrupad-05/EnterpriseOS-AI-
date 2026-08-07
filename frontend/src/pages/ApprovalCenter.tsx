import { useState } from "react"
import { motion } from "framer-motion"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useToast } from "@/components/ui/toast"
import { approvals as initialApprovals, type Approval } from "@/data/mockData"
import { Check, X, MessageSquare, ShieldCheck } from "lucide-react"
import { cn } from "@/lib/utils"

const riskVariant: Record<Approval["risk"], "crit" | "warn" | "default"> = { high: "crit", medium: "warn", low: "default" }

export default function ApprovalCenter() {
  const [items] = useState(initialApprovals)
  const [decided, setDecided] = useState<Record<string, "approved" | "rejected">>({})
  const { toast } = useToast()

  function decide(id: string, title: string, action: "approved" | "rejected") {
    setDecided((d) => ({ ...d, [id]: action }))
    toast({
      title: action === "approved" ? "Action approved" : "Action rejected",
      description: title,
      variant: action === "approved" ? "success" : "error",
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 font-display text-xl font-semibold tracking-tight">
          <ShieldCheck className="h-5 w-5 text-warn" /> Approval Center
        </h1>
        <p className="text-sm text-ink-faint">Every consequential AI action stops here. Approve, reject, modify, or comment.</p>
      </div>

      <div className="space-y-4">
        {items.map((a, i) => {
          const decision = decided[a.id]
          return (
            <motion.div
              key={a.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, delay: i * 0.04 }}
            >
              <Card className={cn(decision === "approved" && "border-good/30", decision === "rejected" && "border-crit/30 opacity-60")}>
                <CardContent className="pt-5">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <Badge variant="default">{a.id}</Badge>
                        <Badge variant={riskVariant[a.risk]}>{a.risk} risk</Badge>
                        {decision && (
                          <motion.span initial={{ scale: 0.6, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
                            <Badge variant={decision === "approved" ? "good" : "crit"}>{decision}</Badge>
                          </motion.span>
                        )}
                      </div>
                      <h3 className="mt-2 text-sm font-medium">{a.title}</h3>
                      <p className="mt-0.5 text-xs text-ink-faint">{a.agent} · linked to {a.requestedFor} · {a.time}</p>
                    </div>
                    {a.amount && <span className="font-mono text-lg font-semibold text-ink">{a.amount}</span>}
                  </div>

                  <div className="mt-4 rounded-lg border border-border bg-canvas-raised p-3.5">
                    <p className="font-mono text-[10px] uppercase tracking-wide text-ink-faint">AI reasoning</p>
                    <p className="mt-1 text-sm text-ink-muted">{a.reasoning}</p>
                  </div>

                  {!decision && (
                    <div className="mt-4 flex flex-wrap gap-2">
                      <Button size="sm" onClick={() => decide(a.id, a.title, "approved")}>
                        <Check className="h-3.5 w-3.5" /> Approve
                      </Button>
                      <Button size="sm" variant="destructive" onClick={() => decide(a.id, a.title, "rejected")}>
                        <X className="h-3.5 w-3.5" /> Reject
                      </Button>
                      <Button size="sm" variant="outline">Modify</Button>
                      <Button size="sm" variant="ghost"><MessageSquare className="h-3.5 w-3.5" /> Comment</Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
