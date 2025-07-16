from uuid import UUID
from app.models.user_contacts import UserContacts
from app.repositories.repositories import DBRepositories
from core.repositories.errors import RowNotFoundError
from core.starlette_ext.errors.errors import NotFoundError


class UserContactsService:
    def __init__(self, db_repos: DBRepositories):
        self.db_repos = db_repos

    async def get_user_contacts(self, **filters) -> list[UserContacts]:
        return await self.db_repos.user_contacts.search(**filters)

    async def create_user_contact(self, **payload) -> UserContacts:
        return await self.db_repos.user_contacts.create(**payload)

    async def update_user_contact_by_id(self, contact_id: UUID, **payload) -> UserContacts:
        try:
            return await self.db_repos.user_contacts.update_by_id(entity_id=contact_id, **payload)
        except RowNotFoundError:
            raise NotFoundError(f'User contact with id {contact_id} not found')

    async def get_user_contact_by_id(self, contact_id: UUID) -> UserContacts:
        try:
            return await self.db_repos.user_contacts.get_by_id(entity_id=contact_id)
        except RowNotFoundError:
            raise NotFoundError(f'User contact with id {contact_id} not found')

    async def delete_user_contact_by_id(self, contact_id: UUID) -> UserContacts:
        try:
            return await self.db_repos.user_contacts.archive_by_id(entity_id=contact_id)
        except RowNotFoundError:
            raise NotFoundError(f'User contact with id {contact_id} not found')

    async def get_contacts_by_user_id(self, user_id: UUID) -> list[UserContacts]:
        try:
            return await self.db_repos.user_contacts.search(user_id=user_id)
        except RowNotFoundError:
            raise NotFoundError(f'User with id {user_id} not found')
