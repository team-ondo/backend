from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

import src.schemas.settings as settings_schema


async def find_user_settings_by_user_id(db: AsyncSession, user_id: str) -> settings_schema.UserSettings:
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
