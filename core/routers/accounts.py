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
    UserUpdateSchema,
)
from core.database import get_db
from core.tasks.accounts import create_passenger, update_user_task
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
    level: Level,
    status: Status,
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    update_user_task(id, level, status, data, db)
    return {"detail": "User account updated successfully."}


@router.patch("/{id}/add_bank_details", status_code=200)
def add_bank_details(
    id: int, data: UserBankDetailSchema, db: Session = Depends(get_db)
):
    db.query(User).filter(User.id == id).update(
        {"bank": data.bank, "account_no": data.account_no, "bvn": data.bvn}
    )
    return {"detail": "User bank updated successfully."}


@router.patch("/{id}/toggle_status", status_code=200)
def toggle_status(id: int, status: Status, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == id).update({"status": status})
    db.commit()
    return


@router.post("/passenger/create", status_code=200)
def add_passenger(data: PassengerCreateSchema, db: Session = Depends(get_db)):
    passenger = create_passenger(data, db)
    if not passenger:
        raise HTTPException(status_code=400, detail="Something went wrong.")
    return passenger
