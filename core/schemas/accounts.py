from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# class User(BaseModel):
#     first_name = str
#     middle_name = Optional[str]
#     last_name = str
#     email = str
#     phone = str
#     account_no = Optional[str]
#     kin_first_name = Optional[str]
#     kin_last_name = Optional[str]
#     kin_phone_no = Optional[str]
#     user_type = str
#     date_joined = str


class LoginSchema(BaseModel):
    email: str
    password: str

    # class Config:
    #     orm_mode = True
