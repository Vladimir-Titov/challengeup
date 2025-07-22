from functools import partial
import logging
from typing import Any

from app.models.user import Users
from core.utils.types import partial_apply
from core.web.endpoints.base import EndpointMeta, RequestParams
from core.web.endpoints.json import JSONEndpoint
from web.api.schemas import GetByID
from web.mixins.challenges_mixin import ChallengesMixin
from . import schemas

logger = logging.getLogger(__name__)

meta = partial(EndpointMeta, tag='users')


class GetUsers(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Get users')

    schema_query = schemas.GetUsersQuery
    schema_response = list[Users]

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.get_users(**params.query)


class CreateUser(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Create user')

    schema_body = partial_apply(Users, only=['first_name', 'last_name', 'full_name'])
    schema_response = Users

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.create_user(**params.body)


class UpdateUserByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Update user by id')

    schema_path = GetByID
    schema_body = partial_apply(Users, only=['first_name', 'last_name', 'full_name'])
    schema_response = Users

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.update_user_by_id(user_id=params.path['id'], **params.body)


class GetUserByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Get user by id')

    schema_path = GetByID
    schema_response = Users

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.get_user_by_id(user_id=params.path['id'])


class DeleteUserByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Delete user by id')

    schema_path = GetByID
    schema_response = Users

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.delete_user_by_id(user_id=params.path['id'])
