import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, X, CheckCircle2 } from 'lucide-react'
import { api } from '../api/client'
import type { Maintenance, MaintenanceCreate } from '../types/maintenance'
import type { Vehicle } from '../types/vehicle'

export default function MaintenanceScreen() {
  const [records, setRecords] = useState<Maintenance[]>([])
  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)

  const fetchAll = async () => {
    setLoading(true)
    try {
      const [recRes, vehRes] = await Promise.all([
        api.get<Maintenance[]>('/maintenance/'),
        api.get<Vehicle[]>('/vehicles/'),
      ])
      setRecords(recRes.data)
      setVehicles(vehRes.data)
    } catch (err) {
      console.error('Failed to fetch maintenance data', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAll()
  }, [])

  const vehicleName = (id: number) => {
    const v = vehicles.find((v) => v.id === id)
    return v ? `${v.reg_no} — ${v.name}` : `#${id}`
  }

  const closeRecord = async (id: number) => {
    try {
      await api.patch(`/maintenance/${id}/close`)
      fetchAll()
    } catch (err) {
      console.error('Failed to close maintenance record', err)
    }
  }

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Maintenance</h1>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 gradient-accent text-white px-4 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity shadow-lg shadow-orange-500/10"
        >
          <Plus size={16} /> Log Service
        </button>
      </div>

      <div className="rounded-xl border border-[var(--color-border)] overflow-hidden bg-[var(--color-surface-elevated)]">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--color-border)] text-gray-400 text-xs uppercase tracking-wide">
              <th className="text-left px-5 py-3 font-medium">Vehicle</th>
              <th className="text-left px-5 py-3 font-medium">Service Type</th>
              <th className="text-left px-5 py-3 font-medium">Date</th>
              <th className="text-left px-5 py-3 font-medium">Cost</th>
              <th className="text-left px-5 py-3 font-medium">Status</th>
              <th className="text-left px-5 py-3 font-medium">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="text-center py-10 text-gray-500">Loading records...</td></tr>
            ) : records.length === 0 ? (
              <tr><td colSpan={6} className="text-center py-10 text-gray-500">No maintenance records yet.</td></tr>
            ) : (
              <AnimatePresence>
                {records.map((r, i) => (
                  <motion.tr
                    key={r.id}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.25, delay: i * 0.03 }}
                    className="border-b border-[var(--color-border)] last:border-0 hover:bg-[var(--color-surface-hover)] transition-colors"
                  >
                    <td className="px-5 py-3 font-medium">{vehicleName(r.vehicle_id)}</td>
                    <td className="px-5 py-3 text-gray-400">{r.service_type}</td>
                    <td className="px-5 py-3 text-gray-400">{r.service_date}</td>
                    <td className="px-5 py-3 text-gray-400">₹{r.cost.toLocaleString()}</td>
                    <td className="px-5 py-3">
                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                          r.status === 'Active'
                            ? 'bg-[var(--color-inshop)]/15 text-[var(--color-inshop)] border-[var(--color-inshop)]/30'
                            : 'bg-[var(--color-available)]/15 text-[var(--color-available)] border-[var(--color-available)]/30'
                        }`}
                      >
                        {r.status}
                      </span>
                    </td>
                    <td className="px-5 py-3">
                      {r.status === 'Active' && (
                        <button
                          onClick={() => closeRecord(r.id)}
                          className="flex items-center gap-1 text-xs text-[var(--color-available)] hover:opacity-80 transition-opacity"
                        >
                          <CheckCircle2 size={14} /> Mark Closed
                        </button>
                      )}
                    </td>
                  </motion.tr>
                ))}
              </AnimatePresence>
            )}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-gray-500 mt-4">
        Rule: Logging active maintenance moves the vehicle to In Shop · Closing it restores Available (unless Retired)
      </p>

      <AnimatePresence>
        {showForm && (
          <MaintenanceFormModal vehicles={vehicles} onClose={() => setShowForm(false)} onSaved={fetchAll} />
        )}
      </AnimatePresence>
    </motion.div>
  )
}

function MaintenanceFormModal({
  vehicles,
  onClose,
  onSaved,
}: {
  vehicles: Vehicle[]
  onClose: () => void
  onSaved: () => void
}) {
  const eligibleVehicles = vehicles.filter((v) => v.status !== 'Retired')
  const [form, setForm] = useState<MaintenanceCreate>({
    vehicle_id: eligibleVehicles[0]?.id ?? 0,
    service_type: '',
    cost: 0,
    service_date: new Date().toISOString().slice(0, 10),
  })
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  const handleSubmit = async () => {
    setError('')
    if (!form.vehicle_id || !form.service_type || form.cost <= 0) {
      setError('Please select a vehicle, service type, and a valid cost.')
      return
    }
    setSaving(true)
    try {
      await api.post('/maintenance/', form)
      onSaved()
      onClose()
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to save record.')
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
          <h2 className="text-lg font-semibold">Log Maintenance</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
            <X size={18} />
          </button>
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-xs text-gray-400 mb-1 block">Vehicle</label>
            <select
              value={form.vehicle_id}
              onChange={(e) => setForm({ ...form, vehicle_id: Number(e.target.value) })}
              className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
            >
              {eligibleVehicles.map((v) => (
                <option key={v.id} value={v.id}>{v.reg_no} — {v.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-gray-400 mb-1 block">Service Type</label>
            <input
              value={form.service_type}
              onChange={(e) => setForm({ ...form, service_type: e.target.value })}
              placeholder="Oil change, brake repair..."
              className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Cost</label>
              <input
                type="number"
                value={form.cost}
                onChange={(e) => setForm({ ...form, cost: Number(e.target.value) })}
                className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg px-3 py-2 text-sm outline-none focus:border-[var(--color-accent-from)]/50"
              />
            </div>
            <div>
              <label className="text-xs text-gray-400 mb-1 block">Date</label>
              <input
                type="date"
                value={form.service_date}
                onChange={(e) => setForm({ ...form, service_date: e.target.value })}
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
            {saving ? 'Saving...' : 'Save Record'}
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}