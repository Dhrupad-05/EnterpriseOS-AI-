import { Outlet } from "react-router-dom"
import { Sidebar } from "./Sidebar"
import { Topbar } from "./Topbar"
import { CommandPalette } from "./CommandPalette"
import { ChatPanel } from "./ChatPanel"

export function AppShell() {
  return (
    <div className="flex min-h-screen bg-canvas">
      <Sidebar />
      <div className="flex-1 min-w-0">
        <Topbar />
        <main className="px-6 py-6">
          <Outlet />
        </main>
      </div>
      <CommandPalette />
      <ChatPanel />
    </div>
  )
}
