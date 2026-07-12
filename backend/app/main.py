from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base
from app.api import vehicles, maintenance

app = FastAPI(title="TransitOps API")

Base.metadata.create_all(bind=engine)

app.include_router(vehicles.router)
app.include_router(maintenance.router)


@app.get("/")
def root():
    return {"status": "TransitOps API running"}