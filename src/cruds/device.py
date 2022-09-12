from sqlalchemy.sql import text
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_device_info(db: AsyncSession, device_id: int) -> (float, float):
    """Get current device info

    Get the latest temperature, humidity from the database.

    Args:
        db (AsyncSession): AsyncSession
        device_id (int): Device id

    Returns:
        (float, float): Tuples in the order of temperature, humidity.
    """
    stmt = text("""
        SELECT
            SUB_TEMP.TEMPERATURE,
            SUB_HUMID.HUMIDITY
        FROM
            (
                SELECT
                    A.TEMPERATURE,
                    ROW_NUMBER() OVER (
                        PARTITION BY DEVICE_ID
                        ORDER BY
                            CREATED_AT DESC
                    ) AS NUM
                FROM
                    TEMPERATURE A
                WHERE
                    A.DEVICE_ID = :device_id
            ) SUB_TEMP
            LEFT JOIN (
                SELECT
                    A.HUMIDITY,
                    ROW_NUMBER() OVER (
                        PARTITION BY DEVICE_ID
                        ORDER BY
                            CREATED_AT DESC
                    ) AS NUM
                FROM
                    HUMIDITY A
                WHERE
                    A.DEVICE_ID = :device_id
            ) SUB_HUMID ON 1 = 1
        WHERE
            SUB_TEMP.NUM = 1
            OR SUB_HUMID.NUM = 1
    """)
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    first = result.first()
    if first is None:
        return (None, None)
    return first
