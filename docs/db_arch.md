# Database Architecture Guide

> This document defines the database architecture and coding conventions for the TransitOps project.
>
> Every team member **must follow these guidelines** to maintain consistency and avoid merge conflicts.

---

# 1. Database Philosophy

- PostgreSQL (Production)
- SQLAlchemy 2.0 ORM
- Alembic for migrations
- One shared database schema
- No duplicate data
- Normalize whenever possible

---

# 2. Database Ownership

The database schema is shared across the team.

Do NOT directly modify

- Existing tables
- Existing relationships
- Existing enums

Instead

1. Discuss
2. Update ER Diagram
3. Generate Migration
4. Everyone pulls latest changes

---

# 3. Base Model

Every table MUST inherit

```python
class Model(Base, BaseModel)
```

Never manually create

- id
- created_at
- updated_at

These already exist inside BaseModel.

---

# 4. Naming Convention

## Table Names

Plural

Examples

vehicles

drivers

trips

maintenance

fuel_logs

expenses

---

## Model Names

Singular

Vehicle

Driver

Trip

FuelLog

Expense

---

## Foreign Keys

Use

vehicle_id

driver_id

trip_id

NOT

vehicleID

driverID

vehicleId

---

## Relationship Names

Use plural for collections

```python
vehicle.trips
```

Use singular for single object

```python
trip.vehicle
```

---

# 5. SQLAlchemy Style

Use SQLAlchemy 2.0 style only.

Example

```python
name: Mapped[str] = mapped_column(...)
```

Never use

```python
Column(...)
```

---

# 6. Enums

Never hardcode status strings.

Use

VehicleStatus.AVAILABLE

TripStatus.DRAFT

DriverStatus.ON_TRIP

Never

"Available"

"Completed"

"Draft"

---

# 7. Relationships

Current ER Diagram

Vehicle

1 ------ M Trips

Vehicle

1 ------ M Maintenance

Vehicle

1 ------ M FuelLogs

Vehicle

1 ------ M Expenses

Driver

1 ------ M Trips

Trip

1 ------ M FuelLogs

Trip

1 ------ M Expenses (Optional)

---

# 8. Relationship Rules

Vehicle

↓

Trip

RESTRICT

Driver

↓

Trip

RESTRICT

Vehicle

↓

Maintenance

RESTRICT

Vehicle

↓

FuelLog

RESTRICT

Vehicle

↓

Expense

RESTRICT

Trip

↓

FuelLog

CASCADE

Trip

↓

Expense

SET NULL

---

# 9. Nullable Rules

Ask yourself

"Can this value be unknown?"

Example

completion_time

YES

nullable=True

Example

vehicle_id

NO

nullable=False

---

# 10. Duplicate Data

Avoid duplicate information.

Example

FuelLog

Should store

trip_id

NOT

trip_id

vehicle_id

Vehicle can already be obtained from Trip.

---

# 11. Model Order

Every model should follow this structure.

```python
Imports

↓

Class

↓

__tablename__

↓

Columns

↓

Relationships

↓

__repr__()
```

Keep every model consistent.

---

# 12. New Fields

Need a new column?

DO NOT directly add it.

Steps

1. Discuss with team
2. Update ER Diagram
3. Update SQLAlchemy Model
4. Generate Alembic Migration
5. Commit
6. Everyone Pull

---

# 13. Deleting Data

Never permanently delete

Vehicle

Driver

Trip

Maintenance

FuelLog

Expense

Instead

Update status whenever possible.

History is valuable.

---

# 14. Indexes

Use indexes for

registration_number

license_number

email

Do NOT create unnecessary indexes.

---

# 15. Constraints

Use

unique=True

where appropriate.

Examples

registration_number

license_number

email

---

# 16. Code Style

One field per line.

Example

```python
name: Mapped[str] = mapped_column(
    String(100),
    nullable=False
)
```

Avoid long single-line declarations.

---

# 17. Comments

Every model must begin with

Purpose

Responsibilities

Relationships

Example

```python
"""
Vehicle Model

Represents every fleet vehicle.

Responsibilities

✓ Store vehicle details

✓ Maintain vehicle status

Relationships

Vehicle -> Trips

Vehicle -> Maintenance

Vehicle -> FuelLogs
"""
```

---

# 18. Golden Rule

Before changing the database ask:

Will this change affect another module?

If yes,

Discuss first.

If no,

Proceed.
