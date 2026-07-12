"""
TransitOps Backend

Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models

from app.db.base import Base
from app.db.database import engine

# Routers
from app.api.trips import router as trip_router
from app.api.vehicles import router as vehicles_router
from app.api.maintenance import router as maintenance_router
from backend.app.api.fuel_logs import router as fuel_router
from app.api.drivers import router as drivers_router
from app.api.expenses import router as expenses_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="TransitOps API",
    description="Fleet Management System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(trip_router)
app.include_router(vehicles_router)
app.include_router(maintenance_router)
app.include_router( fuel_router)
app.include_router(drivers_router)
app.include_router(expenses_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "message": "🚀 TransitOps API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }