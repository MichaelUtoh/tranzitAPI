from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from core.models.accounts import User

from core.schemas.accounts import LoginSchema, RegisterUserSchema

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
    user = User(email=data.email, password=pwd_context.hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users")
def fetch_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
