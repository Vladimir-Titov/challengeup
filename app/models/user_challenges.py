import uuid
from sqlmodel import Field

from core.types.pydantic_base import BaseUjsonModel
from .base import BaseSQLModel, challenges_schema


class UserChallenges(BaseSQLModel, BaseUjsonModel, table=True):
    __tablename__ = 'user_challenges'
    metadata = challenges_schema

    user_id: uuid.UUID = Field(foreign_key='challenges.users.id')
    challenge_id: uuid.UUID = Field(foreign_key='challenges.challenges.id')