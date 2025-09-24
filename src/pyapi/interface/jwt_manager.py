import abc
from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AuthPayload:
    user_id: UUID


class UnmarshalJwtError(ValueError):
    pass


class JwtManager(Protocol):
    @abc.abstractmethod
    def unmarshal_jwt(self, token: str) -> AuthPayload:
        raise NotImplementedError
