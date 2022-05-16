from datetime import datetime
from os import stat
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.models.accounts import Passenger, User
from core.schemas.accounts import (
    Level,
    PassengerBasicSchema,
    Status,
    UserBankDetailSchema,
    UserBasicSchema,
    PassengerCreateSchema,
    UserDetailsSchema,
    UserStatusUpdateSchema,
    UserUpdateSchema,
)
from core.database import get_db
from core.tasks.accounts import (
    create_passenger_,
    fetch_user_details_,
    update_user_,
    update_user_bank_details_,
    update_user_status_,
)
from core.utils import get_current_user


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)],
)


@router.get("/user_details", response_model=UserDetailsSchema)
def get_user(
    id: Optional[int] = None,
    email: Optional[EmailStr] = None,
    db: Session = Depends(get_db),
):
    user_data = fetch_user_details_(id, email, db)
    return user_data


@router.get("/users", response_model=List[UserBasicSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=400, detail="Not found.")
    return users


@router.patch("/update", response_model=UserBankDetailSchema)
def update_user(
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    update_user_(data, db)
    return


@router.patch("/{id}/bank_details", status_code=200)
def add_bank_details(
    id: int,
    data: UserBankDetailSchema,
    db: Session = Depends(get_db),
):
    update_user_bank_details_(id, data, db)
    return {"detail": "Success"}


@router.patch("/{id}/update_status", status_code=200)
def update_status(id: int, data: UserStatusUpdateSchema, db: Session = Depends(get_db)):
    update_user_status_(id, data, db)
    return


@router.get(
    "/passenger/{id}/details",
    response_model=PassengerBasicSchema,
    status_code=200,
)
def fetch_passenger_details(id: int, db: Session = Depends(get_db)):
    pass


@router.post(
    "/passenger/create",
    response_model=PassengerBasicSchema,
    status_code=200,
)
def add_passenger(data: PassengerCreateSchema, db: Session = Depends(get_db)):
    passenger = create_passenger_(data, db)
    if not passenger:
        raise HTTPException(status_code=400, detail="Something went wrong.")
    return passenger
