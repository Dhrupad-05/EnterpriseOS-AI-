import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { workflowEfficiency, responseTimeSeries } from "@/data/mockData"
import { BarChart, Bar, XAxis, ResponsiveContainer, Tooltip, LineChart, Line } from "recharts"
import { BarChart3 } from "lucide-react"

const kpiTiles = [
  { label: "Avg. response time", value: "8.2m" },
  { label: "Workflow efficiency", value: "89%" },
  { label: "Approval delay (median)", value: "12m" },
  { label: "AI decision accuracy", value: "96.4%" },
]

export default function Analytics() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 font-display text-xl font-semibold tracking-tight">
          <BarChart3 className="h-5 w-5 text-signal-strong" /> Analytics
        </h1>
        <p className="text-sm text-ink-faint">KPIs across response time, workflow efficiency, approvals, vendors, and agent usage.</p>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {kpiTiles.map((k) => (
          <Card key={k.label}><CardContent className="pt-5">
            <p className="font-mono text-[10px] uppercase text-ink-faint">{k.label}</p>
            <p className="mt-1 font-display text-2xl font-semibold">{k.value}</p>
          </CardContent></Card>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Workflow efficiency by domain</CardTitle></CardHeader>
          <CardContent className="pt-0">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={workflowEfficiency}>
                <XAxis dataKey="name" tick={{ fill: "#5C6478", fontSize: 10 }} axisLine={false} tickLine={false} interval={0} angle={-15} textAnchor="end" height={50} />
                <Tooltip contentStyle={{ background: "#131822", border: "1px solid rgba(255,255,255,0.14)", borderRadius: 8, fontSize: 12 }} labelStyle={{ color: "#9099AC" }} />
                <Bar dataKey="value" fill="#4C8DFF" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Response time trend</CardTitle></CardHeader>
          <CardContent className="pt-0">
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={responseTimeSeries}>
                <XAxis dataKey="day" tick={{ fill: "#5C6478", fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: "#131822", border: "1px solid rgba(255,255,255,0.14)", borderRadius: 8, fontSize: 12 }} labelStyle={{ color: "#9099AC" }} />
                <Line type="monotone" dataKey="minutes" stroke="#33D2A0" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
