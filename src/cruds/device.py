from datetime import datetime
from typing import List, Tuple

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

import src.schemas.device as device_schema


async def get_latest_device_data(db: AsyncSession, device_id: str) -> Tuple[float, float, bool]:
    """Get latest device info

    Get the latest temperature, humidity from the database.

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id

    Returns:
        (float, float, bool): Tuples in the order of temperature, humidity, alarm.
    """
    stmt = text(
        """
        SELECT
            SUB_TEMP.TEMPERATURE,
            SUB_HUMID.HUMIDITY,
            SUB_ALARM.IS_ALARM
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
            ) SUB_TEMP,
            (
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
            ) SUB_HUMID,
            (
                SELECT
                    A.IS_ALARM,
                    ROW_NUMBER() OVER (
                        PARTITION BY DEVICE_ID
                        ORDER BY
                            CREATED_AT DESC
                    ) AS NUM
                FROM
                    ALARM A
            WHERE
                A.DEVICE_ID = :device_id
            ) SUB_ALARM
        WHERE
            SUB_TEMP.NUM = 1
            AND SUB_HUMID.NUM = 1
            AND SUB_ALARM.NUM = 1
    """
    )
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    first: Tuple[float, float, bool] = result.one()
    return first


async def find_device_name_by_device_id(db: AsyncSession, device_id: str) -> device_schema.DeviceName:
    """
    Find device name by device id.

    Args:
        db (AsyncSession): AsyncSession.
        device_id (str): Device id.

    Returns:
        device_schema.DeviceName: DeviceName object.
    """
    stmt = text(
        """
        SELECT
            DEVICE_NAME
        FROM
            DEVICES
        WHERE
            ID = :device_id
    """
    )
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    return device_schema.DeviceName(device_name=result.one()[0])


async def get_historical_device_data_day(db: AsyncSession, device_id: str) -> List[device_schema.DeviceHistorical]:
    """
    Get 24 hour points of temperature and humidity from device

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id

    Returns:
        [device.schema.DeviceHistorical]: List of device historical data
    """
    stmt = """
        SELECT
            MIN(A.TEMPERATURE) AS MIN_TEMP,
            MAX(A.TEMPERATURE) AS MAX_TEMP,
            MIN(B.HUMIDITY) AS MIN_HUMID,
            MAX(B.HUMIDITY) AS MAX_HUMID,
            TO_CHAR(A.CREATED_AT, 'YYYY/MM/DD HH24:00:00') AS CREATED_DATE
        FROM TEMPERATURE A
        INNER JOIN HUMIDITY B
            ON A.CREATED_AT = B.CREATED_AT
            AND A.DEVICE_ID = B.DEVICE_ID
        WHERE
            A.CREATED_AT BETWEEN now() - INTERVAL '1 day' AND now()
            AND A.DEVICE_ID = :device_id
        GROUP BY CREATED_DATE
        ORDER BY CREATED_DATE
    """
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    rows = result.all()

    result = []
    for row in rows:
        result.append(
            device_schema.DeviceHistorical(
                min_temp=row[0],
                max_temp=row[1],
                min_humid=row[2],
                max_humid=row[3],
                date=row[4],
            )
        )

    return result


async def get_historical_device_data_week(db: AsyncSession, device_id: str) -> List[device_schema.DeviceHistorical]:
    """
    Get 7 days of temperature and humidity from device

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id

    Returns:
        [device.schema.DeviceHistorical]: List of device historical data
    """
    stmt = """
        SELECT
            MIN(A.TEMPERATURE) AS MIN_TEMP,
            MAX(A.TEMPERATURE) AS MAX_TEMP,
            MIN(B.HUMIDITY) AS MIN_HUMID,
            MAX(B.HUMIDITY) AS MAX_HUMID,
            TO_CHAR(A.CREATED_AT, 'YYYY/MM/DD') AS CREATED_DATE
        FROM TEMPERATURE A
        INNER JOIN HUMIDITY B
            ON A.CREATED_AT = B.CREATED_AT
            AND A.DEVICE_ID = B.DEVICE_ID
        WHERE
            A.CREATED_AT BETWEEN now() - INTERVAL '1 week' AND now()
            AND A.DEVICE_ID = :device_id
        GROUP BY CREATED_DATE
        ORDER BY CREATED_DATE
    """
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    rows = result.all()

    result = []
    for row in rows:
        result.append(
            device_schema.DeviceHistorical(
                min_temp=row[0],
                max_temp=row[1],
                min_humid=row[2],
                max_humid=row[3],
                date=row[4],
            )
        )

    return result


