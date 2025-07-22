from uuid import UUID
from app.models.user import Users
from app.repositories.repositories import DBRepositories
from core.repositories.errors import RowNotFoundError
from core.starlette_ext.errors.errors import NotFoundError


class UserService:
    def __init__(self, db_repos: DBRepositories):
        self.db_repos = db_repos

    async def get_users(self, **filters) -> list[Users]:
        return await self.db_repos.users.search(**filters)

    async def create_user(self, **payload) -> Users:
        return await self.db_repos.users.create(**payload)

    async def update_user_by_id(self, user_id: UUID, **payload) -> Users:
        try:
            return await self.db_repos.users.update_by_id(entity_id=user_id, **payload)
        except RowNotFoundError:
            raise NotFoundError(f'User with id {user_id} not found')

    async def get_user_by_id(self, user_id: UUID) -> Users:
        try:
            return await self.db_repos.users.get_by_id(entity_id=user_id)
        except RowNotFoundError:
            raise NotFoundError(f'User with id {user_id} not found')

    async def delete_user_by_id(self, user_id: UUID) -> Users:
        try:
            return await self.db_repos.users.archive_by_id(entity_id=user_id)
        except RowNotFoundError:
            raise NotFoundError(f'User with id {user_id} not found')
