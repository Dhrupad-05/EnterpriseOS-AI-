import { createContext, useContext, useState, type ReactNode } from "react"

export type Role = "CEO" | "Operations Manager" | "Finance" | "HR" | "Admin" | "Employee"

interface AppState {
  role: Role
  setRole: (r: Role) => void
  chatOpen: boolean
  setChatOpen: (v: boolean) => void
  paletteOpen: boolean
  setPaletteOpen: (v: boolean) => void
}

const AppContext = createContext<AppState | null>(null)

export function AppProvider({ children }: { children: ReactNode }) {
  const [role, setRole] = useState<Role>("CEO")
  const [chatOpen, setChatOpen] = useState(false)
  const [paletteOpen, setPaletteOpen] = useState(false)
  return (
    <AppContext.Provider value={{ role, setRole, chatOpen, setChatOpen, paletteOpen, setPaletteOpen }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error("useApp must be used within AppProvider")
  return ctx
}
