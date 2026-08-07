import { Bell, Command, MessageSquareText, ChevronDown } from "lucide-react"
import { useApp, type Role } from "@/context/AppContext"
import { kpis } from "@/data/mockData"
import { useState } from "react"
import { cn } from "@/lib/utils"

const roles: Role[] = ["CEO", "Operations Manager", "Finance", "HR", "Admin", "Employee"]

export function Topbar() {
  const { role, setRole, setChatOpen, setPaletteOpen } = useApp()
  const [roleMenu, setRoleMenu] = useState(false)

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-canvas/90 backdrop-blur-sm px-6">
      <button
        onClick={() => setPaletteOpen(true)}
        className="flex items-center gap-2 rounded-lg border border-border bg-surface px-3 py-1.5 text-xs text-ink-faint hover:text-ink-muted hover:border-border-strong transition-colors"
      >
        <Command className="h-3.5 w-3.5" />
        <span>Quick command</span>
        <kbd className="ml-2 rounded border border-border-strong px-1 font-mono text-[10px]">⌘K</kbd>
      </button>

      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-2 rounded-lg border border-border bg-surface px-3 py-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-good animate-pulse" />
          <span className="font-mono text-xs text-ink-muted">Business Health</span>
          <span className="font-mono text-xs font-semibold text-good">{kpis.businessHealth}%</span>
        </div>

        <button
          onClick={() => setChatOpen(true)}
          className="flex items-center gap-2 rounded-lg border border-signal/30 bg-signal-soft px-3 py-1.5 text-xs font-medium text-signal-strong hover:bg-signal/20 transition-colors"
        >
          <MessageSquareText className="h-3.5 w-3.5" />
          Ask AI COO
        </button>

        <button className="relative text-ink-muted hover:text-ink transition-colors">
          <Bell className="h-4.5 w-4.5" />
          <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-crit" />
        </button>

        <div className="relative">
          <button
            onClick={() => setRoleMenu((v) => !v)}
            className="flex items-center gap-2 rounded-lg border border-border bg-surface px-2.5 py-1.5 text-xs hover:border-border-strong transition-colors"
          >
            <div className="h-5 w-5 rounded-full bg-gradient-to-br from-signal to-violet" />
            <span className="text-ink-muted">{role}</span>
            <ChevronDown className="h-3 w-3 text-ink-faint" />
          </button>
          {roleMenu && (
            <div className="absolute right-0 mt-2 w-48 rounded-lg border border-border-strong bg-canvas-raised shadow-2xl overflow-hidden">
              {roles.map((r) => (
                <button
                  key={r}
                  onClick={() => { setRole(r); setRoleMenu(false) }}
                  className={cn(
                    "block w-full px-3 py-2 text-left text-xs hover:bg-surface-hover transition-colors",
                    r === role ? "text-signal-strong" : "text-ink-muted"
                  )}
                >
                  {r}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
