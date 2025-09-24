from collections.abc import Awaitable, Callable

import structlog
from fastapi import Request, Response


async def structlog_bind_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    structlog.contextvars.bind_contextvars(request_id=str(request.state.request_id))
    return await call_next(request)
