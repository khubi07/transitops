from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleService:
    def __init__(self, db: Session):
        self.repository = VehicleRepository(db)

    def list_vehicles(self):
        return self.repository.get_all()

    def create_vehicle(self, data: VehicleCreate):
        if self.repository.get_by_reg_no(data.reg_no):
            raise HTTPException(400, "Registration number already exists")
        return self.repository.create(data)

    def update_vehicle(self, vehicle_id: int, data: VehicleUpdate):
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(404, "Vehicle not found")
        return self.repository.update(vehicle, data)

    def delete_vehicle(self, vehicle_id: int):
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(404, "Vehicle not found")
        self.repository.delete(vehicle)