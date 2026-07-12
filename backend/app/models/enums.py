"""
Application Enums

Central place for all status values.

Using Enums avoids:
-------------------
- Typing mistakes
- Magic strings
- Inconsistent values

NOTE: this file is the shared, canonical version (as pushed by
Member 1 / teammate). It replaces the module-local enums.py that
previously only had DriverStatus + ExpenseCategory.
"""

from enum import Enum


class VehicleStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    IN_SHOP = "In Shop"
    RETIRED = "Retired"


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