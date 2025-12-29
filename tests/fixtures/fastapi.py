import pytest
from dishka import AsyncContainer
from fastapi import FastAPI

from pyapi.presentation.api.main import create_api_app


@pytest.fixture(scope="session")
def fastapi_app(di_container: AsyncContainer) -> FastAPI:
    app = create_api_app(di_container)
    return app
