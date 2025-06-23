import logging
from app.models.challenges import Challenges
from core.utils.types import partial_apply
from core.web.endpoint import BaseEndpoint, RequestParams
from starlette.responses import JSONResponse, Response


logger = logging.getLogger(__name__)


class GetChallengeByID(BaseEndpoint):
    schema_path = partial_apply(Challenges, only=['id'])

    async def execute(self, params: RequestParams) -> Response:
        logger.info(params)
        return JSONResponse({'message': 'Hello, World!'})
