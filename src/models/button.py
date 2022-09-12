from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.db import Base


class Button(Base):
    __tablename__ = "button"

    id = Column(Integer, primary_key=True, index=True)
    device_listening = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="button_data")
