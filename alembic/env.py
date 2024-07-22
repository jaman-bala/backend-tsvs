import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

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

url = os.environ.get("SQLALCHEMY_DATABASE_URL" + "?async_fallback=True", config.get_main_option("sqlalchemy.url"))


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
    connectable = create_engine(url, echo=True, future=True, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
