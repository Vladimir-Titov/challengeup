from app.models.challenges import Challenges
from app.repositories.repositories import DBRepositories


class ChallengesService:
    def __init__(self, db_repos: DBRepositories):
        self.db_repos = db_repos

    async def get_challenges(self, **filters) -> list[Challenges]:
        return await self.db_repos.challenges.search(**filters)
