export type VehicleStatus = 'Available' | 'On Trip' | 'In Shop' | 'Retired'

export interface Vehicle {
  id: number
  reg_no: string
  name: string
  type: string
  capacity_kg: number
  odometer: number
  acquisition_cost: number
  status: VehicleStatus
}

export interface VehicleCreate {
  reg_no: string
  name: string
  type: string
  capacity_kg: number
  odometer: number
  acquisition_cost: number
}