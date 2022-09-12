from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.db import get_db
import src.cruds.device as device_crud
import src.schemas.device as device_schema

router = APIRouter()


@router.get("/device-info/{device_id}", response_model=device_schema.Device)
async def read_device_info(device_id: int, db: AsyncSession = Depends(get_db)):
    # TODO Need to authenticate before fetching the current data
    result = await device_crud.get_current_device_info(db, device_id)
    return {
        "temperature_celsius": result[0],
        "humidity": result[1],
    }
