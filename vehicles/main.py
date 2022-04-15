from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine
from .models import Manifest, Vehicle
from .schemas import (
    ManifestCreate,
    VehicleBasic,
    VehicleCreate,
    VehicleMake,
    VehicleModel,
    VehicleType,
)
from .services import create_vehicle

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/vehicles",
    response_model=List[VehicleBasic],
    status_code=status.HTTP_200_OK,
    tags=["vehicles"],
)
def fetch_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()


@app.get("/vehicles/{id}", status_code=status.HTTP_200_OK, tags=["vehicles"])
def fetch_vehicle(id: int, db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.id == id).first()


@app.post("/vehicles/new", status_code=status.HTTP_201_CREATED, tags=["vehicles"])
def add_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = create_vehicle(data, db)
    return new_vehicle


@app.post(
    "vehicles/{id}/manifests/new",
    status_code=status.HTTP_201_CREATED,
    tags=["vehicles"],
)
def add_manifest(id: int, req: ManifestCreate):
    return req
