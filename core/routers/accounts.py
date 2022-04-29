from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.models.accounts import Passenger, User
from core.schemas.accounts import (
    Level,
    Status,
    UserBankDetailSchema,
    UserBasicSchema,
    PassengerCreateSchema,
    UserUpdateSchema,
)
from core.database import get_db
from core.tasks.accounts import create_passenger, search_users
from core.utils import get_current_user


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get("/{id}/details", response_model=UserBasicSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()


@router.get("/users", response_model=List[UserBasicSchema])
def get_users(
    email: Optional[EmailStr] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    users = search_users()
    if not users:
        raise HTTPException(status_code=400, detail="Not found.")
    return users


@router.patch("/{id}/update")
def update_user(
    id: int,
    status: Status,
    level: Level,
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


@router.post("/passenger/add", status_code=200)
def add_passenger(data: PassengerCreateSchema, db: Session = Depends(get_db)):
    passenger = create_passenger(data, db)
    if not passenger:
        raise HTTPException(status_code=400, detail="Something went wrong.")
    return passenger
