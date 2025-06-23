from sqlalchemy import String
from sqlmodel import Field

from core.types.pydantic_base import BaseUjsonModel


from .base import BaseSQLModel, challenges_schema


class Challenges(BaseSQLModel, BaseUjsonModel, table=True):
    metadata = challenges_schema

    title: str = Field(sa_type=String)
    description: str | None = Field(default=None, sa_type=String)
