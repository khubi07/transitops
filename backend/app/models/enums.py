<<<<<<< HEAD
import enum


class VehicleStatus(str, enum.Enum):
=======
"""
Application Enums

Central place for all status values.

Using Enums avoids:
-------------------
- Typing mistakes
- Magic strings
- Inconsistent values
"""

from enum import Enum


class VehicleStatus(str, Enum):
>>>>>>> main
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    IN_SHOP = "In Shop"
    RETIRED = "Retired"


<<<<<<< HEAD
class MaintenanceStatus(str, enum.Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"
=======
class DriverStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    OFF_DUTY = "Off Duty"
    SUSPENDED = "Suspended"


class TripStatus(str, Enum):
    DRAFT = "Draft"
    DISPATCHED = "Dispatched"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class MaintenanceStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class ExpenseType(str, Enum):
    FUEL = "Fuel"
    MAINTENANCE = "Maintenance"
    TOLL = "Toll"
    PARKING = "Parking"
    INSURANCE = "Insurance"
    OTHER = "Other"
>>>>>>> main
