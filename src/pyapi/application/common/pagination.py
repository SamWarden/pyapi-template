from dataclasses import dataclass
from enum import Enum


class SortOrder(Enum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True, slots=True)
class Pagination:
    offset: int | None = None
    limit: int | None = None
    order: SortOrder = SortOrder.ASC


@dataclass(frozen=True, slots=True)
class PaginationResult:
    offset: int | None
    limit: int | None
    total: int
    order: SortOrder

    @classmethod
    def from_pagination(cls, pagination: Pagination, total: int) -> "PaginationResult":
        return cls(offset=pagination.offset, limit=pagination.limit, order=pagination.order, total=total)


@dataclass(frozen=True, slots=True)
class PaginatedItems[Item]:
    data: list[Item]
    pagination: PaginationResult
