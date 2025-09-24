from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import dishka
import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from pyapi.presentation.api.config import ApiConfig
from pyapi.presentation.api.middlewares.main import setup_middlewares
from pyapi.presentation.api.orjson import ORJSONResponse
from pyapi.presentation.api.routers.exceptions import setup_exceptions_handlers
from pyapi.presentation.api.routers.main import setup_api_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield
    await app.state.dishka_container.close()


def create_app(di_container: dishka.AsyncContainer | dishka.Container) -> FastAPI:
    app = FastAPI(
        title="PyAPI",
        version="1.0.0",
        servers=[],
        lifespan=lifespan,
        root_path="/api/v1",
        default_response_class=ORJSONResponse,
    )

    setup_middlewares(app)
    setup_api_routers(app)
    setup_exceptions_handlers(app)
    setup_dishka(container=di_container, app=app)

    return app


def run_app(app: FastAPI, config: ApiConfig) -> None:
    uvicorn.run(app, host=config.host, port=config.port, log_config=None)
