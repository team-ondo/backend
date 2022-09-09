from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.db import Base


class Humidity(Base):
    __tablename__ = "humidity"

    id = Column(Integer, primary_key=True, index=True)
    humidity = Column(Integer)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    owner = relationship("Device", back_populates="humidity_data")
