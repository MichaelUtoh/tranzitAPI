from typing import Optional
from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.models.accounts import User
from core.models.vehicles import Manifest, Vehicle
from core.schemas.accounts import Level
from core.schemas.vehicles import (
    ManifestCreateUpdateSchema,
    VehicleCreate,
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


def create_manifest_(data: ManifestCreateUpdateSchema, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
    driver = (
        db.query(User).filter(User.id == data.driver_id, User.level == "driver").first()
    )

    if not vehicle or not driver:
        raise HTTPException(status_code=400, detail="Not found")

    manifest = Manifest(
        vehicle_id=data.vehicle_id,
        driver_id=data.driver_id,
        destination=data.destination,
        timestamp=datetime.now().date(),
    )

    db.add(manifest)
    db.commit()
    db.refresh(manifest)
    return manifest


def search_manifests_(id: Optional[int] = None, db: Session = Depends(get_db)):
    if id:
        return db.query(Manifest).filter(Manifest.id == id).first()
    return db.query(Manifest).all()


def update_manifest_(
    id: int, data: ManifestCreateUpdateSchema, db: Session = Depends(get_db)
):
    # print(id, data, db)
    driver = (
        db.query(User)
        .filter(User.id == data.driver_id, User.level == Level.DRIVER)
        .first()
    )
    if not driver:
        raise HTTPException(status_code=400, detail="Not found")

    db.query(Manifest).filter(Manifest.id == id).update(
        {
            "driver_id": data.driver_id,
            "vehicle_id": data.vehicle_id,
            "destination": data.destination,
        },
        synchronize_session=False,
    )
    db.commit()