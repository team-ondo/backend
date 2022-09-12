import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from src.models import alarm, button, device, humidity, motion, notification, temperature, user


USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'postgres'
DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL, echo=True)


async def drop_database():
    async with engine.begin() as conn:
        await conn.run_sync(alarm.Base.metadata.drop_all)
        await conn.run_sync(button.Base.metadata.drop_all)
        await conn.run_sync(device.Base.metadata.drop_all)
        await conn.run_sync(humidity.Base.metadata.drop_all)
        await conn.run_sync(motion.Base.metadata.drop_all)
        await conn.run_sync(notification.Base.metadata.drop_all)
        await conn.run_sync(temperature.Base.metadata.drop_all)
        await conn.run_sync(user.Base.metadata.drop_all)


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(alarm.Base.metadata.create_all)
        await conn.run_sync(button.Base.metadata.create_all)
        await conn.run_sync(device.Base.metadata.create_all)
        await conn.run_sync(humidity.Base.metadata.create_all)
        await conn.run_sync(motion.Base.metadata.create_all)
        await conn.run_sync(notification.Base.metadata.create_all)
        await conn.run_sync(temperature.Base.metadata.create_all)
        await conn.run_sync(user.Base.metadata.create_all)


async def reset_database():
    await drop_database()
    await create_database()


# only run if directly execute this file
if __name__ == "__main__":
    asyncio.run(reset_database())
