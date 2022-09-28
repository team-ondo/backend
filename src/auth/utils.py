from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.auth as auth_schema
from src.constants.common import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_REFRESH_KEY, JWT_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES
from src.errors.errors import TokenExpiredException, TokenValidationFailException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash_password(password: str) -> str:
    """
    Create hashed password.

    Args:
        password (str): Plain password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


def verify_hash_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the password is valid.

    Args:
        plain_password (str): Plain password.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if the password is valid. False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create access token.

    Args:
        data (TokenPayloadSub): Data to sign.
        expires_delta (timedelta | None): Expire delta. Defaults to None.

    Returns:
        str: Encoded jwt string.
    """
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    _data = data.copy()
    _data.update({"exp": expire})
    return jwt.encode(_data, JWT_SECRET_KEY, ALGORITHM)


def create_refresh_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create refresh access token.

    Args:
        data (TokenPayloadSub): Data to sign.
        expires_delta (timedelta | None): Expire delta. Defaults to None.

    Returns:
        str: Encoded jwt string.
    """
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    _data = data.copy()
    _data.update({"exp": expire})
    return jwt.encode(_data, JWT_REFRESH_KEY, ALGORITHM)


def verify_access_token(token: str, db: AsyncSession) -> auth_schema.TokenPayload:
    """
    Verify the access token.

    Args:
        token (str): Encoded jwt string.
        db (AsyncSession): AsyncSession

    Raises:
        TokenValidationFailException: Failed to validate token.
        TokenExpiredException: Token expired.

    Returns:
        auth_schema.TokenPayload: Payload object.
    """
    try:
        payload: dict = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise TokenValidationFailException()

    token_payload = auth_schema.TokenPayload(**payload)

    if token_payload.user_id is None or token_payload.exp is None:
        raise TokenValidationFailException()

    if datetime.fromtimestamp(token_payload.exp) < datetime.now():
        raise TokenExpiredException()

    return token_payload
