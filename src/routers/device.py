from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.device as device_crud
import src.schemas.device as device_schema
from src.constants.common import RE_UUID
from src.db.db import get_db

router = APIRouter()


@router.get("/device-data/{device_id}/live", response_model=device_schema.Device)
async def read_device_data(device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)) -> dict:
    # TODO Need to authenticate before fetching the current data
    # TODO Check device exists, and owned by user.
    result = await device_crud.get_latest_device_data(db, device_id)
    return {
        "temperature_celsius": result[0],
        "humidity": result[1],
    }


@router.post("/device-data/{device_id}")
async def create_device_data(
    device_data_list: List[device_schema.DeviceDataCreate], device_id: str = Path(regex=RE_UUID), db: AsyncSession = Depends(get_db)
) -> None:
    # TODO Need to authenticate before fetching the current data
    # TODO Check device exists, and owned by user.
    await device_crud.create_device_data(db, device_id, device_data_list)
