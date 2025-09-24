from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiConfig:
    host: str
    port: int
