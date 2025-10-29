from dataclasses import dataclass

import environs


@dataclass(frozen=True)
class PostgresConfig:
    host: str
    port: int
    user: str
    password: str
    database: str
    ssl_mode: str

    @property
    def full_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?ssl={self.ssl_mode}"


def load_config() -> PostgresConfig:
    env = environs.Env()

    return PostgresConfig(
        host=env.str("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        database=env.str("POSTGRES_DATABASE"),
        ssl_mode=env.str("POSTGRES_SSLMODE"),
    )
