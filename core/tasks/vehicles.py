from uuid import uuid4 as uuidlib
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.models.vehicles import Vehicle
from core.schemas.vehicles import VehicleCreate


def create_vehicle(data: VehicleCreate, type, make, model, db: Session):
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong."
        )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle
