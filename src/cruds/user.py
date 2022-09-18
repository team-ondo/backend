from datetime import datetime
from typing import Tuple

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src.auth.utils import create_hash_password
from src.schemas.user import UserCreate


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


async def create_user(db: AsyncSession, user: UserCreate) -> None:
    """
    Create user.

    Args:
        db (AsyncSession): AsyncSession
        user (UserCreate): UserCreate object.
    """
    stmt = text(
        """
        INSERT INTO
            USERS (FIRST_NAME, LAST_NAME, EMAIL, PHONE_NUMBER, PASSWORD, CREATED_AT, UPDATED_AT)
        VALUES
            (:first_name, :last_name, :email, :phone_number, :password, :created_at, :updated_at)
        """
    )
    await db.execute(
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
    await db.commit()
