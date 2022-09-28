from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.device as device_crud
import src.schemas.auth as auth_schema
import src.schemas.device as device_schema
from src.constants.common import RE_UUID
from src.db.db import get_db
from src.errors.errors import TokenExpiredException, TokenValidationFailException, UserNotFoundException, error_response
from src.routers.auth import get_current_user

router = APIRouter()


@router.get(
    "/device-data/{device_id}/live",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
    response_model=device_schema.Device,
)
async def read_device_data(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    device_id: str = Path(regex=RE_UUID),
    db: AsyncSession = Depends(get_db),
):
    # TODO Check device exists, and owned by user.
    result = await device_crud.get_latest_device_data(db, device_id)
    return device_schema.Device(temperature_celsius=result[0], humidity=result[1], alarm=result[2])


@router.get(
    "/device-data/{device_id}/historical/day",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
    response_model=List[device_schema.DeviceHistorical],
)
async def read_device_data_day(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    device_id: str = Path(regex=RE_UUID),
    db: AsyncSession = Depends(get_db),
):
    result = await device_crud.get_historical_device_data_day(db, device_id)
    return result


@router.get(
    "/device-data/{device_id}/historical/week",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
    response_model=List[device_schema.DeviceHistorical],
)
async def read_device_data_week(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    device_id: str = Path(regex=RE_UUID),
    db: AsyncSession = Depends(get_db),
):
    result = await device_crud.get_historical_device_data_week(db, device_id)
    return result


@router.get(
    "/device-data/{device_id}/historical/month",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
    response_model=List[device_schema.DeviceHistorical],
)
async def read_device_data_month(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    device_id: str = Path(regex=RE_UUID),
    db: AsyncSession = Depends(get_db),
):
    result = await device_crud.get_historical_device_data_month(db, device_id)
    return result


@router.get(
    "/device-data/{device_id}/historical/alarm",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
    response_model=List[device_schema.DeviceHistoricalAlarm],
)
async def read_device_data_alarm(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    device_id: str = Path(regex=RE_UUID),
    db: AsyncSession = Depends(get_db),
):
    result = await device_crud.get_historical_device_data_alarm(db, device_id)
    return result


@router.get(
    "/device-data/{device_id}/device-name",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
    response_model=device_schema.DeviceName,
)
async def read_device_name(
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    device_id: str = Path(regex=RE_UUID),
    db: AsyncSession = Depends(get_db),
):
    return await device_crud.find_device_name_by_device_id(db, device_id)


@router.post("/device-data/{device_id}")
async def create_device_data(
    device_data_list: List[device_schema.DeviceDataCreate],
    device_id: str = Path(regex=RE_UUID),
    db: AsyncSession = Depends(get_db),
) -> None:
    # TODO Need to authenticate before fetching the current data
    # TODO Check device exists, and owned by user.
    await device_crud.create_device_data(db, device_id, device_data_list)
