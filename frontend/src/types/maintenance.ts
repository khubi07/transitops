export type MaintenanceStatus = 'Active' | 'Closed'

export interface Maintenance {
  id: number
  vehicle_id: number
  service_type: string
  cost: number
  service_date: string
  status: MaintenanceStatus
}

export interface MaintenanceCreate {
  vehicle_id: number
  service_type: string
  cost: number
  service_date: string
}