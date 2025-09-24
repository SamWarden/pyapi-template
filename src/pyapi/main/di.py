from dishka import AsyncContainer, Provider, Scope, from_context, make_async_container, provide, provide_all
from dishka.integrations.fastapi import FastapiProvider
from starlette.requests import Request

from pyapi.config import Config
from pyapi.infrastructure.identity_provider.api import ApiIdentityProvider
from pyapi.infrastructure.jwt_manager import AuthJwtConfig, JwtManagerImpl
from pyapi.interface.identity_provider import IdentityProvider
from pyapi.interface.jwt_manager import JwtManager


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(Config)

    @provide
    def get_jwt_config(self, config: Config) -> AuthJwtConfig:
        return config.jwt


class IdpProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_api_idp(self, request: Request, jwt_manager: JwtManager) -> ApiIdentityProvider:
        token = request.cookies.get("access_token")
        return ApiIdentityProvider(token=token, jwt_manager=jwt_manager)

    @provide
    async def get_idp(self, container: AsyncContainer) -> IdentityProvider:
        idp: IdentityProvider = await container.get(ApiIdentityProvider)
        return idp


class JwtManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_jwt_manager(self, config: AuthJwtConfig) -> JwtManager:
        return JwtManagerImpl(public_key=config.public_key, algorithm=config.algorithm)


class RequestHandlerProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all()


def setup_di_container(context: dict[object, object]) -> AsyncContainer:
    container = make_async_container(
        RequestHandlerProvider(),
        IdpProvider(),
        JwtManagerProvider(),
        ConfigProvider(),
        FastapiProvider(),
        context=context,
    )

    return container
