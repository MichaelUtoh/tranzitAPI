from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.models.accounts import User
from core.models.vehicles import Manifest, Vehicle, VehicleRating
from core.schemas.vehicles import (
    VehicleBasic,
    VehicleCreate,
    VehicleLocationBasicSchema,
    VehicleLocationDetailsSchema,
    VehicleMake,
    VehicleModel,
    VehicleRatingBasicSchema,
    VehicleRatingCreateSchema,
    VehicleReportSchema,
    VehicleStatus,
    VehicleType,
)
from core.tasks.vehicles import (
    create_or_update_rating_,
    create_or_update_report_,
    create_vehicle_,
    start_trip_,
    fetch_vehicle_ratings_,
    search_vehicles_,
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
    db: Session = Depends(get_db),
):
    is_registered = db.query(Vehicle).filter(Vehicle.reg_id == data.reg_id).first()
    if is_registered:
        raise HTTPException(status_code=400, detail="Not found.")
    new_vehicle = create_vehicle_(data, db)
    return new_vehicle


@router.patch("/{id}/toggle_status", status_code=200)
def toggle_vehicle_status(
    id: int, status: VehicleStatus, db: Session = Depends(get_db)
):
    db.query(Vehicle).filter(Vehicle.id == id).update({"status": status})
    db.commit()
    return db.query(Vehicle).filter(Vehicle.id == id).first()


@router.get(
    "/{id}/ratings",
    response_model=List[VehicleRatingBasicSchema],
    status_code=200,
)
def fetch_vehicle_ratings(id: int, db: Session = Depends(get_db)):
    rating_data = fetch_vehicle_ratings_(id, db)
    return rating_data


@router.patch(
    "/{id}/rating",
    response_model=VehicleRatingBasicSchema,
    status_code=201,
)
def create_vehicle_rating(
    id: int, data: VehicleRatingCreateSchema, db: Session = Depends(get_db)
):
    rating_data = create_or_update_rating_(id, data, db)
    return rating_data


@router.patch("/{id}/report", status_code=200)
def create_vehicle_report(
    id: int,
    passenger_id: int,
    data: VehicleReportSchema,
    db: Session = Depends(get_db),
):
    report_data = create_or_update_report_(id, passenger_id, data, db)
    return


@router.post(
    "/{id}/start_trip",
    response_model=VehicleLocationDetailsSchema,
    status_code=200,
)
def start_trip(
    id: int,
    data: VehicleLocationBasicSchema,
    db: Session = Depends(get_db),
):
    vehicle_data = start_trip_(id, data, db)
    return vehicle_data


@router.post(
    "/{id}/end_trip",
    response_model=VehicleLocationDetailsSchema,
    status_code=200,
)
def end_trip(
    id: int,
    data: VehicleLocationBasicSchema,
    db: Session = Depends(get_db),
):
    vehicle_data = None
    return vehicle_data
