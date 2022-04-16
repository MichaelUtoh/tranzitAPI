from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegisterSchema(BaseModel):
    email: str
    password: str
    password2: str


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
