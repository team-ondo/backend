from src.utils.common import convert_celsius_to_fahrenheit, float_floor


def test_convert_celsius_to_fahrenheit() -> None:
    celsius = 20.4
    expected = 68.72
    assert convert_celsius_to_fahrenheit(celsius) == expected


def test_float_floor() -> None:
    num = 10.269
    n = 1
    expected = 10.2
    assert float_floor(num, n) == expected
