from datetime import datetime
from typing import Optional

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from core.database import Base, engine
from core.routers import accounts, vehicles

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(accounts.router)
app.include_router(vehicles.router)
