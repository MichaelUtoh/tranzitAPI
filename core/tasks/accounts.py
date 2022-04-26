from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas.accounts import PassengerCreateSchema, Status
from core.models.accounts import Passenger, User


def search(
    id: Optional[int] = None,
    email: Optional[str] = None,
    status: Optional[Status] = None,
    db: Session = Depends(get_db),
):
    res = None
    if id and not (email and status):
        res = db.query(User).filter(User.id == id).first()
    elif email and not id and not status:
        res = db.query(User).filter(User.email == email).first()
    elif status and not id and not email:
        res = db.query(User).filter(User.status == status).first()
    return res


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
