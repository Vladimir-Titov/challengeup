from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    token: str = Field(validation_alias='TELEGRAM_BOT_TOKEN', default='')
    base_url: str = Field(validation_alias='TELEGRAM_BASE_URL', default='https://api.telegram.org')


telegram_config = TelegramConfig()
