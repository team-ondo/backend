from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


async def count_registered_unregistered_device_by_device_id(db: AsyncSession, device_id: str) -> int:
    """
    Count registered and unregistered device by device id.

    Args:
        db (AsyncSession): AsyncSession.
        device_id (int): Device id.

    Returns:
        int: Count result.
    """
    stmt = text(
        """
        SELECT
            COUNT(*) AS CNT
        FROM
            REGISTERED A
        WHERE
            A.ID = :device_id
        """
    )
    count_result: Result = await db.execute(stmt, params={"device_id": device_id})
    return count_result.one()[0]


async def count_registered_device_by_device_id(db: AsyncSession, device_id: str) -> int:
    """
    Count registered device by device id.

    Args:
        db (AsyncSession): AsyncSession.
        device_id (int): Device id.

    Returns:
        int: Count result.
    """
    stmt = text(
        """
        SELECT
            COUNT(*) AS CNT
        FROM
            REGISTERED A
        WHERE
            A.ID = :device_id
            AND A.REGISTERED = TRUE
        """
    )
    count_result: Result = await db.execute(stmt, params={"device_id": device_id})
    return count_result.one()[0]


async def register_device_by_device_id(db: AsyncSession, device_id: str) -> None:
    """
    Register device by device id.

    Args:
        db (AsyncSession): AsyncSession.
        device_id (str): Device id.
    """
    stmt = text(
        """
        UPDATE REGISTERED A
        SET
            REGISTERED = TRUE
        WHERE
            A.ID = :device_id
        """
    )
    await db.execute(stmt, params={"device_id": device_id})
    await db.commit()
