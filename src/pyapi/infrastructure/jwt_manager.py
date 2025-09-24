from dataclasses import dataclass
from uuid import UUID

import jwt

from pyapi.interface.jwt_manager import AuthPayload, JwtManager, UnmarshalJwtError


@dataclass(frozen=True, slots=True)
class AuthJwtConfig:
    public_key: str
    algorithm: str


class JwtManagerImpl(JwtManager):
    def __init__(self, public_key: str, algorithm: str = "HS256") -> None:
        self._public_key = public_key
        self._algorithm = algorithm

    def unmarshal_jwt(self, token: str) -> AuthPayload:
        try:
            raw_data = jwt.decode(token, self._public_key, [self._algorithm])
            user_id = UUID(raw_data["user_id"])
        except Exception as err:
            raise UnmarshalJwtError from err
        return AuthPayload(user_id=user_id)
