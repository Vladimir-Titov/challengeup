from abc import abstractmethod
from dataclasses import dataclass
from email.parser import Parser
import logging
from typing import Any, AsyncGenerator, Mapping
from pydantic import BaseModel
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


def parse_params(data: dict[str, Any], schema: BaseModel | None = None) -> Any:
    if schema is None:
        return data

    try:
        model = schema.model_validate(data)
        return model.model_dump()
    except (PydanticSerializationError, PydanticValidationError) as e:
        raise ValidationError(message=str(e))


class BaseEndpoint(HTTPEndpoint):
    schema_response: type[BaseModel] | None = None
    schema_body: type[BaseModel] | None = None
    schema_query: type[BaseModel] | None = None
    schema_path: type[BaseModel] | None = None

    body_parser: Parser

    _media_type: str
    _response_media_type: str

    @abstractmethod
    async def get_response(self, response: Any) -> Response:
        """Method to get response from endpoint"""

    async def dispatch(self):
        try:
            request = Request(self.scope, receive=self.receive)
            path = parse_params(data=request.path_params, schema=self.schema_path)
            query = parse_params(data=request.query_params, schema=self.schema_query)
            headers = parse_params(data=request.headers, schema=self.schema_headers)
            body = self.body_parser(request=request, schema=self.schema_body)

            params = RequestParams(path=path, query=query, headers=headers, body=body)
            response_data = await self.execute(params=params)
            response = await self.get_response(response_data)
            
            return await response(self.scope, self.receive, self.send)
        except ValidationError as e:
            response = JSONResponse(status_code=e.status_code, content=e.message)
            return await response(self.scope, self.receive, self.send)

    @abstractmethod
    async def execute(self, params: RequestParams) -> Any:
        raise NotImplementedError
