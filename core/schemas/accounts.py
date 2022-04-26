from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class DocumentType(str, Enum):
    NATIONAL_IDENTITY_CARD = "national identity card"
    NATIONAL_VOTERS_CARD = "national voters card"
    DRIVERS_LICENSE = "drivers license"
    INTERNATIONAL_PASSPORT = "international passport"
    CERTIFICATE = "certificate"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    NOT_STATED = "not stated"


class Level(str, Enum):
    ADMIN = "admin"
    LINE_MANAGER = "line manager"
    DRIVER = "driver"
    TICKETERS = "ticketers"


class Status(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Title(str, Enum):
    MR = "mr"
    MRS = "mrs"
    MISS = "miss"
    SIR = "sir"


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserBasicSchema(BaseModel):
    user_id: Optional[str]
    email: EmailStr
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone_no: Optional[str]
    level: Optional[str]
    status: Optional[str]
    date_joined: str

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


class PassengerCreateSchema(BaseModel):
    email: EmailStr
    title: Optional[Title]
    first_name: str
    last_name: str
    gender: Gender
    phone_no: str
    next_of_kin_first_name: Optional[str]
    next_of_kin_last_name: Optional[str]
    next_of_kin_phone_no: Optional[str]

    class Config:
        orm_mode = True
