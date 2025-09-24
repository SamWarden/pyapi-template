from pyapi.interface.identity_provider import Identity, IdentityProvider, InvalidIdentityError
from pyapi.interface.jwt_manager import JwtManager, UnmarshalJwtError


class ApiIdentityProvider(IdentityProvider):
    def __init__(self, token: str | None, jwt_manager: JwtManager) -> None:
        self._token = token
        self._jwt_manager = jwt_manager

    async def get_identity(self) -> Identity:
        try:
            payload = self._jwt_manager.unmarshal_jwt(self._token or "")
        except UnmarshalJwtError as err:
            raise InvalidIdentityError from err

        return Identity(id=payload.user_id)
