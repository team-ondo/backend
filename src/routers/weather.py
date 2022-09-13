import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db import get_db
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException
from src.utils.common import convert_celsius_to_fahrenheit
import src.schemas.weather as weather_schema
import src.cruds.device as device_crud


load_dotenv()
router = APIRouter()

OPEN_WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
OPEN_WEATHER_APPID = os.getenv("OPEN_WEATHER_APPID")


@ router.get("/weather-info/{lang}/{device_id}", response_model=weather_schema.Weather)
async def read_weather_info(device_id: int, lang: str = "en", db: AsyncSession = Depends(get_db)):
    if not (lang == "en" or lang == "ja"):
        raise HTTPException(status_code=404, detail="Only supports `en` or `ja`")

    # TODO Need to authenticate before fetching the device latitude and longitude

    lat, lon = await device_crud.get_latitude_and_longitude(db, device_id)
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": OPEN_WEATHER_APPID,
        "lang": lang
    }
    r = requests.get(OPEN_WEATHER_API, params=params)
    try:
        r.raise_for_status()
    except RequestException as e:
        # TODO Replace with logger
        print(f"Request failed: {e.response.text}")
        raise HTTPException(status_code=500, detail="OpenWeatherAPI Request Error")

    json = r.json()
    response = {
        "location_name": json["name"],
        "temperature_c": json["main"]["temp"],
        "temperature_f": convert_celsius_to_fahrenheit(json["main"]["temp"]),
        "humidity": json["main"]["humidity"],
        "weather_icon": json["weather"][0]["icon"],
    }
    return response
