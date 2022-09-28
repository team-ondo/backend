from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.settings as settings_cruds
import src.schemas.auth as auth_schema
import src.schemas.settings as settings_schema
from src.auth.utils import verify_hash_password
from src.constants.common import RE_UUID
from src.db.db import get_db
from src.errors.errors import IncorrectOldPasswordError, TokenExpiredException, TokenValidationFailException, UserNotFoundException, error_response
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


@router.put(
    "/settings/device/{device_id}",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
        ]
    ),
)
async def update_device_settings(
    device: settings_schema.UpdateDeviceSettings,
    device_id: str = Path(RE_UUID),
    current_user: auth_schema.SystemUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await settings_cruds.update_device_settings(db, device, device_id)


@router.put(
    "/settings/user",
    responses=error_response(
        [
            UserNotFoundException,
            TokenValidationFailException,
            TokenExpiredException,
            IncorrectOldPasswordError,
        ]
    ),
)
async def update_user_settings(
    user: settings_schema.UpdateUserSettings, current_user: auth_schema.SystemUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if user.old_password is not None:
        password = await settings_cruds.find_user_password_by_user_id(db, current_user.user_id)
        if not verify_hash_password(user.old_password, password):
            raise IncorrectOldPasswordError()

    await settings_cruds.update_user_settings(db, user, current_user.user_id)
