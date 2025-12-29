import pytest

from pyapi.config import Config
from pyapi.infrastructure.jwt_manager import AuthJwtConfig
from pyapi.infrastructure.log.config import LogFormat, LoggingConfig
from pyapi.infrastructure.postgres.config import PostgresConfig
from pyapi.presentation.api.config import ApiConfig


@pytest.fixture(scope="session")
def config() -> Config:
    return Config(
        log=LoggingConfig(
            format=LogFormat.PLAIN,
            level="DEBUG",
        ),
        postgres=PostgresConfig(
            host="postgres",
            port=5432,
            user="admin",
            password="pass",  # noqa: S106
            database="test_db",
            ssl_mode="disable",
            echo=False,
        ),
        jwt=AuthJwtConfig(public_key="secret", algorithm="HS256"),
        api=ApiConfig(host="test", port=8000),
    )
