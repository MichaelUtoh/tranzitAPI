from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas.accounts import (
    Level,
    PassengerCreateSchema,
    Status,
    UserBankDetailSchema,
    UserDocsSchema,
    UserLevelUpdateSchema,
    UserStatusUpdateSchema,
    UserUpdateSchema,
)
from core.models.accounts import Passenger, User, UserDocument


def fetch_user_details_(
    id: Optional[int],
    email: Optional[EmailStr] = None,
    db: Session = Depends(get_db),
):
    # TODO Only admin authorization for this endpoint
    user = None
    if id:
        user = db.query(User).filter(User.id == id).first()

    elif email and not id:
        user = db.query(User).filter(User.email == email).first()

    return user


def update_user_(
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=403, detail="Not found")

    db.query(User).filter(User.email == data.email).update(
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
            "next_of_kin_phone_no": data.next_of_kin_phone_no,
            "level": data.level,
            "status": Status.ACTIVE,
        },
        synchronize_session=False,
    )
    db.commit()
    return user


def update_user_status_(
    id: int,
    data: UserStatusUpdateSchema,
    db: Session = Depends(get_db),
):
    # TODO Only admin authorization for this endpoint
    if not db.query(User).filter(User.id == id).first():
        raise HTTPException(status_code=403, detail="Not found")

    db.query(User).filter(User.id == id).update({"status": data.status})
    db.commit()


def update_user_level_(
    id: int,
    data: UserLevelUpdateSchema,
    db: Session = Depends(get_db),
):
    # TODO Only admin authorization for this endpoint
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=403, detail="Not found")

    db.query(User).filter(User.id == id).update({"level": data.level})
    db.commit()
    return user


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


def add_employee_document_(
    id: int,
    data: UserDocsSchema,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=400, detail="Not found.")

    if not user.first_name or not user.status or not user.level:
        raise HTTPException(status_code=400, detail="Incomplete registration details.")

    document = UserDocument(
        user_id=user.id,
        document_type=data.document_type,
        document_no=data.document_no,
        document_expiry_date=data.document_expiry_date,
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    return document


# Passenger
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
