from app.models.challenges import Challenges
from core.repositories.db import DBRepository


class DBRepositories:
    challenges = DBRepository(Challenges)
