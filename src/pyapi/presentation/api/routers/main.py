from fastapi import APIRouter, FastAPI

from pyapi.presentation.api.routers.v1 import health


def setup_api_routers(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")
    router.include_router(health.router)

    app.include_router(router)
