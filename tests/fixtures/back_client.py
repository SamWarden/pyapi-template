from collections.abc import AsyncIterator

import httpx
import pytest
from fastapi import FastAPI


@pytest.fixture(scope="session")
async def back_client(fastapi_app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=fastapi_app), base_url="http://test/api/v1"
    ) as client:
        yield client
