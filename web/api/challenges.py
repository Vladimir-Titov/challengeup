import logging
from typing import Any

from starlette.responses import JSONResponse, Response

from app.models.challenges import Challenges
from core.utils.types import partial_apply
from core.web.endpoints.base import BaseEndpoint, RequestParams

logger = logging.getLogger(__name__)


class GetChallengeByID(BaseEndpoint):
    schema_query = partial_apply(Challenges, only=['title'])

    async def get(self, params: RequestParams) -> Response:
        return {'message': 'Hello, World!'}

    async def get_response(self, data: Any, status_code: int = 200, headers: dict[str, str] | None = None) -> Response:
        return JSONResponse(content=data, status_code=status_code, headers=headers)
