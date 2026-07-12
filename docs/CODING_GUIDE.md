# TransitOps Backend Guide

## Folder Purpose

api/
Receives HTTP requests

services/
Contains business logic

repositories/
Only interacts with database

models/
SQLAlchemy models

schemas/
Pydantic request/response models

---

## Model Order

1. Imports

2. Class

3. __tablename__

4. Columns

5. Relationships

6. __repr__()

---

## Naming Convention

Vehicle

vehicle.py

VehicleCreate

VehicleResponse

VehicleService

VehicleRepository

vehicles.py