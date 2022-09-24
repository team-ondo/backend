from typing import List

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.notification as notification_schema


async def notification_belongs_to_user(db: AsyncSession, notification_id: int, user_id: int) -> bool:
    """
    Check the notification data belongs to user.

    Args:
        db (AsyncSession): AsyncSession.
        notification_id (int): Notification id.
        user_id (int): User id.

    Returns:
        bool: True if notification data belongs to user. Otherwise False.
    """
    stmt = """
    SELECT
        COUNT(*)
    FROM NOTIFICATIONS
    WHERE
        ID = :notification_id
        AND DEVICE_ID IN (
            SELECT
                ID
            FROM DEVICES
            WHERE USER_ID = :user_id
        )
    """
    result: Result = await db.execute(stmt, params={"notification_id": notification_id, "user_id": user_id})
    count_result = result.one()[0]
    if count_result > 0:
        return True
    return False


async def update_notification(db: AsyncSession, notification_id: int) -> None:
    """
    Update notification data.

    Args:
        db (AsyncSession): AsyncSession.
        notification_id (int): Notification id.
    """
    stmt = """
    UPDATE NOTIFICATIONS
    SET
        IS_READ = TRUE
    WHERE
        ID = :notification_id
    """
    await db.execute(stmt, params={"notification_id": notification_id})


async def find_device_notification_by_user_id(db: AsyncSession, user_id: int) -> List[notification_schema.DeviceNotificationData]:
    """
    Find device notification data by user id.

    Args:
        db (AsyncSession): AsyncSession.
        user_id (int): User id.

    Returns:
        [notification_schema.DeviceNotificationData]: List of device notification data.
    """
    stmt = """
        SELECT
            ID,
            CONTENT_TYPE,
            CONTENT,
            IS_READ,
            TO_CHAR(CREATED_AT, 'YYYY/MM/DD') AS DATE
        FROM NOTIFICATIONS
        WHERE
            DEVICE_ID IN (
                SELECT
                    ID
                FROM DEVICES
                WHERE
                    USER_ID = :user_id
            )
        ORDER BY DATE
    """

    result: Result = await db.execute(stmt, params={"user_id": user_id})
    rows = result.all()

    result = []
    for row in rows:
        result.append(
            notification_schema.DeviceNotificationData(
                id=row[0],
                content_type=row[1],
                content=row[2],
                is_read=row[3],
                date=row[4],
            )
        )

    return result
