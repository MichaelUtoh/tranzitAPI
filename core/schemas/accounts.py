from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class RegisterUserSchema(BaseModel):
    email: str
    password: str


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone_no: str

    next_of_kin_first_name: str
    next_of_kin_last_name: str

    class Config:
        orm_mode = True
