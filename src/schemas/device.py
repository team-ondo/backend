from datetime import datetime

from pydantic import BaseModel, Field


class Device(BaseModel):
    temperature_celsius: float | None = Field(None, example="25.1", description="Temperature (Celsius)")
    # TODO Add later
    # temperature_fahrenheit: float | None = Field(None, example="77.18", description="Temperature (Fahrenheit)")
    humidity: float | None = Field(None, example="87", description="Humidity (Percentage)")


class DeviceHistorical(BaseModel):
    max_temp: float = Field(example="25.1", description="Max Temperature (Celsius)")
    min_temp: float = Field(example="25.1", description="Min Temperature (Celsius)")
    max_humid: float = Field(example="87.0", description="Max Humidity")
    min_humid: float = Field(example="87.0", description="Min Humidity")
    date: str = Field(example="2022-07-01", description="Created Day")


class DeviceHistoricalAlarm(BaseModel):
    date: str = Field(example="2022-07-01", description="Created Day")
    hour: str = Field(example="13:51", description="Created Time")


class DeviceNotificationData(BaseModel):
    content_type: str = Field(example="Alarm", description="Type of notification to be pushed.")
    content: str = Field(example="Alarm was triggered", description="Content for the notification.")
    is_read: bool = Field(example=True, description="Boolean value to show read / unread status.")
    created_at: datetime = Field(example="2022-07-01 12:23:45", description="Created timestamp")


class DeviceDataCreate(BaseModel):
    temperature_c: float = Field(example="25.1", description="Temperature (Celsius)")
    temperature_f: float = Field(example="77.18", description="Temperature (Fahrenheit)")
    humidity: float = Field(example="87", description="Humidity")
    motion: bool = Field(example=True, description="Motion detected")
    alarm: bool = Field(example=True, description="Alarmed")
    button: bool = Field(example=True, description="Button pressed")
    created_at: datetime = Field(example="2022-07-01 12:23:45", description="Created timestamp")
