# import os
# from logging.config import fileConfig
# from sqlalchemy import engine_from_config
# from sqlalchemy import pool
# from alembic import context
#
# from backend.src.account.user.models import BaseUser
# from backend.src.regions.models import BaseRegion
# from backend.src.departments.models import BaseDepartment
#
# config = context.config
#
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)
#
# target_metadata = (
#     BaseUser.metadata,
#     BaseRegion.metadata,
#     BaseDepartment.metadata,
# )
#
# url = os.environ.get("SQLALCHEMY_DATABASE_URL", config.get_main_option("sqlalchemy.url"))
#
#
# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.
#
#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.
#
#     Calls to context.execute() here emit the given string to the
#     script output.
#
#     """
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )
#
#     with context.begin_transaction():
#         context.run_migrations()
#
#
# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.
#
#     In this scenario we need to create an Engine
#     and associate a connection with the context.
#
#     """
#     config_section = config.get_section(config.config_ini_section)
#     config_section["sqlalchemy.url"] = url
#
#     connectable = engine_from_config(
#         config_section,
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#
#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )
#
#         with context.begin_transaction():
#             context.run_migrations()
#
#
# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()

import os
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine

from backend.src.account.user.models import BaseUser
from backend.src.regions.models import BaseRegion
from backend.src.departments.models import BaseDepartment

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = (
    BaseUser.metadata,
    BaseRegion.metadata,
    BaseDepartment.metadata,
)

url = os.environ.get("SQLALCHEMY_DATABASE_URL", config.get_main_option("sqlalchemy.url"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    async_engine = create_async_engine(url, echo=True, future=True)

    # Use an asynchronous context manager for the connection
    async def run():
        async with async_engine.begin() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()

    asyncio.run(run())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


