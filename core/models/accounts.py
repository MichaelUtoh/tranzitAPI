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
    phone_no = Column(String, index=True, nullable=True)
    last_login = Column(String, index=True)
    level = Column(String, index=True)
    status = Column(String, index=True)
    date_joined = Column(String, index=True)

    next_of_kin_first_name = Column(String, index=True, nullable=True)
    next_of_kin_last_name = Column(String, index=True, nullable=True)

    bank = Column(String, index=True, nullable=True)
    account_no = Column(String, index=True, nullable=True)
    bvn = Column(String, index=True, nullable=True)

    driver = relationship("Driver", back_populates="user")
    documents = relationship("UserDocument", back_populates="users")


class UserDocument(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, index=True)
    document_no = Column(String, index=True)
    document_expiry_date = Column(String, index=True, nullable=True)

    users = relationship("User", back_populates="documents")
