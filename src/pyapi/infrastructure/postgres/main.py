from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import orjson
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .config import PostgresConfig


@asynccontextmanager
async def setup_sa_engine(db_config: PostgresConfig) -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(
        db_config.full_url,
        echo=db_config.echo,
        echo_pool=db_config.echo,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=10,
    )
    yield engine

    await engine.dispose()


def setup_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
    return session_factory
