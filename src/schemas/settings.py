from pydantic import UUID4, BaseModel, Field


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
