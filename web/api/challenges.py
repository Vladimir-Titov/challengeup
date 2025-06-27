import logging
from typing import Any

from pydantic import BaseModel

from core.web.endpoints.base import RequestParams
from core.web.endpoints.json import JSONEndpoint
from web.mixins.challenges_service_mixin import ChallengesServiceMixin

logger = logging.getLogger(__name__)

class GetChallengesQuery(BaseModel):
    title: str | None


class GetChallenges(JSONEndpoint, ChallengesServiceMixin):
    schema_query = GetChallengesQuery

    async def execute(self, params: RequestParams) -> Any:
        return await self.challenges_service.get_challenges(**params.query)
