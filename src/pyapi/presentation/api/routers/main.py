from fastapi import FastAPI

from pyapi.presentation.api.routers.v1 import health


def setup_api_routers(app: FastAPI) -> None:
    app.include_router(health.router)
