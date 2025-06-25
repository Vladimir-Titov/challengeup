import logging
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Callable, Mapping

from pydantic import BaseModel
from pydantic_core import PydanticSerializationError
from pydantic_core import ValidationError as PydanticValidationError
from starlette.datastructures import State
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.starlette_ext.errors.errors import AppError, ValidationError
from core.web.endpoints.parsers.base import BodyParser

logger = logging.getLogger(__name__)


@dataclass
class RequestParams:
    path: Mapping[str, Any] | None = None
    headers: Mapping[str, Any] | None = None
    query: Mapping[str, Any] | None = None
    body: Mapping[str, Any] | list | None | AsyncGenerator = None


def parse_params(data: Any, schema: type[BaseModel] | None = None) -> Any:
    if schema is None:
        return data

    try:
        model = schema.model_validate(data)
        return model.model_dump(exclude_none=True)
    except PydanticValidationError as e:
        raise ValidationError(message=e.json())
    except PydanticSerializationError as e:
        raise ValidationError(message=getattr(e, 'message', 'Unknown error'))


class BaseEndpoint(HTTPEndpoint):
    schema_response: type[BaseModel] | None = None
    schema_body: type[BaseModel] | None = None
    schema_query: type[BaseModel] | None = None
    schema_path: type[BaseModel] | None = None
    schema_headers: type[BaseModel] | None = None

    body_parser: BodyParser

    _media_type: str
    _response_media_type: str

    @abstractmethod
    async def get_response(self, data: Any, status_code: int = 200, headers: dict[str, str] | None = None) -> Any:
        """Method to get response from endpoint"""

    async def _get_request(self, request: Request) -> RequestParams:
        path = parse_params(data=request.path_params, schema=self.schema_path)
        query = parse_params(data=request.query_params, schema=self.schema_query)
        headers = parse_params(data=request.headers, schema=self.schema_headers)
        body = await self.body_parser.parse(request=request, schema=self.schema_body)
        return RequestParams(path=path, query=query, headers=headers, body=body)

    async def _dispatch(self, request: Request):
        request = Request(self.scope, receive=self.receive)
        params = await self._get_request(request=request)

        response_data = await self.execute(params=params, state=request.state)
        response = await self.get_response(data=response_data)

        return await response(self.scope, self.receive, self.send)

    async def _handle_exceptions(self, err: Exception):
        if isinstance(err, AppError):
            response = JSONResponse(
                status_code=err.status_code,
                content={
                    'code': err.code(),
                    'message': err.message,
                },
                headers={
                    'Content-Type': 'application/json',
                },
            )
            return await response(self.scope, self.receive, self.send)
        else:
            response = JSONResponse(
                status_code=500,
                content={
                    'code': 'internal_server_error',
                    'message': 'Internal Server Error',
                },
                headers={
                    'Content-Type': 'application/json',
                },
            )
            logger.error(f'Internal server error: {err}')
            return await response(self.scope, self.receive, self.send)

    async def dispatch(self) -> Any:
        try:
            request = Request(self.scope, receive=self.receive)
            return await self._dispatch(request=request)
        except Exception as err:
            return await self._handle_exceptions(err=err)

    @abstractmethod
    async def execute(self, params: RequestParams, state: State) -> Any:
        """Method to execute endpoint"""