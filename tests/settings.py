from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    TEST_DB_URL: Optional[str] = None

    class Config:
        env_file = Path(__file__).resolve().parent.joinpath('.env')


test_settings = TestSettings()
