import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
Base = declarative_base()


async def get_db() -> sessionmaker:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        else:
            await session.commit()
