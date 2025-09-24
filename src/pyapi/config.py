import base64
from dataclasses import dataclass

import environs

from pyapi.infrastructure.jwt_manager import AuthJwtConfig
from pyapi.infrastructure.log.config import LogFormat, LoggingConfig
from pyapi.presentation.api.config import ApiConfig


@dataclass(frozen=True, slots=True)
class Config:
    log: LoggingConfig
    jwt: AuthJwtConfig
    api: ApiConfig


def load_config() -> Config:
    env = environs.Env()

    return Config(
        log=LoggingConfig(
            format=env.enum("LOG_FORMAT", enum=LogFormat, by_value=True),
            level=env.str("LOG_LEVEL"),
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
