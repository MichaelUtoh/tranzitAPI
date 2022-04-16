from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from core.schemas.accounts import LoginSchema

from core.database import Base, engine
from core.services import create_vehicle, get_db

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginSchema):
    return data
