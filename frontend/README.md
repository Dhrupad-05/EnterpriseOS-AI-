# EnterpriseOS — AI COO

A React + TypeScript frontend for an AI Chief Operating Officer platform: an orchestration engine
that turns every business event (purchase, inventory, vendor delay, machine failure, complaint,
incident) through the same pipeline — classify → plan → approve → execute → audit.

## Stack
- React 19 + TypeScript + Vite
- Tailwind CSS v4
- Framer Motion (animation)
- React Router (routing)
- Recharts (charts)
- lucide-react (icons)

## Run it

```bash
npm install
npm run dev
```

Then open the printed local URL. Visit `/` for the landing page, `/login` to pick a role, `/app` for
the product itself.

## Structure

```
src/
  pages/            Landing, Login, Dashboard, Operations Center, Crisis Center,
                     Approval Center, Agent Monitor, Procurement, Vendor Management,
                     Analytics, Timeline Replay
  components/layout/ Sidebar, Topbar, Command Palette (⌘K), AI COO chat slide-over, AppShell
  components/ui/     Button, Badge, Card, StatusChip primitives
  components/EventPipeline.tsx   the reusable "business event" signature visual
  context/AppContext.tsx         role switcher + chat/palette open state
  data/mockData.ts               all mock data (agents, events, approvals, vendors, KPIs)
```

All data is synthetic/mocked — swap `src/data/mockData.ts` for real API calls when you wire up a backend.

## Notes

- The Crisis Center and Timeline Replay pages have working simulated step-through animations —
  click a scenario / hit "Replay" to see them run.
- The AI COO chat (top-right "Ask AI COO" button, or ⌘K → any nav command) is a slide-over panel with
  a few canned responses, intentionally kept secondary to the dashboard per the "not a chatbot" brief.
- Role switching (top-right avatar menu, or the Login screen) only changes the displayed label for now —
  wire up real route/permission gating if you need it for the demo.
