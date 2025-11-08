import asyncio
from sqlalchemy import pool
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.db.database import Base, SQLALCHEMY_DATABASE_URL

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set DB URL from your app
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# Models metadata
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: (
                context.configure(connection=conn, target_metadata=target_metadata),
                context.begin_transaction(),
                context.run_migrations()
            )
        )
    await connectable.dispose()

def run_migrations_online():
    """Trigger async migrations."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()