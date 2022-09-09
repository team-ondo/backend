from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.db.db import Base


class User(Base):
    # classes will inherit from Base
    __tablename__ = "users"
    # set tablename for use in db

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # relationships
    devices = relationship("Device", back_populates="owner")
