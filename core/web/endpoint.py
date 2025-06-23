from abc import abstractmethod
from dataclasses import dataclass
from http.client import HTTPException
import logging
from typing import Any, AsyncGenerator, Mapping
from pydantic_core import PydanticSerializationError
from sqlmodel import SQLModel
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response
from starlette.requests import Request

from web.api.challenges import ChallengesAPI

logger = logging.getLogger(__name__)


@dataclass
class RequestParams:
    path: Mapping[str, Any] | None = None
    headers: Mapping[str, Any] | None = None
    query: Mapping[str, Any] | None = None
    body: Mapping[str, Any] | list | None | AsyncGenerator | None = None


def parse_params(data: dict[str, Any], schema: SQLModel) -> dict[str, Any]:
    try:
        return schema.model_dump(data, warnings='error')
    except PydanticSerializationError as e:
        raise HTTPException(status_code=400, detail=str(e))


class BaseEndpoint(HTTPEndpoint):
    schema_response: SQLModel
    schema_body: SQLModel
    schema_query: SQLModel
    schema_path: SQLModel

    _media_type: str
    _response_media_type: str


    async def dispatch(self):
        request = Request(self.scope, receive=self.receive)
        request.path_params

        response = await self.execute(params=params)
        return response

    @abstractmethod
    async def execute(self, params: RequestParams) -> Response:
        raise NotImplementedError
