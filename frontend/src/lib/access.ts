import type { Role } from "@/context/AppContext"

/**
 * Employee role is limited to these pages only:
 * Dashboard, Operations Center, Crisis Center, Analytics, Timeline Replay.
 *
 * Every other role (CEO, Operations Manager, Finance, HR, Admin) keeps
 * unrestricted access to all pages — unchanged.
 */
export const EMPLOYEE_ALLOWED_PATHS = [
  "/app",
  "/app/operations",
  "/app/crisis",
  "/app/analytics",
  "/app/timeline",
] as const

export function canAccess(role: Role, path: string): boolean {
  if (role !== "Employee") return true
  return (EMPLOYEE_ALLOWED_PATHS as readonly string[]).includes(path)
}
