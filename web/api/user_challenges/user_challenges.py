from functools import partial
import logging
from typing import Any

from app.models.user import Users
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

    schema_query = partial_apply(UserChallenges, only=['user_id', 'challenge_id'], partial=True)
    schema_response = list[UserChallenges]

    async def execute(self, params: RequestParams) -> Any:
        return await self.user_challenges_service.get_user_challenges(**params.query)
