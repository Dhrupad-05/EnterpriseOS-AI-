import { useState } from "react"
import { Reorder } from "framer-motion"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { StatusChip } from "@/components/ui/status-chip"
import { useToast } from "@/components/ui/toast"
import { kpis, businessEvents, agents, approvals, responseTimeSeries } from "@/data/mockData"
import { useApp } from "@/context/AppContext"
import { AreaChart, Area, ResponsiveContainer, XAxis, Tooltip } from "recharts"
import { AlertTriangle, TrendingUp, Sparkles, Flame, ShieldCheck, ArrowUpRight, ArrowDownRight, GripVertical } from "lucide-react"
import { Link } from "react-router-dom"

const healthCards = [
  { label: "Business Health", value: kpis.businessHealth, trend: 3, key: "business" },
  { label: "Revenue Health", value: kpis.revenueHealth, trend: 2, key: "revenue" },
  { label: "Inventory Health", value: kpis.inventoryHealth, trend: -4, key: "inventory" },
  { label: "Vendor Health", value: kpis.vendorHealth, trend: -1, key: "vendor" },
  { label: "Employee Health", value: kpis.employeeHealth, trend: 1, key: "employee" },
]

const initialPriorities = [
  { id: "p1", text: "Approve emergency compressor PO before 2 PM to keep Line 3 on schedule" },
  { id: "p2", text: "Review Meridian Steel vendor risk — 6 late deliveries this quarter" },
  { id: "p3", text: "Sign off on Chennai recovery crew overtime" },
]

const risks = [
  { label: "Vendor concentration — 34% of raw materials from single supplier", level: "high" },
  { label: "CNC Mill #4 predictive failure within 72h", level: "medium" },
  { label: "Inventory below reorder threshold at 3 warehouses", level: "low" },
]

const recommendations = [
  "Diversify steel sourcing to Delta Alloys to reduce vendor concentration risk",
  "Schedule preventive maintenance for CNC Mill #4 this week",
  "Increase lubricant safety stock by 15% ahead of Q4 demand",
]

