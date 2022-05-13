from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.models.accounts import Passenger
from core.models.vehicles import (
    Location,
    Manifest,
    Vehicle,
    VehicleRating,
    VehicleReport,
)
from core.schemas.vehicles import (
    VehicleCreate,
    VehicleLocationBasicSchema,
    VehicleRatingCreateSchema,
    VehicleReportBasicSchema,
    VehicleStatus,
)


def create_vehicle_(data: VehicleCreate, db: Session):
    is_registered = db.query(Vehicle).filter(Vehicle.reg_id == data.reg_id).first()
    if is_registered:
        raise HTTPException(
            status_code=400,
            detail="Vehicle with this given registration number exists.",
        )
    new_vehicle = Vehicle(
        type=data.type,
        make=data.make,
        model=data.model,
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


def create_or_update_report_(
    id: int,
    passenger_id: int,
    data: VehicleReportBasicSchema,
    db: Session = Depends(get_db),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    passenger = db.query(Passenger).filter(Passenger.id == passenger_id).first()

    if not vehicle or not passenger:
        raise HTTPException(status_code=400, detail="Not found.")

    report = VehicleReport(
        vehicle_id=vehicle.id,
        passenger_id=passenger.id,
        detail=data.detail,
        timestamp=datetime.now().now().date(),
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


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


def add_vehicle_location_(id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Not found")

    location = Location(
        departure_terminal=None,
        destination_terminal=None,
        current_latitude=None,
        current_longitude=None,
        started_trip=None,
        ended_trip=None,
        timestamp=datetime.now().date(),
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return db


def start_trip_(id: int, data, db: Session = Depends(get_db)):
    """
    To start trip, add location details to vehicle
    """
    manifest = db.query(Manifest).filter(Manifest.id == id).first()
    if not manifest:
        raise HTTPException(status_code=400, detail="Not found")

    location = Location(
        departure_terminal=data.departure_terminal,
        destination_terminal=data.destination_terminal,
        current_trip=True,
        started_trip=True,
        ended_trip=False,
        manifest_id=manifest.id,
        timestamp=datetime.now().date(),
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def end_trip_(
    location_id: int,
    data: VehicleLocationBasicSchema,
    db: Session = Depends(get_db),
):
    pass