async def get_historical_device_data_month(db: AsyncSession, device_id: str) -> List[device_schema.DeviceHistorical]:
    """
    Get 4 weeks of temperature and humidity from device

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id

    Returns:
        [device.schema.DeviceHistorical]: List of device historical data
    """

    stmt = """
        SELECT
            MIN(A.TEMPERATURE) AS MIN_TEMP,
            MAX(A.TEMPERATURE) AS MAX_TEMP,
            MIN(B.HUMIDITY) AS MIN_HUMID,
            MAX(B.HUMIDITY) AS MAX_HUMID,
            TO_CHAR(DATE_TRUNC('week', A.CREATED_AT), 'YYYY/MM/DD') AS CREATED_DATE
        FROM TEMPERATURE A
        INNER JOIN HUMIDITY B
            ON A.CREATED_AT = B.CREATED_AT
            AND A.DEVICE_ID = B.DEVICE_ID
        WHERE
            A.CREATED_AT BETWEEN now() - INTERVAL '4 WEEKS' AND now()
            AND A.DEVICE_ID = :device_id
        GROUP BY CREATED_DATE
        ORDER BY CREATED_DATE DESC
    """
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    rows = result.all()

    result = []
    for i, row in enumerate(rows):
        if i == 4:
            break
        result.append(
            device_schema.DeviceHistorical(
                min_temp=row[0],
                max_temp=row[1],
                min_humid=row[2],
                max_humid=row[3],
                date=row[4],
            )
        )

    result.reverse()

    return result


async def get_historical_device_data_alarm(db: AsyncSession, device_id: str) -> List[device_schema.DeviceHistoricalAlarm]:
    """
    Get historical alarm data

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id

    Returns:
        [device.schema.DeviceHistoricalAlarm]: List of device historical alarm data
    """
    #
    stmt = """
        SELECT
            TO_CHAR(CREATED_AT, 'YYYY/MM/DD') AS DATE,
            TO_CHAR(CREATED_AT, 'HH24:MI') AS HOUR
        FROM ALARM
        WHERE
            DEVICE_ID = :device_id
        AND
            IS_ALARM = True
        ORDER BY DATE, HOUR
    """

    result: Result = await db.execute(stmt, params={"device_id": device_id})
    rows = result.all()

    result = []
    for row in rows:
        result.append(
            device_schema.DeviceHistoricalAlarm(
                date=row[0],
                hour=row[1],
            )
        )

    return result


async def get_latitude_and_longitude(db: AsyncSession, device_id: str) -> Tuple[float | None, float | None]:
    """
    Get the latitude and longitude from the device

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id

    Returns:
        (float, float): Tuples in the order of latitude, longitude.
    """
    stmt = text(
        """
        SELECT
            LATITUDE,
            LONGITUDE
        FROM
            DEVICES A
        WHERE
            A.ID = :device_id
    """
    )
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    first: None | Tuple[float, float] = result.first()
    if first is None:
        return (None, None)
    return first


async def create_device(db: AsyncSession, device_id: str, latitude: float, longitude: float, user_id: int) -> None:
    """
    Create device.

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id.
        latitude (float): Latitude.
        longitude (float): Longitude.
        user_id (str): User id.
    """
    stmt = text(
        """
        INSERT INTO
            DEVICES (ID, LATITUDE, LONGITUDE, USER_ID, CREATED_AT, UPDATED_AT)
        VALUES
            (:device_id, :latitude, :longitude, :user_id, :created_at, :updated_at)
        """
    )
    await db.execute(
        stmt,
        params={
            "device_id": device_id,
            "latitude": latitude,
            "longitude": longitude,
            "user_id": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        },
    )


