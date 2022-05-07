from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.models.accounts import User
from core.schemas.accounts import (
    LoginSchema,
    RegisterUserSchema,
)
from core.schemas.auth import Token
from core.database import get_db
from core.utils import (
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


@router.post("/login")
async def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password.")

    access_token = create_access_token(data={"sub": user.email})
    data = {"email": user.email, "access_token": access_token, "token_type": "bearer"}
    return data


@router.post("/register")
def register(data: RegisterUserSchema, db: Session = Depends(get_db)):
    is_registered = db.query(User).filter(User.email == data.email).first()
    if is_registered:
        raise HTTPException(
            status_code=400,
            detail="A registered account with this email already exists.",
        )

    user = User(
        employee_id=str(uuid4()),
        email=data.email,
        password=get_password_hash(data.password),
        status="active",
        date_joined=str(datetime.now().date()),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(data={"sub": user.email})
    data = {"email": user.email, "access_token": access_token, "token_type": "bearer"}
    return data
