import uuid
from sqlmodel import SQLModel, Field

from .base import Base, challenges_schema


class Challenges(Base, table=True):
    # metadata = challenges_schema
    title: str
    description: str
