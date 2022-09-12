from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.db.db import Base


class Motion(Base):
    __tablename__ = "motion"

    id = Column(Integer, primary_key=True, index=True)
    motion = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="motion_data")
