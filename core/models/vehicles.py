from email.policy import default
from operator import index
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from core.database import Base


manifest_passengers = Table(
    "manifest_passengers",
    Base.metadata,
    Column("manifests_id", ForeignKey("manifests.id"), primary_key=True),
    Column("passengers_id", ForeignKey("passengers.id"), primary_key=True),
)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    reg_id = Column(String(20), index=True)
    type = Column(String(9), index=True)
    make = Column(String(20), index=True)
    model = Column(String(50), index=True)
    color = Column(String(20), index=True, nullable=True)
    today_trip_count = Column(Integer, default=0, index=True)
    status = Column(String(14), default="active", index=True)
    maintenance_due_date = Column(String, index=True, nullable=True)
    timestamp = Column(String)
    manifests = relationship("Manifest", back_populates="vehicle")
    locations = relationship("Location", back_populates="vehicle")
    ratings = relationship("VehicleRating", back_populates="vehicle")
    reports = relationship("VehicleReport", back_populates="vehicle")

    def __repr__(self):
        return self.reg_id


class VehicleReport(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report = Column(String(255), index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    passenger_id = Column(Integer, ForeignKey("passengers.id"))
    timestamp = Column(String, index=True)
    vehicle = relationship("Vehicle", back_populates="reports")
    passengers = relationship("Passenger", back_populates="reports")


class VehicleRating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    timestamp = Column(String, index=True)
    vehicle = relationship("Vehicle", back_populates="ratings")


class Manifest(Base):
    __tablename__ = "manifests"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String(50))
    driver_id = Column(Integer, ForeignKey("users.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    timestamp = Column(String)
    vehicle = relationship("Vehicle", back_populates="manifests")
    driver = relationship("User", back_populates="manifests")
    passengers = relationship(
        "Passenger", secondary="manifest_passengers", back_populates="manifests"
    )

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
    vehicle = relationship("Vehicle", back_populates="locations")

    def __repr__(self):
        return self.destination_terminal
