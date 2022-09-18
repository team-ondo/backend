import math
import re
from typing import Tuple

import requests
from requests.exceptions import RequestException

HEART_RAILS_API = "http://geoapi.heartrails.com/api/json?method=searchByPostal"


def convert_celsius_to_fahrenheit(temp_c: float) -> float:
    """
    Convert celsius to fahrenheit.
    Second decimal place will be rounded down.

    Args:
        temp_c (float): Celsius temperature.

    Returns:
        float: Fahrenheit temperature.
    """
    return float_floor(temp_c * 1.8 + 32, 2)


def float_floor(num: float, n: int = 2) -> float:
    """
    Floor float number with specified decimal space.

    Args:
        num (float): Float number.
        n (int): Decimal place to floor, Default value is 2.

    Returns:
        float: Rounded down float number.
    """
    return float(math.floor(num * 10**n) / (10**n))


def is_phone_number(v: str) -> bool:
    """
    Check it is phone number.

    Args:
        v (str): Value.

    Returns:
        bool: True if it is phone number. False otherwise.
    """
    # Japan landline phone numbers
    # 0X-XXXX-XXXX
    # 0XX-XXX-XXXX
    # 0XXX-XX-XXXX
    # 0XXXX-X-XXXX
    RE_LANDLINE_PHONE = r"^0([0-9]-[0-9]{4}|[0-9]{2}-[0-9]{3}|[0-9]{3}-[0-9]{2}|[0-9]{4}-[0-9])-[0-9]{4}$"

    # Japan wireless phone
    # 090-XXXX-XXXX
    # 080-XXXX-XXXX
    # 070-XXXX-XXXX
    # 020-XXXX-XXXX
    RE_WIRELESS_PHONE = r"^(090|080|070|020)-[0-9]{4}-[0-9]{4}$"

    if re.fullmatch(RE_LANDLINE_PHONE, v) is None and re.fullmatch(RE_WIRELESS_PHONE, v) is None:
        return False
    return True


def is_zip_code(v: str) -> bool:
    """
    Check it is zip code.

    Args:
        v (str): Value.

    Returns:
        bool: True if it is zip code. False otherwise.
    """
    if re.fullmatch(r"^[0-9]{7}$", v) is None:
        return False
    return True


def fetch_longitude_latitude_from_zip_code(zip_code: str) -> Tuple[float, float]:
    """
    Fetch longitude and latitude from zip code.

    Args:
        zip_code (str): Zip code.

    Raises:
        ValueError: If the HeartRailsAPI Request fails.
        ValueError: If the longitude and latitude cannot find from zip code.

    Returns:
        Tuple[float, float]: Tuples in the order of longitude, latitude.
    """
    params = {"postal": zip_code}
    r = requests.get(HEART_RAILS_API, params=params)
    try:
        r.raise_for_status()
    except RequestException as e:
        # TODO Replace with logger
        print(f"Request failed: {e.response.text}")
        raise ValueError("HeartRailsAPI Request Error")

    response = r.json().get("response")
    error = response.get("error")
    if error is not None:
        raise ValueError("Cannot found longitude and latitude from zip code")

    # TODO Even if the same zip code is the same, the prefecture may be different
    # Examples
    # 4980000   愛知県
    # 4980000   三重県
    # 6180000   京都府
    # 6180000   大阪府
    # 8710000   福岡県
    # 8710000   大分県
    location = response.get("location")[0]
    longitude = float(location["x"])
    latitude = float(location["y"])

    return (longitude, latitude)
