from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.models.accounts import User

from core.schemas.accounts import (
    Level,
    LoginSchema,
    RegisterUserSchema,
    Status,
    UserBasicSchema,
    UserUpdateSchema,
)
from core.services import get_db
from utils import get_current_user


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=List[UserBasicSchema])
def fetch_users(db: Session = Depends(get_db)):
    # users = db.query(User).all()
    users = db.query(User).filter(User.status == "active").all()
    return users


@router.get("/{id}", response_model=UserBasicSchema)
def fetch_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account with this id doesn't exists.",
        )
    return user


@router.patch("/{id}/update")
def update_user(
    id: int,
    status: Status,
    level: Level,
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
):
    db.query(User).filter(User.id == id).update(
        {
            "first_name": data.first_name,
            "middle_name": data.middle_name,
            "last_name": data.last_name,
            "last_login": datetime.now(),
            "phone_no": data.phone_no,
            "next_of_kin_first_name": data.next_of_kin_first_name,
            "next_of_kin_last_name": data.next_of_kin_last_name,
            "level": level,
            "status": status,
        },
        synchronize_session=False,
    )
    db.commit()
    return {"detail": "User account updated successfully."}


@router.patch("/{id}/remove", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(id: int, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()
    return
