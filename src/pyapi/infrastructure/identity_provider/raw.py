from pyapi.interface.identity_provider import Identity, IdentityProvider


class RawIdentityProvider(IdentityProvider):
    def __init__(self, identity: Identity) -> None:
        self._identity = identity

    async def get_identity(self) -> Identity:
        return self._identity
