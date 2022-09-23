from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.settings as settings_cruds
import src.schemas.auth as auth_schema
import src.schemas.settings as settings_schema
from src.auth.utils import create_hash_password, verify_hash_password
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


@router.post(
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
    params = dict(
        (name, getattr(user, name))
        for name in dir(user)
        if name
        in [
            "first_name",
            "last_name",
            "email",
            "phone_number",
        ]
        and getattr(user, name) is not None
    )
    if user.old_password is not None:
        password = await settings_cruds.find_user_password_by_user_id(db, current_user.user_id)
        if not verify_hash_password(user.old_password, password):
            raise IncorrectOldPasswordError()
        new_password = create_hash_password(user.new_password)
        params["password"] = new_password

    await settings_cruds.update_user_settings(db, params)