async def create_device_data(db: AsyncSession, device_id: str, device_data_list: list[device_schema.DeviceDataCreate]) -> None:
    """
    Create each parameter data from device data

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id
        device_data_list (list[device_schema.DeviceDataCreate]): List of device data
    """
    collected_data: dict = {
        "temperature": [],
        "humidity": [],
        "motion": [],
        "alarm": [],
        "button": [],
    }
    for device_data in device_data_list:
        collected_data["temperature"].append({"temperature": device_data.temperature_c, "created_at": device_data.created_at, "device_id": device_id})
        collected_data["humidity"].append({"humidity": device_data.humidity, "created_at": device_data.created_at, "device_id": device_id})
        collected_data["motion"].append({"motion": device_data.motion, "created_at": device_data.created_at, "device_id": device_id})
        collected_data["alarm"].append({"is_alarm": device_data.alarm, "created_at": device_data.created_at, "device_id": device_id})
        collected_data["button"].append({"device_listening": device_data.button, "created_at": device_data.created_at, "device_id": device_id})

    await _create_temperature(db, collected_data["temperature"])
    await _create_humidity(db, collected_data["humidity"])
    await _create_motion(db, collected_data["motion"])
    await _create_alarm(db, collected_data["alarm"])
    await _create_button(db, collected_data["button"])


async def _create_temperature(db: AsyncSession, temperature_data_list: list[dict]) -> None:
    """
    Create temperature data.

    Args:
        db (AsyncSession): AsyncSession
        temperature_data_list (list[dict]): List of temperature table parameters
    """
    stmt = text(
        """
        INSERT INTO
            TEMPERATURE (temperature, created_at, device_id)
        VALUES
            (:temperature, :created_at, :device_id)
    """
    )
    await db.execute(stmt, params=temperature_data_list)


async def _create_humidity(db: AsyncSession, humidity_data_list: list[dict]) -> None:
    """
    Create humidity data.

    Args:
        db (AsyncSession): AsyncSession
        humidity_data_list (list[dict]): List of humidity table parameters
    """
    stmt = text(
        """
        INSERT INTO
            HUMIDITY (humidity, created_at, device_id)
        VALUES
            (:humidity, :created_at, :device_id)
    """
    )
    await db.execute(stmt, params=humidity_data_list)


async def _create_motion(db: AsyncSession, motion_data_list: list[dict]) -> None:
    """
    Create motion data.

    Args:
        db (AsyncSession): AsyncSession
        motion_data_list (list[dict]): List of motion table parameters
    """
    stmt = text(
        """
        INSERT INTO
            MOTION (motion, created_at, device_id)
        VALUES
            (:motion, :created_at, :device_id)
    """
    )
    await db.execute(stmt, params=motion_data_list)


async def _create_alarm(db: AsyncSession, alarm_data_list: list[dict]) -> None:
    """
    Create alarm data.

    Args:
        db (AsyncSession): AsyncSession
        alarm_data_list (list[dict]): List of alarm table parameters
    """
    stmt = text(
        """
        INSERT INTO
            ALARM (is_alarm, created_at, device_id)
        VALUES
            (:is_alarm, :created_at, :device_id)
    """
    )
    await db.execute(stmt, params=alarm_data_list)


async def _create_button(db: AsyncSession, button_data_list: list[dict]) -> None:
    """
    Create button data.

    Args:
        db (AsyncSession): AsyncSession
        button_data_list (list[dict]): List of button table parameters
    """
    stmt = text(
        """
        INSERT INTO
            BUTTON (device_listening, created_at, device_id)
        VALUES
            (:device_listening, :created_at, :device_id)
    """
    )
    await db.execute(stmt, params=button_data_list)
