import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from alembic import context

# Add app path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import settings and models
from app.settings import settings
from app.models import Base

# Alembic Config object
config = context.config

# Load logging configuration from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# PATCH: convert async DB URL to sync for Alembic
db_url = settings.database_url
if db_url.startswith("sqlite+aiosqlite"):
    db_url = db_url.replace("sqlite+aiosqlite", "sqlite")
elif db_url.startswith("postgresql+asyncpg"):
    db_url = db_url.replace("postgresql+asyncpg", "postgresql")

config.set_main_option("sqlalchemy.url", db_url)

# Set target metadata for autogeneration
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations without a DB connection (generates SQL scripts)."""
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
    """Run migrations with a DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


# Entrypoint for Alembic
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
