import { Outlet, Navigate, useLocation } from "react-router-dom"
import { Sidebar } from "./Sidebar"
import { Topbar } from "./Topbar"
import { CommandPalette } from "./CommandPalette"
import { ChatPanel } from "./ChatPanel"
import { useApp } from "@/context/AppContext"
import { canAccess } from "@/lib/access"

export function AppShell() {
  const { role } = useApp()
  const location = useLocation()

  // Employee role only sees Dashboard, Operations, Crisis, Analytics, Timeline.
  // Every other role is unaffected and keeps access to all pages.
  if (!canAccess(role, location.pathname)) {
    return <Navigate to="/app" replace />
  }

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
