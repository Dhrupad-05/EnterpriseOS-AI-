import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { vendors } from "@/data/mockData"
import { Users2, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

const riskVariant = { low: "good", medium: "warn", high: "crit" } as const

export default function VendorManagement() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 font-display text-xl font-semibold tracking-tight">
          <Users2 className="h-5 w-5 text-signal-strong" /> Vendor Management
        </h1>
        <p className="text-sm text-ink-faint">Score, risk, contract status, and AI recommendations for every supplier.</p>
      </div>

      <div className="overflow-hidden rounded-xl border border-border">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border bg-canvas-raised text-left text-[11px] uppercase tracking-wide text-ink-faint">
              <th className="px-4 py-3 font-mono">Vendor</th>
              <th className="px-4 py-3 font-mono">Category</th>
              <th className="px-4 py-3 font-mono">Score</th>
              <th className="px-4 py-3 font-mono">Risk</th>
              <th className="px-4 py-3 font-mono">On-time %</th>
              <th className="px-4 py-3 font-mono">Late deliveries</th>
              <th className="px-4 py-3 font-mono">Contract expiry</th>
            </tr>
          </thead>
          <tbody>
            {vendors.map((v) => (
              <tr key={v.id} className="border-b border-border last:border-0 hover:bg-surface-hover">
                <td className="px-4 py-3">{v.name}</td>
                <td className="px-4 py-3 text-ink-muted">{v.category}</td>
                <td className="px-4 py-3 font-mono">{v.score}</td>
                <td className="px-4 py-3"><Badge variant={riskVariant[v.risk]}>{v.risk}</Badge></td>
                <td className="px-4 py-3 font-mono">{v.onTime}%</td>
                <td className={cn("px-4 py-3 font-mono", v.lateDeliveries > 3 ? "text-crit" : "text-ink-muted")}>{v.lateDeliveries}</td>
                <td className="px-4 py-3 text-ink-faint">{v.contractExpiry}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Card>
        <CardContent className="flex items-start gap-3 pt-5">
          <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-violet" />
          <p className="text-sm text-ink-muted">
            <span className="text-ink">AI recommendation:</span> Meridian Steel Co. risk score has declined 12 points this quarter.
            Consider shifting 30% of raw material volume to Delta Alloys to reduce single-vendor exposure.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
