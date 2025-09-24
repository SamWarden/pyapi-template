import abc
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Identity:
    id: UUID


class InvalidIdentityError(Exception):
    pass


class IdentityProvider(Protocol):
    @abc.abstractmethod
    async def get_identity(self) -> Identity:
        raise NotImplementedError
