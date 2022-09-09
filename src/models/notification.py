from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.db import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    isRead = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    owner = relationship("Device", back_populates="notification_data")
