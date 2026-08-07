import { AnimatePresence, motion } from "framer-motion"
import { useApp } from "@/context/AppContext"
import { Search, LayoutGrid, Flame, ShieldCheck, Bot, PackageSearch } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { useEffect, useState } from "react"

const commands = [
  { label: "Go to Dashboard", path: "/app", icon: LayoutGrid },
  { label: "Open Crisis Center", path: "/app/crisis", icon: Flame },
  { label: "Review pending approvals", path: "/app/approvals", icon: ShieldCheck },
  { label: "View Agent Monitor", path: "/app/agents", icon: Bot },
  { label: "Create purchase request", path: "/app/procurement", icon: PackageSearch },
]

export function CommandPalette() {
  const { paletteOpen, setPaletteOpen } = useApp()
  const [query, setQuery] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault()
        setPaletteOpen(!paletteOpen)
      }
      if (e.key === "Escape") setPaletteOpen(false)
    }
    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)
  }, [paletteOpen, setPaletteOpen])

  const filtered = commands.filter((c) => c.label.toLowerCase().includes(query.toLowerCase()))

  return (
    <AnimatePresence>
      {paletteOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={() => setPaletteOpen(false)}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
          />
          <motion.div
            initial={{ opacity: 0, y: -12, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -12, scale: 0.98 }}
            transition={{ duration: 0.15 }}
            className="fixed left-1/2 top-24 z-50 w-full max-w-lg -translate-x-1/2 overflow-hidden rounded-xl border border-border-strong bg-canvas-raised shadow-2xl"
          >
            <div className="flex items-center gap-3 border-b border-border px-4 py-3">
              <Search className="h-4 w-4 text-ink-faint" />
              <input
                autoFocus
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Type a command or search..."
                className="w-full bg-transparent text-sm text-ink placeholder:text-ink-faint outline-none"
              />
              <kbd className="rounded border border-border-strong px-1.5 py-0.5 font-mono text-[10px] text-ink-faint">ESC</kbd>
            </div>
            <div className="max-h-80 overflow-y-auto p-2">
              {filtered.map((c) => (
                <button
                  key={c.path}
                  onClick={() => { navigate(c.path); setPaletteOpen(false); setQuery("") }}
                  className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm text-ink-muted hover:bg-surface-hover hover:text-ink transition-colors"
                >
                  <c.icon className="h-4 w-4" />
                  {c.label}
                </button>
              ))}
              {filtered.length === 0 && (
                <p className="px-3 py-6 text-center text-xs text-ink-faint">No matching commands.</p>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
