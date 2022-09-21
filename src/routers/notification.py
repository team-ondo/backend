import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from twilio.rest import Client

from src.constants.common import RE_UUID
from src.db.db import get_db

load_dotenv()
router = APIRouter()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.getenv("TWILIO_VERIFIED_NUMBER")


@router.post("/device/{device_id}/alarm/on")
async def device_alarm_on(device_id: str = Path(regex=RE_UUID)):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    notification_text = "TEST MESSAGE FROM ONDO BACKEND"

    message = client.messages.create(body=notification_text, from_=TWILIO_VIRTUAL_NUMBER, to=TWILIO_VERIFIED_NUMBER)

    # print if successfully sent
    print(message.sid)
