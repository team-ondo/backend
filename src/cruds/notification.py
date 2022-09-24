from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


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
