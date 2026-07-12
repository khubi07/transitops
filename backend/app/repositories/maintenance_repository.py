from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance
from app.models.enums import MaintenanceStatus
from app.schemas.maintenance import MaintenanceCreate


class MaintenanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Maintenance]:
        return self.db.query(Maintenance).all()

    def get_by_id(self, maintenance_id: int) -> Maintenance | None:
        return self.db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()

    def create(self, data: MaintenanceCreate) -> Maintenance:
        record = Maintenance(**data.model_dump(), status=MaintenanceStatus.ACTIVE)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def close(self, record: Maintenance) -> Maintenance:
        record.status = MaintenanceStatus.CLOSED
        self.db.commit()
        self.db.refresh(record)
        return record