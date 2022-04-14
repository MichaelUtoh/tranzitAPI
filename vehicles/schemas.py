from typing import Optional

from pydantic import BaseModel
from sqlalchemy import null


class Vehicle(BaseModel):
    reg_id: str
    color: str
    trip_count: int
    in_workshop: Optional[bool] = False
    maintenance_due_date: Optional[str] = None

