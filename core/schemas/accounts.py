from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Level(str, Enum):
    ADMIN = "admin"
    LINE_MANAGER = "line manager"
    DRIVER = "driver"
    TICKETERS = "ticketers"


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


class UserBasicSchema(BaseModel):
    user_id: Optional[str]
    email: str
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone_no: Optional[str]

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone_no: Optional[str]

    next_of_kin_first_name: Optional[str]
    next_of_kin_last_name: Optional[str]

    class Config:
        orm_mode = True


class UserBankDetailSchema(BaseModel):
    bank: str
    account_no: str
    bvn: Optional[str]

    class Config:
        orm_mode = True
