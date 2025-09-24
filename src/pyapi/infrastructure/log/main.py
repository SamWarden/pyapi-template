import logging.config
from collections.abc import Callable
from uuid import UUID

import orjson
import pydantic
import structlog
from sqlalchemy import log as sa_log
from structlog.processors import CallsiteParameter, CallsiteParameterAdder
from structlog.typing import EventDict

from pyapi.infrastructure.log.config import LogFormat, LoggingConfig

ProcessorType = Callable[
    [
        structlog.types.WrappedLogger,
        str,
        structlog.types.EventDict,
    ],
    str | bytes,
]

logger_ = logging.getLogger(__name__)


def additionally_serialize(obj: object) -> object:
    match obj:
        case UUID() as obj:
            return str(obj)
        case pydantic.BaseModel() as obj:
            return obj.dict()

    logger_.warning("Type is not JSON serializable: %s", type(obj), extra={"obj": repr(obj)})
    return repr(obj)


def serialize_to_json(data: EventDict, default: Callable[[object], object]) -> str:
    result: str = orjson.dumps(
        data,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_SERIALIZE_UUID,
        default=additionally_serialize,
    ).decode()
    return result


class UnknownLogFormatError(ValueError):
    def __init__(self, log_format: LogFormat) -> None:
        self.log_format = log_format
        super().__init__(f"Unknown log format value: {log_format}")


def get_render_processor(
    *,
    log_format: LogFormat,
    serializer: Callable[[EventDict, Callable[[object], object]], str | bytes] = serialize_to_json,
    colors: bool = True,
) -> ProcessorType:
    processor: ProcessorType
    match log_format:
        case LogFormat.PLAIN:
            processor = structlog.dev.ConsoleRenderer(colors=colors)
        case LogFormat.JSON:
            processor = structlog.processors.JSONRenderer(serializer=serializer)
        case _:
            raise UnknownLogFormatError(log_format)
    return processor


def setup_logging(config: LoggingConfig) -> None:
    # Mute SQLAlchemy default logger handler
    sa_log._add_default_handler = lambda logger: None  # noqa: SLF001

    common_processors = (
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ExtraAdder(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True),
        structlog.contextvars.merge_contextvars,
        structlog.processors.format_exc_info,  # print exceptions from event dict
        CallsiteParameterAdder(
            (
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            ),
        ),
    )
    logging_processors = (structlog.stdlib.ProcessorFormatter.remove_processors_meta,)
    logging_console_processors = (
        *logging_processors,
        get_render_processor(log_format=config.format, colors=True),
    )

    handler = logging.StreamHandler()
    handler.set_name("default")
    handler.setLevel(config.level)
    console_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=common_processors,
        processors=logging_console_processors,
    )
    handler.setFormatter(console_formatter)

    handlers: list[logging.Handler] = [handler]

    logging.basicConfig(handlers=handlers, level=config.level)
