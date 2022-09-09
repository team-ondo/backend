from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.db import Base


class Device(Base):
    __tablename__ = "devices"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    device_name = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    # relationships
    owner = relationship("User", back_populates="devices")

    temperature_data = relationship("Temperature", back_populates="owner")

    humidity_data = relationship("Humidity", back_populates="owner")

    motion_data = relationship("Motion", back_populates="owner")

    button_data = relationship("Button", back_populates="owner")

    alarm_data = relationship("Alarm", back_populates="owner")
