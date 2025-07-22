from uuid import UUID

from app.models.challenges import Challenges
from app.repositories.repositories import DBRepositories
from core.repositories.errors import RowNotFoundError
from core.starlette_ext.errors.errors import NotFoundError


class ChallengesService:
    def __init__(self, db_repos: DBRepositories):
        self.db_repos = db_repos

    async def get_challenges(self, **filters) -> list[Challenges]:
        return await self.db_repos.challenges.search(**filters)

    async def create_challenge(self, **payload) -> Challenges:
        return await self.db_repos.challenges.create(**payload)

    async def update_challenge_by_id(self, challenge_id: UUID, **payload) -> Challenges:
        try:
            return await self.db_repos.challenges.update_by_id(entity_id=challenge_id, **payload)
        except RowNotFoundError:
            raise NotFoundError(f'Challenge with id {challenge_id} not found')

    async def get_challenge_by_id(self, challenge_id: UUID) -> Challenges:
        try:
            return await self.db_repos.challenges.get_by_id(entity_id=challenge_id)
        except RowNotFoundError:
            raise NotFoundError(f'Challenge with id {challenge_id} not found')

    async def delete_challenge_by_id(self, challenge_id: UUID) -> Challenges:
        try:
            return await self.db_repos.challenges.archive_by_id(entity_id=challenge_id)
        except RowNotFoundError:
            raise NotFoundError(f'Challenge with id {challenge_id} not found')
