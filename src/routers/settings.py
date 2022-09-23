from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.settings as settings_cruds
import src.schemas.auth as auth_schema
import src.schemas.settings as settings_schema
from src.db.db import get_db
from src.errors.errors import TokenExpiredException, TokenValidationFailException, UserNotFoundException, error_response
from src.routers.auth import get_current_user

router = APIRouter()


@router.get(
    "/settings/user",
    response_model=settings_schema.UserSettings,
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
)
async def read_user_settings(current_user: auth_schema.SystemUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await settings_cruds.find_user_settings_by_user_id(db, current_user.user_id)


@router.get(
    "/settings/device",
    response_model=List[settings_schema.DeviceSettings],
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
)
async def read_device_settings(current_user: auth_schema.SystemUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await settings_cruds.find_device_settings_by_user_id(db, current_user.user_id)


@router.post(
    "/settings/device",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
)
async def update_device_settings(
    device: settings_schema.UpdateDeviceSettings, current_user: auth_schema.SystemUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    await settings_cruds.update_device_settings(db, device)
