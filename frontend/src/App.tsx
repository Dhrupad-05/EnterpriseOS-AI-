import { BrowserRouter, Routes, Route } from "react-router-dom"
import { AppProvider } from "@/context/AppContext"
import { ToastProvider } from "@/components/ui/toast"
import { AppShell } from "@/components/layout/AppShell"
import Landing from "@/pages/Landing"
import Login from "@/pages/Login"
import Dashboard from "@/pages/Dashboard"
import OperationsCenter from "@/pages/OperationsCenter"
import CrisisCenter from "@/pages/CrisisCenter"
import ApprovalCenter from "@/pages/ApprovalCenter"
import AgentMonitor from "@/pages/AgentMonitor"
import Procurement from "@/pages/Procurement"
import VendorManagement from "@/pages/VendorManagement"
import Analytics from "@/pages/Analytics"
import TimelineReplay from "@/pages/TimelineReplay"

export default function App() {
  return (
    <AppProvider>
      <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/app" element={<AppShell />}>
            <Route index element={<Dashboard />} />
            <Route path="operations" element={<OperationsCenter />} />
            <Route path="crisis" element={<CrisisCenter />} />
            <Route path="approvals" element={<ApprovalCenter />} />
            <Route path="agents" element={<AgentMonitor />} />
            <Route path="procurement" element={<Procurement />} />
            <Route path="vendors" element={<VendorManagement />} />
            <Route path="analytics" element={<Analytics />} />
            <Route path="timeline" element={<TimelineReplay />} />
          </Route>
        </Routes>
      </BrowserRouter>
      </ToastProvider>
    </AppProvider>
  )
}
