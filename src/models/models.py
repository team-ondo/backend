from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String(20))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    devices = relationship("Device", back_populates="user")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    device_name = Column(String(100))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="devices")

    temperature_data = relationship("Temperature", back_populates="device")
    humidity_data = relationship("Humidity", back_populates="device")
    motion_data = relationship("Motion", back_populates="device")
    button_data = relationship("Button", back_populates="device")
    alarm_data = relationship("Alarm", back_populates="device")
    notification_data = relationship("Notification", back_populates="device")


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="temperature_data")


class Humidity(Base):
    __tablename__ = "humidity"

    id = Column(Integer, primary_key=True, index=True)
    humidity = Column(Float)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="humidity_data")


class Motion(Base):
    __tablename__ = "motion"

    id = Column(Integer, primary_key=True, index=True)
    motion = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="motion_data")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300))
    is_read = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="notification_data")


class Button(Base):
    __tablename__ = "button"

    id = Column(Integer, primary_key=True, index=True)
    device_listening = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="button_data")


class Alarm(Base):
    __tablename__ = "alarm"

    id = Column(Integer, primary_key=True, index=True)
    is_alarm = Column(Boolean)
    created_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey("devices.id"))

    device = relationship("Device", back_populates="alarm_data")
