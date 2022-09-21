from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

import src.schemas.settings as settings_schema


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
            A.TEMP_LOWER_LIMIT
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
            )
        )

    return result
