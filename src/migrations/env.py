import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from migrations.config import load_config
from pyapi.infrastructure.postgres.models.base import BaseModel

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

pg_config = load_config()
FULL_URL = pg_config.full_url

TARGET_METADATA = BaseModel.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=FULL_URL,
        target_metadata=TARGET_METADATA,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=TARGET_METADATA)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(engine: Engine) -> None:
    with engine.connect() as connection:
        do_run_migrations(connection)

    engine.dispose()


async def run_async_migrations(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()


def setup_engine() -> Engine:
    return engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
        url=FULL_URL,
    )


def run_migrations_online() -> None:
    connection: Connection | None = config.attributes.get("connection", None)
    match connection:
        case None:
            engine = setup_engine()
            if engine.driver == "asyncpg":
                async_engine = AsyncEngine(engine)
                asyncio.run(run_async_migrations(async_engine))
            else:
                run_migrations(engine)
        case Connection():
            do_run_migrations(connection)
        case _:
            raise UnexpectedConnectionTypeError(type(connection))


class UnexpectedConnectionTypeError(TypeError):
    def __init__(self, value: type[object]) -> None:
        self.value = value


def main() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


main()
