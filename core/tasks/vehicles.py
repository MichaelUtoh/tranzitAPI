from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.models.vehicles import Vehicle, VehicleRating, VehicleReport
from core.schemas.vehicles import (
    VehicleCreate,
    VehicleRatingCreateSchema,
    VehicleStatus,
)


def create_vehicle_(data: VehicleCreate, type, make, model, db: Session):
    new_vehicle = Vehicle(
        type=type,
        make=make,
        model=model,
        reg_id=data.reg_id,
        color=data.color,
        maintenance_due_date=data.maintenance_due_date,
        timestamp=datetime.now().date(),
    )
    if not new_vehicle:
        raise HTTPException(status_code=400, detail="Something went wrong.")
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle


def search_vehicles_(
    id: Optional[int] = None,
    reg_id: Optional[str] = None,
    status: Optional[VehicleStatus] = None,
    db: Session = Depends(get_db),
):
    res = db.query(Vehicle).all()
    if id and reg_id:
        res = (
            db.query(Vehicle)
            .filter(Vehicle.id == id)
            .filter(Vehicle.reg_id == reg_id)
            .first()
        )
    elif id and status and not reg_id:
        res = (
            db.query(Vehicle)
            .filter(Vehicle.id == id)
            .filter(Vehicle.status == status)
            .first()
        )
    elif id and not reg_id:
        res = db.query(Vehicle).filter(Vehicle.id == id).first()
    elif reg_id and not id and not status:
        res = db.query(Vehicle).filter(Vehicle.reg_id == reg_id).first()
    elif status and not id and not reg_id:
        res = db.query(Vehicle).filter(Vehicle.status == status).all()
    return res


def create_or_update_reoprt_(id: int, data: VehicleReport, db: Session):
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Not found.")

    report = db.query(VehicleReport).filter(VehicleReport.vehicle_id == vehicle.id)
    pass


def create_or_update_rating_(
    id: int, data: VehicleRatingCreateSchema, db: Session = Depends(get_db)
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    rating = (
        db.query(VehicleRating)
        .filter(
            VehicleRating.vehicle_id == vehicle.id,
            VehicleRating.passenger_id == data.passenger_id,
        )
        .first()
    )
    if rating:
        db.query(VehicleRating).filter(
            VehicleRating.vehicle_id == vehicle.id,
            VehicleRating.passenger_id == data.passenger_id,
        ).update({"rating": data.rating, "timestamp": datetime.now().date()})
        db.commit()
    else:
        rating = VehicleRating(
            vehicle_id=vehicle.id,
            passenger_id=data.passenger_id,
            rating=data.rating,
            timestamp=datetime.now().date(),
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
    return rating


def fetch_vehicle_ratings_(id: Optional[int] = None, db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Not found")

    return vehicle.ratings
