from collections.abc import AsyncGenerator
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config

from sqlalchemy.ext.asyncio import AsyncSession as SAAsyncSession, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession as SMAsyncSession


async_engine = AsyncEngine(
    create_engine(
        url=config.DATABASE_URL,
        echo=True
    )
)


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=SMAsyncSession,
)


async def get_session() -> AsyncGenerator[SAAsyncSession, None]:
    async with async_session_maker() as session:
        yield session
