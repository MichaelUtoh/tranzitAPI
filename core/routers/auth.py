from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.models.accounts import User
from core.schemas.accounts import (
    LoginSchema,
    RegisterUserSchema,
    UserBasicSchema,
)
from core.schemas.auth import Token
from core.services import get_db
from utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials.",
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password.",
        )

    access_token = create_access_token(data={"sub": user.email})
    data = {"email": user.email, "access_token": access_token, "token_type": "bearer"}
    return data


@router.post("/register")
def register(data: RegisterUserSchema, db: Session = Depends(get_db)):
    is_registered = db.query(User).filter(User.email == data.email).first()
    if is_registered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A registered account with this email already exists.",
        )

    user = User(
        user_id=uuid4().__str__(),
        email=data.email,
        password=get_password_hash(data.password),
        date_joined=datetime.now(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(data={"sub": user.email})
    data = {"email": user.email, "access_token": access_token, "token_type": "bearer"}
    return data