export default function Dashboard() {
  const { role } = useApp()
  const { toast } = useToast()
  const [priorities, setPriorities] = useState(initialPriorities)
  const activeCrisis = businessEvents.find((e) => e.kind === "incident" && e.stage !== "completed" && e.stage !== "archived")

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="font-display text-xl font-semibold tracking-tight">Executive Dashboard</h1>
          <p className="text-sm text-ink-faint">Welcome back — viewing as {role}</p>
        </div>
        {activeCrisis && (
          <Link to="/app/crisis" className="flex items-center gap-2 rounded-lg border border-crit/30 bg-crit-soft px-3.5 py-2 text-xs text-crit">
            <Flame className="h-3.5 w-3.5 animate-pulse" /> 1 active crisis — {activeCrisis.title}
          </Link>
        )}
      </div>

      {/* Health scores */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
        {healthCards.map((c) => (
          <Card key={c.key}>
            <CardContent className="pt-5">
              <p className="font-mono text-[10px] uppercase tracking-wide text-ink-faint">{c.label}</p>
              <div className="mt-2 flex items-end justify-between">
                <span className="font-display text-3xl font-semibold">{c.value}%</span>
                <span className={`flex items-center gap-0.5 text-xs font-mono ${c.trend >= 0 ? "text-good" : "text-crit"}`}>
                  {c.trend >= 0 ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
                  {Math.abs(c.trend)}%
                </span>
              </div>
              <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-canvas-raised">
                <div className="h-full rounded-full bg-signal" style={{ width: `${c.value}%` }} />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        {/* Response time chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Response time — last 7 days</CardTitle>
            <TrendingUp className="h-4 w-4 text-good" />
          </CardHeader>
          <CardContent className="pt-0">
            <ResponsiveContainer width="100%" height={180}>
              <AreaChart data={responseTimeSeries}>
                <defs>
                  <linearGradient id="fill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#4C8DFF" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="#4C8DFF" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="day" tick={{ fill: "#5C6478", fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ background: "#131822", border: "1px solid rgba(255,255,255,0.14)", borderRadius: 8, fontSize: 12 }}
                  labelStyle={{ color: "#9099AC" }}
                />
                <Area type="monotone" dataKey="minutes" stroke="#4C8DFF" strokeWidth={2} fill="url(#fill)" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Pending approvals summary */}
        <Card>
          <CardHeader>
            <CardTitle>Pending Approvals</CardTitle>
            <ShieldCheck className="h-4 w-4 text-warn" />
          </CardHeader>
          <CardContent className="space-y-3 pt-0">
            {approvals.slice(0, 3).map((a) => (
              <div key={a.id} className="flex items-start justify-between gap-3 border-b border-border pb-3 last:border-0 last:pb-0">
                <div className="min-w-0">
                  <p className="truncate text-sm">{a.title}</p>
                  <p className="text-[11px] text-ink-faint">{a.agent} · {a.time}</p>
                </div>
                {a.amount && <span className="shrink-0 font-mono text-xs text-ink-muted">{a.amount}</span>}
              </div>
            ))}
            <Link to="/app/approvals" className="block pt-1 text-xs text-signal-strong hover:underline">View all {kpis.pendingApprovals} approvals →</Link>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Card interactive={false}>
          <CardHeader>
            <CardTitle>Today's Priorities</CardTitle>
            <span className="font-mono text-[10px] text-ink-faint">drag to reorder</span>
          </CardHeader>
          <CardContent className="pt-0">
            <Reorder.Group
              axis="y"
              values={priorities}
              onReorder={(next) => {
                setPriorities(next)
                toast({ title: "Priorities reordered", description: "Your ranking has been saved.", variant: "success" })
              }}
              className="space-y-2"
            >
              {priorities.map((p) => (
                <Reorder.Item
                  key={p.id}
                  value={p}
                  className="flex cursor-grab items-start gap-2 rounded-lg border border-transparent px-2 py-1.5 text-sm text-ink-muted transition-colors hover:border-border hover:bg-surface-hover active:cursor-grabbing"
                  whileDrag={{ scale: 1.02, boxShadow: "0 12px 30px -12px rgba(0,0,0,0.5)" }}
                >
                  <GripVertical className="mt-0.5 h-3.5 w-3.5 shrink-0 text-ink-faint" />
                  <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-signal" />
                  {p.text}
                </Reorder.Item>
              ))}
            </Reorder.Group>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Risks</CardTitle>
            <AlertTriangle className="h-4 w-4 text-warn" />
          </CardHeader>
          <CardContent className="space-y-3 pt-0">
            {risks.map((r, i) => (
              <div key={i} className="flex items-start gap-2.5 text-sm text-ink-muted">
                <Badge variant={r.level === "high" ? "crit" : r.level === "medium" ? "warn" : "default"} className="mt-0.5 shrink-0">{r.level}</Badge>
                {r.label}
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>AI Recommendations</CardTitle>
            <Sparkles className="h-4 w-4 text-violet" />
          </CardHeader>
          <CardContent className="space-y-3 pt-0">
            {recommendations.map((r, i) => (
              <div key={i} className="flex items-start gap-2.5 text-sm text-ink-muted">
                <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-violet" /> {r}
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Recent AI Decisions</CardTitle></CardHeader>
          <CardContent className="space-y-3 pt-0">
            {agents.filter(a => a.status === "completed").map((a) => (
              <div key={a.id} className="flex items-start justify-between gap-3 border-b border-border pb-3 last:border-0 last:pb-0">
                <div>
                  <p className="text-sm">{a.lastAction}</p>
                  <p className="text-[11px] text-ink-faint">{a.name}</p>
                </div>
                <Badge variant="good">done</Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Business Timeline</CardTitle></CardHeader>
          <CardContent className="space-y-3 pt-0">
            {businessEvents.slice(0, 5).map((e) => (
              <div key={e.id} className="flex items-center justify-between gap-3 border-b border-border pb-3 last:border-0 last:pb-0">
                <div className="min-w-0">
                  <p className="truncate text-sm">{e.title}</p>
                  <p className="text-[11px] text-ink-faint">{e.id} · {e.time}</p>
                </div>
                <StatusChip stage={e.stage} />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
