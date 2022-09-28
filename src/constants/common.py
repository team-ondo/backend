import os

from dotenv import load_dotenv
from jose.constants import ALGORITHMS

load_dotenv()
RE_UUID = r"^([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})$"
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.getenv("TWILIO_VERIFIED_NUMBER")
OPEN_WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
OPEN_WEATHER_APPID = os.getenv("OPEN_WEATHER_APPID")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 10080  # 60 * 24 * 7 (7 days)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_KEY = os.getenv("JWT_REFRESH_KEY")
ALGORITHM = ALGORITHMS.HS256
