from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogsConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    log_level: str = Field(default='debug', validation_alias='LOG_LEVEL')
    log_config: str = Field(default='log_cfg.yaml', validation_alias='LOG_CONFIG')
    use_colors: bool = Field(default=True, validation_alias='USE_COLORS')


logs_config = LogsConfig()
