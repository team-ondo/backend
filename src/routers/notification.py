import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.rest import Client

import src.cruds.notification as notification_crud
import src.schemas.auth as auth_schema
import src.schemas.notification as notification_schema
from src.constants.common import RE_UUID
from src.db.db import get_db
from src.errors.errors import IncorrectUserUpdate, TokenExpiredException, TokenValidationFailException, UserNotFoundException, error_response
from src.routers.auth import get_current_user

load_dotenv()
router = APIRouter()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.getenv("TWILIO_VERIFIED_NUMBER")


@router.post("/device/{device_id}/alarm/on")
async def device_alarm_on(notification_status: notification_schema.NotificationStatus, device_id: str = Path(regex=RE_UUID)):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    notification_text = notification_status.message

    message = client.messages.create(body=notification_text, from_=TWILIO_VIRTUAL_NUMBER, to=TWILIO_VERIFIED_NUMBER)

    # print if successfully sent
    print(message.sid)

    # TODO Handle failed messages


@router.put(
    "/notifications/{notification_id}",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
            IncorrectUserUpdate,
        ]
    ),
)
async def update_notification(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    notification_id: int = Path(example=1, description="Notification id"),
    db: AsyncSession = Depends(get_db),
):
    notification_belongs_to_user = await notification_crud.notification_belongs_to_user(db, notification_id, current_user.user_id)
    if not notification_belongs_to_user:
        raise IncorrectUserUpdate()
    await notification_crud.update_notification(db, notification_id)
