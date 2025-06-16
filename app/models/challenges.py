import uuid
from sqlalchemy import String
from sqlmodel import SQLModel, Field

from .base import Base, challenges_schema


class Challenges(Base, table=True):
    metadata = challenges_schema

    title: str = Field(sa_type=String)
    description: str | None = Field(default=None, sa_type=String)
