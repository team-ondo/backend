from pydantic import BaseModel, Field


class Weather(BaseModel):
    location_name: str | None = Field(None, example="Horinouchi", description="Location name")
    temperature_c: float | None = Field(None, example="23.72", description="Temperature (Celsius)")
    temperature_f: float | None = Field(None, example="74.69", description="Temperature (Fahrenheit)")
    humidity: int | None = Field(None, example="88", description="Humidity (%)")
    weather_icon: str | None = Field(None, example="50n", description="Weather icon id")
