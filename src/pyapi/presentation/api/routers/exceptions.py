import logging
from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Request, status
from starlette.applications import Starlette

from pyapi.domain.error_code import ErrorCode
from pyapi.interface.identity_provider import InvalidIdentityError
from pyapi.presentation.api.orjson import ORJSONResponse
from pyapi.presentation.api.responses.error import ErrorResponse

logger = logging.getLogger(__name__)


def setup_exceptions_handlers(app: Starlette) -> None:
    add_exception_handlers(
        app,
        [
            ExceptionHandler(
                exception=InvalidIdentityError,
                http_code=status.HTTP_401_UNAUTHORIZED,
                code=ErrorCode.INVALID_IDENTITY_ERROR,
            ),
            ExceptionHandler(
                exception=Exception,
                http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                code=ErrorCode.INTERNAL_ERROR,
                get_data=lambda err: {},
                log_level="ERROR",
            ),
        ],
    )


def add_exception_handlers(app: Starlette, handlers: list["ExceptionHandler[Exception]"]) -> None:
    for handler in handlers:
        app.add_exception_handler(handler.exception, handler)


def _default_get_data(err: object) -> dict[str, object]:
    return dict(vars(err))


@dataclass(slots=True, frozen=True)
class ExceptionHandler[E]:
    exception: type[E]
    http_code: int
    code: ErrorCode
    get_data: Callable[[E], dict[str, object]] = _default_get_data
    log_level: str = "WARNING"

    async def __call__(self, request: Request, err: E) -> ORJSONResponse:
        error_data = ErrorResponse(id=request.state.request_id, code=self.code, data=self.get_data(err))
        error_response = ORJSONResponse(
            content={"error": error_data},
            status_code=self.http_code,
        )
        exception_info: dict[str, E] = {"exc_info": err} if self.log_level == "ERROR" else {}
        logger.log(
            logging.getLevelName(self.log_level),
            "An error occurred: %r",
            err,
            extra={
                "error_code": error_data.code,
                "request": {
                    "method": request.method,
                    "url": str(request.url),
                },
                "status_code": error_response.status_code,
            },
            **exception_info,  # type: ignore[arg-type]
        )
        return error_response
