import logging

from pyapi.config import Config, load_config
from pyapi.infrastructure.log.main import setup_logging
from pyapi.main.di import setup_di_container
from pyapi.presentation.api.main import create_app, run_app

logger = logging.getLogger(__name__)


def main() -> None:
    config = load_config()
    setup_logging()
    logger.info("Launching app...")

    di_container = setup_di_container(context={Config: config})

    app = create_app(di_container)
    run_app(app, config.api)


if __name__ == "__main__":
    main()
