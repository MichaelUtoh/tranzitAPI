from datetime import datetime
from typing import Optional

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
from core.database import get_db
from core.tasks.accounts import search
from core.utils import get_current_user


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get("/search", response_model=UserBasicSchema)
def search_users(
    id: Optional[int] = None,
    email: Optional[str] = None,
    status: Optional[Status] = None,
    db: Session = Depends(get_db),
):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=400, detail="Not found.")
    users = search(id, email, status, db)
    print(users)
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


@router.patch("/{id}/toggle_status", status_code=status.HTTP_200_OK)
def toggle_status(id: int, status: Status, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == id).update({"status": status})
    db.commit()
    return
