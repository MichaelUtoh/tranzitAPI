from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    first_name = Column(String(30), index=True, nullable=True)
    middle_name = Column(String(30), index=True, nullable=True)
    last_name = Column(String(30), index=True, nullable=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    phone_no_1 = Column(String, index=True, nullable=True)
    phone_no_2 = Column(String, index=True, nullable=True)
    gender = Column(String, index=True, nullable=True)
    marital_status = Column(String, index=True, nullable=True)
    nationality = Column(String, index=True, nullable=True)
    next_of_kin_first_name = Column(String, index=True, nullable=True)
    next_of_kin_last_name = Column(String, index=True, nullable=True)
    level = Column(String, index=True)
    status = Column(String, index=True)
    last_login = Column(String, index=True)
    bank = Column(String, index=True, nullable=True)
    account_no = Column(String, index=True, nullable=True)
    bvn = Column(String, index=True, nullable=True)
    date_joined = Column(String, index=True)

    manifests = relationship("Manifest", back_populates="driver")
    documents = relationship("UserDocument", back_populates="users")


class UserDocument(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String, index=True)
    document_name = Column(String, index=True)
    document_no = Column(String, index=True)
    document_expiry_date = Column(String, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"{self.document_type} {self.document_number}"


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), index=True, nullable=True)
    last_name = Column(String(30), index=True, nullable=True)
    email = Column(String, index=True)
    phone_no = Column(String, index=True, nullable=True)
    next_of_kin_first_name = Column(String, index=True, nullable=True)
    next_of_kin_last_name = Column(String, index=True, nullable=True)
    date_joined = Column(String, index=True)
    manifest_id = Column(Integer, ForeignKey("manifests.id"))

    manifest = relationship("Manifest", back_populates="passengers")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
