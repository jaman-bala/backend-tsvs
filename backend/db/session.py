from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from backend.config import settings

async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    async with async_session_factory() as session:
        yield session
