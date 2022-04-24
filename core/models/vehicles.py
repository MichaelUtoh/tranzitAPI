from email.policy import default
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
    location = Column(Integer, ForeignKey("locations.id"))
    timestamp = Column(String)

    manifests = relationship("Manifest", back_populates="vehicle")
    location = relationship("Location", back_populates="vehicle")

    def __repr__(self):
        return self.reg_id


class Manifest(Base):
    __tablename__ = "manifests"

    id = Column(Integer, primary_key=True, index=True)
    driver_phone_no = (String, ForeignKey("users.phone_no"))
    location = Column(String(50))
    driver_id = Column(Integer, ForeignKey("users.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    timestamp = Column(String)

    vehicle = relationship("Vehicle", back_populates="manifests")
    driver = relationship("User", back_populates="manifests")
    passengers = relationship("Passenger", back_populates="manifest")

    def __repr__(self):
        return self.vehicle


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    departure_terminal = Column(String(50), index=True, nullable=True)
    destination_terminal = Column(String(50), index=True, nullable=True)
    current_latitude = Column(String(20), index=True, nullable=True)
    current_longitude = Column(String(20), index=True, nullable=True)
    started_trip = Column(Boolean, default=False, index=True)
    ended_trip = Column(Boolean, default=False, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    vehicle = relationship("Vehicle", back_populates="location")

    def __repr__(self):
        return self.destination_terminal
