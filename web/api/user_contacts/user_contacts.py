import logging
from functools import partial
from typing import Any

from app.models.user_contacts import UserContacts
from core.utils.types import partial_apply
from core.web.endpoints.base import EndpointMeta, RequestParams
from core.web.endpoints.json import JSONEndpoint
from web.api.schemas import GetByID
from web.mixins.challenges_mixin import ChallengesMixin

from . import schemas

logger = logging.getLogger(__name__)

meta = partial(EndpointMeta, tag='user_contacts')


class GetUserContacts(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Get user contacts')

    schema_query = schemas.GetUserContactsQuery
    schema_response = list[UserContacts]

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_contacts_service.get_user_contacts(**params.query)


class CreateUserContact(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Create user contact')

    schema_body = partial_apply(UserContacts, only=['user_id', 'contact_type', 'contact'])
    schema_response = UserContacts

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_contacts_service.create_user_contact(**params.body)


class UpdateUserContactByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Update user contact by id')

    schema_path = GetByID
    schema_body = partial_apply(UserContacts, only=['contact_type', 'contact'])
    schema_response = UserContacts

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_contacts_service.update_user_contact_by_id(contact_id=params.path['id'], **params.body)


class GetUserContactByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Get user contact by id')

    schema_path = GetByID
    schema_response = UserContacts

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_contacts_service.get_user_contact_by_id(contact_id=params.path['id'])


class DeleteUserContactByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Delete user contact by id')
    schema_path = GetByID
    schema_response = UserContacts

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_contacts_service.delete_user_contact_by_id(contact_id=params.path['id'])


class GetContactsByUserID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Get contacts by user id')

    schema_path = schemas.GetContactsByUserIDPath
    schema_response = list[UserContacts]

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_contacts_service.get_contacts_by_user_id(user_id=params.path['user_id'])
