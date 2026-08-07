import { AnimatePresence, motion } from "framer-motion"
import { useApp } from "@/context/AppContext"
import { X, Send, Sparkles, Bot } from "lucide-react"
import { chatSuggestions } from "@/data/mockData"
import { useState } from "react"

interface Msg { role: "user" | "assistant"; text: string }

const canned: Record<string, string> = {
  "why is procurement delayed?": "PO-2291 is waiting on CFO approval because the alternate vendor quote exceeds budget threshold by 12%. Everything else in the procurement queue is on schedule.",
  "show pending approvals": "There are 4 pending approvals: an $18,400 emergency compressor purchase, a vendor switch for Meridian Steel, overtime authorization for the Chennai recovery crew, and a routine lubricant reorder.",
  "generate a recovery plan for the chennai outage": "Recovery plan drafted: 1) Reroute Line 2 load to backup generators, 2) expedite compressor PO-2291, 3) authorize recovery crew overtime, 4) notify affected downstream customers. Awaiting your approval on steps 2 and 3.",
  "summarize today's operations": "Business health is at 92%. One active crisis (Chennai power outage, executing), 4 pending approvals, and 2 vendor risk flags. Everything else is nominal.",
  "simulate a supplier failure": "Simulating Meridian Steel Co. failure — Vendor Intelligence has already surfaced Delta Alloys as the top alternate (98.2% on-time, +3% cost). Want me to draft the switch request?",
}

export function ChatPanel() {
  const { chatOpen, setChatOpen } = useApp()
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", text: "I'm the AI COO. Ask me about operations, approvals, or run a simulation." },
  ])
  const [input, setInput] = useState("")

  function send(text: string) {
    if (!text.trim()) return
    const reply = canned[text.trim().toLowerCase()] ?? "I've logged that request and routed it to the relevant agent. You'll see it appear in the Operations Center shortly."
    setMessages((m) => [...m, { role: "user", text }, { role: "assistant", text: reply }])
    setInput("")
  }

  return (
    <AnimatePresence>
      {chatOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={() => setChatOpen(false)}
            className="fixed inset-0 z-40 bg-black/50 backdrop-blur-[2px]"
          />
          <motion.div
            initial={{ x: "100%" }} animate={{ x: 0 }} exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 28, stiffness: 300 }}
            className="fixed right-0 top-0 z-50 flex h-screen w-full max-w-md flex-col border-l border-border-strong bg-canvas-raised"
          >
            <div className="flex items-center justify-between border-b border-border px-5 py-4">
              <div className="flex items-center gap-2.5">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-signal-soft">
                  <Bot className="h-4 w-4 text-signal-strong" />
                </div>
                <div>
                  <p className="text-sm font-medium">AI COO</p>
                  <p className="text-[11px] text-ink-faint">One entry point, not the product</p>
                </div>
              </div>
              <button onClick={() => setChatOpen(false)} className="text-ink-faint hover:text-ink">
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
              {messages.map((m, i) => (
                <div key={i} className={m.role === "user" ? "flex justify-end" : "flex justify-start"}>
                  <div className={
                    m.role === "user"
                      ? "max-w-[85%] rounded-xl rounded-tr-sm bg-signal px-3.5 py-2.5 text-sm text-white"
                      : "max-w-[85%] rounded-xl rounded-tl-sm border border-border bg-surface px-3.5 py-2.5 text-sm text-ink-muted"
                  }>
                    {m.text}
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t border-border px-5 py-3 space-y-2">
              <div className="flex flex-wrap gap-1.5">
                {chatSuggestions.slice(0, 3).map((s) => (
                  <button
                    key={s}
                    onClick={() => send(s)}
                    className="flex items-center gap-1 rounded-full border border-border px-2.5 py-1 text-[11px] text-ink-faint hover:border-signal/40 hover:text-signal-strong transition-colors"
                  >
                    <Sparkles className="h-2.5 w-2.5" /> {s}
                  </button>
                ))}
              </div>
              <div className="flex items-center gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && send(input)}
                  placeholder="Ask the AI COO anything..."
                  className="flex-1 rounded-lg border border-border bg-surface px-3 py-2.5 text-sm outline-none placeholder:text-ink-faint focus:border-signal/50"
                />
                <button onClick={() => send(input)} className="flex h-10 w-10 items-center justify-center rounded-lg bg-signal text-white hover:bg-signal-strong transition-colors">
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
