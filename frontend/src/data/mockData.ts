export type AgentStatus = "idle" | "working" | "waiting" | "completed" | "error"

export interface Agent {
  id: string
  name: string
  role: string
  status: AgentStatus
  progress: number
  lastAction: string
  confidence: number
  latencyMs: number
  tokens: number
}

export const agents: Agent[] = [
  { id: "coo", name: "COO Agent", role: "Orchestrator", status: "working", progress: 72, lastAction: "Routing crisis event CE-1042 to Crisis & Vendor agents", confidence: 0.94, latencyMs: 340, tokens: 1820 },
  { id: "planner", name: "Planner Agent", role: "Execution planning", status: "completed", progress: 100, lastAction: "Generated 4-step recovery plan for factory outage", confidence: 0.91, latencyMs: 812, tokens: 3120 },
  { id: "procurement", name: "Procurement Agent", role: "Purchasing & budget", status: "working", progress: 45, lastAction: "Comparing 3 alternate suppliers for PO-2291", confidence: 0.88, latencyMs: 560, tokens: 2210 },
  { id: "vendor", name: "Vendor Intelligence", role: "Supplier risk", status: "waiting", progress: 0, lastAction: "Queued: awaiting budget confirmation from Finance Agent", confidence: 0.0, latencyMs: 0, tokens: 0 },
  { id: "finance", name: "Finance Agent", role: "Budget & cost", status: "working", progress: 61, lastAction: "Validating $18,400 reallocation against Q3 budget", confidence: 0.96, latencyMs: 290, tokens: 1440 },
  { id: "compliance", name: "Compliance Agent", role: "Policy checks", status: "completed", progress: 100, lastAction: "Confirmed emergency procurement policy EP-04 applies", confidence: 0.99, latencyMs: 180, tokens: 940 },
  { id: "crisis", name: "Crisis Agent", role: "Disruption response", status: "working", progress: 88, lastAction: "Drafting recovery workflow for Chennai facility outage", confidence: 0.9, latencyMs: 940, tokens: 4110 },
  { id: "audit", name: "Audit Agent", role: "Logging & traceability", status: "working", progress: 100, lastAction: "Recorded 14 events in the last 6 minutes", confidence: 1, latencyMs: 90, tokens: 610 },
]

export type EventKind = "purchase" | "inventory" | "vendor" | "incident" | "complaint" | "machine"
export type EventStage = "pending" | "planning" | "approval" | "executing" | "completed" | "archived"

export interface BusinessEvent {
  id: string
  kind: EventKind
  title: string
  stage: EventStage
  owner: string
  time: string
  severity: "low" | "medium" | "high" | "critical"
  summary: string
}

export const businessEvents: BusinessEvent[] = [
  { id: "CE-1042", kind: "incident", title: "Power outage — Chennai fabrication unit", stage: "executing", owner: "Crisis Agent", time: "6m ago", severity: "critical", summary: "Grid failure at 04:12 IST halted line 2 and 3. Backup generators covering 40% load." },
  { id: "PO-2291", kind: "purchase", title: "Replacement compressor unit — Line 3", stage: "approval", owner: "Procurement Agent", time: "11m ago", severity: "high", summary: "Emergency purchase request routed for CFO sign-off, $18,400." },
  { id: "VD-0087", kind: "vendor", title: "Vendor delay — Meridian Steel Co.", stage: "planning", owner: "Vendor Intelligence", time: "22m ago", severity: "medium", summary: "Shipment ETA slipped 4 days. Alternate supplier shortlist generated." },
  { id: "IN-3305", kind: "inventory", title: "Low stock — Industrial lubricant SKU-2210", stage: "pending", owner: "Operations Agent", time: "34m ago", severity: "low", summary: "Reorder threshold crossed at 3 of 6 warehouses." },
  { id: "MC-0021", kind: "machine", title: "Predictive failure — CNC Mill #4", stage: "planning", owner: "Operations Agent", time: "51m ago", severity: "medium", summary: "Vibration sensors trending toward bearing failure within 72h." },
  { id: "CX-9911", kind: "complaint", title: "Customer escalation — Order #88213 delay", stage: "completed", owner: "Compliance Agent", time: "1h ago", severity: "low", summary: "Resolved with expedited shipping credit, logged and closed." },
  { id: "PO-2288", kind: "purchase", title: "Bulk raw material restock", stage: "archived", owner: "Procurement Agent", time: "3h ago", severity: "low", summary: "Standard reorder approved and delivered on schedule." },
]

