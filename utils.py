import os
from dotenv import load_dotenv

from passlib.context import CryptContext

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGRITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
