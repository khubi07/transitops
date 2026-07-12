import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { LayoutDashboard, Truck, Users, Route as RouteIcon, Wrench, Fuel, BarChart3, Settings } from 'lucide-react'
import VehicleRegistry from './pages/VehicleRegistry'
import MaintenanceScreen from './pages/MaintenanceScreen'

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/fleet', label: 'Fleet', icon: Truck },
  { to: '/drivers', label: 'Drivers', icon: Users },
  { to: '/trips', label: 'Trips', icon: RouteIcon },
  { to: '/maintenance', label: 'Maintenance', icon: Wrench },
  { to: '/fuel', label: 'Fuel & Expenses', icon: Fuel },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/settings', label: 'Settings', icon: Settings },
]

function Sidebar() {
  return (
    <aside className="w-56 shrink-0 border-r border-[var(--color-border)] bg-[var(--color-surface-elevated)] min-h-screen px-4 py-6">
      <div className="flex items-center gap-2 mb-8 px-2">
        <div className="w-8 h-8 rounded-lg gradient-accent" />
        <span className="text-lg font-semibold tracking-tight">TransitOps</span>
      </div>
      <nav className="flex flex-col gap-1">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                isActive
                  ? 'bg-white/5 text-white border border-[var(--color-accent-from)]/40'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <Icon size={17} />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

function Topbar() {
  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-[var(--color-border)]">
      <input
        placeholder="Search..."
        className="w-72 bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50 transition-colors"
      />
      <div className="flex items-center gap-3">
        <span className="text-sm text-gray-400">Raven K.</span>
        <div className="flex items-center gap-2 border border-[var(--color-accent-from)]/40 rounded-full pl-3 pr-1 py-1">
          <span className="text-xs text-[var(--color-accent-from)]">Dispatcher</span>
          <div className="w-6 h-6 rounded-full gradient-accent flex items-center justify-center text-[10px] font-bold">
            RK
          </div>
        </div>
      </div>
    </header>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Sidebar />
        <div className="flex-1">
          <Topbar />
          <main className="p-6">
            <Routes>
              <Route path="/fleet" element={<VehicleRegistry />} />
              <Route path="/maintenance" element={<MaintenanceScreen />} />
              <Route path="*" element={<VehicleRegistry />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}