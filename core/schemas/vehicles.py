from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class VehicleStatus(str, Enum):
    ACTIVE = "active"
    DECOMMISSIONED = "decommissioned"
    MAINTENANCE = "maintenance"


class VehicleType(str, Enum):
    LUXURY_BUS = "luxury bus"
    SPACE_BUS = "space bus"


class VehicleMake(str, Enum):
    TOYOTA = "toyota"
    MERCEDES = "mercedes"
    HONDA = "honda"
    FIAT = "fiat"
    MARCOPOLO = "marcopolo"


class VehicleModel(str, Enum):
    SIENNA = "sienna"
    HIACE = "hiace"


class VehicleRating(str, Enum):
    EXCELLENT = 1
    VERY_GOOD = 2
    GOOD = 3
    FAIR = 4
    POOR = 5


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


class VehicleReportBasicSchema(BaseModel):
    passenger_id: int
    vehicle_id: int
    detail: str


class VehicleReportSchema(BaseModel):
    detail: str

    class Config:
        orm_mode = True


class VehicleRatingBasicSchema(BaseModel):
    vehicle_id: int
    passenger_id: int
    rating: int

    class Config:
        orm_mode = True


class VehicleRatingCreateSchema(BaseModel):
    passenger_id: int
    rating: int

    class Config:
        orm_mode = True


class ManifestCreateUpdateSchema(BaseModel):
    driver_id: int
    vehicle_id: int
    destination: str

    class Config:
        orm_mode = True


class ManifestPassengerSchema(BaseModel):
    passenger_ids: List[int] = []


class VehicleLocationBasicSchema(BaseModel):
    departure_terminal: str
    destination_terminal: str
    started_trip: Optional[bool] = False
    ended_trip: Optional[bool] = False

    class Config:
        orm_mode = True


class VehicleLocationCoordSchema(BaseModel):
    current_latitude: str
    current_longitude: str

    class Config:
        orm_mode = True
