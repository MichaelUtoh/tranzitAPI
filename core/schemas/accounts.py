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
