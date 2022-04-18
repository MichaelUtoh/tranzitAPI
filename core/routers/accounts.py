from datetime import datetime
from multiprocessing import synchronize
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.orm import Session
from core.models.accounts import User

from core.schemas.accounts import LoginSchema, RegisterUserSchema, UserUpdateSchema

from core.database import Base, engine
from core.services import create_vehicle, get_db
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


@router.put("/users/{id}/update")
def update_user(id: int, data: UserUpdateSchema, db: Session = Depends(get_db)):
    return data


@router.patch("/users/{id}/remove", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(id: int, db: Session = Depends(get_db)):
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()
    return
