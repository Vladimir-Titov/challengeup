from uuid import UUID
from app.models.challenges import Challenges
from app.repositories.repositories import DBRepositories


class ChallengesService:
    def __init__(self, db_repos: DBRepositories):
        self.db_repos = db_repos

    async def get_challenges(self, **filters) -> list[Challenges]:
        return await self.db_repos.challenges.search(**filters)

    async def create_challenge(self, **payload) -> Challenges:
        return await self.db_repos.challenges.create(**payload)

    async def update_challenge_by_id(self, challenge_id: UUID, **payload) -> Challenges:
        return await self.db_repos.challenges.update_by_id(entity_id=challenge_id, **payload)
