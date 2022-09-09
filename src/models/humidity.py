from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.db import Base


class Humidity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    humidity = Column(Float)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    owner = relationship("Device", back_populates="humidity_data")