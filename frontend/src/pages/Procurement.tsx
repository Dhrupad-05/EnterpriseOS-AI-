import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { StatusChip } from "@/components/ui/status-chip"
import { businessEvents } from "@/data/mockData"
import { Button } from "@/components/ui/button"
import { ShoppingCart, PackageCheck, Truck } from "lucide-react"

const purchases = businessEvents.filter((e) => e.kind === "purchase")

export default function Procurement() {
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="flex items-center gap-2 font-display text-xl font-semibold tracking-tight">
            <ShoppingCart className="h-5 w-5 text-signal-strong" /> Procurement
          </h1>
          <p className="text-sm text-ink-faint">Purchase requests, vendor comparison, budget checks, and delivery status.</p>
        </div>
        <Button size="sm">New purchase request</Button>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardContent className="pt-5"><p className="font-mono text-[10px] uppercase text-ink-faint">Open requests</p><p className="mt-1 font-display text-2xl font-semibold">{purchases.length}</p></CardContent></Card>
        <Card><CardContent className="pt-5"><p className="font-mono text-[10px] uppercase text-ink-faint">Budget consumed (Q3)</p><p className="mt-1 font-display text-2xl font-semibold">68%</p></CardContent></Card>
        <Card><CardContent className="pt-5"><p className="font-mono text-[10px] uppercase text-ink-faint">Avg. approval time</p><p className="mt-1 font-display text-2xl font-semibold">3.2h</p></CardContent></Card>
      </div>

      <Card>
        <CardHeader><CardTitle>Purchase requests</CardTitle></CardHeader>
        <CardContent className="pt-0 space-y-2.5">
          {purchases.map((p) => (
            <div key={p.id} className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-border bg-canvas-raised px-4 py-3">
              <div>
                <p className="text-sm">{p.title}</p>
                <p className="text-[11px] text-ink-faint">{p.id} · {p.owner} · {p.time}</p>
              </div>
              <div className="flex items-center gap-2.5">
                <Badge variant={p.severity === "high" ? "crit" : "default"}>{p.severity}</Badge>
                <StatusChip stage={p.stage} />
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Vendor comparison — PO-2291</CardTitle></CardHeader>
          <CardContent className="pt-0 space-y-2.5">
            {[{ name: "Primary vendor", lead: "9 days", cost: "$16,400", flag: false }, { name: "Delta Alloys (alt.)", lead: "3 days", cost: "$18,400", flag: true }].map((v) => (
              <div key={v.name} className="flex items-center justify-between rounded-lg border border-border px-4 py-3">
                <div className="flex items-center gap-2.5">
                  <Truck className="h-4 w-4 text-ink-faint" />
                  <div>
                    <p className="text-sm">{v.name}</p>
                    <p className="text-[11px] text-ink-faint">Lead time {v.lead}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-mono text-sm">{v.cost}</p>
                  {v.flag && <p className="text-[10px] text-warn">above budget threshold</p>}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Delivery status</CardTitle></CardHeader>
          <CardContent className="pt-0 space-y-2.5">
            {[{ id: "PO-2288", label: "Bulk raw material restock", pct: 100 }, { id: "PO-2291", label: "Replacement compressor unit", pct: 20 }].map((d) => (
              <div key={d.id}>
                <div className="mb-1.5 flex items-center justify-between text-xs">
                  <span className="flex items-center gap-1.5 text-ink-muted"><PackageCheck className="h-3.5 w-3.5" /> {d.label}</span>
                  <span className="font-mono text-ink-faint">{d.pct}%</span>
                </div>
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-canvas-raised">
                  <div className="h-full rounded-full bg-signal" style={{ width: `${d.pct}%` }} />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
