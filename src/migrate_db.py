import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

from src.models import models

load_dotenv()
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)


async def drop_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def reset_database() -> None:
    await drop_database()
    await create_database()


if __name__ == "__main__":
    asyncio.run(reset_database())
