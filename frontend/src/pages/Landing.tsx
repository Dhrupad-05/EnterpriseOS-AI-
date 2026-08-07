import { motion } from "framer-motion"
import { Link } from "react-router-dom"
import { ArrowRight, ShieldCheck, GitBranch, Bot, Flame, Gauge, Layers } from "lucide-react"
import { EventPipeline } from "@/components/EventPipeline"
import { Button } from "@/components/ui/button"
import { BorderBeam } from "@/components/ui/border-beam"

const stats = [
  { label: "Business events unified", value: "6", note: "one engine, not six systems" },
  { label: "Avg. response time", value: "5m", note: "down from 47m manual" },
  { label: "Actions requiring approval", value: "100%", note: "nothing executes unsupervised" },
]

const agents = [
  { name: "COO Agent", role: "Coordinates. Never executes.", icon: Layers },
  { name: "Crisis Agent", role: "Builds recovery workflows in real time.", icon: Flame },
  { name: "Procurement Agent", role: "Budget, vendor, PO generation.", icon: Gauge },
  { name: "Compliance Agent", role: "Checks every action against policy.", icon: ShieldCheck },
]

export default function Landing() {
  return (
    <div className="min-h-screen bg-canvas text-ink overflow-x-hidden">
      <header className="fixed top-0 z-40 w-full border-b border-border bg-canvas/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <div className="flex items-center gap-2.5">
            <div className="h-7 w-7 rounded-md bg-signal flex items-center justify-center">
              <span className="font-display text-xs font-bold text-white">eOS</span>
            </div>
            <span className="font-display text-sm font-semibold tracking-tight">EnterpriseOS</span>
          </div>
          <nav className="hidden md:flex items-center gap-8 text-sm text-ink-muted">
            <a href="#product" className="hover:text-ink transition-colors">Product</a>
            <a href="#architecture" className="hover:text-ink transition-colors">Architecture</a>
            <a href="#agents" className="hover:text-ink transition-colors">Agents</a>
          </nav>
          <div className="flex items-center gap-3">
            <Link to="/login" className="text-sm text-ink-muted hover:text-ink transition-colors">Log in</Link>
            <Button size="sm" asChild><Link to="/login">Launch demo</Link></Button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative pt-40 pb-28">
        <div className="grid-fade absolute inset-0 h-[700px]" />
        <div className="relative mx-auto max-w-4xl px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-border-strong bg-surface px-3.5 py-1.5 font-mono text-[11px] uppercase tracking-wide text-ink-muted"
          >
            <span className="h-1.5 w-1.5 rounded-full bg-good animate-pulse" /> Every action, human-approved
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.1 }}
            className="text-balance font-display text-5xl font-semibold leading-[1.05] tracking-tight md:text-6xl"
          >
            <span className="gradient-text">Your company's first</span>
            <br />
            <span className="text-signal-strong">AI Chief Operating Officer</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.2 }}
            className="mx-auto mt-6 max-w-xl text-balance text-ink-muted"
          >
            Autonomous workflows. Human-approved decisions. EnterpriseOS coordinates procurement,
            operations, compliance, and crisis response through specialized agents — orchestrated,
            never unsupervised.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.3 }}
            className="mt-9 flex items-center justify-center gap-3"
          >
            <Button size="lg" className="glow-signal" asChild><Link to="/login">Launch demo <ArrowRight className="h-4 w-4" /></Link></Button>
            <Button size="lg" variant="outline" asChild><a href="#architecture">View architecture</a></Button>
          </motion.div>

          {/* Signature: live business event pipeline */}
          <motion.div
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.45 }}
            className="mx-auto mt-16 w-fit"
          >
            <BorderBeam active className="rounded-2xl">
              <div className="rounded-2xl border border-border bg-surface/60 px-5 py-6 backdrop-blur-sm sm:px-8">
                <p className="mb-4 text-left font-mono text-[11px] uppercase tracking-wide text-ink-faint">Live: business event pipeline</p>
                <EventPipeline />
              </div>
            </BorderBeam>
          </motion.div>
        </div>
      </section>

      {/* Stats strip */}
      <section className="border-y border-border bg-canvas-raised/60">
        <div className="mx-auto grid max-w-5xl grid-cols-1 divide-y divide-border sm:grid-cols-3 sm:divide-x sm:divide-y-0">
          {stats.map((s) => (
            <div key={s.label} className="px-8 py-10 text-center">
              <p className="font-display text-4xl font-semibold text-signal-strong">{s.value}</p>
              <p className="mt-1 text-sm text-ink">{s.label}</p>
              <p className="mt-0.5 text-xs text-ink-faint">{s.note}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Product framing */}
      <section id="product" className="mx-auto max-w-5xl px-6 py-28">
        <div className="grid gap-14 md:grid-cols-2 md:items-center">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-wide text-signal-strong">Not a chatbot with dashboards</p>
            <h2 className="mt-3 text-balance font-display text-3xl font-semibold tracking-tight md:text-4xl">
              One workflow engine. Every business event.
            </h2>
            <p className="mt-4 text-ink-muted">
              Purchase requests, vendor delays, machine failures, customer escalations, cyber incidents —
              every input is a Business Event processed by the same orchestration engine. Add a new
              event type, not a new system.
            </p>
            <ul className="mt-6 space-y-3 text-sm text-ink-muted">
              {["Classify, plan, and route through specialized agents", "Every consequential action stops for human approval", "Full audit trail — replay any incident like git history"].map((t) => (
                <li key={t} className="flex items-start gap-2.5">
                  <GitBranch className="mt-0.5 h-4 w-4 shrink-0 text-signal-strong" /> {t}
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-border bg-surface p-6">
            <p className="mb-5 font-mono text-[11px] uppercase tracking-wide text-ink-faint">Same engine, different workflows</p>
            <div className="space-y-3">
              {["Purchase Request", "Vendor Delay", "Machine Failure", "Customer Escalation", "Cyber Incident"].map((w) => (
                <div key={w} className="flex items-center justify-between rounded-lg border border-border bg-canvas-raised px-4 py-2.5 text-sm">
                  <span className="text-ink-muted">{w}</span>
                  <span className="font-mono text-[10px] text-ink-faint">→ business_event</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Architecture */}
      <section id="architecture" className="border-t border-border bg-canvas-raised/40 py-28">
        <div className="mx-auto max-w-5xl px-6">
          <p className="text-center font-mono text-[11px] uppercase tracking-wide text-signal-strong">Architecture</p>
          <h2 className="mt-3 text-center font-display text-3xl font-semibold tracking-tight md:text-4xl">Orchestrated, not autonomous</h2>
          <div className="mt-14 flex flex-col items-center gap-6">
            <div className="rounded-xl border border-border-strong bg-surface px-6 py-3 font-mono text-sm">CEO Dashboard</div>
            <div className="h-8 w-px bg-border-strong" />
            <div className="rounded-xl border border-signal/40 bg-signal-soft px-6 py-3 font-mono text-sm text-signal-strong">AI COO Orchestrator</div>
            <div className="h-8 w-px bg-border-strong" />
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
              {["Procurement", "Operations", "Crisis", "Finance", "Compliance"].map((a) => (
                <div key={a} className="rounded-lg border border-border bg-surface px-4 py-2.5 text-center font-mono text-xs text-ink-muted">{a}</div>
              ))}
            </div>
            <div className="h-8 w-px bg-border-strong" />
            <div className="rounded-xl border border-border bg-canvas-raised px-6 py-3 font-mono text-sm text-ink-muted">Business Event Engine</div>
            <div className="h-8 w-px bg-border-strong" />
            <div className="rounded-xl border border-warn/30 bg-warn-soft px-6 py-3 font-mono text-sm text-warn">Human Approval Queue</div>
            <div className="h-8 w-px bg-border-strong" />
            <div className="rounded-xl border border-good/30 bg-good-soft px-6 py-3 font-mono text-sm text-good">Execution + Audit Logs</div>
          </div>
        </div>
      </section>

      {/* Agents */}
      <section id="agents" className="mx-auto max-w-5xl px-6 py-28">
        <p className="font-mono text-[11px] uppercase tracking-wide text-signal-strong">Agents</p>
        <h2 className="mt-3 text-balance font-display text-3xl font-semibold tracking-tight md:text-4xl">
          Hire one AI. Get a coordinated team.
        </h2>
        <div className="mt-10 grid gap-4 sm:grid-cols-2">
          {agents.map((a) => (
            <div key={a.name} className="card-lift flex items-start gap-4 rounded-xl border border-border bg-surface p-5">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-signal-soft">
                <a.icon className="h-5 w-5 text-signal-strong" />
              </div>
              <div>
                <p className="font-medium">{a.name}</p>
                <p className="mt-0.5 text-sm text-ink-muted">{a.role}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-border py-24">
        <div className="mx-auto max-w-2xl px-6 text-center">
          <Bot className="mx-auto h-8 w-8 text-signal-strong" />
          <h2 className="mt-5 text-balance font-display text-3xl font-semibold tracking-tight">See it coordinate a live crisis.</h2>
          <p className="mt-3 text-ink-muted">Walk through the Executive Dashboard, trigger a simulated disruption, and watch agents propose — and wait for your approval.</p>
          <Button size="lg" className="mt-7" asChild><Link to="/login">Launch demo <ArrowRight className="h-4 w-4" /></Link></Button>
        </div>
      </section>

      <footer className="border-t border-border py-8">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 text-xs text-ink-faint">
          <span>EnterpriseOS — Autonomous Enterprise Operations. Human-Governed Decisions.</span>
          <span className="font-mono">v0.1 hackathon build</span>
        </div>
      </footer>
    </div>
  )
}
