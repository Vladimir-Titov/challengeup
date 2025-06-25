import logging
from typing import Any

from app.models.challenges import Challenges
from core.utils.types import partial_apply
from core.web.endpoints.base import RequestParams
from core.web.endpoints.json import JSONEndpoint

logger = logging.getLogger(__name__)


class GetChallengeByID(JSONEndpoint):
    schema_query = partial_apply(Challenges, only=['title'])

    async def get(self, params: RequestParams) -> Any:
        return {'message': 'Hello, World!'}
