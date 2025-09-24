from dataclasses import dataclass
from enum import Enum


class LogFormat(Enum):
    PLAIN = "PLAIN"
    JSON = "JSON"


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    format: LogFormat
    level: str = "DEBUG"
