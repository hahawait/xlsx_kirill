from typing import Literal
from functools import lru_cache
from dataclasses import dataclass

from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings as PydanticSettings


class BaseSettings(PydanticSettings):
    model_config = SettingsConfigDict(env_file="prod.env", extra="allow")


class DriverSettings(BaseSettings):
    DRIVER_PATH: str | None = 'driver/chromedriver.exe'


class FastAPISettings(BaseSettings):
    MODE: Literal["PROD", "DEV", "LOCAL"] = "LOCAL"

    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    FASTAPI_DOMAIN: str = F"http://{FASTAPI_HOST}"

    LOGGING_LEVEL: Literal["DEBUG", "INFO", "WARN", "ERROR", "FATAL"] = "INFO"

    PROJECT_NAME: str = "FastAPI"
    VERSION: str = "1.0.0"


@dataclass
class Config:
    driver_settings: DriverSettings
    fastapi_settings: FastAPISettings


@lru_cache
def get_config():
    return Config(
        driver_settings=DriverSettings(),
        fastapi_settings=FastAPISettings()
    )
