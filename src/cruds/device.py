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
        select
            sub_temp.temperature,
            sub_humid.humidity
        from
            (
                select
                    a.temperature,
                    ROW_NUMBER() OVER (
                        PARTITION BY device_id
                        ORDER BY
                            created_at DESC
                    ) AS num
                FROM
                    temperature a
                WHERE
                    a.device_id = :device_id
            ) sub_temp
            LEFT JOIN (
                select
                    a.humidity,
                    ROW_NUMBER() OVER (
                        PARTITION BY device_id
                        ORDER BY
                            created_at DESC
                    ) AS num
                FROM
                    humidity a
                WHERE
                    a.device_id = :device_id
            ) sub_humid ON 1 = 1
        where
            sub_temp.num = 1
            or sub_humid.num = 1
    """)
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    first = result.first()
    if first is None:
        return (None, None)
    return first
