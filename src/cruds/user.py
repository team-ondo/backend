from datetime import datetime
from typing import List, Tuple

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

import src.schemas.user as user_schema
from src.auth.utils import create_hash_password


async def count_user_by_user_id(db: AsyncSession, user_id: int) -> int:
    """
    Count user by user id.

    Args:
        db (AsyncSession): AsyncSession.
        user_id (int): User id.

    Returns:
        int: Count result.
    """
    stmt = text(
        """
        SELECT
            COUNT(*) AS CNT
        FROM
            USERS A
        WHERE
            A.ID = :user_id
        """
    )
    count_result: Result = await db.execute(stmt, params={"user_id": user_id})
    return count_result.one()[0]


async def count_user_by_email(db: AsyncSession, email: str) -> int:
    """
    Count user by email.

    Args:
        db (AsyncSession): AsyncSession.
        user_id (int): Email.

    Returns:
        int: Count result.
    """
    stmt = text(
        """
        SELECT
            COUNT(*) AS CNT
        FROM
            USERS A
        WHERE
            A.EMAIL = :email
        """
    )
    count_result: Result = await db.execute(stmt, params={"email": email})
    return count_result.one()[0]


async def find_user_by_email(db: AsyncSession, email: str) -> Tuple[int, str] | None:
    """
    Find user by email.
    None when the user was not found.

    Args:
        db (AsyncSession): AsyncSession.
        email (str): Email

    Returns:
        Tuple[int, str] | None: Tuples in order of user id and password. Or None.
    """
    stmt = text(
        """
        SELECT
            ID,
            PASSWORD
        FROM
            USERS A
        WHERE
            A.EMAIL = :email
        """
    )
    result: Result = await db.execute(stmt, params={"email": email})
    return result.first()


async def create_user(db: AsyncSession, user: user_schema.UserCreate) -> int:
    """
    Create user.
    Return the created user id.

    Args:
        db (AsyncSession): AsyncSession
        user (user_schema.UserCreate): UserCreate object.

    Returns:
        int: Created user id.
    """
    stmt = text(
        """
        INSERT INTO
            USERS (FIRST_NAME, LAST_NAME, EMAIL, PHONE_NUMBER, PASSWORD, CREATED_AT, UPDATED_AT)
        VALUES
            (:first_name, :last_name, :email, :phone_number, :password, :created_at, :updated_at)
        RETURNING ID
        """
    )
    result: Result = await db.execute(
        stmt,
        params={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "password": create_hash_password(user.password),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        },
    )
    created_user_id = result.first()[0]
    return created_user_id


async def find_device_id_by_user_id(db: AsyncSession, user_id: int) -> List[user_schema.UserDevice]:
    """
    Find device id owned by user.

    Args:
        db (AsyncSession): AsyncSession.
        user_id (int): User id.

    Returns:
        List[user_schema.UserDevice]: List of UserDevice object.
    """
    stmt = text(
        """
        SELECT
            A.ID
        FROM
            DEVICES A
        WHERE
            A.USER_ID = :user_id
        """
    )
    execute_result: Result = await db.execute(stmt, params={"user_id": user_id})

    result = []
    rows = execute_result.all()
    for row in rows:
        result.append(user_schema.UserDevice(device_id=row[0]))

    return result
