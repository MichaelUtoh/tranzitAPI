from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from ..database import Base, engine
from ..models.vehicles import Manifest, Vehicle
from ..schemas.vehicles import (
    ManifestCreate,
    VehicleBasic,
    VehicleCreate,
)
from ..services import create_vehicle, get_db


router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
    responses={404: {"description": "Not found"}},
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


@router.post("/new", status_code=status.HTTP_201_CREATED, tags=["vehicles"])
def add_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = create_vehicle(data, db)
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
