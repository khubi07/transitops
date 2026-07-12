import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, X } from 'lucide-react'
import { api } from '../api/client'
import type { Vehicle, VehicleCreate, VehicleStatus } from '../types/vehicle'

const statusStyles: Record<VehicleStatus, string> = {
  Available: 'bg-[var(--color-available)]/15 text-[var(--color-available)] border-[var(--color-available)]/30',
  'On Trip': 'bg-[var(--color-ontrip)]/15 text-[var(--color-ontrip)] border-[var(--color-ontrip)]/30',
  'In Shop': 'bg-[var(--color-inshop)]/15 text-[var(--color-inshop)] border-[var(--color-inshop)]/30',
  Retired: 'bg-[var(--color-retired)]/15 text-[var(--color-retired)] border-[var(--color-retired)]/30',
}

function StatusBadge({ status }: { status: VehicleStatus }) {
  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${statusStyles[status]}`}>
      {status}
    </span>
  )
}

export default function VehicleRegistry() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [typeFilter, setTypeFilter] = useState('All')
  const [statusFilter, setStatusFilter] = useState('All')
  const [search, setSearch] = useState('')

  const fetchVehicles = async () => {
    setLoading(true)
    try {
      const res = await api.get<Vehicle[]>('/vehicles/')
      setVehicles(res.data)
    } catch (err) {
      console.error('Failed to fetch vehicles', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchVehicles()
  }, [])

  const filtered = vehicles.filter((v) => {
    const matchesType = typeFilter === 'All' || v.type === typeFilter
    const matchesStatus = statusFilter === 'All' || v.status === statusFilter
    const matchesSearch = v.reg_no.toLowerCase().includes(search.toLowerCase())
    return matchesType && matchesStatus && matchesSearch
  })

  const types = ['All', ...Array.from(new Set(vehicles.map((v) => v.type)))]
  const statuses = ['All', 'Available', 'On Trip', 'In Shop', 'Retired']

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Vehicle Registry</h1>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 gradient-accent text-white px-4 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity shadow-lg shadow-orange-500/10"
        >
          <Plus size={16} /> Add Vehicle
        </button>
      </div>

      <div className="flex gap-3 mb-5">
        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
        >
          {types.map((t) => (
            <option key={t} value={t}>Type: {t}</option>
          ))}
        </select>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
        >
          {statuses.map((s) => (
            <option key={s} value={s}>Status: {s}</option>
          ))}
        </select>
        <input
          placeholder="Search reg no..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
        />
      </div>

      <div className="rounded-xl border border-[var(--color-border)] overflow-hidden bg-[var(--color-surface-elevated)]">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--color-border)] text-gray-400 text-xs uppercase tracking-wide">
              <th className="text-left px-5 py-3 font-medium">Reg. No.</th>
              <th className="text-left px-5 py-3 font-medium">Name/Model</th>
              <th className="text-left px-5 py-3 font-medium">Type</th>
              <th className="text-left px-5 py-3 font-medium">Capacity</th>
              <th className="text-left px-5 py-3 font-medium">Odometer</th>
              <th className="text-left px-5 py-3 font-medium">Acq. Cost</th>
              <th className="text-left px-5 py-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={7} className="text-center py-10 text-gray-500">Loading vehicles...</td>
              </tr>
            ) : filtered.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-10 text-gray-500">No vehicles found.</td>
              </tr>
            ) : (
              <AnimatePresence>
                {filtered.map((v, i) => (
                  <motion.tr
                    key={v.id}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.25, delay: i * 0.03 }}
                    className="border-b border-[var(--color-border)] last:border-0 hover:bg-[var(--color-surface-hover)] transition-colors"
                  >
                    <td className="px-5 py-3 font-medium">{v.reg_no}</td>
                    <td className="px-5 py-3">{v.name}</td>
                    <td className="px-5 py-3 text-gray-400">{v.type}</td>
                    <td className="px-5 py-3 text-gray-400">{v.capacity_kg} kg</td>
                    <td className="px-5 py-3 text-gray-400">{v.odometer.toLocaleString()}</td>
                    <td className="px-5 py-3 text-gray-400">₹{v.acquisition_cost.toLocaleString()}</td>
                    <td className="px-5 py-3"><StatusBadge status={v.status} /></td>
                  </motion.tr>
                ))}
              </AnimatePresence>
            )}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-gray-500 mt-4">
        Rule: Registration No. must be unique · Retired/In Shop vehicles are hidden from Trip Dispatcher
      </p>

      <AnimatePresence>
        {showForm && <VehicleFormModal onClose={() => setShowForm(false)} onSaved={fetchVehicles} />}
      </AnimatePresence>
    </motion.div>
  )
}

function VehicleFormModal({ onClose, onSaved }: { onClose: () => void; onSaved: () => void }) {
  const [form, setForm] = useState<VehicleCreate>({
    reg_no: '',
    name: '',
    type: 'Van',
    capacity_kg: 0,
    odometer: 0,
    acquisition_cost: 0,
  })
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  const handleSubmit = async () => {
    setError('')
    if (!form.reg_no || !form.name || form.capacity_kg <= 0) {
      setError('Please fill in registration number, name, and a valid capacity.')
      return
    }
    setSaving(true)
    try {
      await api.post('/vehicles/', form)
      onSaved()
      onClose()
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to save vehicle.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 10 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 10 }}
        transition={{ duration: 0.2 }}
        onClick={(e) => e.stopPropagation()}
        className="bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl p-6 w-full max-w-md"
      >
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-lg font-semibold">Add Vehicle</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X size={18} />
          </button>
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-xs text-gray-400 mb-1 block">Registration Number</label>
            <input
              value={form.reg_no}
              onChange={(e) => setForm({ ...form, reg_no: e.target.value })}
              placeholder="GJ01AB1234"
              className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
            />
          </div>
          <div>
            <label className="text-xs text-gray-400 mb-1 block">Name / Model</label>
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="Van-05"
              className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Type</label>
              <select
                value={form.type}
                onChange={(e) => setForm({ ...form, type: e.target.value })}
                className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
              >
                <option>Van</option>
                <option>Truck</option>
                <option>Mini</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Capacity (kg)</label>
              <input
                type="number"
                value={form.capacity_kg}
                onChange={(e) => setForm({ ...form, capacity_kg: Number(e.target.value) })}
                className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Odometer</label>
              <input
                type="number"
                value={form.odometer}
                onChange={(e) => setForm({ ...form, odometer: Number(e.target.value) })}
                className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
              />
            </div>
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Acquisition Cost</label>
              <input
                type="number"
                value={form.acquisition_cost}
                onChange={(e) => setForm({ ...form, acquisition_cost: Number(e.target.value) })}
                className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
              />
            </div>
          </div>

          {error && <p className="text-xs text-red-400">{error}</p>}

          <button
            onClick={handleSubmit}
            disabled={saving}
            className="w-full gradient-accent text-white rounded-lg py-2.5 text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50 mt-2"
          >
            {saving ? 'Saving...' : 'Save Vehicle'}
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}