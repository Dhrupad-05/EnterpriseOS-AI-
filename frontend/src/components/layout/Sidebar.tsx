import { NavLink } from "react-router-dom"
import {
  LayoutGrid, Radio, Flame, ShieldCheck, Users2, PackageSearch,
  BarChart3, Bot, History, ChevronsLeft, ChevronsRight,
} from "lucide-react"
import { useState } from "react"
import { cn } from "@/lib/utils"
import { useApp } from "@/context/AppContext"
import { canAccess } from "@/lib/access"

const nav = [
  { to: "/app", label: "Dashboard", icon: LayoutGrid, end: true },
  { to: "/app/operations", label: "Operations Center", icon: Radio },
  { to: "/app/crisis", label: "Crisis Center", icon: Flame, accent: "crit" },
  { to: "/app/approvals", label: "Approval Center", icon: ShieldCheck },
  { to: "/app/agents", label: "Agent Monitor", icon: Bot },
  { to: "/app/procurement", label: "Procurement", icon: PackageSearch },
  { to: "/app/vendors", label: "Vendor Management", icon: Users2 },
  { to: "/app/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/app/timeline", label: "Timeline Replay", icon: History },
]

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const { role } = useApp()
  const visibleNav = nav.filter((item) => canAccess(role, item.to))

  return (
    <aside
      className={cn(
        "sticky top-0 h-screen shrink-0 border-r border-border bg-canvas-raised/80 backdrop-blur-sm transition-all duration-200 flex flex-col",
        collapsed ? "w-[68px]" : "w-[240px]"
      )}
    >
      <div className="flex h-16 items-center gap-2.5 px-4 border-b border-border">
        <div className="h-7 w-7 shrink-0 rounded-md bg-signal flex items-center justify-center">
          <span className="font-display text-xs font-bold text-white">eOS</span>
        </div>
        {!collapsed && <span className="font-display text-sm font-semibold tracking-tight">EnterpriseOS</span>}
      </div>

      <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        {visibleNav.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            className={({ isActive }) =>
              cn(
                "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
                isActive
                  ? "bg-signal-soft text-signal-strong"
                  : "text-ink-muted hover:text-ink hover:bg-surface-hover"
              )
            }
            title={collapsed ? item.label : undefined}
          >
            <item.icon className="h-4 w-4 shrink-0" />
            {!collapsed && <span className="truncate">{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      <button
        onClick={() => setCollapsed((c) => !c)}
        className="flex items-center gap-2 border-t border-border px-4 py-3 text-xs text-ink-faint hover:text-ink-muted transition-colors"
      >
        {collapsed ? <ChevronsRight className="h-4 w-4" /> : <><ChevronsLeft className="h-4 w-4" /> Collapse</>}
      </button>
    </aside>
  )
}
