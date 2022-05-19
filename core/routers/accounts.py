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
    UserDocsSchema,
    UserLevelUpdateSchema,
    UserStatusUpdateSchema,
    UserUpdateSchema,
)
from core.database import get_db
from core.tasks.accounts import (
    add_employee_document_,
    create_passenger_,
    fetch_user_details_,
    update_user_,
    update_user_bank_details_,
    update_user_level_,
    update_user_status_,
)
from core.utils import get_current_user


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)],
)


# Employee


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
    # TODO Only admin authorization for this endpoint
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=400, detail="Not found.")
    return users


@router.patch("/update", response_model=UserDetailsSchema)
def update_user(
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    user = update_user_(data, db)
    return user


@router.patch("/{id}/bank_details", status_code=200)
def add_bank_details(
    id: int,
    data: UserBankDetailSchema,
    db: Session = Depends(get_db),
):
    update_user_bank_details_(id, data, db)
    return {"detail": "Success"}


@router.patch("/{id}/update_status", response_model=UserDetailsSchema, status_code=200)
def update_status(id: int, data: UserStatusUpdateSchema, db: Session = Depends(get_db)):
    update_user_status_(id, data, db)
    return


@router.patch("/{id}/update_level", response_model=UserBasicSchema, status_code=200)
def update_level(id: int, data: UserLevelUpdateSchema, db: Session = Depends(get_db)):
    user_data = update_user_level_(id, data, db)
    return user_data


@router.patch("/{id}/create_document")
def add_employee_document(
    id: int,
    data: UserDocsSchema,
    db: Session = Depends(get_db),
):
    document = add_employee_document_(id, data, db)
    return document


# Passengers
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
