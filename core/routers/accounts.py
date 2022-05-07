from datetime import datetime
from os import stat
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.models.accounts import Passenger, User
from core.schemas.accounts import (
    Level,
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
    update_user_,
    update_user_bank_details_,
    update_user_status_,
)
from core.utils import get_current_user


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get("/{id}/details", response_model=UserDetailsSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()


@router.get("/users", response_model=List[UserBasicSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=400, detail="Not found.")
    return users


@router.patch("/{id}/update")
def update_user(
    id: int,
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    update_user_(id, data, db)
    return {"detail": "Success"}


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


@router.post("/passenger/create", status_code=200)
def add_passenger(data: PassengerCreateSchema, db: Session = Depends(get_db)):
    passenger = create_passenger_(data, db)
    if not passenger:
        raise HTTPException(status_code=400, detail="Something went wrong.")
    return passenger
