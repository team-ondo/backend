import pytest

from src.utils.common import convert_celsius_to_fahrenheit, fetch_longitude_latitude_from_zip_code, float_floor, is_phone_number, is_zip_code


def test_convert_celsius_to_fahrenheit() -> None:
    celsius = 20.4
    expected = 68.72
    assert convert_celsius_to_fahrenheit(celsius) == expected


def test_float_floor() -> None:
    num = 10.269
    n = 1
    expected = 10.2
    assert float_floor(num, n) == expected


def test_is_phone_number_valid() -> None:
    phone_numbers = [
        "01-1111-1111",
        "011-111-1111",
        "0111-11-1111",
        "01111-1-1111",
        "090-1111-1111",
        "080-1111-1111",
        "070-1111-1111",
        "020-1111-1111",
    ]
    for phone_number in phone_numbers:
        assert is_phone_number(phone_number)


def test_is_phone_number_invalid() -> None:
    phone_numbers = [
        "01111-1111-1111",
        "01111-111-1111",
        "01111-11-1111",
        "0111-1111-1111",
        "0111-111-1111",
        "0111-1-1111",
        "011-1111-1111",
        "011-11-1111",
        "011-1-1111",
        "01-111-1111",
        "01-11-1111",
        "01-1-1111",
        "010-1111-1111",
        "030-1111-1111",
        "040-1111-1111",
        "050-1111-1111",
        "060-1111-1111",
    ]
    for phone_number in phone_numbers:
        assert not is_phone_number(phone_number)


def test_is_zip_code_valid() -> None:
    v = "1234567"
    assert is_zip_code(v)


def test_is_zip_code_invalid() -> None:
    zip_codes = [
        "1",
        "12",
        "123",
        "1234",
        "12345",
        "123456",
        "12345678",
        "123-4567",
    ]
    for zip_code in zip_codes:
        assert not is_zip_code(zip_code)


def test_fetch_longitude_latitude_from_zip_code_valid() -> None:
    zip_code = "1250062"
    result = fetch_longitude_latitude_from_zip_code(zip_code)
    expected = (139.854395, 35.749805)
    assert result == expected


def test_fetch_longitude_latitude_from_zip_code_invalid() -> None:
    zip_code = "12345678"
    with pytest.raises(ValueError) as e:
        fetch_longitude_latitude_from_zip_code(zip_code)

    assert str(e.value) == "Cannot found longitude and latitude from zip code"
