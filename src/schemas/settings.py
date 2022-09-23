from typing import Any, Dict, Optional

from pydantic import UUID4, BaseModel, Field, root_validator

from src.utils.common import fetch_longitude_latitude_from_zip_code, is_zip_code


class UserSettings(BaseModel):
    first_name: str = Field(example="John", description="First name")
    last_name: str = Field(example="Doe", description="Last name")
    email: str = Field(example="example@example.com", description="Email address")
    phone_number: str = Field(example="09000000000", description="Phone number(Landline phone, Wireless phone numbers only)")


class DeviceSettings(BaseModel):
    device_id: UUID4 = Field(example="a7382f5c-3326-4cf8-b717-549affe1c2eb", description="Device id")
    device_name: str = Field(example="Roppongi_Device", description="Device name")
    temperature_upper_limit: float = Field(example=30.2, description="Upper limit for temperature")
    temperature_lower_limit: float = Field(example=29.2, description="Lower limit for temperature")
    zip_code: str = Field(example="1001701", description="Zip code(Without Hyphen)")


class UpdateDeviceSettings(BaseModel):
    device_name: Optional[str] = Field(None, example="Roppongi_Device", description="Device name")
    temperature_upper_limit: Optional[float] = Field(None, example=30.2, description="Upper limit for temperature")
    temperature_lower_limit: Optional[float] = Field(None, example=29.2, description="Lower limit for temperature")
    zip_code: Optional[str] = Field(None, example="1001701", description="Zip code(Without Hyphen)")
    longitude: Optional[float] = Field(None, example="139.7247", description="Longitude")
    latitude: Optional[float] = Field(None, example="35.656", description="Latitude")

    @root_validator()
    def validate_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        # Validate temperature upper and lower limit
        temperature_upper_limit: Optional[float] = values.get("temperature_upper_limit")
        temperature_lower_limit: Optional[float] = values.get("temperature_lower_limit")
        if temperature_lower_limit is not None and temperature_upper_limit is None:
            raise ValueError("Temperature upper limit is missing")
        if temperature_upper_limit is not None and temperature_lower_limit is None:
            raise ValueError("Temperature lower limit is missing")
        if temperature_lower_limit is not None and temperature_upper_limit is not None:
            if not (temperature_lower_limit <= temperature_upper_limit):
                raise ValueError("Inconsistency between upper and lower limits")

        # Validate zip code
        zip_code = values.get("zip_code")
        if zip_code is not None:
            if not is_zip_code(zip_code):
                raise ValueError("Zip code format is not correct")

            longitude, latitude = fetch_longitude_latitude_from_zip_code(zip_code)
            cls.longitude = longitude
            cls.latitude = latitude

        return values
