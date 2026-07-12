from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.maintenance_repository import MaintenanceRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.models.enums import VehicleStatus
from app.schemas.maintenance import MaintenanceCreate


class MaintenanceService:
    def __init__(self, db: Session):
        self.repository = MaintenanceRepository(db)
        self.vehicle_repository = VehicleRepository(db)
        self.db = db

    def create_maintenance(self, data: MaintenanceCreate):
        vehicle = self.vehicle_repository.get_by_id(data.vehicle_id)
        if not vehicle:
            raise HTTPException(404, "Vehicle not found")
        if vehicle.status == VehicleStatus.RETIRED:
            raise HTTPException(400, "Cannot log maintenance for a retired vehicle")

        record = self.repository.create(data)
        vehicle.status = VehicleStatus.IN_SHOP
        self.db.commit()
        return record

    def close_maintenance(self, maintenance_id: int):
        record = self.repository.get_by_id(maintenance_id)
        if not record:
            raise HTTPException(404, "Maintenance record not found")

        record = self.repository.close(record)
        vehicle = self.vehicle_repository.get_by_id(record.vehicle_id)
        if vehicle.status != VehicleStatus.RETIRED:
            vehicle.status = VehicleStatus.AVAILABLE
            self.db.commit()
        return record