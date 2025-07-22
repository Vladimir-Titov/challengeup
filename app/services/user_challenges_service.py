from uuid import UUID
from app.repositories.repositories import DBRepositories
from app.models.user_challenges import UserChallenges


class UserChallengesService:
    def __init__(self, db_repos: DBRepositories):
        self.db_repos = db_repos

    async def get_user_challenges(self, **filters) -> list[UserChallenges]:
        return await self.db_repos.user_challenges.search(**filters)

    async def create_user_challenge(self, **payload) -> UserChallenges:
        return await self.db_repos.user_challenges.create(**payload)

    async def get_user_challenge_by_id(self, user_challenge_id: UUID) -> UserChallenges:
        return await self.db_repos.user_challenges.get_by_id(user_challenge_id)

    async def update_user_challenge_by_id(self, user_challenge_id: UUID, **payload) -> UserChallenges:
        return await self.db_repos.user_challenges.update_by_id(user_challenge_id, **payload)

    async def delete_user_challenge_by_id(self, user_challenge_id: UUID) -> UserChallenges:
        return await self.db_repos.user_challenges.archive_by_id(user_challenge_id)