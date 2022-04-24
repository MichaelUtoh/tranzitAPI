from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from utils import get_current_user

from core.database import get_db
from core.tasks.vehicles import create, search
from core.models.vehicles import Manifest, Vehicle
from core.schemas.vehicles import (
    ManifestCreate,
    VehicleBasic,
    VehicleCreate,
    VehicleMake,
    VehicleModel,
    VehicleStatus,
    VehicleType,
)

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
    # responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get("", status_code=200)
def search_vehicles(
    id: Optional[int] = None,
    reg_id: Optional[str] = None,
    status: Optional[VehicleStatus] = None,
    db: Session = Depends(get_db),
):
    vehicles = db.query(Vehicle).all()
    if not vehicles:
        raise HTTPException(status_code=400, detail="Not found.")
    vehicles = search(id, reg_id, status, db)
    return vehicles


@router.post("/new", status_code=200)
def add_vehicle(
    data: VehicleCreate,
    type: VehicleType,
    make: VehicleMake,
    model: VehicleModel,
    db: Session = Depends(get_db),
):
    is_registered = db.query(Vehicle).filter(Vehicle.reg_id == data.reg_id).first()
    if is_registered:
        raise HTTPException(status_code=400, detail="Not found.")
    new_vehicle = create(data, type, make, model, db)
    return new_vehicle


@router.patch("/{id}/toggle_status", status_code=200)
def toggle_vehicle_status(
    id: int, status: VehicleStatus, db: Session = Depends(get_db)
):
    db.query(Vehicle).filter(Vehicle.id == id).update({"status": status})
    db.commit()
    return db.query(Vehicle).filter(Vehicle.id == id).first()


@router.post("/{id}/manifests/new", status_code=201)
def add_manifest(id: int, req: ManifestCreate):
    return req


@router.post("/{id}/report", response_model=VehicleBasic, status_code=200)
def report_vehicle(id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Not found.")
    return vehicle
