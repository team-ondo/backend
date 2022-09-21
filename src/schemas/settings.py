from pydantic import BaseModel, Field


class UserSettings(BaseModel):
    first_name: str = Field(example="John", description="First name")
    last_name: str = Field(example="Doe", description="Last name")
    email: str = Field(example="example@example.com", description="Email address")
    phone_number: str = Field(example="09000000000", description="Phone number(Landline phone, Wireless phone numbers only)")
