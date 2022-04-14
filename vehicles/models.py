from email.policy import default
from lib2to3.pgen2 import driver
from operator import index
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    reg_id = Column(String(20), index=True)
    color = Column(String(20), index=True, nullable=True)
    today_trip_count = Column(Integer(3, index=True))
    in_workshop = Column(Boolean, default=True)
    maintenance_due_date = Column(String, index=True, nullable=True)
    timestamp = Column(String)

    def __repr__(self):
        return self.reg_id


class Manifesto(Base):
    __tablename__ = 'manifestos'

    id = Column(Integer, primary_key=True, index=True)
    vehicle = relationship('Vehicle', back_populates='manifestos')
    
    def __repr__(self):
        return self.vehicle