export interface Approval {
  id: string
  title: string
  agent: string
  requestedFor: string
  amount?: string
  risk: "low" | "medium" | "high"
  time: string
  reasoning: string
}

export const approvals: Approval[] = [
  { id: "AP-501", title: "Emergency PO — replacement compressor", agent: "Procurement Agent", requestedFor: "PO-2291", amount: "$18,400", risk: "high", time: "2m ago", reasoning: "Line 3 is offline; compressor lead time from primary vendor is 9 days. Alternate vendor quote is 12% above budget threshold, requires CFO approval per policy EP-04." },
  { id: "AP-502", title: "Switch supplier — Meridian Steel → Delta Alloys", agent: "Vendor Intelligence", requestedFor: "VD-0087", risk: "medium", time: "14m ago", reasoning: "Delta Alloys has 98.2% on-time history and can meet the original delivery window at a 3% cost increase." },
  { id: "AP-503", title: "Overtime authorization — Line 2 recovery crew", agent: "Crisis Agent", requestedFor: "CE-1042", amount: "$4,200", risk: "low", time: "19m ago", reasoning: "6 technicians for 8hr overtime shift to restore Line 2 ahead of the Monday production run." },
  { id: "AP-504", title: "Reorder — industrial lubricant, 3 warehouses", agent: "Operations Agent", requestedFor: "IN-3305", amount: "$2,150", risk: "low", time: "40m ago", reasoning: "Standard reorder within approved quarterly budget, no policy exceptions triggered." },
]

export const kpis = {
  businessHealth: 92,
  revenueHealth: 88,
  inventoryHealth: 76,
  vendorHealth: 81,
  employeeHealth: 94,
  crisisStatus: "1 active" as const,
  pendingApprovals: approvals.length,
}

export const responseTimeSeries = [
  { day: "Mon", minutes: 14 }, { day: "Tue", minutes: 11 }, { day: "Wed", minutes: 9 },
  { day: "Thu", minutes: 13 }, { day: "Fri", minutes: 7 }, { day: "Sat", minutes: 6 }, { day: "Sun", minutes: 5 },
]

export const workflowEfficiency = [
  { name: "Procurement", value: 88 }, { name: "Crisis Response", value: 94 },
  { name: "Compliance", value: 97 }, { name: "Vendor Mgmt", value: 79 }, { name: "Finance", value: 91 },
]

export interface Vendor {
  id: string
  name: string
  category: string
  score: number
  risk: "low" | "medium" | "high"
  onTime: number
  contractExpiry: string
  lateDeliveries: number
}

export const vendors: Vendor[] = [
  { id: "V-01", name: "Delta Alloys", category: "Raw materials", score: 94, risk: "low", onTime: 98, contractExpiry: "Mar 2027", lateDeliveries: 1 },
  { id: "V-02", name: "Meridian Steel Co.", category: "Raw materials", score: 68, risk: "high", onTime: 74, contractExpiry: "Nov 2026", lateDeliveries: 6 },
  { id: "V-03", name: "Pacific Logistics", category: "Freight", score: 87, risk: "low", onTime: 95, contractExpiry: "Jun 2027", lateDeliveries: 2 },
  { id: "V-04", name: "Nexus Components", category: "Electronics", score: 79, risk: "medium", onTime: 88, contractExpiry: "Jan 2027", lateDeliveries: 3 },
  { id: "V-05", name: "Vertex Packaging", category: "Packaging", score: 91, risk: "low", onTime: 96, contractExpiry: "Aug 2026", lateDeliveries: 1 },
]

export const chatSuggestions = [
  "Why is procurement delayed?",
  "Show pending approvals",
  "Generate a recovery plan for the Chennai outage",
  "Summarize today's operations",
  "Simulate a supplier failure",
]
