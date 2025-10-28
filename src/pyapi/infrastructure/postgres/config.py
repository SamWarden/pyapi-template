from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    host: str
    port: int
    user: str
    password: str
    database: str
    ssl_mode: str
    echo: bool

    @property
    def full_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?ssl={self.ssl_mode}"
