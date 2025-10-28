import base64
from dataclasses import dataclass

import environs

from pyapi.infrastructure.jwt_manager import AuthJwtConfig
from pyapi.infrastructure.log.config import LogFormat, LoggingConfig
from pyapi.infrastructure.postgres.config import PostgresConfig
from pyapi.presentation.api.config import ApiConfig


@dataclass(frozen=True, slots=True)
class Config:
    log: LoggingConfig
    postgres: PostgresConfig
    jwt: AuthJwtConfig
    api: ApiConfig


def load_config() -> Config:
    env = environs.Env()

    return Config(
        log=LoggingConfig(
            format=env.enum("LOG_FORMAT", enum=LogFormat, by_value=True),
            level=env.str("LOG_LEVEL"),
        ),
        postgres=PostgresConfig(
            host=env.str("POSTGRES_HOST"),
            port=env.int("POSTGRES_PORT"),
            user=env.str("POSTGRES_USER"),
            password=env.str("POSTGRES_PASSWORD"),
            database=env.str("POSTGRES_DATABASE"),
            ssl_mode=env.str("POSTGRES_SSLMODE"),
            echo=env.bool("POSTGRES_ECHO"),
        ),
        jwt=AuthJwtConfig(
            public_key=base64.b64decode(env.str("AUTH_JWT_PUBLIC_KEY")).decode(),
            algorithm=env.str("AUTH_JWT_ALGORITHM"),
        ),
        api=ApiConfig(
            host=env.str("API_HOST"),
            port=env.int("API_PORT"),
        ),
    )
