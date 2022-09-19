from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import src.cruds.device as device_cruds
import src.cruds.register as register_cruds
import src.cruds.user as user_cruds
import src.schemas.auth as auth_schema
from src.auth.utils import create_access_token, create_refresh_access_token, oauth2_scheme, verify_access_token, verify_hash_password
from src.constants.auth import (
    INCORRECT_EMAIL_OR_PASSWORD_EXCEPTION,
    SERIAL_NUMBER_ALREADY_REGISTERED_EXCEPTION,
    SERIAL_NUMBER_NOT_FOUND_EXCEPTION,
    USER_ALREADY_EXISTS_EXCEPTION,
    USER_NOT_FOUND_EXCEPTION,
)
from src.db.db import get_db
from src.schemas.auth import TokenData
from src.schemas.user import UserCreate

router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> auth_schema.SystemUser:
    """
    Verify the token and return the current user info.

    Args:
        token (str): Token. Defaults to Depends(oauth2_scheme).
        db (AsyncSession): AsyncSession. Defaults to Depends(get_db).

    Raises:
        USER_NOT_FOUND_EXCEPTION: User not found.

    Returns:
        auth_schema.SystemUser: User info object.
    """
    token_payload = verify_access_token(token, db)
    count = user_cruds.count_user_by_user_id(db, token_payload.user_id)
    if count == 0:
        raise USER_NOT_FOUND_EXCEPTION
    return auth_schema.SystemUser(user_id=token_payload.user_id)


@router.post("/signup", summary="Create new user")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    count = await user_cruds.count_user_by_email(db, user.email)
    if count != 0:
        raise USER_ALREADY_EXISTS_EXCEPTION

    device_id = user.serial_number
    registered_unregistered_count = await register_cruds.count_registered_unregistered_device_by_device_id(db, device_id)
    if registered_unregistered_count == 0:
        raise SERIAL_NUMBER_NOT_FOUND_EXCEPTION
    registered_count = await register_cruds.count_registered_device_by_device_id(db, device_id)
    if registered_count > 0:
        raise SERIAL_NUMBER_ALREADY_REGISTERED_EXCEPTION

    user_id = await user_cruds.create_user(db, user)
    await device_cruds.create_device(db, device_id, user._latitude, user._longitude, user_id)
    await register_cruds.register_device_by_device_id(db, device_id)


@router.post("/login", response_model=TokenData)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Check the user exists
    user = await user_cruds.find_user_by_email(db, form_data.username)
    if user is None:
        raise INCORRECT_EMAIL_OR_PASSWORD_EXCEPTION

    # Check the password is valid
    user_id, user_password = user
    if not verify_hash_password(form_data.password, user_password):
        raise INCORRECT_EMAIL_OR_PASSWORD_EXCEPTION

    data = {"user_id": user_id}
    return {
        "access_token": create_access_token(data),
        "refresh_token": create_refresh_access_token(data),
    }
