from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    debug: bool = Field(default=False, validation_alias='DEBUG')
    port: int = Field(default=5000, validation_alias='PORT')
    event_loop: str = Field(default='uvloop', validation_alias='EVENT_LOOP')
    cors_settings: dict[str, Any] = Field(
        default={
            'allow_origins': ['*'],
            'allow_methods': ['*'],
            'allow_headers': ['*'],
        },
        validation_alias='CORS_SETTINGS',
    )


app_config = AppConfig()
