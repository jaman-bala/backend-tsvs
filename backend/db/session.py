from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from backend.config import settings
from backend.src.account.user.models import BaseUser
from backend.src.regions.models import BaseRegion
from backend.src.departments.models import BaseDepartment

# Создание синхронного движка для создания таблиц
sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL.replace('asyncpg', 'psycopg2'),
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

# Создание всех таблиц
BaseUser.metadata.create_all(sync_engine)
BaseRegion.metadata.create_all(sync_engine)
BaseDepartment.metadata.create_all(sync_engine)

# Создание асинхронного движка и сессии для работы с асинхронным кодом
async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session
