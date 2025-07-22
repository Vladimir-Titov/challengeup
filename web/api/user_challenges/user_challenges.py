import logging
from functools import partial
from typing import Any

from app.models.user_challenges import UserChallenges
from core.utils.types import partial_apply
from core.web.endpoints.base import EndpointMeta, RequestParams
from core.web.endpoints.json import JSONEndpoint
from web.api.schemas import GetByID
from web.mixins.challenges_mixin import ChallengesMixin

logger = logging.getLogger(__name__)

meta = partial(EndpointMeta, tag='user_challenges')


class GetUserChallenges(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Get user challenges')

    schema_query = partial_apply(UserChallenges, only=['user_id', 'challenge_id', 'status'], partial=True)
    schema_response = list[UserChallenges]

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_challenges_service.get_user_challenges(**params.query)


class CreateUserChallenge(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Create user challenge')

    schema_body = partial_apply(UserChallenges, only=['user_id', 'challenge_id', 'status'])
    schema_response = UserChallenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_challenges_service.create_user_challenge(**params.body)


class GetUserChallengeByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Get user challenge by ID')

    schema_path = GetByID
    schema_response = UserChallenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_challenges_service.get_user_challenge_by_id(params.path['id'])


class UpdateUserChallengeByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Update user challenge by ID')

    schema_path = GetByID
    schema_body = partial_apply(UserChallenges, only=['status'], partial=True)
    schema_response = UserChallenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_challenges_service.update_user_challenge_by_id(params.path['id'], **params.body)


class DeleteUserChallengeByID(JSONEndpoint, ChallengesMixin):
    meta = meta(summary='Delete user challenge by ID')

    schema_path = GetByID
    schema_response = UserChallenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_challenges_service.delete_user_challenge_by_id(params.path['id'])
