import logging
import os
from logging.config import fileConfig

import alembic
from alembic import context
from psycopg2 import DatabaseError
from sqlalchemy import create_engine
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.core.config import DATABASE_URL
from app.core.config import POSTGRES_DB


config = context.config

fileConfig(config.config_file_name)

logger = logging.getLogger('alembic.env')


def run_migrations_offline():
    """ Run migrations in 'offline' mode. """
    if os.environ.get('TESTING'):
        raise DatabaseError(
            'Running testing migrations offline currently not permitted.')

    context.configure(
        url=str(DATABASE_URL),
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    DB_URL = f'{DATABASE_URL}_test' if os.environ.get(
        'TESTING') else str(DATABASE_URL)
    # handle testing config for migrations
    if os.environ.get('TESTING'):
        # connect to primary db
        default_engine = create_engine(
            str(DATABASE_URL), isolation_level='AUTOCOMMIT')
        # drop testing db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(f'DROP DATABASE IF EXISTS {POSTGRES_DB}_test')
            default_conn.execute(f'CREATE DATABASE {POSTGRES_DB}_test')

    connectable = config.attributes.get('connection', None)
    config.set_main_option('sqlalchemy.url', DB_URL)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=None
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    logger.info('Running migrations offline')
    run_migrations_offline()
else:
    logger.info('Running migrations online')
    run_migrations_online()
