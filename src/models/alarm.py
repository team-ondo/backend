from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.db import Base


class Alarm(Base):
    __tablename__ = "alarm"

    id = Column(Integer, primary_key=True, index=True)
    is_alarm = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    owner = relationship("Device", back_populates="alarm_data")
