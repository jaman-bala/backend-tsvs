from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from backend.config import settings
from backend.src.account.user.models import BaseUser
from backend.src.regions.models import BaseRegion
from backend.src.departments.models import BaseDepartment

async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

BaseUser.metadata.create_all(async_engine)
BaseRegion.metadata.create_all(async_engine)
BaseDepartment.metadata.create_all(async_engine)


async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    async with async_session_factory() as session:
        yield session
