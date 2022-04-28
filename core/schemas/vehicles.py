from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from core.schemas.accounts import PassengerBasicSchema


class VehicleStatus(str, Enum):
    ACTIVE = "active"
    DECOMMISSIONED = "decommissioned"
    MAINTENANCE = "maintenance"


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
    reg_id: str
    color: str
    in_workshop: Optional[bool] = False
    maintenance_due_date: Optional[str] = None

    class Config:
        orm_mode = True


class ManifestCreate(BaseModel):
    driver_id: int
    vehicle_id: int
    destination: str
    # passengers: List[int]

    class Config:
        orm_mode = True


class ManifestBasic(BaseModel):
    # id: int
    destination: Optional[str] = None


class ManifestPassengerSchema(BaseModel):
    pass
