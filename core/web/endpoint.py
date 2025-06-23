from abc import abstractmethod
from dataclasses import dataclass
import logging
from typing import Any, AsyncGenerator, Mapping
from pydantic_core import PydanticSerializationError, ValidationError as PydanticValidationError
from sqlmodel import SQLModel
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, JSONResponse
from starlette.requests import Request

from core.starlette_ext.errors.errors import ValidationError


logger = logging.getLogger(__name__)


@dataclass
class RequestParams:
    path: Mapping[str, Any] | None = None
    headers: Mapping[str, Any] | None = None
    query: Mapping[str, Any] | None = None
    body: Mapping[str, Any] | list | None | AsyncGenerator | None = None


def parse_params(data: dict[str, Any], schema: SQLModel | None = None) -> Any:
    if schema is None:
        return data

    try:
        model = schema.model_validate(data)
        return model.model_dump()
    except (PydanticSerializationError, PydanticValidationError) as e:
        raise ValidationError(message=str(e))


class BaseSQLModelSQLModelEndpoint(HTTPEndpoint):
    schema_response: SQLModel | None = None
    schema_body: SQLModel | None = None
    schema_query: SQLModel | None = None
    schema_path: SQLModel | None = None

    body_parser = None

    _media_type: str
    _response_media_type: str

    async def dispatch(self):
        try:
            request = Request(self.scope, receive=self.receive)
            path = parse_params(data=request.path_params, schema=self.schema_path)
            query = parse_params(data=request.query_params, schema=self.schema_query)
            # body = parse_params(await request.json(), self.schema_body)
            # headers = parse_params(request.headers, self.schema_headers)

            params = RequestParams(path=path, query=query)
            response = await self.execute(params=params)
            return await response(self.scope, self.receive, self.send)
        except ValidationError as e:
            logger.error(e)
            response = JSONResponse(status_code=e.status_code, content=e.message)
            return await response(self.scope, self.receive, self.send)

    @abstractmethod
    async def execute(self, params: RequestParams) -> Response:
        raise NotImplementedError
