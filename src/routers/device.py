from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.device as device_crud
import src.schemas.device as device_schema
from src.db.db import get_db

router = APIRouter()


@router.get("/device-data/{device_id}/live", response_model=device_schema.Device)
async def read_device_data(device_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    # TODO Need to authenticate before fetching the current data
    result = await device_crud.get_latest_device_data(db, device_id)
    return {
        "temperature_celsius": result[0],
        "humidity": result[1],
    }


@router.post("/device-data/{device_id}")
async def create_device_data(device_id: int, device_data_list: List[device_schema.DeviceDataCreate], db: AsyncSession = Depends(get_db)) -> None:
    await device_crud.create_device_data(db, device_id, device_data_list)
