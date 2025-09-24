from dataclasses import dataclass
from uuid import UUID

from pyapi.domain.error_code import ErrorCode


@dataclass(frozen=True, slots=True)
class ErrorResponse:
    id: UUID
    data: dict[str, object]
    code: ErrorCode
