from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.device as device_crud
import src.schemas.auth as auth_schema
import src.schemas.device as device_schema
from src.constants.common import RE_UUID
from src.db.db import get_db
from src.routers.auth import get_current_user

router = APIRouter()


@router.get("/device-data/{device_id}/live", response_model=device_schema.Device)
async def read_device_data(device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)):
    # TODO Need to authenticate before fetching the current data
    # TODO Check device exists, and owned by user.
    result = await device_crud.get_latest_device_data(db, device_id)
    return device_schema.Device(temperature_celsius=result[0], humidity=result[1])


@router.get("/device-data/{device_id}/historical/day", response_model=List[device_schema.DeviceHistorical])
async def read_device_data_day(device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)):
    result = await device_crud.get_historical_device_data_day(db, device_id)
    return result


@router.get("/device-data/{device_id}/historical/week", response_model=List[device_schema.DeviceHistorical])
async def read_device_data_week(device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)):
    result = await device_crud.get_historical_device_data_week(db, device_id)
    return result


@router.get("/device-data/{device_id}/historical/month", response_model=List[device_schema.DeviceHistorical])
async def read_device_data_month(device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)):
    result = await device_crud.get_historical_device_data_month(db, device_id)
    return result


@router.get("/device-data/{device_id}/historical/alarm", response_model=List[device_schema.DeviceHistoricalAlarm])
async def read_device_data_alarm(device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)):
    result = await device_crud.get_historical_device_data_alarm(db, device_id)
    return result


@router.get("/notifications", response_model=List[device_schema.DeviceNotificationData])
async def read_device_data_notifications(current_user: auth_schema.SystemUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await device_crud.get_device_data_notifications(db, current_user.user_id)
    return result


@router.post("/device-data/{device_id}")
async def create_device_data(
    device_data_list: List[device_schema.DeviceDataCreate], device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)
) -> None:
    # TODO Need to authenticate before fetching the current data
    # TODO Check device exists, and owned by user.
    await device_crud.create_device_data(db, device_id, device_data_list)
