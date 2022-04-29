from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas.accounts import Level, PassengerCreateSchema, Status, UserUpdateSchema
from core.models.accounts import Passenger, User


def create_passenger(data: PassengerCreateSchema, db: Session = Depends(get_db)):
    passenger = Passenger(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        phone_no=data.phone_no,
        gender=data.gender,
        next_of_kin_first_name=data.next_of_kin_first_name,
        next_of_kin_last_name=data.next_of_kin_last_name,
        next_of_kin_phone_no=data.next_of_kin_phone_no,
        date_joined=datetime.now().date(),
    )
    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return passenger


def update_user_task(
    id: int,
    level: Level,
    status: Status,
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    if not db.query(User).filter(User.id == id).first():
        raise HTTPException(status_code=403, detail="Not found")
    db.query(User).filter(User.id == id).update(
        {
            "first_name": data.first_name,
            "middle_name": data.middle_name,
            "last_name": data.last_name,
            "last_login": datetime.now(),
            "phone_no_1": data.phone_no_1,
            "phone_no_2": data.phone_no_2,
            "gender": data.gender,
            "marital_status": data.marital_status,
            "nationality": data.nationality,
            "next_of_kin_first_name": data.next_of_kin_first_name,
            "next_of_kin_last_name": data.next_of_kin_last_name,
            "level": level,
            "status": status,
        },
        synchronize_session=False,
    )
    db.commit()
