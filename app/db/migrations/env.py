import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import DATABASE_URL
from app.core.config import POSTGRES_DB
from app.core.logging import logger
from app.db import models

# models metadata for autogenerate support
target_metadata = models.Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    if os.environ.get('TESTING'):
        raise Exception(
            'Running testing migrations offline currently not permitted.')

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    DB_URL = f'{DATABASE_URL}_test' if os.environ.get(
        'TESTING') else DATABASE_URL

    if os.environ.get('TESTING'):
        logger.info('RUNNING ON TEST DATABASE')
        # connect to primary db
        engine = create_async_engine(
            DB_URL, isolation_level='AUTOCOMMIT')
        # drop testing db if it exists and create a fresh one
        async with engine.connect() as connection:
            # TODO: try if it works replacig string with
            # target_metadata.drop_all etc
            await connection.execute(f'DROP DATABASE IF EXISTS {POSTGRES_DB}_test')
            await connection.execute(f'CREATE DATABASE {POSTGRES_DB}_test')

    connectable = config.attributes.get('connection', None)
    config.set_main_option('sqlalchemy.url', DB_URL)

    if connectable is None:
        connectable = AsyncEngine(
            engine_from_config(
                config.get_section(config.config_ini_section),
                prefix='sqlalchemy.',
                poolclass=pool.NullPool,
                future=True,
            )
        )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    logger.info('RUNNING OFFLINE')
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
