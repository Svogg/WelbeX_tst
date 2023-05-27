from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, create_session, Session
from config import DB_DRIVER, DB_CONNECTOR, CELERY_DB_CONNECTOR, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = "{}+{}://{}:{}@{}:{}/{}".format(
    DB_DRIVER, DB_CONNECTOR,
    DB_USER, DB_PASS,
    DB_HOST, DB_PORT,
    DB_NAME
)

CELERY_DATABASE_URL = "{}+{}://{}:{}@{}:{}/{}".format(
    DB_DRIVER, CELERY_DB_CONNECTOR,
    DB_USER, DB_PASS,
    DB_HOST, DB_PORT,
    DB_NAME
)

Base = declarative_base()

metadata = MetaData()

celery_engine = create_session(CELERY_DATABASE_URL)


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session



