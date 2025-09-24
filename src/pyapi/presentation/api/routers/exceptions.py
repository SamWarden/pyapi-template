import logging
from collections.abc import Awaitable, Callable

from fastapi import Request, status
from starlette.applications import Starlette

from pyapi.domain.error_code import ErrorCode
from pyapi.interface.identity_provider import InvalidIdentityError
from pyapi.presentation.api.orjson import ORJSONResponse
from pyapi.presentation.api.responses.error import ErrorResponse

logger = logging.getLogger(__name__)


def setup_exceptions_handlers(app: Starlette) -> None:
    app.add_exception_handler(
        InvalidIdentityError,
        error_handler(
            http_code=status.HTTP_401_UNAUTHORIZED,
            code=ErrorCode.INVALID_IDENTITY_ERROR,
        ),
    )
    app.add_exception_handler(
        Exception,
        error_handler(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=ErrorCode.INTERNAL_ERROR,
            get_data=lambda err: {},
        ),
    )


def error_handler[E: Exception](
    http_code: int,
    code: ErrorCode,
    get_data: Callable[[E], dict[str, object]] | None = None,
) -> Callable[[Request, E], Awaitable[ORJSONResponse]]:
    if get_data is None:
        get_data = _default_get_data

    async def _handle(request: Request, err: E) -> ORJSONResponse:
        error_data = ErrorResponse(id=request.state.request_id, code=code, data=get_data(err))
        error_response = ORJSONResponse(
            content={"error": error_data},
            status_code=http_code,
        )
        logger.error(
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
        )
        return error_response

    return _handle


def _default_get_data(err: Exception) -> dict[str, object]:
    return dict(vars(err))
