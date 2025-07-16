from functools import partial
import logging
from typing import Any

from app.models.challenges import Challenges
from core.utils.types import partial_apply
from core.web.endpoints.base import EndpointMeta, RequestParams
from core.web.endpoints.json import JSONEndpoint
from web.api.schemas import GetByID
from web.mixins.challenges_service_mixin import ChallengesServiceMixin
from . import schemas

logger = logging.getLogger(__name__)

meta = partial(EndpointMeta, tag='challenges')


class GetChallenges(JSONEndpoint, ChallengesServiceMixin):
    meta = meta(summary='Get challenges')

    schema_query = schemas.GetChallengesQuery
    schema_response = list[Challenges]

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.get_challenges(**params.query)


class CreateChallenge(JSONEndpoint, ChallengesServiceMixin):
    meta = meta(summary='Create challenge')

    schema_body = partial_apply(Challenges, only=['title', 'description'])
    schema_response = Challenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.create_challenge(**params.body)


class UpdateChallengeByID(JSONEndpoint, ChallengesServiceMixin):
    meta = meta(summary='Update challenge by id')

    schema_path = GetByID
    schema_body = partial_apply(Challenges, only=['title', 'description'])
    schema_response = Challenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.update_challenge_by_id(challenge_id=params.path['id'], **params.body)


class GetChallengeByID(JSONEndpoint, ChallengesServiceMixin):
    meta = meta(summary='Get challenge by id')

    schema_path = GetByID
    schema_response = Challenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.get_challenge_by_id(challenge_id=params.path['id'])


class DeleteChallengeByID(JSONEndpoint, ChallengesServiceMixin):
    meta = meta(summary='Delete challenge by id')

    schema_path = GetByID
    schema_response = Challenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.delete_challenge_by_id(challenge_id=params.path['id'])
        
