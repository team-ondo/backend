import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.db.db import Base


class CreatedUpdatedDefaultTimeStampMixin:
    @declared_attr
    def created_at(cls) -> Column:
        return Column(DateTime, default=datetime.now(), nullable=False)

    @declared_attr
    def updated_at(cls) -> Column:
        return Column(DateTime, default=datetime.now(), nullable=False)


class CreatedNoDefaultTimeStampMixin:
    @declared_attr
    def created_at(cls) -> Column:
        return Column(DateTime, nullable=False)


class Register(Base, CreatedUpdatedDefaultTimeStampMixin):
    __tablename__ = "registered"

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    registered = Column(Boolean)


class User(Base, CreatedUpdatedDefaultTimeStampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String(20))
    password = Column(String)

    devices = relationship("Device", back_populates="user")


class Device(Base, CreatedUpdatedDefaultTimeStampMixin):
    __tablename__ = "devices"

    id = Column(UUIDType(binary=False), primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    device_name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="devices")

    temperature_data = relationship("Temperature", back_populates="device")
    humidity_data = relationship("Humidity", back_populates="device")
    motion_data = relationship("Motion", back_populates="device")
    button_data = relationship("Button", back_populates="device")
    alarm_data = relationship("Alarm", back_populates="device")
    notification_data = relationship("Notification", back_populates="device")


class Temperature(Base, CreatedNoDefaultTimeStampMixin):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    device_id = Column(UUIDType(binary=False), ForeignKey("devices.id"))

    device = relationship("Device", back_populates="temperature_data")


class Humidity(Base, CreatedNoDefaultTimeStampMixin):
    __tablename__ = "humidity"

    id = Column(Integer, primary_key=True, index=True)
    humidity = Column(Float)
    device_id = Column(UUIDType(binary=False), ForeignKey("devices.id"))

    device = relationship("Device", back_populates="humidity_data")


class Motion(Base, CreatedNoDefaultTimeStampMixin):
    __tablename__ = "motion"

    id = Column(Integer, primary_key=True, index=True)
    motion = Column(Boolean)
    device_id = Column(UUIDType(binary=False), ForeignKey("devices.id"))

    device = relationship("Device", back_populates="motion_data")


class Notification(Base, CreatedNoDefaultTimeStampMixin):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300))
    is_read = Column(Boolean)
    device_id = Column(UUIDType(binary=False), ForeignKey("devices.id"))

    device = relationship("Device", back_populates="notification_data")


class Button(Base, CreatedNoDefaultTimeStampMixin):
    __tablename__ = "button"

    id = Column(Integer, primary_key=True, index=True)
    device_listening = Column(Boolean)
    device_id = Column(UUIDType(binary=False), ForeignKey("devices.id"))

    device = relationship("Device", back_populates="button_data")


class Alarm(Base, CreatedNoDefaultTimeStampMixin):
    __tablename__ = "alarm"

    id = Column(Integer, primary_key=True, index=True)
    is_alarm = Column(Boolean)
    device_id = Column(UUIDType(binary=False), ForeignKey("devices.id"))

    device = relationship("Device", back_populates="alarm_data")
