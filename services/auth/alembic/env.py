import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# Allow importing from your app directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import settings and models
from app.settings import settings
from app.models import Base

# Load alembic.ini logging configuration
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 👇 Replace async driver with sync driver for Alembic
db_url = settings.database_url.replace("+aiosqlite", "")  # if using SQLite + async
config.set_main_option("sqlalchemy.url", db_url)

# Set metadata for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# Entry point
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
