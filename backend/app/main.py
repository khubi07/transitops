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
from app.api import vehicles, maintenance

app = FastAPI(title="TransitOps API")

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

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TransitOps API",
    description="Fleet Management System",
    version="1.0.0"
)

# Register routers
app.include_router(trip_router)
app.include_router(vehicles.router)
app.include_router(maintenance.router)


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