from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Vehicle]:
        return self.db.query(Vehicle).all()

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_by_reg_no(self, reg_no: str) -> Vehicle | None:
        return self.db.query(Vehicle).filter(Vehicle.reg_no == reg_no).first()

    def create(self, data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(**data.model_dump())
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def update(self, vehicle: Vehicle, data: VehicleUpdate) -> Vehicle:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(vehicle, key, value)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self.db.delete(vehicle)
        self.db.commit()