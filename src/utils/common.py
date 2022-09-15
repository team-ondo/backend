import math


def convert_celsius_to_fahrenheit(temp_c: float) -> float:
    """
    Convert celsius to fahrenheit.
    Second decimal place will be rounded down.

    Args:
        temp_c (float): Celsius temperature

    Returns:
        float: Fahrenheit temperature
    """
    return float_floor(temp_c * 1.8 + 32, 2)


def float_floor(num: float, n: int = 2) -> float:
    """
    Floor float number with specified decimal space.

    Args:
        num (float): Float number
        n (int): Decimal place to floor, Default value is 2.

    Returns:
        float: Rounded down float number
    """
    return float(math.floor(num * 10**n) / (10**n))
