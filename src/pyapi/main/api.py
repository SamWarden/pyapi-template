import logging

from fastapi import FastAPI

from pyapi.config import Config, load_config
from pyapi.infrastructure.log.main import setup_logging
from pyapi.main.di import setup_di_container
from pyapi.presentation.api.main import create_api_app, run_app

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    config = load_config()
    setup_logging(config.log)

    di_container = setup_di_container(context={Config: config})
    app = create_api_app(di_container)

    logger.info("Created FastAPI app")

    return app


def main() -> None:
    app = create_app()
    config = load_config()

    run_app(app, config.api)


if __name__ == "__main__":
    main()
