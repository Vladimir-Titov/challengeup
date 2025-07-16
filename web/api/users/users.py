from functools import partial
import logging
from typing import Any

from app.models.user import User
from core.utils.types import partial_apply
from core.web.endpoints.base import EndpointMeta, RequestParams
from core.web.endpoints.json import JSONEndpoint
from web.api.schemas import GetByID
from web.mixins.user_service_mixin import UserServiceMixin
from . import schemas

logger = logging.getLogger(__name__)

meta = partial(EndpointMeta, tag='users')


class GetUsers(JSONEndpoint, UserServiceMixin):
    meta = meta

    schema_query = schemas.GetUsersQuery
    schema_response = list[User]

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.get_users(**params.query)


class CreateUser(JSONEndpoint, UserServiceMixin):
    meta = meta(summary='Create user')

    schema_body = partial_apply(User, only=['first_name', 'last_name', 'full_name'])
    schema_response = User

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.create_user(**params.body)


class UpdateUserByID(JSONEndpoint, UserServiceMixin):
    meta = meta(summary='Update user by id')

    schema_path = GetByID
    schema_body = partial_apply(User, only=['first_name', 'last_name', 'full_name'])
    schema_response = User

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.update_user_by_id(user_id=params.path['id'], **params.body)


class GetUserByID(JSONEndpoint, UserServiceMixin):
    meta = meta(summary='Get user by id')

    schema_path = GetByID
    schema_response = User

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.get_user_by_id(user_id=params.path['id'])


class DeleteUserByID(JSONEndpoint, UserServiceMixin):
    meta = meta(summary='Delete user by id')

    schema_path = GetByID
    schema_response = User

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_service.delete_user_by_id(user_id=params.path['id'])
