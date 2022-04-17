from datetime import datetime
from typing import Optional

from fastapi import FastAPI, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from core.database import Base, engine
from core.routers import accounts, vehicles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tranzit")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(accounts.router)
app.include_router(vehicles.router)
