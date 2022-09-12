from pydantic import BaseModel, Field


class Device(BaseModel):
    temperature_celsius: float | None = Field(None, example="25.1", description="Temperature (Celsius)")
    # TODO Add later
    # temperature_fahrenheit: float | None = Field(None, example="77.18", description="Temperature (Fahrenheit)")
    humidity: int | None = Field(None, example="87", description="Humidity (Percentage)")

    class Config:
        orm_mode = True
