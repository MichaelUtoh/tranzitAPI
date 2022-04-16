from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    reg_id = Column(String(20), index=True)
    type = Column(String(9), index=True)
    make = Column(String(20), index=True)
    model = Column(String(50), index=True)
    color = Column(String(20), index=True, nullable=True)
    today_trip_count = Column(Integer, default=0, index=True)
    in_workshop = Column(Boolean, default=True)
    maintenance_due_date = Column(String, index=True, nullable=True)
    timestamp = Column(String)

    manifests = relationship("Manifest", back_populates="vehicle")

    def __repr__(self):
        return self.reg_id


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), index=True)
    middle_name = Column(String(30), index=True, nullable=True)
    last_name = Column(String(30), index=True)
    phone_no = Column(String(20), index=True, nullable=True)

    manifests = relationship("Manifest", back_populates="driver")


class Manifest(Base):
    __tablename__ = "manifests"

    id = Column(Integer, primary_key=True, index=True)
    driver_phone_no = (String, ForeignKey("drivers.phone_no"))
    location = Column(String(50))
    timestamp = Column(String)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    vehicle = relationship("Vehicle", back_populates="manifests")
    driver = relationship("Driver", back_populates="manifests")

    def __repr__(self):
        return self.vehicle
