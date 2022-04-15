from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import null


class VehicleType(str, Enum):
    LUXURY_BUS = "luxury bus"
    SPACE_BUS = "space bus"
    SUV = "sports utility vehicle"
    CAR = "car"


class VehicleMake(str, Enum):
    TOYOTA = "toyota"
    MERCEDES = "mercedes"
    HONDA = "honda"
    FIAT = "fiat"
    MARCOPOLO = "marcopolo"


class VehicleModel(str, Enum):
    SIENNA = "sienna"
    HIACE = "hiace"


class VehicleBasic(BaseModel):
    id: int
    reg_id: str
    color: str
    today_trip_count: int
    in_workshop: Optional[bool] = False
    maintenance_due_date: Optional[str] = None

    class Config:
        orm_mode = True


class VehicleCreate(BaseModel):
    type: VehicleType
    make: VehicleMake
    model: VehicleModel
    reg_id: str
    color: str
    in_workshop: Optional[bool] = False
    maintenance_due_date: Optional[str] = None


class ManifestCreate(BaseModel):
    driver: int
    driver_phone_no: str
    vehicle: int
    location: str
