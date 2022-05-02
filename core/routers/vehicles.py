from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.models.accounts import User
from core.models.vehicles import Manifest, Vehicle
from core.schemas.vehicles import (
    ManifestCreateUpdateSchema,
    ManifestPassengerSchema,
    VehicleBasic,
    VehicleCreate,
    VehicleMake,
    VehicleModel,
    VehicleStatus,
    VehicleType,
)
from core.tasks.vehicles import (
    create_manifest_,
    create_vehicle_,
    depopulate_manifest_,
    populate_manifest_,
    search_vehicles_,
    search_manifests_,
    update_manifest_,
)
from core.utils import get_current_user


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
    # current_user: User = Depends(get_current_user),
):
    vehicles = db.query(Vehicle).all()
    if not vehicles:
        raise HTTPException(status_code=400, detail="Not found.")
    vehicles = search_vehicles_(id, reg_id, status, db)
    return vehicles


@router.post("/create", status_code=200)
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
    new_vehicle = create_vehicle_(data, type, make, model, db)
    return new_vehicle


@router.patch("/{id}/toggle_status", status_code=200)
def toggle_vehicle_status(
    id: int, status: VehicleStatus, db: Session = Depends(get_db)
):
    db.query(Vehicle).filter(Vehicle.id == id).update({"status": status})
    db.commit()
    return db.query(Vehicle).filter(Vehicle.id == id).first()


@router.post("/{id}/report", response_model=VehicleBasic, status_code=200)
def report_vehicle(id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Not found.")
    return vehicle
