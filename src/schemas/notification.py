from pydantic import BaseModel, Field


class NotificationStatus(BaseModel):
    message: str = Field(example="It's too cold in the room! Please check on your loved one", description="Status message")
