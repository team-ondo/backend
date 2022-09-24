from pydantic import BaseModel, Field


class NotificationStatus(BaseModel):
    message: str = Field(example="It's too cold in the room! Please check on your loved one", description="Status message")


class DeviceNotificationData(BaseModel):
    id: int = Field(example=1, description="Notification id")
    content_type: str = Field(example="Alarm", description="Type of notification to be pushed.")
    content: str = Field(example="Alarm was triggered", description="Content for the notification.")
    is_read: bool = Field(example=True, description="Boolean value to show read / unread status.")
    date: str = Field(example="2022-07-01 12:23:45", description="Created timestamp")
