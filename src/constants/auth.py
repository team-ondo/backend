import os

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose.constants import ALGORITHMS

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 10080  # 60 * 24 * 7 (7 days)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_KEY = os.getenv("JWT_REFRESH_KEY")
ALGORITHM = ALGORITHMS.HS256
BEARER_HEADER = {"WWW-Authenticate": "Bearer"}
TOKEN_EXPIRED_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=BEARER_HEADER)
TOKEN_VALIDATION_FAIL_EXCEPTION = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate token", headers=BEARER_HEADER)
USER_NOT_FOUND_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
USER_ALREADY_EXISTS_EXCEPTION = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
INCORRECT_EMAIL_OR_PASSWORD_EXCEPTION = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
SERIAL_NUMBER_NOT_FOUND_EXCEPTION = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Serial number not found")
SERIAL_NUMBER_ALREADY_REGISTERED_EXCEPTION = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Serial number already registered")
