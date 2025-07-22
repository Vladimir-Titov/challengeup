from sqlalchemy import String
from sqlmodel import Field

from core.types.pydantic_base import BaseUjsonModel

from .base import BaseSQLModel, challenges_schema


class Users(BaseSQLModel, BaseUjsonModel, table=True):
    metadata = challenges_schema

    first_name: str | None = Field(default=None, sa_type=String)
    last_name: str | None = Field(default=None, sa_type=String)
    full_name: str | None = Field(default=None, sa_type=String)
