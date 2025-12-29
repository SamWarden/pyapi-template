import pytest
from dishka import AsyncContainer

from pyapi.config import Config
from pyapi.main.di import setup_di_container


@pytest.fixture(scope="session")
def di_container(config: Config) -> AsyncContainer:
    di_container = setup_di_container(context={Config: config})
    return di_container
