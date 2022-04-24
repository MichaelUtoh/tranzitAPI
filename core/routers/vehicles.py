from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from utils import get_current_user

from core.database import get_db
from core.tasks.vehicles import create_vehicle
from core.models.vehicles import Manifest, Vehicle
from core.schemas.vehicles import (
    ManifestCreate,
    VehicleBasic,
    VehicleCreate,
    VehicleMake,
    VehicleModel,
    VehicleType,
)

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=List[VehicleBasic],
    status_code=status.HTTP_200_OK,
    tags=["vehicles"],
)
def fetch_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()


@router.get("/{id}", status_code=status.HTTP_200_OK, tags=["vehicles"])
def fetch_vehicle(id: int, db: Session = Depends(get_db)):
    return db.query(Vehicle).filter(Vehicle.id == id).first()


@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    tags=["vehicles"],
)
def add_vehicle(
    data: VehicleCreate,
    type: VehicleType,
    make: VehicleMake,
    model: VehicleModel,
    db: Session = Depends(get_db),
):
    is_registered = db.query(Vehicle).filter(Vehicle.reg_id == data.reg_id).first()
    if is_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A vehicle with this registration number already exists.",
        )
    new_vehicle = create_vehicle(data, type, make, model, db)
    return new_vehicle


@router.patch("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT, tags=["vehicles"])
def remove_vehicle(id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == id)
    vehicle.delete()
    db.commit()
    db.refresh()
    return


@router.post(
    "/{id}/manifests/new",
    status_code=status.HTTP_201_CREATED,
    tags=["vehicles"],
)
def add_manifest(id: int, req: ManifestCreate):
    return req
