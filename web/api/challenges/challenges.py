import logging
from typing import Any


from app.models.challenges import Challenges
from core.utils.types import partial_apply
from core.web.endpoints.base import RequestParams
from core.web.endpoints.json import JSONEndpoint
from web.api.schemas import GetByID
from web.mixins.challenges_service_mixin import ChallengesServiceMixin
from . import schemas

logger = logging.getLogger(__name__)


class GetChallenges(JSONEndpoint, ChallengesServiceMixin):
    schema_query = schemas.GetChallengesQuery
    schema_response = list[Challenges]

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.get_challenges(**params.query)


class CreateChallenge(JSONEndpoint, ChallengesServiceMixin):
    schema_body = partial_apply(Challenges, only=['title', 'description'])
    schema_response = Challenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.create_challenge(**params.body)


class UpdateChallengeByID(JSONEndpoint, ChallengesServiceMixin):
    schema_path = GetByID
    schema_body = partial_apply(Challenges, only=['title', 'description'])
    schema_response = Challenges

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.update_challenge_by_id(challenge_id=params.path['id'], **params.body)
