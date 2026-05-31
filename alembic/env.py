"""
Alembic environment configuration.
Executes migration scripts in 'offline' or 'online' mode.
"""
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Ensure /app is importable inside the backend container
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Alembic Config object
config = context.config

# Setup logging (fileConfig interprets the config file as Logging configuration)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models to register them with Base.metadata
from app.database import Base
from app.models import User, Match, Prediction, MatchStatus

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    sqlalchemy_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/worldcup")
    context.configure(
        url=sqlalchemy_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    sqlalchemy_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/worldcup")
    
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = sqlalchemy_url

    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
