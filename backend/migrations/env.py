from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os, sys, pathlib

# add app to PYTHONPATH
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.models import Base         # ...existing code...
from app.config import settings     # ...existing code...

config = context.config
fileConfig(config.config_file_name)

# inject DATABASE_URL from .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=settings.DATABASE_URL, target_metadata=target_metadata,
                      literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()