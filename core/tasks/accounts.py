from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas.accounts import (
    Level,
    PassengerCreateSchema,
    Status,
    UserBankDetailSchema,
    UserStatusUpdateSchema,
    UserUpdateSchema,
)
from core.models.accounts import Passenger, User


def update_user_(
    id: int,
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
            "level": data.level,
            "status": data.status,
        },
        synchronize_session=False,
    )
    db.commit()


def update_user_status_(
    id: int, data: UserStatusUpdateSchema, db: Session = Depends(get_db)
):
    if not db.query(User).filter(User.id == id).first():
        raise HTTPException(status_code=403, detail="Not found")

    db.query(User).filter(User.id == id).update({"status": data.status})
    db.commit()


def update_user_bank_details_(
    id: int,
    data: UserBankDetailSchema,
    db: Session = Depends(get_db),
):
    db.query(User).filter(User.id == id).update(
        {
            "bank": data.bank,
            "account_no": data.account_no,
            "bvn": data.bvn,
        }
    )
    db.commit()


def create_passenger_(data: PassengerCreateSchema, db: Session = Depends(get_db)):
    if db.query(Passenger).filter(Passenger.email == data.email).first():
        raise HTTPException(
            status_code=400, detail="An account with this email already exists"
        )

    passenger = Passenger(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        phone_no_1=data.phone_no_1,
        phone_no_2=data.phone_no_2,
        gender=data.gender,
        title=data.title,
        next_of_kin_first_name=data.next_of_kin_first_name,
        next_of_kin_last_name=data.next_of_kin_last_name,
        next_of_kin_phone_no=data.next_of_kin_phone_no,
        date_joined=datetime.now().date(),
    )
    db.add(passenger)
    db.commit()
    db.refresh(passenger)
    return passenger
