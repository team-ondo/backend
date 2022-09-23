from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

import src.schemas.settings as settings_schema
from src.auth.utils import create_hash_password


async def find_user_settings_by_user_id(db: AsyncSession, user_id: int) -> settings_schema.UserSettings:
    """
    Find user settings by user id.

    Args:
        db (AsyncSession): AsyncSession.
        user_id (int): User id.

    Returns:
        settings_schema.UserSettings: User settings.
    """
    stmt = text(
        """
        SELECT
            FIRST_NAME,
            LAST_NAME,
            EMAIL,
            PHONE_NUMBER
        FROM
            USERS A
        WHERE
            A.ID = :user_id
        """
    )
    execute_result: Result = await db.execute(stmt, params={"user_id": user_id})
    row = execute_result.one()
    return settings_schema.UserSettings(
        first_name=row[0],
        last_name=row[1],
        email=row[2],
        phone_number=row[3],
    )


async def find_device_settings_by_user_id(db: AsyncSession, user_id: int) -> List[settings_schema.DeviceSettings]:
    """
    Find device settings by user id.

    Args:
        db (AsyncSession): AsyncSession.
        user_id (int): User id.

    Returns:
        settings_schema.DeviceSettings: Device settings.
    """
    stmt = text(
        """
        SELECT
            A.ID,
            A.DEVICE_NAME,
            A.TEMP_UPPER_LIMIT,
            A.TEMP_LOWER_LIMIT,
            A.ZIP_CODE
        FROM
            DEVICES A
        WHERE
            A.USER_ID = :user_id
        ORDER BY A.ID
        """
    )
    execute_result: Result = await db.execute(stmt, params={"user_id": user_id})
    rows = execute_result.all()

    result = []
    for row in rows:
        result.append(
            settings_schema.DeviceSettings(
                device_id=row[0],
                device_name=row[1],
                temperature_upper_limit=row[2],
                temperature_lower_limit=row[3],
                zip_code=row[4],
            )
        )

    return result


async def update_device_settings(db: AsyncSession, device: settings_schema.UpdateDeviceSettings):
    """
    Update device settings.

    Args:
        db (AsyncSession): AsyncSession.
        device (settings_schema.UpdateDeviceSettings): UpdateDeviceSettings object.
    """
    update_set_values = []
    if device.device_name is not None:
        update_set_values.append("DEVICE_NAME = :device_name")
    if device.temperature_upper_limit is not None:
        update_set_values.append("TEMP_UPPER_LIMIT = :temp_upper_limit")
    if device.temperature_lower_limit is not None:
        update_set_values.append("TEMP_LOWER_LIMIT = :temp_lower_limit")
    if device.zip_code is not None:
        update_set_values.append("ZIP_CODE = :zip_code")
    if device.latitude is not None:
        update_set_values.append("LATITUDE = :latitude")
    if device.longitude is not None:
        update_set_values.append("LONGITUDE = :longitude")
    update_set_values_joined = ",\n".join(update_set_values)

    stmt = text(
        f"""
        UPDATE DEVICES
        SET
            {update_set_values_joined}
        """
    )
    await db.execute(
        stmt,
        params={
            "device_name": device.device_name,
            "temp_upper_limit": device.temperature_upper_limit,
            "temp_lower_limit": device.temperature_lower_limit,
            "zip_code": device.zip_code,
            "latitude": device.latitude,
            "longitude": device.longitude,
        },
    )


async def find_user_password_by_user_id(db: AsyncSession, user_id: int) -> str:
    """
    Find user password by user id.

    Args:
        db (AsyncSession): AsyncSession.
        user_id (int): User id.

    Returns:
        str: User password.
    """
    stmt = text(
        """
        SELECT
            PASSWORD
        FROM
            USERS A
        WHERE
            A.ID = :user_id
        """
    )
    result: Result = await db.execute(stmt, params={"user_id": user_id})
    return result.first()[0]


async def update_user_settings(db: AsyncSession, user: settings_schema.UpdateUserSettings):
    """
    Update user settings.

    Args:
        db (AsyncSession): AsyncSession.
        user (Dict[str, settings_schema.UpdateUserSettings]): UpdateUserSettings object.
    """
    update_set_values = []
    if user.first_name is not None:
        update_set_values.append("FIRST_NAME = :first_name")
    if user.last_name is not None:
        update_set_values.append("LAST_NAME = :last_name")
    if user.email is not None:
        update_set_values.append("EMAIL = :email")
    if user.phone_number is not None:
        update_set_values.append("PHONE_NUMBER = :phone_number")
    if user.new_password is not None:
        update_set_values.append("PASSWORD = :password")
    update_set_values_joined = ",\n".join(update_set_values)
    stmt = text(
        f"""
        UPDATE USERS
        SET
            {update_set_values_joined}
        """
    )
    await db.execute(
        stmt,
        params={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "password": user.new_password if user.new_password is None else create_hash_password(user.new_password),
        },
    )
