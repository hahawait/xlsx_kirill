from fastapi import FastAPI

from apps.app.router import files_router
from logger.logger import init_logger

from settings import Config


def get_app(config: Config):
    init_logger(config.fastapi_settings.LOGGING_LEVEL)

    fastapi_params = dict(
        title=config.fastapi_settings.PROJECT_NAME,
        version=config.fastapi_settings.VERSION,
    )

    # app = FastAPI(**fastapi_params, debug=False)
    app = FastAPI(**fastapi_params)

    app.include_router(files_router)

    return app