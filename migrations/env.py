from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import SQLModel
from decouple import config as conf
from alembic import context
import os

# Import all models here so SQLModel can find them
from app import models  # Make sure this imports all your models

# this is the Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", conf("DATABASE_URL"))

# Set the database URL from environment
database_url = conf("DATABASE_URL")
print(f"Attempting to connect to: {database_url}")

# Handle SQLite database creation
if database_url.startswith('sqlite:///'):
    db_path = database_url.replace('sqlite:///', '')
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    # Touch the file to create it
    if not os.path.exists(db_path):
        open(db_path, 'a').close()
        print(f"Created SQLite database file at: {db_path}")
else:
    # For other databases (PostgreSQL, MySQL, etc.)
    engine = create_engine(database_url)
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created successfully!")

# Make sure all models are imported and metadata is loaded
target_metadata = SQLModel.metadata

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
