from sqlalchemy import String
from sqlmodel import Field

from .base import BaseSQLModel, challenges_schema


class User(BaseSQLModel, table=True):
    metadata = challenges_schema

    first_name: str | None = Field(default=None, sa_type=String)
    last_name: str | None = Field(default=None, sa_type=String)
    full_name: str | None = Field(default=None, sa_type=String)
