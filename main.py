from datetime import datetime
from typing import Optional

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from core.database import Base, engine
from core.routers import accounts, auth, vehicles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tranzit")

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(vehicles.router)
