import { useNavigate } from "react-router-dom"
import { Crown, Wrench, Landmark, Users, ShieldEllipsis, User, ArrowLeft } from "lucide-react"
import { useApp, type Role } from "@/context/AppContext"
import { BorderBeam } from "@/components/ui/border-beam"
import { Link } from "react-router-dom"

const roles: { role: Role; icon: typeof Crown; note: string; accent: string }[] = [
  { role: "CEO", icon: Crown, note: "Full visibility across the business", accent: "text-signal-strong bg-signal-soft" },
  { role: "Operations Manager", icon: Wrench, note: "Operations Center, Crisis Center", accent: "text-good bg-good-soft" },
  { role: "Finance", icon: Landmark, note: "Budget approvals, cost analytics", accent: "text-warn bg-warn-soft" },
  { role: "HR", icon: Users, note: "Employee health, workforce events", accent: "text-violet bg-violet/15" },
  { role: "Admin", icon: ShieldEllipsis, note: "Policies, agent configuration", accent: "text-crit bg-crit-soft" },
  { role: "Employee", icon: User, note: "Submit requests, track status", accent: "text-ink-muted bg-surface-hover" },
]

export default function Login() {
  const { setRole } = useApp()
  const navigate = useNavigate()

  function enter(role: Role) {
    setRole(role)
    navigate("/app")
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-canvas px-6 py-16">
      <div className="grid-fade pointer-events-none absolute inset-0" />
      <div className="pointer-events-none absolute left-1/2 top-0 h-[420px] w-[720px] -translate-x-1/2 rounded-full bg-signal/10 blur-[120px]" />

      <Link
        to="/"
        className="absolute left-6 top-6 flex items-center gap-1.5 text-xs text-ink-faint transition-colors hover:text-ink"
      >
        <ArrowLeft className="h-3.5 w-3.5" /> Back home
      </Link>

      <div className="relative w-full max-w-xl">
        <div className="mb-9 text-center">
          <div className="glow-signal mx-auto mb-5 flex h-11 w-11 items-center justify-center rounded-xl bg-signal">
            <span className="font-display text-sm font-bold text-white">eOS</span>
          </div>
          <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">Sign in to EnterpriseOS</h1>
          <p className="mt-2 text-sm text-ink-muted">Choose a role to preview its view of the demo.</p>
        </div>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {roles.map(({ role, icon: Icon, note, accent }) => (
            <BorderBeam key={role} className="rounded-xl">
              <button
                onClick={() => enter(role)}
                className="group relative z-[2] flex w-full items-start gap-3 rounded-xl border border-border bg-surface p-4 text-left transition-all duration-200 hover:-translate-y-0.5 hover:border-border-strong hover:bg-surface-hover"
              >
                <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg transition-transform duration-200 group-hover:scale-105 ${accent}`}>
                  <Icon className="h-4.5 w-4.5" />
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-ink">{role}</p>
                  <p className="mt-0.5 text-xs leading-relaxed text-ink-muted">{note}</p>
                </div>
              </button>
            </BorderBeam>
          ))}
        </div>

        <p className="mt-9 text-center text-xs text-ink-faint">Demo build — no credentials required.</p>
      </div>
    </div>
  )
}
