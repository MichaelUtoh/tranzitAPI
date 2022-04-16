from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Bank(Base):
    __tablename__ = "banks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)