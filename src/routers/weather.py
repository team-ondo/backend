import requests
from fastapi import APIRouter, Depends, Path
from requests.exceptions import RequestException
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.device as device_crud
import src.schemas.weather as weather_schema
from src.constants.common import OPEN_WEATHER_API, OPEN_WEATHER_APPID, RE_UUID
from src.db.db import get_db
from src.errors.errors import WeatherAPIRequestError, WeatherLangSupportException, error_response
from src.utils.common import convert_celsius_to_fahrenheit

router = APIRouter()


@router.get(
    "/weather-info/{lang}/{device_id}",
    response_model=weather_schema.Weather,
    responses=error_response(
        [
            WeatherLangSupportException,
            WeatherAPIRequestError,
        ]
    ),
)
async def read_weather_info(device_id: str = Path(regex=RE_UUID), lang: str = "en", db: AsyncSession = Depends(get_db)) -> dict:
    if not (lang == "en" or lang == "ja"):
        raise WeatherLangSupportException()

    # TODO Need to authenticate before fetching the device latitude and longitude
    # TODO Check device exists, and owned by user.

    lat, lon = await device_crud.get_latitude_and_longitude(db, device_id)
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": OPEN_WEATHER_APPID, "lang": lang}
    r = requests.get(OPEN_WEATHER_API, params=params)
    try:
        r.raise_for_status()
    except RequestException as e:
        # TODO Replace with logger
        print(f"Request failed: {e.response.text}")
        raise WeatherAPIRequestError()

    json = r.json()
    response = {
        "location_name": json["name"],
        "temperature_c": json["main"]["temp"],
        "temperature_f": convert_celsius_to_fahrenheit(json["main"]["temp"]),
        "humidity": json["main"]["humidity"],
        "weather_icon": json["weather"][0]["icon"],
    }
    return response
