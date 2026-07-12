import enum


class VehicleStatus(str, enum.Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    IN_SHOP = "In Shop"
    RETIRED = "Retired"


class MaintenanceStatus(str, enum.Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"