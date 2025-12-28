import pytest
from fastapi import FastAPI

from pyapi.main.api import create_app


@pytest.fixture(scope="session")
def fastapi_app() -> FastAPI:
    app = create_app()
    return app
