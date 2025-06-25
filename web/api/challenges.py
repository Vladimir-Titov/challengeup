import logging
from typing import Any

from pydantic import BaseModel
from starlette.datastructures import State

from app.repositories.repositories import DBRepositories
from core.web.endpoints.base import RequestParams
from core.web.endpoints.json import JSONEndpoint

logger = logging.getLogger(__name__)

class GetChallengesQuery(BaseModel):
    title: str | None = None


class GetChallenges(JSONEndpoint):
    schema_query = GetChallengesQuery

    async def execute(self, params: RequestParams, state: State) -> Any:
        db = state.db_pool
        dao = DBRepositories.create(db_pool=db)
        challenges = await dao.challenges.search(**params.query)
        return challenges
