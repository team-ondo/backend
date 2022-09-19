from typing import Tuple

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

import src.schemas.device as device_schema


async def get_latest_device_data(db: AsyncSession, device_id: str) -> Tuple[float | None, float | None]:
    """Get latest device info

    Get the latest temperature, humidity from the database.

    Args:
        db (AsyncSession): AsyncSession
        device_id (str): Device id

    Returns:
        (float, float): Tuples in the order of temperature, humidity.
    """
    stmt = text(
        """
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
            ) SUB_HUMID
        WHERE
            SUB_TEMP.NUM = 1
            AND SUB_HUMID.NUM = 1
    """
    )
    result: Result = await db.execute(stmt, params={"device_id": device_id})
    first: None | Tuple[float, float] = result.first()
    if first is None:
        return (None, None)
    return first


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
    await db.commit()


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
    await db.commit()


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
    await db.commit()


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
    await db.commit()


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
    await db.commit()
