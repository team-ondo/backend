from typing import List, Type

from fastapi import status

BEARER_HEADER = {"WWW-Authenticate": "Bearer"}


class APIError(Exception):
    status_code: int = 400
    detail: str = "Error message detail"
    headers: dict | None = None


class TokenExpiredException(APIError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"
    headers = BEARER_HEADER


class TokenValidationFailException(APIError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Could not validate token"
    headers = BEARER_HEADER


class UserNotFoundException(APIError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Could not find user"


class UserAlreadyExistsException(APIError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User already exists"


class IncorrectEmailOrPasswordException(APIError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect email or password"


class SerialNumberNotFoundException(APIError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Serial number not found"


class SerialNumberAlreadyRegisteredException(APIError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Serial number already registered"


class WeatherLangSupportException(APIError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Only supports `en` or `ja`"


class WeatherAPIRequestError(APIError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to request to OpenWeatherAPI"


def error_response(error_types: List[Type[APIError]]) -> dict:
    """
    Convert error_types to OpenAPI format.

    Args:
        error_types (List[Type[APIError]]): List of APIError.

    Returns:
        dict: Error types OpenAPI format.
    """
    result: dict = {}
    for error_type in error_types:
        status_code = error_type.status_code
        detail = error_type.detail
        if not result.get(status_code):
            result[status_code] = {
                "description": f'"{detail}"',
                "content": {
                    "application/json": {
                        "example": {
                            "detail": detail,
                        }
                    }
                },
            }
        else:
            result[status_code]["description"] += f'<br>"{detail}"'
    return result
