from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.models.accounts import User

from core.database import Base, engine
from core.schemas.accounts import LoginSchema, RegisterUserSchema, UserUpdateSchema
from core.services import get_db
from utils import pwd_context


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    return data


@router.post("/register")
def register(data: RegisterUserSchema, db: Session = Depends(get_db)):
    is_registered = db.query(User).filter(User.email == data.email).first()
    if is_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A registered account with this email already exists.",
        )
    user = User(email=data.email, password=pwd_context.hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users")
def fetch_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.patch("/users/{id}/update")
def update_user(id: int, data: UserUpdateSchema, db: Session = Depends(get_db)):

    db.query(User).filter(User.id == id).update(
        {
            "first_name": data.first_name,
            "middle_name": data.middle_name,
            "last_name": data.last_name,
            "last_login": datetime.now(),
            "phone_no": data.phone_no,
            "next_of_kin_first_name": data.next_of_kin_first_name,
            "next_of_kin_last_name": data.next_of_kin_last_name,
        },
        synchronize_session=False,
    )
    db.commit()
    return {"detail": "User account updated successfully."}


@router.patch("/users/{id}/remove", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(id: int, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()
    return
