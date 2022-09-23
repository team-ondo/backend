from pydantic import BaseModel, EmailStr, Field, validator

from src.utils.common import fetch_longitude_latitude_from_zip_code, is_phone_number, is_zip_code


class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, example="John", description="First name")
    last_name: str = Field(min_length=1, max_length=50, example="Doe", description="Last name")
    email: EmailStr = Field(example="example@example.com", description="Email address")
    phone_number: str = Field(max_length=20, example="090-0000-0000", description="Phone number(Landline phone, Wireless phone numbers only)")
    zip_code: str = Field(max_length=7, example="1001701", description="Zip code(Without Hyphen)")
    serial_number: str = Field(example="cf57432e-809e-4353-adbd-9d5c0d733868", description="Serial number on the device")
    password: str = Field(min_length=8, max_length=16, example="secretPassword!", description="Password")
    _longitude: float
    _latitude: float

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if not is_phone_number(v):
            raise ValueError("Phone number format is not correct")

        return v

    @validator("zip_code")
    def validate_zip_code(cls, v):
        if not is_zip_code(v):
            raise ValueError("Zip code format is not correct")

        longitude, latitude = fetch_longitude_latitude_from_zip_code(v)
        cls._longitude = longitude
        cls._latitude = latitude

        return v
