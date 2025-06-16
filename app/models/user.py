from sqlalchemy import String
from sqlmodel import SQLModel, Field

from .base import Base, challenges_schema


class User(Base, table=True):
    metadata = challenges_schema

    first_name: str | None = Field(default=None, sa_type=String)
    last_name: str | None = Field(default=None, sa_type=String)
    full_name: str | None = Field(default=None, sa_type=String)
