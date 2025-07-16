from uuid import UUID
from app.models.user import User
from app.repositories.repositories import DBRepositories
from core.repositories.errors import RowNotFoundError
from core.starlette_ext.errors.errors import NotFoundError


class UserService:
    def __init__(self, db_repos: DBRepositories):
        self.db_repos = db_repos

    async def get_users(self, **filters) -> list[User]:
        return await self.db_repos.user.search(**filters)

    async def create_user(self, **payload) -> User:
        return await self.db_repos.user.create(**payload)

    async def update_user_by_id(self, user_id: UUID, **payload) -> User:
        try:
            return await self.db_repos.user.update_by_id(entity_id=user_id, **payload)
        except RowNotFoundError:
            raise NotFoundError(f'User with id {user_id} not found')

    async def get_user_by_id(self, user_id: UUID) -> User:
        try:
            return await self.db_repos.user.get_by_id(entity_id=user_id)
        except RowNotFoundError:
            raise NotFoundError(f'User with id {user_id} not found')

    async def delete_user_by_id(self, user_id: UUID) -> User:
        try:
            return await self.db_repos.user.archive_by_id(entity_id=user_id)
        except RowNotFoundError:
            raise NotFoundError(f'User with id {user_id} not found')
